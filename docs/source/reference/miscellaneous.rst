Miscellaneous
=============

This is a collection of modules and members with a general scope.

cohesivm.config
---------------

.. automodule:: cohesivm.config
    :members:
    :undoc-members:
    :show-inheritance:

cohesivm.serial_communication
-----------------------------

.. automodule:: cohesivm.serial_communication
    :members:
    :undoc-members:
    :show-inheritance:

Exceptions
----------

.. autoexception:: cohesivm.CompatibilityError

.. autoexception:: cohesivm.experiment.StateError

Type Aliases
------------

.. class:: DatabaseValue

.. data:: cohesivm.database.DatabaseValue
    :type: Union[typing.Tuple[Union[int, float, bool]], int, float, bool, str]
    :noindex:

    A value with the appropriate type to be stored in the database.

.. class:: DatabaseDict

.. data:: cohesivm.database.DatabaseDict
    :type: typing.Dict[str, DatabaseValue]
    :noindex:

    A dictionary mapping strings to values which can be stored in the database.

.. class:: Dataset

.. data:: cohesivm.database.Dataset
    :type: typing.Tuple[typing.Dict[str, numpy.ndarray], ~cohesivm.database.Metadata]
    :noindex:

    A tuple of (i) data arrays which are mapped to contact IDs and (ii) the corresponding metadata of the dataset.

Generics
--------

.. class:: cohesivm.channels.TChannel

.. data:: cohesivm.channels.TChannel
    :noindex:

    A generic type which is bound to :class:`cohesivm.channels.Channel`.

.. class:: cohesivm.devices.ossila.OssilaX200.TChannel

.. data:: cohesivm.devices.ossila.OssilaX200.TChannel
    :noindex:

    A generic type which is bound to :class:`cohesivm.devices.ossila..OssilaX200.OssilaX200Channel`.

.. class:: cohesivm.devices.agilent.Agilent4156C.TChannel

.. data:: cohesivm.devices.agilent.Agilent4156C.TChannel
    :noindex:

    A generic type which is bound to :class:`cohesivm.devices.agilent.Agilent4156C.Agilent4156CChannel`.
