from __future__ import annotations

import ipywidgets
import IPython.display
import threading
import time
import datetime
import bqplot
import numpy as np
from typing import Dict, Tuple, Callable
from .experiment import ExperimentState, ExperimentABC
from .analysis import AnalysisABC
from .plots import DataStreamPlotABC, PlotABC
from .database import Database


class InterfacePlotGUI:
    def __init__(self):
        self.plot = None
        self.interface_frame = None
        self.plot_frame = None

    def _make_interface_frame(self, pixel_positions: Dict[str, Tuple[float, float]], height: int):
        interface_frame = ipywidgets.Output(layout=ipywidgets.Layout(height=f'{height}px'))
        interface_frame.add_class('interface-frame')
        x_coords = []
        y_coords = []
        for coords in pixel_positions.values():
            x_coords.append(coords[0])
            y_coords.append(coords[1])
        x_lim, y_lim = [(min(coords), max(coords)) for coords in [x_coords, y_coords]]
        x_len, y_len = [lim[1] - lim[0] for lim in [x_lim, y_lim]]
        if x_len < y_len:
            x_center = x_lim[0] + x_len/2
            x_lim = (x_center - y_len/2, x_center + y_len/2)
        elif x_len > y_len:
            y_center = y_lim[0] + y_len/2
            y_lim = (y_center - x_len/2, y_center + x_len/2)
        x_scale = bqplot.LinearScale(min=x_lim[0]-x_len*.1, max=x_lim[1]+x_len*.1)
        y_scale = bqplot.LinearScale(min=y_lim[0]-y_len*.1, max=y_lim[1]+y_len*.1)
        self.interface_scatter = bqplot.Scatter(x=x_coords, y=y_coords, names=list(pixel_positions.keys()),
                                                colors=[state_colors['INITIAL']], default_size=100,
                                                scales={'x': x_scale, 'y': y_scale})
        ax_x = bqplot.Axis(scale=x_scale, grid_lines='none', visible=False)
        ax_y = bqplot.Axis(scale=y_scale, grid_lines='none', visible=False)
        fm = 0
        self.interface_fig = bqplot.Figure(marks=[self.interface_scatter], axes=[ax_x, ax_y],
                                           figsize=(5, 5), padding_x=0, padding_y=0,
                                           fig_margin={'top': fm, 'bottom': fm, 'left': fm, 'right': fm})
        return interface_frame

    def _update_interface_frame(self, *args, **kwargs):
        pass

    def _display_interface_frame(self):
        self._update_interface_frame()
        self.interface_frame.clear_output(wait=True)
        with self.interface_frame:
            IPython.display.display(self.interface_fig)

    def _make_plot_frame(self, height: int):
        plot_frame = ipywidgets.Output(layout=ipywidgets.Layout(height=f'{height}px'))
        plot_frame.add_class('plot-frame')
        self.plot.make_plot()
        return plot_frame

    def _update_plot_frame(self, *args, **kwargs):
        pass

    def _display_plot_frame(self):
        self._update_plot_frame()
        self.plot_frame.clear_output(wait=True)
        with self.plot_frame:
            IPython.display.display(self.plot.figure)


