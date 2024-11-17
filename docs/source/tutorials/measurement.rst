Implement a Measurement
=======================

.. include:: ../_snippets/important_contribute.rst

This tutorial will guide you through the process of implementing a new measurement procedure following
the :class:`~cohesivm.measurements.Measurement` abstract base class. To simulate a realistic use case, the tutorials
are based on the measurement of the sheet resistance and resistivity of materials using a four-point probe.

Here, we want to implement a routine which can be used to obtain the data for the four-point probe measurement.
Usually, you would only need a single datapoint but in some materials, e.g., semiconductors, you might observe a
current dependency of the sheet resistance. This gives us the possibility to actually collect arrays of datapoints
which is more application-oriented this tutorial as well as for the :doc:`/tutorials/analysis` tutorial.

Measurement Class
-----------------

Firstly, we have to define the private class attributes, beginning with the :class:`~cohesivm.interfaces.InterfaceType`
which we implemented in the tutorial :doc:`/tutorials/interface` already. Then follows the list of required channels,
which on the first position is a :class:`~cohesivm.channels.CurrentSource` and on the second position a
:class:`~cohesivm.channels.Voltmeter`. Finally, the :attr:`~cohesivm.measurements.Measurement.output_type` is defined
which is used to generate a `structured array <https://numpy.org/doc/stable/user/basics.rec.html>`_ from the data.

After that, we implement the constructor and the abstract :meth:`~cohesivm.measurements.Measurement.run`:

.. literalinclude:: /tutorials/workflow/fpp_components.py
    :language: python
    :lines: 1-3,7,9,13,14,145-180

During initialization, we ask for an explicit tuple of currents to be measured instead of a value range because it is
easier to implement. Additionally, the ``temperature`` has to and the ``film_thickness`` can be provided which are then
stored in the :class:`~cohesivm.database.Metadata` object. The former value might be necessary for compliance and data
completeness while the latter one can be important for the corresponding :class:`~cohesivm.analysis.Analysis`. The
dictionary of these settings is then passed to the constructor of the parent class.

For the measurement routine itself, we firstly handle the :class:`multiprocessing.Queue` object which is used to stream
measurement data to an output (e.g., for real-time plotting) and is a :class:`~cohesivm.data_stream.FakeQueue` by
default. Then, we open the device connection as a resource and loop over the ``currents`` where on the first channel,
the current is set and on the second channel, the voltage is measured. The result is put into the ``data_stream`` and
stored in a ``results`` list to, finally, return the data array.


Example Usage
-------------

This example depends on what we implemented in the tutorials :doc:`/tutorials/device` as well as part of the
:doc:`/tutorials/workflow/fpp_connect` module which is defined in the usage example. Additional resources are not
necessary, so let's run a measurement:

.. code-block:: pycon

    >>> cs = CurrentSourceChannel(False, 5.)
    >>> vm = VoltmeterChannel()
    >>> device = FPPDevice('123', [cs, vm])
    >>> currents = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
    >>> measurement = FPPMeasurement(currents, 300)
    >>> measurement.run(device)
    array([(1.e-06, 2.e-04), (1.e-05, 2.e-03), (1.e-04, 2.e-02),
           (1.e-03, 2.e-01), (1.e-02, 2.e+00), (1.e-01, 0.e+00)],
          dtype=[('Current (A)', '<f8'), ('Voltage (V)', '<f8')])

The result is exactly what we would expect because we know the resistance is 100 Ω which yields according to Ohm's
Law a 100-times higher voltage than the sourced current. For 0.1 A, we would measure a voltage of 10 V which is
above the ``max_voltage`` from the device settings, so we receive 0 V as final result. If we set a current above
0.2 A, we would trigger a ``ValueError`` from the ``CurrentSourceChannel``.
