Implement a Device
==================

.. include:: ../_snippets/important_contribute.rst

This tutorial will guide you through the process of implementing a new device following
the :class:`~cohesivm.devices.Device` abstract base class. To simulate a realistic use case, the tutorials are based on
the measurement of the sheet resistance and resistivity of materials using a four-point probe.

Channel Classes
---------------

To begin with, child classes of the :class:`~cohesivm.channels.Channel` must be defined. The four-point resistivity
measurement requires to source a specific current between two terminals and measure the resulting voltage across two
other terminals. Therefore, we need two channels to act as a current source and voltmeter, respectively:

.. literalinclude:: /tutorials/workflow/fpp_components.py
    :language: python
    :lines: 4,5,8,9,19-86

Here we consider an actual physical device which can be controlled through a simple Python API. This mimetic module
provides only two methods ``set()`` and ``get()`` which allows us to perform all necessary tasks.

Firstly, we define a general ``FPPChannel`` which implements the abstract methods that are required by
the :class:`~cohesivm.channels.Channel`. The resource of the device connection is put into
the :attr:`~cohesivm.channels.Channel.connection` by the :meth:`~cohesivm.devices.Device.connect` contextmanager (see
below). On this, we simply call in :meth:`~cohesivm.channels.Channel.get_property` and
:meth:`~cohesivm.channels.Channel.set_property` the methods from our mimetic API and specify which channel we are
referring to. The :meth:`~cohesivm.channels.Channel.enable` and :meth:`~cohesivm.channels.Channel.disable` methods are
self-explanatory.

The ``CurrentSourceChannel`` inherits, next to this general channel class, a specific trait class
:class:`~cohesivm.channels.CurrentSource` which includes the :meth:`~cohesivm.channels.Channel.source_current()`
abstract method. Its implementation ensures through type and value checking that the ``current`` can be safely sent to
the device. Additionally, the ``_check_settings()`` ensures that the settings which are specified in the constructor
comply with the equipment.

In the same way, the ``VoltmeterChannel`` inherits the :meth:`~cohesivm.channels.Channel.measure_voltage()` through
the :class:`~cohesivm.channels.Voltmeter` trait class. However, the implementation is much simpler because no safety
measures are required in this case.


Device Class
------------

For the actual :class:`~cohesivm.devices.Device` itself only a single abstract method must be implemented but we also
define a constructor which allows us to do some parameter checking:

.. literalinclude:: /tutorials/workflow/fpp_components.py
    :language: python
    :lines: 6,10,15-20,89-114

We check, if the provided channels are subclasses of the ``FPPChannel`` and if there are no duplicate
channels. Since we hardcoded the :attr:`~cohesivm.channels.Channel.identifier`, only a single ``CurrentSourceChannel``
and a single ``VoltmeterChannel`` are allowed but we may use one or both. Additionally, we have to provide a
``com_port`` in the constructor which is used by the :meth:`~cohesivm.devices.Device._establish_connection`.


Example Usage
-------------

In order to test the implemented device, we build part of the :doc:`/tutorials/workflow/fpp_connect` mimetic module:

.. literalinclude:: /tutorials/workflow/fpp_connect.py
    :language: python
    :lines: 1-11,17-55

Here, we simulate the behaviour of a simple resistor and depending on the applied current we will measure a specific
voltage which corresponds to the predefined resistance after Ohm's Law.

Finally, let's initialize the channels and device and run a measurement:

.. code-block:: python

    >>> cs = CurrentSourceChannel(False, 5.)
    >>> vm = VoltmeterChannel()
    >>> device = FPPDevice('4', [cs, vm])
    >>> with device.connect():
    ...     device.channels[0].source_current(0.02)
    ...     print(device.channels[1].measure_voltage())
    2.0
    >>> with device.connect():
    ...     device.channels[0].source_current(0.051)
    ...     print(device.channels[1].measure_voltage())
    0.0

The first print statement outputs the expected value since we set a resistance of 100 Ω in the class which results
in 2 V at 20 mA. In the second case, since the resulting voltage would exceed the ``max_voltage`` of 5 V, the
current is set to 0 A and 0 V are measured. This example also confirms that the settings, as provided in the
constructor, are correctly sent to the device.