class ExperimentGUI(InterfacePlotGUI):
    """
    A graphical user interface for monitoring and controlling an experiment within a Jupyter Notebook.
    """

    instance = None

    def __new__(cls, **kwargs):
        if cls.instance is None:
            cls.instance = super(ExperimentGUI, cls).__new__(cls)
        return cls.instance

    def __init__(self, experiment: ExperimentABC, plot: DataStreamPlotABC):
        """Initializes the ExperimentGUI by generating the widgets in the background.

        :param experiment: An instance of the `Experiment` class (or a class derived from `ExperimentABC`).
        :param plot: An instance of a class which implements the `DataStreamPlotABC` and is compatible with the
            experiment.
        """
        InterfacePlotGUI.__init__(self)
        plot.check_compatibility(experiment.measurement.output_type)
        experiment.data_stream = plot.data_stream
        self.experiment = experiment
        self.current_pixel = None
        self.preview_pixel = None
        self.plot = plot

        self.statusbar = self._make_statusbar()
        self.buttons = self._make_buttons()
        self.interface_frame = self._make_interface_frame(experiment.interface.pixel_positions, 400)
        self.interface_scatter.on_element_click(self._preview_click)
        self.plot_frame = self._make_plot_frame(438)
        self.widget = self._make_widget()

        self.update_worker = None
        self.stop_update = True

    @staticmethod
    def _make_statusbar():
        statusbar = [ipywidgets.HTML(), ipywidgets.HTML()]
        statusbar[0].style = {
            'font_size': '18px',
        }
        statusbar[1].style = {
            'font_size': '18px'
        }
        return statusbar

    def _update_statusbar(self):
        self.statusbar[0].value = \
            f'State: <span style="font-weight: bold; color: {state_colors[self.experiment.state.name]}">' \
            f'{self.experiment.state.name}</span>'
        pixel_status = ''
        if self.experiment.state in [ExperimentState.RUNNING, ExperimentState.ABORTED]:
            if self.current_pixel is None:
                pixel_status = f'[PREVIEW: {self.preview_pixel}]'
            else:
                pixel_status = f'[{self.current_pixel}]'
        self.statusbar[1].value = f'{self.experiment.measurement.name}: {self.experiment.sample_id} {pixel_status}'

    def _make_buttons(self):
        setup_button = ipywidgets.Button(description='Setup', disabled=True, icon='cogs')
        setup_button.add_class('setup-button')
        start_button = ipywidgets.Button(description='Start', disabled=True, icon='play')
        start_button.add_class('start-button')
        abort_button = ipywidgets.Button(description='Abort', disabled=True, icon='stop')
        abort_button.add_class('abort-button')

        setup_button.on_click(self._setup_button_click)
        start_button.on_click(self._start_button_click)
        abort_button.on_click(self._abort_button_click)

        return [setup_button, start_button, abort_button]

    def _setup_button_click(self, button):
        self.experiment.setup()

    def _start_button_click(self, button):
        self.experiment.start()

    def _abort_button_click(self, button):
        self.experiment.abort()

    def _update_buttons(self):
        if self.experiment.state in [ExperimentState.INITIAL, ExperimentState.FINISHED, ExperimentState.ABORTED]:
            self.buttons[0].disabled = False
        else:
            self.buttons[0].disabled = True
        if self.experiment.state == ExperimentState.READY:
            self.buttons[1].disabled = False
        else:
            self.buttons[1].disabled = True
        if self.experiment.state in [ExperimentState.READY, ExperimentState.RUNNING]:
            self.buttons[2].disabled = False
        else:
            self.buttons[2].disabled = True

    def _preview_click(self, event, data):
        if self.experiment.state == ExperimentState.RUNNING:
            return
        pixel = data['data']['name']
        self.preview_pixel = pixel
        self.plot.clear_plot()
        self.experiment.preview(pixel)

    def _update_interface_frame(self):
        colors = []
        for pixel in self.experiment.interface.pixel_ids:
            if pixel == self.preview_pixel and self.experiment.state == ExperimentState.RUNNING:
                colors.append(state_colors['RUNNING'])
            elif pixel not in self.experiment.selected_pixels:
                colors.append('black')
            elif self.experiment.current_pixel_idx == -2:
                colors.append(state_colors['INITIAL'])
            elif self.experiment.current_pixel_idx < self.experiment.selected_pixels.index(pixel):
                colors.append(state_colors['READY'])
            elif self.experiment.current_pixel_idx > self.experiment.selected_pixels.index(pixel):
                colors.append(state_colors['FINISHED'])
            elif pixel == self.experiment.selected_pixels[self.experiment.current_pixel_idx]:
                if self.experiment.state == ExperimentState.RUNNING:
                    colors.append(state_colors['RUNNING'])
                if self.experiment.state == ExperimentState.ABORTED:
                    colors.append(state_colors['ABORTED'])
        self.interface_scatter.colors = colors
        if self.experiment.state == ExperimentState.RUNNING:
            self.interface_frame.remove_class('interactive-interface')
        else:
            self.interface_frame.add_class('interactive-interface')

    def _update_plot_frame(self):
        if self.experiment.state is ExperimentState.ABORTED:
            return
        if self.experiment.state is not ExperimentState.RUNNING:
            self.plot.clear_plot()
            return
        if self.experiment.current_pixel_idx < 0:
            pass
        elif self.current_pixel != self.experiment.selected_pixels[self.experiment.current_pixel_idx]:
            self.current_pixel = self.experiment.selected_pixels[self.experiment.current_pixel_idx]
            self.plot.clear_plot()
        self.plot.update_plot()

    def _make_widget(self):
        frame_layout = ipywidgets.Layout(border='2px #dddddd solid', border_top='none',
                                         justify_content='center', margin='2px')
        left_body = ipywidgets.VBox([
            ipywidgets.HBox([self.statusbar[0]],
                            layout=ipywidgets.Layout(justify_content='center')),
            self.interface_frame,
            ipywidgets.HBox(self.buttons,
                            layout=ipywidgets.Layout(justify_content='center'))
        ], layout=frame_layout)
        right_body = ipywidgets.VBox([
            ipywidgets.HBox([self.statusbar[1]],
                            layout=ipywidgets.Layout(justify_content='center')),
            self.plot_frame
        ], layout=frame_layout)
        left_column = ipywidgets.VBox([
            ipywidgets.HTML('Control').add_class('column-heading'),
            left_body
        ], layout=ipywidgets.Layout(width='400px'))
        right_column = ipywidgets.VBox([
            ipywidgets.HTML('Plot').add_class('column-heading'),
            right_body
        ], layout=ipywidgets.Layout(width='585px'))
        return ipywidgets.HBox([
            ipywidgets.HTML(f"<style>{style}</style>",
                            layout=ipywidgets.Layout(display='none')),
            left_column,
            right_column
        ])

    def _update_widget(self):
        self.stop_update = False
        while not self.stop_update:
            self._update_statusbar()
            self._update_buttons()
            self._update_interface_frame()
            self._update_plot_frame()

    def display(self):
        """Displays the ExperimentGUI widget and starts the update loop in a separate thread."""
        self.stop_update = True
        time.sleep(1)
        IPython.display.display(self.widget, clear=True)
        self._display_interface_frame()
        self._display_plot_frame()
        self.update_worker = threading.Thread(target=self._update_widget)
        self.update_worker.start()


