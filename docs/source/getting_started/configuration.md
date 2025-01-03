# Configuration

A ``config.ini`` file should be placed in the root of your project to configure the hardware ports/addresses of the
contact interfaces and measurement devices. Some DCMI metadata terms also need to be defined there. COHESIVM implements
a config parser which allows to access these values, e.g.:

```pycon
>>> import cohesivm
>>> cohesivm.config.get_option('DCMI', 'creator')
Dow, John
```

## Template

[A preconfigured file](https://github.com/mxwalbert/cohesivm/blob/main/config.ini) with the currently implemented 
interfaces and devices can be copied from the repository, or you can create your own from this template:

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

The names of the sections (e.g., ``NAME_OF_USB_INTERFACE``) must be unique but can be chosen freely since they are 
referenced manually. The options (e.g., ``com_port``), on the other hand, should follow the signature of the class 
constructor to use them efficiently. For example, an {class}`~cohesivm.interfaces.Interface` implementation 
``DemoInterface`` which requires the ``com_port`` parameter could be initialized using the configuration template 
from above:

```python
interface = DemoInterface(**config.get_section('NAME_OF_USB_INTERFACE'))
```

## Example

In a common scenario, you probably want to configure multiple devices to use them at once. Let's consider the case 
where you need two {class}`~cohesivm.devices.ossila.OssilaX200` devices which are both connected via USB. Then, in the 
``DEVICES`` part of the configuration, you would define two distinctive sections and set the required ``address`` 
option:

```ini
# DEVICES -------------------------------------------------------------------------------------------------------------

[OssilaX200_1]
address = COM4

[OssilaX200_2]
address = COM5

# ---------------------------------------------------------------------------------------------------------------------
```

To initialize the devices, you could do something similar to the {doc}`Basic Usage</getting_started/basic_usage>` 
example:


```python
from cohesivm import config
from cohesivm.devices.ossila import OssilaX200
smu1 = OssilaX200.VoltageSMUChannel()
device1 = OssilaX200.OssilaX200(channels=[smu1], **config.get_section('OssilaX200_1'))
smu2 = OssilaX200.VoltageSMUChannel()
device2 = OssilaX200.OssilaX200(channels=[smu2], **config.get_section('OssilaX200_2'))
```
