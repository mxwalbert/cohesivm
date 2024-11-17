Complete GUI Workflow
=====================

In this tutorial, we will use the components of the four point probe measurement which we implemented in the previous
tutorials and put it to the test by running a complete workflow in the graphical user interfaces.


Environment
-----------

.. include:: ../_snippets/important_gui_extra.rst

We will be working in Jupyter and need to put together the implemented components (:class:`~cohesivm.devices.Device`,
:class:`~cohesivm.interfaces.Interface`, and :class:`~cohesivm.measurements.Measurement`) in
:doc:`/tutorials/workflow/fpp_components`, the :class:`~cohesivm.analysis.Analysis` in
:doc:`/tutorials/workflow/fpp_analysis`, as well as the mimetic :doc:`/tutorials/workflow/fpp_connect` module.

Here is the recommended test folder structure:

.. code-block::

    src
     ├── fpp_analysis.py
     ├── fpp_components.py
     ├── fpp_connect.py
     └── workflow.ipynb

.. toctree::
    :hidden:

    /tutorials/workflow/fpp_analysis
    /tutorials/workflow/fpp_components
    /tutorials/workflow/fpp_connect


Run the Experiment
------------------

Following the procedure given in :doc:`/guis/experiment`, we initialize the experiment and a
:class:`~cohesivm.gui.DataStreamPlot` which are injected into the :class:`~cohesivm.gui.ExperimentGUI`.

.. code-block:: python

    from cohesivm.database import Database
    from cohesivm.experiment import Experiment
    from cohesivm.gui import XYDataStreamPlot ExperimentGUI
    from fpp_components import CurrentSourceChannel, VoltmeterChannel, FPPDevice, FPP2X2, FPPMeasurement

    db = Database('workflow.h5')

    current_source = CurrentSourceChannel(max_voltage=5.)
    voltmeter = VoltmeterChannel()
    device = FPPDevice('4')
    interface = FPP2X2('5')
    measurement = FPPMeasurement(
        currents=[1e-6, 1e-5, 1e-4, 5e-4, 1e-3, 3.3e-3, 6.7e-3, 1e-2],
        temperature=300,
        film_thickness=2e-4
    )

    experiment = Experiment(
        database=db,
        device=device,
        interface=interface,
        measurement=measurement,
        sample_id='fpp_test',
        selected_contacts=None
    )

    plot = XYDataStreamPlot('Current (A)', 'Voltage (V)')

    ExperimentGUI(experiment=experiment, plot=plot).display()

This will display the following Graphical User Interface which we can use to run and observe the experiment by clicking
`Setup` and `Start`.

.. image:: /_static/img/tutorial_workflow_experiment.png


Locate the Dataset
------------------

Now, an additional file has been created in the project folder:

.. code-block::
    :emphasize-lines: 5

    src
     ├── fpp_analysis.py
     ├── fpp_components.py
     ├── fpp_connect.py
     ├── workflow.h5
     └── workflow.ipynb

This HDF5 file stores the measurement data alongside the metadata which was automatically collected. We can display its
contents using the :class:`~cohesivm.guis.DatabaseGUI`.

.. code-block:: python

    from cohesivm.database import Database
    from cohesivm.gui import DatabaseGUI

    db = Database('workflow.h5')

    DatabaseGUI(db).display()

There, we locate the measurement in the `Sample` folder and copy the dataset path by clicking on the `Copy` button:

.. image:: /_static/img/tutorial_workflow_database.png


Check the Results
-----------------

After loading the dataset using the path sting from before, we initialize and display the
:class:`~cohesivm.gui.AnalysisGUI`, to get an overview of the data and analysis results.

.. code-block:: python

    from cohesivm.database import Database
    from cohesivm.gui import AnalysisGUI
    from fpp_analysis import FPPAnalysis

    db = Database('workflow.h5')

    dataset = db.load_dataset(
        # input your copied dataset path
    )

    analysis = FPPAnalysis(dataset)

    AnalysisGUI(analysis).display()

After clicking on one of the contacts in the left panel, the results from the :attr:`~cohesivm.analysis.Analysis.plots`
and :attr:`~cohesivm.analysis.Analysis.functions` will appear on the right and bottom, respectively.

.. image:: /_static/img/tutorial_workflow_analysis.png
