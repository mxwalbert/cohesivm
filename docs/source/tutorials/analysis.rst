Implement an Analysis
=====================

This tutorial will guide you through the process of implementing a class for automatized data analysis following
the :class:`~cohesivm.analysis.Analysis` abstract base class. To simulate a realistic use case, the tutorials are based
on the measurement of the sheet resistance and resistivity of materials using a four-point probe.


Theory
------

For the evaluation of the measurement data, we first need to introduce the equations that we will be using. Generally,
two things need to be considered: (i) the relation between the contact distance and film thickness and (ii) the
distance of the contacts from the edge of the sample. Since the ``film_thickness`` is only an optional argument in the
``FPPMeasurement`` (see :doc:`/tutorials/measurement`), we do not check for the relation of (i) but just implement
both cases (a) thin film and (b) bulk material. For (ii) we consider two additional cases where we introduce imaginary
current source contacts that are mirrored along the sample edge (which is obtained from the
:attr:`~cohesivm.interfaces.Interface.interface_dimensions`).

Firstly, we introduce :math:`l_{mn}` and :math:`s_{mn}` which are distance related factors for the cases (a) and (b),
respectively.

.. math:: l_{mn} = \ln{ \Bigl( (x_m - x_n)^2 + (y_m - y_n)^2 \Bigr) }

.. math:: s_{mn} = \sqrt{ (x_m - x_n)^2 + (y_m - y_n)^2}

These factors are then used in the distance terms for the regular case :math:`L_0`, :math:`S_0` and the edge case
:math:`L_m`, :math:`S_m`. The contacts of the current source will be denoted by the indices :math:`0` and :math:`3`,
corresponding to the list indices as defined in the ``FPP2X2`` (see :doc:`/tutorials/interface`). Accordingly, the
voltmeter contacts are denoted :math:`1` and :math:`2`, whereas the mirrored current source contacts are :math:`0_m`
and :math:`3_m`.

.. math:: L_0 = l_{10} + l_{23} - l_{13} - l_{20}

.. math:: S_0 = - \frac{1}{s_{10}} - \frac{1}{s_{23}} + \frac{1}{s_{13}} + \frac{1}{s_{20}}

.. math:: L_m = L + l_{10_m} + l_{23_m} - l_{13_m} - l_{20_m}

.. math:: S_m = S - \frac{1}{s_{10_m}} - \frac{1}{s_{23_m}} + \frac{1}{s_{13_m}} + \frac{1}{s_{20_m}}

This leads to the equations for the resistivity :math:`\rho` and, if the thickness :math:`t` of the film is unknown,
the sheet resistance :math:`R_{\square}`. The measured voltage is denoted by :math:`V_{12}` while :math:`I_{03}`
denotes the measured current.

.. math:: R_{\square} = 4 \pi \frac{V_{12}}{I_{03}} \frac{1}{L}

.. math:: \rho_{film} = t R_{\square}

.. math:: \rho_{bulk} = 2 \pi \frac{V_{12}}{I_{03}} \frac{1}{S}


Analysis Class
--------------

The main requirement to follow the :class:`~cohesivm.analysis.Analysis` abstract base class are the definition of the
:attr:`~cohesivm.analysis.Analysis.functions` and the :attr:`~cohesivm.analysis.Analysis.plots`. These dictionaries
tell the parent class and, consequently, the tightly bound :class:`~cohesivm.gui.AnalysisGUI` which methods should be
called for the analysis. For convenience, the :meth:`~cohesivm.analysis.result_buffer` can be used to decorate all
methods which follow the :attr:`~cohesivm.analysis.Analysis.functions` signature (``Callable[[str], DatabaseValue]]``)
to store already calculated results.

.. literalinclude:: /tutorials/workflow/fpp_analysis.py
    :language: python

This is quite a lot, but let's go through it part by part:

* :meth:`__init__`
    The constructor of the class takes as required argument the ``dataset`` which contains the measurement data
    together with the corresponding :class:`~cohesivm.database.Metadata` object as retrieved by
    :meth:`~cohesivm.database.Database.load_dataset`. Optionally, if no metadata is provided, the other arguments must
    be filled as stated in the docstring. Then, the method defines the available ``functions`` and ``plots`` which are
    passed to the parent :class:`~cohesivm.analysis.Analysis`. Finally, measurement and interface properties are stored
    for later use.

* :meth:`temperature`, :meth:`film_thickness`
    These methods are actually just instance properties but they are defined with an optional argument such that they
    can be used in the :attr:`~cohesivm.analysis.Analysis.functions` dictionary (which asks for a specific signature).

* :meth:`probe_coordinates`, :meth:`line_distance`, :meth:`edge_distances`, :meth:`mirrored_coordinates`
    Since the equations above depend on the location of the probe contacts relative to the sample, these methods
    retrieve and calculate the absolute coordinates of the actual and imaginary/mirrored contacts. The edge with the
    lowest average distance with respect to the two current source contacts (labels :math:`0` and :math:`3`) will be
    selected.

* :meth:`l_mn`, :meth:`s_mn`
    The distance related factors :math:`l_{mn}` and :math:`s_{mn}` are implemented as static methods which take as
    argument a list of coordinates and the indices for which the factor should be calculated.

