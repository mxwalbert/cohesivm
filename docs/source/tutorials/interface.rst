Implement an Interface
======================

This tutorial will guide you through the process of implementing a new contact interface following
the :class:`~cohesivm.interfaces.Interface` abstract base class. To simulate a realistic use case, the tutorials are
based on the measurement of the sheet resistance and resistivity of materials using a four-point probe.


Interface Class
---------------

Since we need to tell the :class:`~cohesivm.experiment.Experiment`, that the :class:`~cohesivm.interfaces.Interface`
and the :class:`~cohesivm.measurements.Measurement` are going to be compatible, we first have to implement
an :class:`~cohesivm.interfaces.InterfaceType` subclass. After that, we define the mandatory private class attributes
and abstract methods of the :class:`~cohesivm.interfaces.Interface` itself:

.. literalinclude:: /tutorials/workflow/fpp_components.py
    :language: python
    :lines: 11,12,15-17,117-144

As stated in the docstring, the mimetic ``FPP2X2`` interface consists of a total of four measurement points which are
labelled in the ``_contact_ids`` class attribute. The positions of these points and the overall dimensions of the
interface are defined afterwards. In the constructor, the :attr:`~cohesivm.interfaces.Interface.pixel_dimensions` are
specified, which we defined using the :class:`~cohesivm.database.Dimensions.Generic` shape to implicate the coordinates
of the individual contacts on each four-point probe. As a convention, we consider the first and the last coordinate to
correspond to the current source and the middle ones to correspond to the voltmeter. Further, the interface hardware is
initialized where we use as stand-in a simple API that is implemented in the mimetic
:doc:`/tutorials/workflow/fpp_connect` module.

Finally, the most important abstract :meth:`~cohesivm.interfaces.Interface._select_contact` must be implemented to
perform the actual switching between contacts on the interface hardware. We just call the respective method from our
mimetic API.


Example Usage
-------------

In order to test the implemented interface, we build part of the :doc:`/tutorials/workflow/fpp_connect` mimetic module:

.. literalinclude:: /tutorials/workflow/fpp_connect.py
    :language: python
    :lines: 4-16,58-67

Here, we change the resistance depending on the contact that we select and provide a public function to read the value
of the ``_resistance`` attribute.

Now we can test switching a contact:

.. code-block:: pycon

    >>> interface = FPP2X2('5')
    ... fpp_connect.get_resistance()
    100.
    >>> interface.select_contact('BR')
    ... fpp_connect.get_resistance()
    200.
