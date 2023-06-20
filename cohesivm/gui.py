import ipywidgets
import IPython.display
import threading
import matplotlib.pyplot as plt
from cohesivm.abcs import ExperimentState, ExperimentABC, PlotABC


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
    def __init__(self, experiment: ExperimentABC, plot: PlotABC):
        experiment.data_stream = plot.data_stream
        self.experiment = experiment
        self.plot = plot

        self.buttons = self._make_buttons()
        self.interface_frame = self._make_interface_frame()
        self.plot_frame = self._make_plot_frame()
        self.output = self._make_output()
        self.no_output = ipywidgets.Output(layout=ipywidgets.Layout(heithg='0', width='0'))

        self.update_worker = None
        self.input_disabled = False

    def _make_buttons(self):
        setup_button = ipywidgets.Button(description='Setup', disabled=True, icon='cogs', button_style="primary")
        start_button = ipywidgets.Button(description='Start', disabled=True, icon='play', button_style="success")
        abort_button = ipywidgets.Button(description='Abort', disabled=True, icon='stop', button_style="danger")

        setup_button.on_click(self._bind_setup_button)
        start_button.on_click(self._bind_start_button)
        abort_button.on_click(self._bind_abort_button)

        return [setup_button, start_button, abort_button]

    @button_click
    def _bind_setup_button(self, button):
        self.experiment.setup()

    @button_click
    def _bind_start_button(self, button):
        self.experiment.start()

    @button_click
    def _bind_abort_button(self, button):
        self.experiment.abort()

    def _update_buttons(self):
        for button, active_state in zip(
                self.buttons,
                [ExperimentState.INITIAL, ExperimentState.READY, ExperimentState.RUNNING]):
            if self.experiment.state == active_state and not self.input_disabled:
                button.disabled = False
            else:
                button.disabled = True

    def _make_interface_frame(self):
        interface_frame = ipywidgets.Output(layout=ipywidgets.Layout(height='300px'))
        x_coords = [point[0] for point in self.experiment.interface.sample_layout.values()]
        y_coords = [point[1] for point in self.experiment.interface.sample_layout.values()]
        with plt.ioff():
            self.interface_fig, ax = plt.subplots()
            ax.axis('off')
            self.scatter = ax.scatter(x_coords, y_coords, c='gray')
            for label, coords in self.experiment.interface.sample_layout.items():
                ax.annotate(label, coords, textcoords="offset points", xytext=(8, -10), ha='center')
        return interface_frame

    def _update_interface_frame(self):
        colors = []
        for pixel, coordinates in self.experiment.interface.sample_layout.items():
            if pixel not in self.experiment.selected_pixels:
                colors.append('gray')
            elif self.experiment.current_pixel_idx is None:
                colors.append('black')
            elif self.experiment.current_pixel_idx < self.experiment.selected_pixels.index(pixel):
                colors.append('blue')
            elif self.experiment.current_pixel_idx > self.experiment.selected_pixels.index(pixel):
                colors.append('green')
            elif pixel == self.experiment.selected_pixels[self.experiment.current_pixel_idx]:
                colors.append('red')
        self.interface_frame.clear_output(wait=True)
        with self.interface_frame:
            self.scatter.set_color(colors)
            IPython.display.display(self.interface_fig)

    def _make_plot_frame(self):
        plot_frame = ipywidgets.Output(layout=ipywidgets.Layout(height='440px'))
        with plt.ioff():
            self.plot.make_plot()
        return plot_frame

    def _update_plot_frame(self):
        self.plot_frame.clear_output(wait=True)
        with self.plot_frame:
            self.plot.update_plot()
            self.plot.figure.canvas.draw()
            IPython.display.display(self.plot.figure)

    def _make_output(self):
        left_column = ipywidgets.VBox([
            ipywidgets.VBox([self.interface_frame], layout=ipywidgets.Layout(justify_content='center', height='400px')),
            ipywidgets.HBox(self.buttons, layout=ipywidgets.Layout(justify_content='center'))
        ], layout=ipywidgets.Layout(width='390px', justify_content='space-between'))
        right_column = ipywidgets.VBox([self.plot_frame], layout=ipywidgets.Layout(width='590px'))
        return ipywidgets.HBox([
            ipywidgets.HTML(f"<style>{style}</style>", layout=ipywidgets.Layout(display='none')),
            left_column,
            right_column
        ], layout=ipywidgets.Layout(width='980px', height='440px', justify_content='center'))

    def _update_gui(self):
        while self.experiment.state not in [ExperimentState.FINISHED, ExperimentState.ABORTED]:
            if self.input_disabled:
                continue
            self._update_buttons()
            self._update_interface_frame()
            plt.pause(0.05)
            self._update_plot_frame()
            plt.pause(0.05)
        self._update_buttons()
        self._update_interface_frame()

    def display(self):
        IPython.display.display(self.output)
        try:
            self.update_worker.stop()
        except AttributeError:
            pass
        self.update_worker = threading.Thread(target=self._update_gui, daemon=True)
        self.update_worker.start()


style = """
.widget-button {
    min-width: 100px;
    margin: 5px;
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
}

.widget-button .icon {
    margin-right: 5px;
}

.widget-button.primary {
    background-color: #007bff;
    color: #000;
}

.widget-button.success {
    background-color: #28a745;
    color: #000;
}

.widget-button.danger {
    background-color: #dc3545;
    color: #000;
}

.widget-button:disabled {
    pointer-events: none;
}
"""