class AnalysisGUI(InterfacePlotGUI):

    def __init__(self, analysis: AnalysisABC, plot: PlotABC):
        InterfacePlotGUI.__init__(self)
        self.analysis = analysis
        self.plot = plot

        self.current_pixel = None
        self.current_plot = 0
        self.available_plots = ['Measurement'] + list(self.analysis.plots.keys())

        self.interface_frame = self._make_interface_frame(analysis.pixel_positions, 420)
        self.interface_frame.add_class('interactive-interface')
        self.interface_scatter.on_element_click(self._select_pixel)
        self.plot_heading = ipywidgets.HTML('Plot: Measurement')
        self.switch_plot_buttons = self._make_switch_plot_buttons()
        self.plot_frame = self._make_plot_frame(420)
        self.results_frame = ipywidgets.HTML()
        self.widget = self._make_widget()

    def _select_pixel(self, event, data):
        pixel = data['data']['name']
        self.current_pixel = pixel
        self._update_plot_frame()
        self._update_results_frame()
        self._update_interface_frame()

    def _update_interface_frame(self):
        colors = []
        for pixel in self.analysis.pixel_positions.keys():
            if pixel not in self.analysis.dataset.keys():
                colors.append('black')
            elif pixel == self.current_pixel:
                colors.append(state_colors['FINISHED'])
            else:
                colors.append(state_colors['INITIAL'])
        self.interface_scatter.colors = colors

    def _make_switch_plot_buttons(self):
        left_button = ipywidgets.Button(icon='caret-left', disabled=True)
        left_button.value = 'left'
        left_button.on_click(self._switch_plot)
        right_button = ipywidgets.Button(icon='caret-right', disabled=True)
        right_button.value = 'right'
        right_button.on_click(self._switch_plot)
        return ipywidgets.HBox([left_button, right_button])

    def _switch_plot(self, button):
        if button.value == 'left':
            self.current_plot -= 1
        else:
            self.current_plot += 1
        self._update_switch_plot_buttons()
        self._update_plot_frame()

    def _update_switch_plot_buttons(self):
        left_button, right_button = self.switch_plot_buttons.children
        if self.current_plot == 0:
            left_button.disabled = True
        elif self.current_plot > 0:
            left_button.disabled = False
        if self.current_plot < len(self.available_plots) - 1:
            right_button.disabled = False
        else:
            right_button.disabled = True

    def _update_plot_frame(self):
        self.plot_heading.value = f'Plot: {self.available_plots[self.current_plot]}'
        if self.current_pixel is None:
            return
        if self.current_plot == 0:
            data = self.analysis.dataset[self.current_pixel]
            self.plot_frame.clear_output(wait=True)
            with self.plot_frame:
                self.plot.update_plot(data)
                IPython.display.display(self.plot.figure)
        else:
            figure = self.analysis.plots[self.available_plots[self.current_plot]](self.current_pixel)
            self.plot_frame.clear_output(wait=True)
            with self.plot_frame:
                IPython.display.display(figure)

    def _update_results_frame(self):
        results = []
        for func_name, func in self.analysis.functions.items():
            try:
                result = func(self.current_pixel)
            except Exception as exc:
                result = type(exc).__name__
            results.append(f'<tr><td style="font-weight:bold;">{func_name}</td><td>{result}</td></tr>')
        self.results_frame.value = f'<table class="results-table">' \
                                   f'<thead><tr><th>Function</th><th>Result</th></tr></thead>' \
                                   f'<tbody>{"".join(results)}</tbody>' \
                                   f'</table>'

    def _make_widget(self):
        frame_layout = ipywidgets.Layout(border='2px #dddddd solid', border_top='none',
                                         justify_content='center', margin='2px')
        left_column = ipywidgets.VBox([
            ipywidgets.HTML('Interface').add_class('column-heading'),
            ipywidgets.VBox([self.interface_frame], layout=frame_layout)
        ], layout=ipywidgets.Layout(width='400px'))
        right_column = ipywidgets.VBox([
            ipywidgets.HBox([
                self.plot_heading,
                self.switch_plot_buttons
            ]).add_class('column-heading'),
            ipywidgets.VBox([self.plot_frame], layout=frame_layout)
        ], layout=ipywidgets.Layout(width='585px'))
        widget_top = ipywidgets.HBox([
            ipywidgets.HTML(f"<style>{style}</style>",
                            layout=ipywidgets.Layout(display='none')),
            left_column,
            right_column
        ])
        widget = ipywidgets.VBox([
            widget_top,
            self.results_frame
        ])
        widget.add_class('analysis-gui')
        return widget

    def display(self):
        """Displays the AnalysisGUI widget."""
        IPython.display.display(self.widget, clear=True)
        self._display_interface_frame()
        self._update_switch_plot_buttons()


