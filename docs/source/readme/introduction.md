# Introduction

The COHESIVM Python package provides a versatile framework for conducting combinatorial voltaic measurements in
scientific research and development. In order to enable a broad range of electrical and electrochemical analysis
methods, COHESIVM uses a generalized design of the main components which facilitates the extension and adaptation to
different measurement devices and routines. These components are cohesively put together in an
{class}`~cohesivm.experiment.Experiment` class which runs compatibility checks and executes the actual measurements.

## Key Features:

- **Modular Design:** COHESIVM adopts a module-oriented approach where components such as measurement devices
  ({class}`~cohesivm.devices.Device`), contacting interfaces ({class}`~cohesivm.interfaces.Interface`), and measurement
  routines ({class}`~cohesivm.measurements.Measurement`) are abstracted into interchangeable units. This modular
  architecture enhances flexibility in experimental setups and makes it easy to add new component implementations.
- **Combinatorial Flexibility:** By abstracting the class for the contacting interface, COHESIVM enables diverse
  configurations for sample investigation. Researchers can simply implement their combinatorial sample design or even
  interface a robotic contacting system.
- **Data Handling:** Collected data is stored in a structured [HDF5](https://www.hdfgroup.org/solutions/hdf5/) database
  format using the {class}`~cohesivm.database.Database` class, ensuring efficient data management and accessibility.
  {class}`~cohesivm.database.Metadata` is collected based on the [DCMI standard](http://purl.org/dc/terms/) which is
  extended by COHESIVM-specific metadata terms.
- **Analysis and GUIs:** Alongside the measurement routines, analysis functions and plots can be implemented, extending
  the {class}`~cohesivm.analysis.Analysis` base class. Together with the graphical user interface (also available for
  conducting experiments and reviewing the database contents), initial screening of the data is facilitated.
 