# COHESIVM: Combinatorial h+/e- Sample Investigation using Voltaic Measurements

## Introduction

The COHESIVM Python package provides a versatile framework for conducting combinatorial voltaic measurements in
scientific research and development. In order to enable a broad range of electrical and electrochemical analysis
methods, COHESIVM uses a generalized design of the main components which facilitates the extension and adaptation to
different measurement devices and routines. These components are cohesively put together in an
[``Experiment``](https://cohesivm.readthedocs.io/reference/experiment.html#cohesivm.experiment.Experiment) class which runs compatibility checks and executes the actual measurements.

### Key Features:

- **Modular Design:** COHESIVM adopts a module-oriented approach where components such as measurement devices
  ([``Device``](https://cohesivm.readthedocs.io/reference/devices.html#cohesivm.devices.Device)), contacting interfaces ([``Interface``](https://cohesivm.readthedocs.io/reference/interfaces.html#cohesivm.interfaces.Interface)), and measurement
  routines ([``Measurement``](https://cohesivm.readthedocs.io/reference/measurements.html#cohesivm.measurements.Measurement)) are abstracted into interchangeable units. This modular
  architecture enhances flexibility in experimental setups and makes it easy to add new component implementations.
- **Combinatorial Flexibility:** By abstracting the class for the contacting interface, COHESIVM enables diverse
  configurations for sample investigation. Researchers can simply implement their combinatorial sample design or even
  interface a robotic contacting system.
- **Data Handling:** Collected data is stored in a structured [HDF5](https://www.hdfgroup.org/solutions/hdf5/) database
  format using the [``Database``](https://cohesivm.readthedocs.io/reference/database.html#cohesivm.database.Database) class, ensuring efficient data management and accessibility.
  [``Metadata``](https://cohesivm.readthedocs.io/reference/database.html#cohesivm.database.Metadata) is collected based on the [DCMI standard](http://purl.org/dc/terms/) which is
  extended by COHESIVM-specific metadata terms.
- **Analysis and GUIs:** Alongside the measurement routines, analysis functions and plots can be implemented, extending
  the [``Analysis``](https://cohesivm.readthedocs.io/reference/analysis.html#cohesivm.analysis.Analysis) base class. Together with the graphical user interface (also available for
  conducting experiments and reviewing the database contents), initial screening of the data is facilitated.
 
## Table of Contents
- [Getting Started](#getting-started)
- [Graphical User Interfaces](#graphical-user-interfaces)
- [Examples](#examples)
- [Package Reference](#package-reference)
- [Contributing](#contributing)
- [License](#license)

## Getting Started <a name="getting-started"></a>

### Installation

#### Using pip
To install the core COHESIVM package from the Python Package Index (PyPI), simply run:

```console
pip install cohesivm
```

This command will download and install the latest stable version of COHESIVM and its core dependencies.

If you want to use the Graphical User Interfaces inside your [Jupyter](https://jupyter.org/) environment, make sure to 
specify the ``gui`` extra:

```console
pip install cohesivm[gui]
```

Further extras exist for the implemented devices and for developers (refer to the ``pyproject.toml`` in the source 
files to get a listing of all available optional dependencies).

#### Cloning from GitHub
If you want to install the development version of the package from the GitHub repository, follow these steps:
1. **Clone** the repository to your local machine:
    ```console
    git clone https://github.com/mxwalbert/cohesivm.git
    ```
2. **Navigate** into the cloned directory:
    ```console
    cd cohesivm
    ```
3. **Install** the package and its dependencies:
    ```console
    pip install .
    ```

### Configuration

A ``config.ini`` file should be placed in the root of your project to configure the hardware ports/addresses of the
contact interfaces and measurement devices. Some DCMI metadata terms also need to be defined there. COHESIVM implements
a config parser which allows to access these values, e.g.:

```pycon
>>> import cohesivm
>>> cohesivm.config.get_option('DCMI', 'creator')
Dow, John
```

A working file with the implemented interfaces and devices can be copied from the GitHub repository, or you can create
your own from this template:

```ini
# This file is used to configure the project as well as the devices and interfaces (e.g., COM ports, addresses, ...).

# METADATA ------------------------------------------------------------------------------------------------------------

[DCMI]
# The following options correspond to the terms defined by the Dublin Core Metadata Initiative.
# See https://purl.org/dc/terms/ for detailed descriptions.
publisher = "Your Company Ltd."
creator = "Dow, John"
rights = <https://link.to/licence>
subject = "modular design"; "combinatorial flexibility"; "data handling"; "analysis and gui"

# ---------------------------------------------------------------------------------------------------------------------


# INTERFACES ----------------------------------------------------------------------------------------------------------

[NAME_OF_USB_INTERFACE]
com_port = 42

# ---------------------------------------------------------------------------------------------------------------------


# DEVICES -------------------------------------------------------------------------------------------------------------

[NAME_OF_NETWORK_DEVICE]
address = localhost
port = 8888
timeout = 0.1

# ---------------------------------------------------------------------------------------------------------------------
```

### Basic Usage

With working implementations of the main components ([``Device``](https://cohesivm.readthedocs.io/reference/devices.html#cohesivm.devices.Device),
[``Interface``](https://cohesivm.readthedocs.io/reference/interfaces.html#cohesivm.interfaces.Interface), [``Measurement``](https://cohesivm.readthedocs.io/reference/measurements.html#cohesivm.measurements.Measurement)), setting up and running an
experiment only takes a few lines of code:

```python
from cohesivm import config
from cohesivm.database import Database, Dimensions
from cohesivm.devices.agilent import Agilent4156C
from cohesivm.measurements.iv import CurrentVoltageCharacteristic
from cohesivm.interfaces import MA8X8
from cohesivm.experiment import Experiment
from cohesivm.progressbar import ProgressBar

# Create a new or load an existing database
db = Database('Test.h5')

# Configure the components
smu = Agilent4156C.SweepVoltageSMUChannel()
device = Agilent4156C.Agilent4156C(channels=[smu], **config.get_section('Agilent4156C'))
interface = MA8X8(com_port=config.get_option('MA8X8', 'com_port'), pixel_dimensions=Dimensions.Circle(radius=0.425))
measurement = CurrentVoltageCharacteristic(start_voltage=-2.0, end_voltage=2.0, voltage_step=0.01, illuminated=True)

# Combine the components in an experiment
experiment = Experiment(
    database=db,
    device=device,
    interface=interface,
    measurement=measurement,
    sample_id='test_sample_42',
    selected_contacts=None
)

# Optionally set up a progressbar
pbar = ProgressBar(experiment)

# Run the experiment
with pbar.show():
    experiment.quickstart()
```

If you want to change the measurement device to a different one, you only need to adjust the lines for the
[``Channel``](https://cohesivm.readthedocs.io/reference/channels.html#cohesivm.channels.Channel) and the [``Device``](https://cohesivm.readthedocs.io/reference/devices.html#cohesivm.devices.Device) accordingly:

```python
from cohesivm.devices.ossila import OssilaX200
smu = OssilaX200.VoltageSMUChannel()
device = OssilaX200.OssilaX200(channels=[smu], **config.get_section('OssilaX200'))
```

## Graphical User Interfaces <a name="graphical-user-interfaces"></a>

If you work with [Jupyter](https://jupyter.org/), you may use the Graphical User Interfaces (GUIs) which are implemented
in the form of [Jupyter Widgets](https://ipywidgets.readthedocs.io/en/stable/). Currently, three GUIs are available:

### Experiment GUI

![experiment-gui](https://github.com/mxwalbert/cohesivm/assets/84664695/3de52bdc-1c8e-4de3-944c-e2db6df759f1)
On the left panel "Control", you see the current [``ExperimentState``](https://cohesivm.readthedocs.io/reference/experiment.html#cohesivm.experiment.ExperimentState), followed by a 
representation of the [``Interface``](https://cohesivm.readthedocs.io/reference/interfaces.html#cohesivm.interfaces.Interface) and the control buttons at the bottom. The circles are 
annotated with the [``contact_ids``](https://cohesivm.readthedocs.io/reference/interfaces.html#cohesivm.interfaces.Interface.contact_ids) and the colors correspond to their current state. 
On the right panel "Plot", the currently running [``Measurement``](https://cohesivm.readthedocs.io/reference/measurements.html#cohesivm.measurements.Measurement) is displayed. The plot is 
automatically updated as soon as new measurement data arrives in the 
[``data_stream``](https://cohesivm.readthedocs.io/reference/experiment.html#cohesivm.experiment.Experiment.data_stream) of the [``Experiment``](https://cohesivm.readthedocs.io/reference/experiment.html#cohesivm.experiment.Experiment) object.

### Database GUI

![database-gui](https://github.com/mxwalbert/cohesivm/assets/84664695/3ad88365-1bf1-4281-87bf-78aa8e9dc918)
This GUI enables to display and filter the measurement data which is stored in an HDF5 file. At the top, you select to
display the data grouped in terms of the [``Measurement``](https://cohesivm.readthedocs.io/reference/measurements.html#cohesivm.measurements.Measurement) or by the
[``sample_name``](https://cohesivm.readthedocs.io/reference/experiment.html#cohesivm.experiment.Experiment.sample_name) of the [``Experiment``](https://cohesivm.readthedocs.io/reference/experiment.html#cohesivm.experiment.Experiment) object. If you
choose the former one, you may additionally filter the data by means of measurement parameters. The button to the very
right of each data row enables you to copy the dataset path, to access it in the [``Database``](https://cohesivm.readthedocs.io/reference/database.html#cohesivm.database.Database).

### Analysis GUI

![analysis-gui](https://github.com/mxwalbert/cohesivm/assets/84664695/0f8dbdb2-1464-456a-a0ac-cfed42ec9b4a)
Similar to the Experiment GUI, the "Interface" panel represents the contacts with their respective IDs. They can be
clicked to display the measured data in the "Plot" panel to the right. There, the arrows can be used to switch between
[``functions``](https://cohesivm.readthedocs.io/reference/analysis.html#cohesivm.analysis.Analysis.functions) that are defined in the [``Analysis``](https://cohesivm.readthedocs.io/reference/analysis.html#cohesivm.analysis.Analysis) class. The
results of the [``functions``](https://cohesivm.readthedocs.io/reference/analysis.html#cohesivm.analysis.Analysis.functions), which are also implemented there, are shown in the table
below.

Detailed guides to work with the GUIs can be found in the [documentation](https://cohesivm.readthedocs.io/).

## Examples <a name="examples"></a>

### Run an Experiment

Follow the [Basic Usage](https://cohesivm.readthedocs.io//getting_started/basic_usage.html) example to set up and run an 
[``Experiment``](https://cohesivm.readthedocs.io/reference/experiment.html#cohesivm.experiment.Experiment). If you do not have all components ready yet, follow these tutorials:

- [Implement a Device](https://cohesivm.readthedocs.io//tutorials/device.html)
- [Implement an Interface](https://cohesivm.readthedocs.io//tutorials/interface.html)
- [Implement a Measurement](https://cohesivm.readthedocs.io//tutorials/measurement.html)

To follow the other examples you may just run the code from the [Basic Usage](https://cohesivm.readthedocs.io//getting_started/basic_usage.html) 
example even if you do not have access to the hardware. This will fail but create an HDF5 file and store an empty 
dataset entry.

### Manage the Data

After you collected some data and stored it in an HDF5 file, you can use the [``Database``](https://cohesivm.readthedocs.io/reference/database.html#cohesivm.database.Database) class
to work with it. First, initialise the [``Database``](https://cohesivm.readthedocs.io/reference/database.html#cohesivm.database.Database) object and list the samples which are stored
there:

```pycon
>>> from cohesivm.database import Database
>>> db = Database('Test.h5')
>>> db.get_sample_ids()
['test_sample_42']
```

This is exactly the [``sample_id``](https://cohesivm.readthedocs.io/reference/experiment.html#cohesivm.experiment.Experiment.sample_id) which was specified when the
[``Experiment``](https://cohesivm.readthedocs.io/reference/experiment.html#cohesivm.experiment.Experiment) was configured, and it can be used to retrieve the actual
[``dataset``](https://cohesivm.readthedocs.io/reference/experiment.html#cohesivm.experiment.Experiment.dataset) path in the [``Database``](https://cohesivm.readthedocs.io/reference/database.html#cohesivm.database.Database) object:

```pycon
>>> db.filter_by_sample_id('test_sample_42')
['/CurrentVoltageCharacteristic/55d96687ee75aa11:26464063430fe52f:a69a946e7a02e547:c8965a35118ce6fc:67a8bfb44702cfc7:8131a44cea4d4bb8/2024-07-01T10:44:59.033161-test_sample_42']
```

The resulting list contains the path strings for all experiments with the specified
[``sample_id``](https://cohesivm.readthedocs.io/reference/experiment.html#cohesivm.experiment.Experiment.sample_id) (currently only one entry). These strings get quite long because they
contain the [``name``](https://cohesivm.readthedocs.io/reference/measurements.html#cohesivm.measurements.Measurement.name) of the [``Measurement``](https://cohesivm.readthedocs.io/reference/measurements.html#cohesivm.measurements.Measurement)
procedure, followed by a hashed representation of the [``settings``](https://cohesivm.readthedocs.io/reference/measurements.html#cohesivm.measurements.Measurement.settings) dictionary,
and finally the datetime combined with the [``sample_id``](https://cohesivm.readthedocs.io/reference/experiment.html#cohesivm.experiment.Experiment.sample_id). With this
[``dataset``](https://cohesivm.readthedocs.io/reference/experiment.html#cohesivm.experiment.Experiment.dataset) path, you may retrieve some information from the
[``Metadata``](https://cohesivm.readthedocs.io/reference/database.html#cohesivm.database.Metadata) object which got created by the [``Experiment``](https://cohesivm.readthedocs.io/reference/experiment.html#cohesivm.experiment.Experiment):

```pycon
>>> dataset = db.filter_by_sample_id('test_sample_42')[0]
>>> metadata = db.load_metadata(dataset)
>>> metadata.sample_id, metadata.device, metadata.interface, metadata.measurement
('test_sample_42', 'Agilent4156C', 'MA8X8', 'CurrentVoltageCharacteristic')
```

Storing a new dataset is less trivial because you need a fully qualified [``Metadata``](https://cohesivm.readthedocs.io/reference/database.html#cohesivm.database.Metadata) object,
which asks for a large number of arguments. Anyway, this is usually handled by the
[``Experiment``](https://cohesivm.readthedocs.io/reference/experiment.html#cohesivm.experiment.Experiment) class because it guarantees that the specified components are compatible. For
testing, the [``Metadata``](https://cohesivm.readthedocs.io/reference/database.html#cohesivm.database.Metadata) object from above may be used to initialize a new dataset:

```pycon
>>> db.initialize_dataset(metadata)
'/CurrentVoltageCharacteristic/55d96687ee75aa11:26464063430fe52f:a69a946e7a02e547:c8965a35118ce6fc:67a8bfb44702cfc7:8131a44cea4d4bb8/2024-07-01T10:46:05.910371-test_sample_42'
```

This yields practically the same ``dataset`` path as before, only the datetime is different. Adding data entries, on
the other hand, is fairly simple because you only need to specify the ``dataset`` and the ``contact_id`` (alongside
the ``data`` of course):

```pycon
>>> db.save_data(np.array([1]), dataset)
>>> db.save_data(np.array([42]), dataset, '1')
```

Finally, you may load a data entry by specifying the ``contact_id`` (or a list of several) or load an entire dataset,
including the [``Metadata``](https://cohesivm.readthedocs.io/reference/database.html#cohesivm.database.Metadata):

```pycon
>>> db.load_data(dataset, '0')
[array([1])]
>>> db.load_data(dataset, ['0', '1'])
[array([1]), array([42])]
>>> db.load_dataset(dataset)
({'0': array([1]), '1': array([42])}, Metadata(CurrentVoltageCharacteristic, Agilent4156C, MA8X8))
```

The [``Database``](https://cohesivm.readthedocs.io/reference/database.html#cohesivm.database.Database) class also implements methods for filtering datasets based on
[``settings``](https://cohesivm.readthedocs.io/reference/measurements.html#cohesivm.measurements.Measurement.settings) of the [``Measurement``](https://cohesivm.readthedocs.io/reference/measurements.html#cohesivm.measurements.Measurement). Check out the 
documentation of the [``filter_by_settings``](https://cohesivm.readthedocs.io/reference/database.html#cohesivm.database.Database.filter_by_settings) and 
[``filter_by_settings_batch``](https://cohesivm.readthedocs.io/reference/database.html#cohesivm.database.Database.filter_by_settings_batch) to learn more.
### Analyse the Results

The [``Analysis``](https://cohesivm.readthedocs.io/reference/analysis.html#cohesivm.analysis.Analysis) is tightly bound with the [``Measurement``](https://cohesivm.readthedocs.io/reference/measurements.html#cohesivm.measurements.Measurement) because
this will determine how the data is shaped and which features you want to extract from it. Therefore, the base class
should be extended as explained in this tutorial:

- [Implement an Analysis](https://cohesivm.readthedocs.io//tutorials/analysis.html)

However, in the following example, the base class will be used to show the basic functionality.

Since the [``MA8X8``](https://cohesivm.readthedocs.io/reference/interfaces.html#cohesivm.interfaces.MA8X8) interface was used in the previous examples, the dataset should be filled
with ``data`` accordingly. If you already have an HDF5 file from following the basic usage example ("Test.h5"), then
this script should do the job:

```python
import numpy as np
from cohesivm.database import Database

# load existing data and corresponding metadata
db = Database('Test.h5')
dataset = db.filter_by_sample_id('test_sample_42')[0]
metadata = db.load_metadata(dataset)

# create a new data to not interfere with previous examples
dataset = db.initialize_dataset(metadata)

# iterate over contact_ids and save data arrays
for contact_id in metadata.contact_ids:
    db.save_data(np.array(range(10), dtype=[('Voltage (V)', float)]), dataset, contact_id)

# load the data
data, metadata = db.load_dataset(dataset)
```

This time, the [``save_data``](https://cohesivm.readthedocs.io/reference/database.html#cohesivm.database.Database.save_data) method was used correctly (contrary to the previous
examples) because the provided ``data`` should always be
a [structured array](https://numpy.org/doc/stable/user/basics.rec.html).

Next, [``functions``](https://cohesivm.readthedocs.io/reference/analysis.html#cohesivm.analysis.Analysis.functions) and [``plots``](https://cohesivm.readthedocs.io/reference/analysis.html#cohesivm.analysis.Analysis.plots) must be defined:

```pycon
>>> def maximum(contact_id: str) -> float:
...     return max(data[contact_id]['Voltage (V)'])
>>> functions = {'Maximum': maximum}
>>> plots = {}  # will be spared for simplicity (refer to the tutorial instead)
```

This approach seems too complex for what the function does, but it makes sense if you consider that this should be
implemented in a separate [``Analysis``](https://cohesivm.readthedocs.io/reference/analysis.html#cohesivm.analysis.Analysis) class. There, the data is stored as a property and the
[``functions``](https://cohesivm.readthedocs.io/reference/analysis.html#cohesivm.analysis.Analysis.functions) (i.e., methods) have direct access to it. Due to the use of structured
arrays (which facilitate to store the quantity and the unit alongside the data), the label also needs to be stated
explicitly. But, again, this will normally be available as a property.

In the following, the class is initialized with and without using the [``Metadata``](https://cohesivm.readthedocs.io/reference/database.html#cohesivm.database.Metadata) from the
dataset. The former approach has the advantage that all available fields could be accessed by the
[``functions``](https://cohesivm.readthedocs.io/reference/analysis.html#cohesivm.analysis.Analysis.functions), e.g., values that are stored in the
[``measurement_settings``](https://cohesivm.readthedocs.io/reference/database.html#cohesivm.database.Metadata.measurement_settings).

```pycon
>>> from cohesivm.analysis import Analysis
# without metadata, the contact_position_dict must be provided
>>> analysis = Analysis(functions, plots, data, metadata.contact_position_dict)
# with metadata, additional metadata fields can be used in the analysis
>>> analysis = Analysis(functions, plots, (data, metadata))
>>> analysis.metadata.measurement_settings['illuminated']
True
```

The main usage of the [``Analysis``](https://cohesivm.readthedocs.io/reference/analysis.html#cohesivm.analysis.Analysis), besides providing the framework for
the [Analysis GUI](https://cohesivm.readthedocs.io//guis/analysis.html), is to quickly generate maps of analysis results:

```pycon
>>> analysis.generate_result_maps('Maximum')[0]
array([[9., 9., 9., 9., 9., 9., 9., 9.],
       [9., 9., 9., 9., 9., 9., 9., 9.],
       [9., 9., 9., 9., 9., 9., 9., 9.],
       [9., 9., 9., 9., 9., 9., 9., 9.],
       [9., 9., 9., 9., 9., 9., 9., 9.],
       [9., 9., 9., 9., 9., 9., 9., 9.],
       [9., 9., 9., 9., 9., 9., 9., 9.],
       [9., 9., 9., 9., 9., 9., 9., 9.]])
```

As expected, the maximum value of the generated data is placed in a 2D numpy array on locations corresponding to
the [``contact_positions``](https://cohesivm.readthedocs.io/reference/Interface.html#interfaces.Interface.contact_positions).
## Package Reference <a name="package-reference"></a>

The package reference can be found in the [documentation](https://cohesivm.readthedocs.io/).

## Contributing <a name="contributing"></a>

We welcome contributions from the community to make COHESIVM better! If you'd like to contribute an implementation 
of a [``Device``](https://cohesivm.readthedocs.io/reference/devices.html#cohesivm.devices.Device), an [``Interface``](https://cohesivm.readthedocs.io/reference/interfaces.html#cohesivm.interfaces.Interface), 
a [``Measurement``](https://cohesivm.readthedocs.io/reference/measurements.html#cohesivm.measurements.Measurement) or an [``Analysis``](https://cohesivm.readthedocs.io/reference/analysis.html#cohesivm.analysis.Analysis), please follow these steps:

1. Fork the repository to your own GitHub account.
2. Clone your forked repository to your local machine.
3. Create a new branch for your new component: git checkout -b my-new-component.
4. Make your changes and ensure the code passes existing tests.
5. Add new tests for your changes, if applicable.
6. Commit your changes with clear and concise messages.
7. Push your branch to your forked repository: git push origin my-new-feature.
8. Open a pull request to the main repository, describing the changes and why they should be merged.

Please make sure to follow the project's structure. The best way to start is to have a look at the tutorials given in 
the [documentation](https://cohesivm.readthedocs.io/). Also, don't forget to write tests for your newly implemented feature which may requires a new custom 
marker in the ``conftest.py`` (e.g., if you implement a physical device for which the tests will always fail if it is 
not connected).

You may also contribute by submitting feature requests, bugs and other issues over GitHub.

Thank you for your contributions!


## License <a name="license"></a>
The source code of this project is licensed under the [MIT license](LICENSE), and the hardware design and schematics 
are licensed under the [CERN OHL v2 Permissive license](hardware/LICENSE).
