# Configuration

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
