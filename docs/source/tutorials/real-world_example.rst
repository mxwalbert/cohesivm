Real-World Example
==================

This tutorial provides a high-level description of using COHESIVM, based on a real-world example.


Sample and Measurement Setup
----------------------------

.. image:: https://raw.githubusercontent.com/mxwalbert/cohesivm/refs/heads/main/hardware/ma8x8/ma8x8.png

The sample to be measured is a heterojunction of Ga\ :sub:`2`\ O\ :sub:`3` and Cu\ :sub:`2`\ O thin films deposited on
an ITO-covered glass substrate with a size of 25 |_| mm |_| x |_| 25 |_| mm. Details for the preparation and
properties of these thin films are described in [DWEW24]_.

Using the contact mask for the :class:`~cohesivm.interfaces.ma8x8.MA8X8` interface, for which the hardware description
is `available in the repository <https://github.com/mxwalbert/cohesivm/tree/main/hardware/ma8x8>`_, gold is sputtered
on top of the heterojunction to obtain 64 |_| devices. The sample is mounted on the contact interface, with the gold
areas facing the pogo pins. For measuring with and without illumination, the whole interface setup is placed in a
lightproof enclosure, under an `Ossila Solar Simulator <https://www.ossila.com/products/solar-simulator>`_ at the
recommended distance of 85 |_| mm.

The `Agilent 4156C Precision Semiconductor Parameter Analyzer <https://www.keysight.com/at/de/product/4156C/precision-semiconductor-parameter-analyzer.html>`_,
as implemented in the :class:`~cohesivm.devices.agilent.Agilent4156C.Agilent4156C` device class, is employed to measure
the :class:`~cohesivm.measurements.iv.CurrentVoltageCharacteristic` of the heterojunction devices.


Running the Experiment
----------------------

Exactly like in the :doc:`../getting_started/basic_usage` example, we begin with importing the required modules and
classes. Depending on the application, only the highlighted lines will be different, because this is where we select
the :class:`~cohesivm.devices.Device`, :class:`~cohesivm.interfaces.Interface`, and
:class:`~cohesivm.measurements.Measurement` for a specific :class:`~cohesivm.experiment.Experiment`.

.. code-block:: python
    :emphasize-lines: 5-7

    from cohesivm import config
    from cohesivm.database import Database, Dimensions
    from cohesivm.experiment import Experiment
    from cohesivm.progressbar import ProgressBar
    from cohesivm.devices.agilent import Agilent4156C
    from cohesivm.interfaces import MA8X8
    from cohesivm.measurements.iv import CurrentVoltageCharacteristic

Next, we create the :class:`~cohesivm.database.Database` and give it a meaningful name. At a later stage, we can use
the same file to store measurements of similar samples.

.. code-block:: python

    db = Database('Ga2O3-Cu2O-Heterojunction.h5')

We begin the configuration of the components with the :class:`~cohesivm.measurements.Measurement`, specifically the
:class:`~cohesivm.measurements.iv.CurrentVoltageCharacteristic` as mentioned above. The voltage sweep is setup to start
at -2.0 |_| V and end at 2.0 |_| V, with a step size of 0.01 |_| V. For now, the ``illuminated`` parameter is set to
``False`` and we keep the solar simulator off, to obtain the dark current-voltage characteristic (dark IV) curves.

.. code-block:: python

    measurement = CurrentVoltageCharacteristic(start_voltage=-2.0, end_voltage=2.0, voltage_step=0.02, illuminated=False)

After initializing the :class:`~cohesivm.measurements.Measurement`, we can check the requirements regarding the
:class:`~cohesivm.devices.Device` and the :class:`~cohesivm.interfaces.Interface`:

.. code-block:: python

    >>> measurement.required_channels
    [(cohesivm.channels.VoltageSMU, cohesivm.channels.SweepVoltageSMU)]
    >>> measurement.interface_type
    cohesivm.interfaces.HighLow

This means, that we need a :class:`~cohesivm.devices.Device` with a single :class:`~cohesivm.channels.Channel` which
is either a :class:`~cohesivm.channels.VoltageSMU` or a :class:`~cohesivm.channels.SweepVoltageSMU`.
The :class:`~cohesivm.interfaces.InterfaceType` of the :class:`~cohesivm.interfaces.Interface` must be
a :class:`~cohesivm.interfaces.HighLow`.

Consequently, we initialize the :class:`~cohesivm.devices.agilent.Agilent4156C.SweepVoltageSMUChannel` and inject it
into the initializer of the :class:`~cohesivm.devices.agilent.Agilent4156C.Agilent4156C`.
We also initialize the :class:`~cohesivm.interfaces.ma8x8.MA8X8` and provide it the
:class:`~cohesivm.database.Dimensions` of the sputtered gold areas. The connection parameters are filled utilizing
the :mod:`~cohesivm.config`, as described in the :doc:`../getting_started/configuration` section.

.. code-block:: python

    smu = Agilent4156C.SweepVoltageSMUChannel()
    device = Agilent4156C.Agilent4156C(channels=[smu], **config.get_section('Agilent4156C'))
    interface = MA8X8(pixel_dimensions=Dimensions.Circle(radius=0.425), **config.get_section('MA8X8'))

Lastly, we put all the components together in the :class:`~cohesivm.experiment.Experiment`, where we also set the name
of the sample and select to measure at all available contact positions:

.. code-block:: python

    experiment = Experiment(
        database=db,
        device=device,
        interface=interface,
        measurement=measurement,
        sample_id='Ga2O3-50c_Cu2O-300s',
        selected_contacts=None
    )