class DatabaseGUI:

    def __init__(self, database: Database):
        self.database = database

        self.toggle = self._make_toggle()
        self.results_count = ipywidgets.HTML()
        self.results_count.add_class('results-count')
        self.buttons_frame = ipywidgets.HBox()
        self.buttons_frame.add_class('buttons-frame')
        self.filters_frame = ipywidgets.VBox()
        self.filters_frame.add_class('filters-frame')
        self.filter_values = {}
        self.filter_widgets = {}
        self.results_frame = ipywidgets.HTML()
        self.results_frame.add_class('results-frame')
        self.widget = self._make_widget()

        self.timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

    def _make_toggle(self):
        toggle = ipywidgets.ToggleButtons(value=None, options=['Measurements', 'Samples'], icons=['folder']*2)
        toggle.add_class('dataset-toggle')
        toggle.observe(self._toggle_click, 'value')
        return toggle

    def _toggle_click(self, change):
        self._update_results_frame()
        self.filters_frame.children = []
        icons = ['folder'] * 2
        if change['new'] == 'Measurements':
            self._measurements_toggle()
            icons[0] = 'folder-open'
        else:
            self._samples_toggle()
            icons[1] = 'folder-open'
        self.toggle.icons = icons

    def _enable_buttons(self):
        for button in self.buttons_frame.children:
            button.disabled = False

    def _measurements_toggle(self):
        measurement_buttons = [ipywidgets.Button(description=measurement)
                               for measurement in self.database.get_measurements()]
        for button in measurement_buttons:
            button.add_class('measurement-button')
            button.on_click(self._measurement_button_click)
        self.buttons_frame.children = measurement_buttons

    def _measurement_button_click(self, button):
        self._enable_buttons()
        button.disabled = True
        measurement = button.description
        self.filter_values = self.database.get_filters(measurement)
        self.filter_widgets = {}
        measurement_filters = []
        checkbox_layout = ipywidgets.Layout(width='30px')
        label_layout = ipywidgets.Layout(padding='8px 10px', min_width='200px')
        row_layout = ipywidgets.Layout(padding='6px 0px', align_items='center')
        for setting, values in self.filter_values.items():
            if len(values) == 1:
                widget = ipywidgets.HTML(f'{list(values)[0]}')
                widget.disabled = True
            elif all([np.issubdtype(type(value), bool)
                      for value in values]):
                widget = ipywidgets.SelectMultiple(value=(True, False), options=[True, False], rows=2, disabled=True)
            elif all([np.issubdtype(type(value), np.integer)
                      for value in values]):
                widget = ipywidgets.IntRangeSlider(value=[min(values), max(values)], min=min(values), max=max(values),
                                                   continous_update=False, disabled=True)
            elif all([np.issubdtype(type(value), np.integer) or np.issubdtype(type(value), np.floating)
                      for value in values]):
                widget = ipywidgets.FloatRangeSlider(value=[min(values), max(values)], min=min(values), max=max(values),
                                                     continous_update=False, disabled=True)
            else:
                widget = ipywidgets.SelectMultiple(value=tuple(values), options=values, disabled=True)
            self.filter_widgets[setting] = widget
            widget.observe(self._change_filter(measurement), 'value')
            checkbox = ipywidgets.Checkbox(value=False, layout=checkbox_layout)
            checkbox.observe(self._toggle_filter(measurement, setting), 'value')
            measurement_filters.append(ipywidgets.HBox([
                checkbox,
                ipywidgets.HTML(f'{setting}', layout=label_layout),
                widget
            ], layout=row_layout))
        self.filters_frame.children = measurement_filters

    def _toggle_filter(self, measurement: str, setting: str) -> Callable:
        def func(change):
            self.filter_widgets[setting].disabled = not change['new']
            self._apply_filters(measurement)
        return func

    def _change_filter(self, measurement: str) -> Callable:
        def func(change):
            self._apply_filters(measurement)
        return func

    def _apply_filters(self, measurement: str):
        filters = {}
        for setting, widget in self.filter_widgets.items():
            if widget.disabled:
                continue
            if type(widget) == ipywidgets.HTML:
                filters[setting] = list(self.filter_values[setting])
            elif type(widget) == ipywidgets.SelectMultiple:
                filters[setting] = list(widget.value)
            else:
                filters[setting] = [value for value in self.filter_values[setting]
                                    if (value >= widget.value[0]) and (value <= widget.value[1])]
        if len(filters) == 0:
            self._update_results_frame()
            return
        results = self.database.filter_by_settings_batch(measurement, filters)
        self._update_results_frame(results)

    def _samples_toggle(self):
        sample_buttons = [ipywidgets.Button(description=sample) for sample in self.database.get_sample_ids()]
        for button in sample_buttons:
            button.add_class('sample-button')
            button.on_click(self._sample_button_click)
        self.buttons_frame.children = sample_buttons

    def _sample_button_click(self, button):
        self._enable_buttons()
        button.disabled = True
        results = self.database.filter_by_sample_id(button.description)
        self._update_results_frame(results)

    def _update_results_frame(self, results=None):
        if results is None:
            self.results_frame.value = ''
            self.results_count.value = ''
        else:
            result_rows = []
            for result in results:
                row = []
                _, measurement, _, datetime_sample = result.split('/')
                measurement_datetime = datetime_sample[:26]
                row.append(datetime.datetime.fromisoformat(measurement_datetime + '+00:00').astimezone(self.timezone))
                row.append(measurement)
                row.append(', '.join([str(v) for v in self.database.get_measurement_settings(result).values()]))
                row.append(datetime_sample[27:])
                row.append(self.database.get_dataset_length(result))
                row.append(f'<a href="#" onclick="'
                           f'const old_icon = document.querySelector(\'i.fa-check\'); '
                           f'if (old_icon != null) {{ '
                           f'old_icon.classList.toggle(\'fa-clone\'); old_icon.classList.toggle(\'fa-check\'); }}'
                           f'const new_icon = this.querySelector(\'i\'); '
                           f'new_icon.classList.toggle(\'fa-clone\'); new_icon.classList.toggle(\'fa-check\'); '
                           f'navigator.clipboard.writeText(\'{result}\')">'
                           f'<i class="fa fa-clone"></i> Copy'
                           f'</a>')
                result_rows.append(row)
            result_rows.sort(key=lambda x: x[0], reverse=True)
            result_rows = [f'<tr>'
                           f'<td>{row[0].strftime("%d.%m.%y")}</td>'
                           f'<td>{row[0].strftime("%H:%M:%S")}</td>'
                           f'<td>{row[1]}</td>'
                           f'<td>{row[2]}</td>'
                           f'<td>{row[3]}</td>'
                           f'<td>{row[4]}</td>'
                           f'<td>{row[5]}</td>'
                           f'</tr>' for row in result_rows]
            results_table = f'<table class="results-table">' \
                            f'<thead><tr>' \
                            f'<th>Date</th>' \
                            f'<th>Time</th>' \
                            f'<th>Measurement</th>' \
                            f'<th>Settings</th>' \
                            f'<th>Sample&nbsp;ID</th>' \
                            f'<th>Entries</th>' \
                            f'<th>Path</th>' \
                            f'</tr></thead>' \
                            f'<tbody>{"".join(result_rows)}</tbody>' \
                            f'</table>'
            self.results_frame.value = results_table
            self.results_count.value = f'{len(result_rows)} results'

    def _make_widget(self):
        widget = ipywidgets.VBox([
            ipywidgets.HTML(f'<style>{style}</style>', layout=ipywidgets.Layout(display='none')),
            ipywidgets.HBox([self.toggle, self.results_count],
                            layout=ipywidgets.Layout(justify_content='space-between', align_items='center')),
            self.buttons_frame,
            self.filters_frame,
            self.results_frame
        ])
        widget.add_class('database-gui')
        return widget

    def display(self):
        """Displays the DatabaseGUI widget."""
        IPython.display.display(self.widget, clear=True)


