<a name="graphical-user-interfaces"></a>
# Graphical User Interfaces

If you work with [Jupyter](https://jupyter.org/), you may use the Graphical User Interfaces (GUIs) which are implemented
in the form of [Jupyter Widgets](https://ipywidgets.readthedocs.io/en/stable/).

Currently, three GUIs are available:

## Experiment GUI

![experiment-gui](https://github.com/mxwalbert/cohesivm/assets/84664695/3de52bdc-1c8e-4de3-944c-e2db6df759f1)
On the left panel "Control", you see the current {class}`~cohesivm.experiment.ExperimentState`, followed by a 
representation of the {class}`~cohesivm.interfaces.Interface` and the control buttons at the bottom. The circles are 
annotated with the {attr}`~cohesivm.interfaces.Interface.contact_ids` and the colors correspond to their current state. 
On the right panel "Plot", the currently running {class}`~cohesivm.measurements.Measurement` is displayed. The plot is 
automatically updated as soon as new measurement data arrives in the 
{attr}`~cohesivm.experiment.Experiment.data_stream` of the {class}`~cohesivm.experiment.Experiment` object.

## Database GUI

![database-gui](https://github.com/mxwalbert/cohesivm/assets/84664695/3ad88365-1bf1-4281-87bf-78aa8e9dc918)
This GUI enables to display and filter the measurement data which is stored in an HDF5 file. At the top, you select to
display the data grouped in terms of the {class}`~cohesivm.measurements.Measurement` or by the
{attr}`~cohesivm.experiment.Experiment.sample_name` of the {class}`~cohesivm.experiment.Experiment` object. If you
choose the former one, you may additionally filter the data by means of measurement parameters. The button to the very
right of each data row enables you to copy the dataset path, to access it in the {class}`~cohesivm.database.Database`.

## Analysis GUI

![analysis-gui](https://github.com/mxwalbert/cohesivm/assets/84664695/0f8dbdb2-1464-456a-a0ac-cfed42ec9b4a)
Similar to the Experiment GUI, the "Interface" panel represents the contacts with their respective IDs. They can be
clicked to display the measured data in the "Plot" panel to the right. There, the arrows can be used to switch between
{attr}`~cohesivm.analysis.Analysis.functions` that are defined in the {class}`~cohesivm.analysis.Analysis` class. The
results of the {attr}`~cohesivm.analysis.Analysis.functions`, which are also implemented there, are shown in the table
below.

Detailed guides to work with the GUIs can be found in the {doc}`/`.