* :meth:`l0`, :meth:`s0`, :meth:`lm`, :meth:`sm`
    These are the distance terms for the four cases which are introduced above: :math:`L_0`, :math:`S_0`, :math:`L_m`,
    and :math:`S_m`. They depend on the contact because this defines the absolute coordinates on the interface.

* :meth:`linear`
    This method is necessary because we measure multiple datapoints and need to extract the fraction
    :math:`{V_{12}}/{I_{03}}` which is the slope of the linear fit. It corresponds to the resistance after Ohm's Law.

* :meth:`sheet`, :meth:`rho_film`, :meth:`rho_bulk`
    These methods extract the resistance/resistivity for the regular case after the equations from above.

* :meth:`edge_dist_i0`, :meth:`edge_dist_i3`
    These values help to judge if a probe can be considered close to an edge and support the interpretation of the data.

* :meth:`edge_sheet`, :meth:`edge_rho_film`, :meth:`edge_rho_bulk`
    These methods extract the resistance/resistivity for the edge case after the equations from above.

* :meth:`measurement`, :meth:`resistance_plot`
    Finally, the methods for the :attr:`~cohesivm.analysis.Analysis.plots` are implemented which enable quick
    inspection of the data (especially in combination with the :class:`~cohesivm.gui.AnalysisGUI`.


Example Usage
-------------

Since we implemented the ``FPPAnalysis`` to not require a :class:`~cohesivm.database.Metadata` object, an instance can
be created straightaway. First, we generate some data:

.. code-block:: pycon

    >>> dtype = [('Current (A)', float), ('Voltage (V)', float)]
    ... d1 = np.array([(a, 100 * a) for a in range(1, 10)], dtype=dtype)
    ... d2 = d1.copy()
    ... d3 = np.array([(a, 50 * a + np.random.rand() * 10 - 5) for a in range(1, 10)], dtype=dtype)
    >>> dataset = {'P1': d1, 'P2': d2, 'P3': d3}

Then, we define the other arguments and initialize the class:

.. code-block:: pycon

    >>> if_dim = Dimensions.Rectangle(20., 20.)
    ... con_pos = {'P1': (5., 1.), 'P2': (10., 10.), 'P3': (15., 15.)}
    ... pix_dim = {k: Dimensions.Generic([-1.5, -0.5, 0.5, 1.5], [0., 0., 0., 0.]) for k in dataset.keys()}
    ... temp = 300.
    ... t = 1.
    >>> analysis = FPPAnalysis(dataset, if_dim, con_pos, pix_dim, temp, t)

Finally, we can do some analysis:

.. code-block:: pycon

    >>> analysis.temperature(), analysis.functions['Temperature (K)']()
    (300.0, 300.0)
    >>> analysis.linear('P1'), analysis.linear('P2'), analysis.linear('P3')
    (99.99999999999999, 99.99999999999999, 50.26502217652153)
    >>> analysis.sheet('P1'), analysis.sheet('P2'), analysis.sheet('P3')
    (453.2360141827193, 453.2360141827193, 227.81918304092616)

As you can see, the methods can either be called directly or by accessing them by their name from the
:attr:`~cohesivm.analysis.Analysis.functions`. The linear fit seems to be working since we obtain 100 Ω for ``P1``
and ``P2``, whereas ``P3`` is a little different than 50 Ω from the random noise that we added. Accordingly, the
sheet resistance is approximately half as big for ``P3`` than for the other two probes.

.. code-block:: pycon

    >>> analysis.edge_sheet('P1'), analysis.edge_sheet('P2'), analysis.edge_sheet('P3')
    (338.47934651602014, 450.8122096478881, 222.87207821984683)
    >>> analysis.probe_coordinates('P1'), analysis.mirrored_coordinates('P1')
    ([(3.5, 1.0), (4.5, 1.0), (5.5, 1.0), (6.5, 1.0)], [(3.5, -1.0), (6.5, -1.0)])

If we consider the distance between the probes and the edge of the sample, clearly, the resistance for ``P1`` is much
smaller but the values for the other two probes barely change. We then confirm that the coordinates of the current
sourcing contacts are correctly mirrored.

.. code-block:: pycon

    >>> result_map = analysis.generate_result_maps('Edge Sheet Resistance (Ohm)')[0]
    ... result_map
    array([[338.47934652,          nan,          nan],
           [         nan, 450.81220965,          nan],
           [         nan,          nan, 224.91600737]])

The :meth:`~cohesivm.analysis.Analysis.generate_result_maps` returns an array where the values are placed according to
their location on the sample/interface. The resulting array does not capture the exact distances because the contacts
are placed irregularly but it delivers qualitatively the correct positions. We can use the
:meth:`~cohesivm.analysis.plot_result_map` to plot it:

.. code-block:: python

    from cohesivm.analysis import plot_result_map
    plot_result_map(result_map, 'Edge Sheet Resistance (Ohm)')

.. image:: /_static/img/tutorial_analysis_map.png

To conclude, let's visualize the data using the methods defined in the :attr:`~cohesivm.analysis.Analysis.plots`:

.. code-block:: pycon

    >>> analysis.measurement('P1')
    ... plt.show()

.. image:: /_static/img/tutorial_analysis_measurement.png

.. code-block:: pycon

    >>> analysis.resistance_plot('P3')
    ... plt.show()

.. image:: /_static/img/tutorial_analysis_resistance.png