For keeping track of the progress, we create a :class:`~cohesivm.progressbar.Progressbar` and, finally, start
the :class:`~cohesivm.experiment.Experiment`:

.. code-block:: python

    pbar = ProgressBar(experiment)
    with pbar.show():
        experiment.quickstart()

The resulting terminal output should look like this:

.. code-block::

    Contacts:    25%|████████████████                                               | 16/64 [09:23<28:07,  34.97s/it]
    Datapoints:  67%|█████████████████████████████████████████                      | 134/201 [00:24<00:11, 5.74it/s]

For the light IV measurements, we turn on the solar simulator and change the respective setting in
the :class:`~cohesivm.measurements.iv.CurrentVoltageCharacteristic`, followed by running the complete script again.

.. code-block:: python

    measurement = CurrentVoltageCharacteristic(start_voltage=-2.0, end_voltage=2.0, voltage_step=0.01, illuminated=True)


Data Analysis
-------------

To work with the measurement results, we firstly load the :class:`~cohesivm.database.Database` from before and filter
for the specified ``sample_id``. We obtain a list of strings where each item corresponds to a stored
:class:`~cohesivm.database.Dataset`.

.. code-block:: python

    >>> from cohesivm.database import Database
    ... db = Database('Ga2O3-Cu2O-Heterojunction.h5')
    ... db.filter_by_sample_id('Ga2O3-50c_Cu2O-300s')
    ['/CurrentVoltageCharacteristic/3361670997efa438:26464063430fe52f:d11d583e386e4720:c8965a35118ce6fc:ab60964b1ca23b77:8131a44cea4d4bb8/2024-10-10T13:13:09.028445-Ga2O3-50c_Cu2O-300s',
     '/CurrentVoltageCharacteristic/3361670997efa438:26464063430fe52f:a69a946e7a02e547:c8965a35118ce6fc:ab60964b1ca23b77:8131a44cea4d4bb8/2024-10-10T13:59:17.276789-Ga2O3-50c_Cu2O-300s']

From the datetime at the very end of the strings, we can identify the (older) dark IVs and the (newer) light IVs. For
more complicated scenarios, where more results exist for a single ``sample_id``, it is advisable to filter them based
on the :attr:`~cohesivm.measurements.Measurement.settings`, using the
:meth:`~cohesivm.database.Database.filter_by_settings`, e.g.:

.. code-block:: python

    >>> db.filter_by_settings('CurrentVoltageCharacteristic', {'illuminated': True})
    ['/CurrentVoltageCharacteristic/3361670997efa438:26464063430fe52f:a69a946e7a02e547:c8965a35118ce6fc:ab60964b1ca23b77:8131a44cea4d4bb8/2024-10-10T13:59:17.276789-Ga2O3-50c_Cu2O-300s']

We load the :class:`~cohesivm.database.Dataset` of the light IV measurements and initialize a
:class:`~cohesivm.analysis.iv.CurrentVoltageCharacteristic`, which is an :class:`~cohesivm.analysis.Analysis`
specifically for our application:

.. code-block:: python

    from cohesivm.analysis.iv import CurrentVoltageCharacteristic
    dataset = db.filter_by_sample_id('Ga2O3-50c_Cu2O-300s')[1]
    light_iv_dataset = db.load_dataset(dataset)
    analysis = CurrentVoltageCharacteristic(light_iv_dataset)

Then, for quickly checking the data, we plot a result map of the open circuit voltage (Voc), using the method referenced
in the :attr:`~cohesivm.analysis.Analysis.functions` of the :class:`~cohesivm.analysis.iv.CurrentVoltageCharacteristic`:

.. code-block:: python

    from cohesivm.analysis import plot_result_map
    result_map = analysis.generate_result_maps('Open Circuit Voltage (V)')[0]
    plot_result_map(result_map, 'Voc map of Ga2O3-Cu2O heterojunction')

.. image:: ../_static/img/tutorial_real-world_example_voc-map.png

.. note::

    The :class:`~cohesivm.analysis.Analysis` is much more powerful in the context of the graphical user interfaces.
    Have a look at the description of the :doc:`../guis/analysis` or walk through the :doc:`../tutorials/workflow`
    tutorial to learn more.

Since the data itself is represented as dictionary of contact IDs that index
`structured arrays <https://numpy.org/doc/stable/user/basics.rec.html>`_, we select a single measurement curve by its
contact ID and plot it using the field names:

.. code-block:: python

    import matplotlib.pyplot as plt
    contact_id = '45'
    measurement_curve = light_iv_dataset[0][contact_id]
    x_name, y_name = 'Voltage (V)', 'Current (A)'
    plt.scatter(measurement_curve[x_name], abs(measurement_curve[y_name]))
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.yscale('log')
    plt.title(f'Current-Voltage Characteristic of Contact {contact_id}')
    plt.show()

.. image:: ../_static/img/tutorial_real-world_example_iv45.png

Closing Remarks
---------------

If you want to integrate your laboratory equipment and measurement routines into COHESIVM, learn how to implement your
own components in the respective tutorials:

- :doc:`device`
- :doc:`interface`
- :doc:`measurement`
- :doc:`analysis`

.. include:: ../_snippets/important_contribute.rst

Also, have a look on the :doc:`workflow` to learn how to make use of the graphical user interfaces.

References
----------

.. [DWEW24] Dimopoulos, T., Wibowo, R. A., Edinger, S., Wolf, M., & Fix, T. (2024). Heterojunction Devices Fabricated from Sprayed n-Type Ga2O3, Combined with Sputtered p-Type NiO and Cu2O. Nanomaterials, 14(3), 300. https://doi.org/10.3390/nano14030300

.. |_| unicode:: 0xA0
   :trim:
