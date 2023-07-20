import ipywidgets
import IPython.display
import threading
import time
import matplotlib.pyplot as plt
import numpy as np
from .experiment import ExperimentState, ExperimentABC, CompatibilityError
from .data_stream import PlotABC


def button_click(func):
    def wrapper(self, *args, **kwargs):
        with self.no_output:
            self.input_disabled = True
            self._update_buttons()
            func(self, *args, **kwargs)
            plt.pause(1)
            self.input_disabled = False
    return wrapper


class GUI:
    """
    A graphical user interface for monitoring and controlling an experiment within a Jupyter Notebook.
    """

    instance = None

    def __new__(cls, **kwargs):
        if cls.instance is None:
            cls.instance = super(GUI, cls).__new__(cls)
        return cls.instance

    def __init__(self, experiment: ExperimentABC, plot: PlotABC):
        """Initializes the GUI by generating the widgets in the background.

        :param experiment: An instance of the `Experiment` class (or a class derived from `ExperimentABC`).
        :param plot: An instance of a class which implements the `PlotABC` and is compatible with the experiment.
        """
        experiment.data_stream = plot.data_stream
        self.experiment = experiment
        self.plot = plot
        self.current_pixel = None
        self.preview = False

        self._check_compatibility()

        self.statusbar = self._make_statusbar()
        self.preview_dropdown = self._make_preview_dropdown()
        self.buttons = self._make_buttons()
        self.interface_frame = self._make_interface_frame()
        self.plot_frame = self._make_plot_frame()
        self.widget = self._make_widget()
        self.no_output = ipywidgets.Output(layout=ipywidgets.Layout(heithg='0', width='0'))

        self.update_worker = None
        self.stop_update = True
        self.input_disabled = False

    def _check_compatibility(self):
        if len(self.experiment.measurement.output_type) != len(self.plot.data_types):
            raise CompatibilityError(
                "The output_type of the measurement and the data_types of the plot must have the same lengths!")
        for mtype_name, ptype in zip(self.experiment.measurement.output_type.names, self.plot.data_types):
            if not np.issubdtype(self.experiment.measurement.output_type[mtype_name], ptype):
                raise CompatibilityError(
                    "All items of the output_type must be sub-dtypes of the plot data_types in correct order!")

    def _make_statusbar(self):
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
                pixel_status = '[PREVIEW]'
            else:
                pixel_status = f'[{self.current_pixel}]'
        self.statusbar[1].value = f'{self.experiment.measurement.name}: {self.experiment.sample_id} {pixel_status}'

    def _make_preview_dropdown(self):
        preview_dropdown = ipywidgets.Dropdown(
            options=self.experiment.selected_pixels,
            value=self.experiment.selected_pixels[0],
            description='Pixel ID:'
        )
        return preview_dropdown

    def _make_buttons(self):
        setup_button = ipywidgets.Button(description='Setup', disabled=True, icon='cogs', button_style="warning")
        start_button = ipywidgets.Button(description='Start', disabled=True, icon='play', button_style="success")
        abort_button = ipywidgets.Button(description='Abort', disabled=True, icon='stop', button_style="danger")
        preview_button = ipywidgets.Button(description='Preview', disabled=True, icon='eye')

        setup_button.on_click(self._setup_button_click)
        start_button.on_click(self._start_button_click)
        abort_button.on_click(self._abort_button_click)
        preview_button.on_click(self._preview_button_click)

        return [setup_button, start_button, abort_button, preview_button]

    @button_click
    def _setup_button_click(self, button):
        self.experiment.setup()

    @button_click
    def _start_button_click(self, button):
        self.experiment.start()

    @button_click
    def _abort_button_click(self, button):
        self.experiment.abort()

    @button_click
    def _preview_button_click(self, button):
        self.current_pixel = None
        self.preview = True
        self.experiment.preview(self.preview_dropdown.value)

    def _update_buttons(self):
        if self.input_disabled:
            for button in self.buttons:
                button.disabled = True
            self.preview_dropdown.disabled = True
            return
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
        if self.experiment.state is not ExperimentState.RUNNING:
            self.buttons[3].disabled = False
            self.preview_dropdown.disabled = False
        else:
            self.buttons[3].disabled = True

    def _make_interface_frame(self):
        interface_frame = ipywidgets.Output(layout=ipywidgets.Layout(height='400px'))
        x_coords = [point[0] for point in self.experiment.interface.sample_layout.values()]
        y_coords = [point[1] for point in self.experiment.interface.sample_layout.values()]
        with plt.ioff():
            self.interface_fig, ax = plt.subplots(figsize=(5, 5))
            ax.axis('equal')
            ax.axis('off')
            self.scatter = ax.scatter(x_coords, y_coords, c='gray', s=100)
            for label, coords in self.experiment.interface.sample_layout.items():
                ax.annotate(label, coords, textcoords="offset points", xytext=(8, -10), ha='left')
            self.interface_fig.tight_layout()
        return interface_frame

    def _update_interface_frame(self):
        colors = []
        for pixel, coordinates in self.experiment.interface.sample_layout.items():
            if pixel not in self.experiment.selected_pixels:
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
        self.interface_frame.clear_output(wait=True)
        with self.interface_frame:
            self.scatter.set_color(colors)
            IPython.display.display(self.interface_fig)

    def _make_plot_frame(self):
        plot_frame = ipywidgets.Output(layout=ipywidgets.Layout(height='430px'))
        with plt.ioff():
            self.plot.make_plot()
        return plot_frame

    def _update_plot_frame(self):
        if self.experiment.state is ExperimentState.ABORTED:
            return
        self.plot_frame.clear_output(wait=True)
        with self.plot_frame:
            if self.experiment.state is not ExperimentState.RUNNING:
                return
            if self.preview:
                self.preview = False
                self.plot.clear_plot()
            if self.experiment.current_pixel_idx < 0:
                pass
            elif self.current_pixel != self.experiment.selected_pixels[self.experiment.current_pixel_idx]:
                self.current_pixel = self.experiment.selected_pixels[self.experiment.current_pixel_idx]
                self.plot.clear_plot()
            self.plot.update_plot()
            self.plot.figure.canvas.draw()
            IPython.display.display(self.plot.figure)

    def _make_widget(self):
        left_column = ipywidgets.VBox([
            ipywidgets.HBox([self.statusbar[0]],
                            layout=ipywidgets.Layout(justify_content='center')),
            ipywidgets.VBox([self.interface_frame],
                            layout=ipywidgets.Layout(justify_content='center', height='400px')),
            ipywidgets.HBox(self.buttons[0:3],
                            layout=ipywidgets.Layout(justify_content='center')),
            ipywidgets.HBox([self.preview_dropdown, self.buttons[3]],
                            layout=ipywidgets.Layout(justify_content='center'))
        ], layout=ipywidgets.Layout(width='400px', border='2px black solid', margin='2px', padding='5px'))
        right_column = ipywidgets.VBox([
            ipywidgets.HBox([self.statusbar[1]],
                            layout=ipywidgets.Layout(justify_content='center')),
            ipywidgets.VBox([self.plot_frame],
                            layout=ipywidgets.Layout(justify_content='center', height='480px'))
        ], layout=ipywidgets.Layout(width='580px', border='2px black solid', margin='2px', padding='5px'))
        return ipywidgets.HBox([
            ipywidgets.HTML(f"<style>{style}</style>",
                            layout=ipywidgets.Layout(display='none')),
            left_column,
            right_column
        ], layout=ipywidgets.Layout(height='600'))

    def _update_gui(self):
        self.stop_update = False
        while not self.stop_update:
            if self.input_disabled:
                continue
            self._update_statusbar()
            self._update_buttons()
            self._update_interface_frame()
            plt.pause(0.05)
            self._update_plot_frame()
            plt.pause(0.05)

    def display(self):
        """Displays the GUI widget and starts the update loop in a separate thread."""
        self.stop_update = True
        time.sleep(1)
        IPython.display.display(self.widget, display_id='display', clear=True)
        self.update_worker = threading.Thread(target=self._update_gui)
        self.update_worker.start()


state_colors = {
    'INITIAL': '#6c757d',
    'READY': '#ffc107',
    'RUNNING': '#28a745',
    'FINISHED': '#007bff',
    'ABORTED': '#dc3545'
}

style = f"""
.output_area + .output_area {{
    display: none;
}}


.widget-container {{
    overflow: hidden;
}}

.widget-dropdown {{
    width: initial;
    margin: 5px;
    font-size: 14px;
}}

.widget-dropdown .widget-label {{
    width: initial;
}}

.widget-dropdown select {{
    width: 115px;
}}

.widget-button {{
    width: 115px;
    margin: 5px;
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
}}

.widget-button .icon {{
    margin-right: 5px;
}}

.widget-button.mod-warning {{
    background-color: {state_colors['READY']};
    color: #fff;
}}

.widget-button.mod-success {{
    background-color: {state_colors['RUNNING']};
    color: #fff;
}}

.widget-button.mod-danger {{
    background-color: {state_colors['ABORTED']};
    color: #fff;
}}

.widget-button:disabled {{
    pointer-events: none;
}}
"""
