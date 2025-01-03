# Introduction

The COHESIVM Python package provides a generalized framework for conducting combinatorial voltaic measurements in
scientific research and development. The modular architecture enables researchers to adapt it to diverse experimental 
setups by extending its components to support custom configurations. These components are cohesively put together in an
{class}`~cohesivm.experiment.Experiment` class which runs compatibility checks, manages data storage, and 
executes the measurements.

## Key Features:

- **Modular Design:** COHESIVM adopts a module-oriented approach where components such as measurement devices
  ({class}`~cohesivm.devices.Device`), contacting interfaces ({class}`~cohesivm.interfaces.Interface`), and measurement
  routines ({class}`~cohesivm.measurements.Measurement`) are abstracted into interchangeable units. This modular
  architecture enhances flexibility in experimental setups and makes it easy to add new component implementations.
  The tutorials in the {doc}`/` provide an extensive description of implementing custom components.
- **Combinatorial Flexibility:** By abstracting the class for the contacting interface, COHESIVM enables diverse
  configurations for sample investigation. The [MA8X8 measurement array](https://github.com/mxwalbert/cohesivm/tree/main/hardware/ma8x8), as implemented in the current core 
  version, is only one example for an electrode contact array. Researchers can add custom implementations of the 
  {class}`~cohesivm.interfaces.Interface` class to support other configurations or, for example, robotic contacting 
  systems.
- **Data Handling:** Collected data is stored in a structured [HDF5](https://www.hdfgroup.org/solutions/hdf5/) database
  format using the {class}`~cohesivm.database.Database` class, ensuring efficient data management and accessibility.
  {class}`~cohesivm.database.Metadata` is collected based on the [DCMI standard](http://purl.org/dc/terms/) which is
  extended by COHESIVM-specific metadata terms.
- **Analysis and GUIs:** Alongside the measurement routines, analysis functions and plots can be implemented, extending
  the {class}`~cohesivm.analysis.Analysis` base class. Together with the graphical user interface (also available for
  conducting experiments and reviewing the database contents), initial screening of the data is facilitated.
 