state_colors = {
    'INITIAL': '#6c757d',
    'READY': '#ffc107',
    'RUNNING': '#28a745',
    'FINISHED': '#007bff',
    'ABORTED': '#dc3545'
}

style = f"""
.column-heading {{
    background-color: {state_colors['FINISHED']};
    padding: 12px 15px;
    margin: 2px;
    margin-bottom: -2px;
    justify-content: space-between;
}}

.column-heading .widget-html {{
    font-size: inherit;
    margin: 0;
}}

.column-heading, .column-heading .widget-html-content {{
    color: #ffffff;
    font-size: 120%;
    font-weight: bold;
}}

.column-heading button {{
    width: auto;
    margin: 0;
    font-size: 150%;
    background: none!important;
    outline: none!important;
    box-shadow: none!important;
    color: #ffffff;
}}

.interface-frame .output, .interface-frame .output_area, .interface-frame .output_subarea, .interface-frame .bqplot,
.plot-frame .output, .plot-frame .output_area, .plot-frame .output_subarea {{
    height: 100%;
    overflow: hidden;
}}

.plot-frame img, .plot-frame .bqplot {{
    height: 100%!important;
    width: 100%!important;
}}

.interactive-interface .dot.element {{
    cursor: pointer;
}}

.interactive-interface .dot.element:hover {{
    transform: scale(1.3);
}}

.output_area + .output_area {{
    display: none;
}}

.widget-container {{
    overflow: hidden;
}}

.widget-button, .dataset-toggle button {{
    margin: 5px;
    font-size: 110%;
    font-weight: bold;
    cursor: pointer;
}}

.dataset-toggle button {{
    width: 170px;
}}

.widget-button .icon {{
    margin-right: 5px;
}}

.dataset-toggle i {{
    margin-left: 5px;
}}

.widget-button:disabled {{
    pointer-events: none;
}}

.setup-button, .start-button, .abort-button {{
    width: 115px;
    color: #fff;
}}

.setup-button {{
    background-color: {state_colors['READY']};
}}

.start-button {{
    background-color: {state_colors['RUNNING']};
}}

.abort-button {{
    background-color: {state_colors['ABORTED']};
}}

.results-count {{
    padding-right: 12px;
    font-size: 120%;
}}

.buttons-frame {{
    margin-left: 2px;
    margin-right: 2px;
    margin-top: 0px;
    margin-bottom: 2px;
    flex-wrap: wrap;
}}

.measurement-button, .sample-button {{
    font-weight: normal;
    width: auto;
}}

.measurement-button:disabled, .sample-button:disabled {{
    font-weight: bold;
    background-color: {state_colors['FINISHED']};
    color: #fff;
}}

.filters-frame {{
    margin: 10px 2px;
    margin-top: 0;
}}

.filters-frame:empty {{
    margin: 0;
}}

.filters-frame .widget-hbox {{
    border: 2px #dddddd solid;
    margin-bottom: -2px;
}}

.filters-frame .widget-hbox:last-child {{
    border-bottom: 4px #dddddd solid;
}}

.filters-frame .widget-hbox:nth-of-type(even) {{
    background-color: #f3f3f3;
}}

.filters-frame .widget-hbox:hover {{
    border-left: 2px {state_colors['FINISHED']} solid;
    border-right: 2px {state_colors['FINISHED']} solid;
}}

.filters-frame .widget-checkbox .widget-label {{
    width: 0;
    margin-top: 3px;
}}

.filters-frame .widget-select-multiple select {{
    padding: 3px;
}}

.filters-frame :disabled div {{
    pointer-events: none;
    color: #888888;
}}

.results-frame {{
    margin-top: 5px;
}}

.results-frame:empty {{
    margin: 0;
}}

.results-table {{
    border-collapse: collapse;
    border: 2px #dddddd solid;
    width: 100%;
    font-family: sans-serif;
}}

.results-table thead tr {{
    border: 2px {state_colors['FINISHED']} solid;
    background-color: {state_colors['FINISHED']};
    color: #ffffff;
    text-align: left;
    font-size: 120%;
}}

.results-table th,
.results-table td {{
    padding: 12px 15px;
    line-height: 1.1;
}}



.analysis-gui .results-table th,
.analysis-gui .results-table td {{
    width: 50%;
}}

.results-table tbody tr {{
    border-bottom: 2px solid #dddddd;
}}

.results-table tbody tr:hover {{
    border-left: 2px {state_colors['FINISHED']} solid;
    border-right: 2px {state_colors['FINISHED']} solid;
}}

.results-table tbody tr:nth-of-type(even) {{
    background-color: #f3f3f3;
}}

.results-table tbody tr:last-of-type {{
    border-bottom: 3px solid {state_colors['FINISHED']};
}}
"""
