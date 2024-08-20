# Manage the Data

After you collected some data and stored it in an HDF5 file, you can use the {class}`~cohesivm.database.Database` class
to work with it. First, initialise the {class}`~cohesivm.database.Database` object and list the samples which are stored
there:

```pycon
>>> from cohesivm.database import Database
>>> db = Database('Test.h5')
>>> db.get_sample_ids()
['test_sample_42']
```

This is exactly the {attr}`~cohesivm.experiment.Experiment.sample_id` which was specified when the
{class}`~cohesivm.experiment.Experiment` was configured, and it can be used to retrieve the actual
{attr}`~cohesivm.experiment.Experiment.dataset` path in the {class}`~cohesivm.database.Database` object:

```pycon
>>> db.filter_by_sample_id('test_sample_42')
['/CurrentVoltageCharacteristic/55d96687ee75aa11:26464063430fe52f:a69a946e7a02e547:c8965a35118ce6fc:67a8bfb44702cfc7:8131a44cea4d4bb8/2024-07-01T10:44:59.033161-test_sample_42']
```

The resulting list contains the path strings for all experiments with the specified
{attr}`~cohesivm.experiment.Experiment.sample_id` (currently only one entry). These strings get quite long because they
contain the {attr}`~cohesivm.measurements.Measurement.name` of the {class}`~cohesivm.measurements.Measurement`
procedure, followed by a hashed representation of the {attr}`~cohesivm.measurements.Measurement.settings` dictionary,
and finally the datetime combined with the {attr}`~cohesivm.experiment.Experiment.sample_id`. With this
{attr}`~cohesivm.experiment.Experiment.dataset` path, you may retrieve some information from the
{class}`~cohesivm.database.Metadata` object which got created by the {class}`~cohesivm.experiment.Experiment`:

```pycon
>>> dataset = db.filter_by_sample_id('test_sample_42')[0]
>>> metadata = db.load_metadata(dataset)
>>> metadata.sample_id, metadata.device, metadata.interface, metadata.measurement
('test_sample_42', 'Agilent4156C', 'MA8X8', 'CurrentVoltageCharacteristic')
```

Storing a new dataset is less trivial because you need a fully qualified {class}`~cohesivm.database.Metadata` object,
which asks for a large number of arguments. Anyway, this is usually handled by the
{class}`~cohesivm.experiment.Experiment` class because it guarantees that the specified components are compatible. For
testing, the {class}`~cohesivm.database.Metadata` object from above may be used to initialize a new dataset:

```pycon
>>> db.initialize_dataset(metadata)
'/CurrentVoltageCharacteristic/55d96687ee75aa11:26464063430fe52f:a69a946e7a02e547:c8965a35118ce6fc:67a8bfb44702cfc7:8131a44cea4d4bb8/2024-07-01T10:46:05.910371-test_sample_42'
```

This yields practically the same ``dataset`` path as before, only the datetime is different. Adding data entries, on
the other hand, is fairly simple because you only need to specify the ``dataset`` and the ``contact_id`` (alongside
the ``data`` of course):

```pycon
>>> db.save_data(np.array([1]), dataset)
>>> db.save_data(np.array([42]), dataset, '1')
```

Finally, you may load a data entry by specifying the ``contact_id`` (or a list of several) or load an entire dataset,
including the {class}`~cohesivm.database.Metadata`:

```pycon
>>> db.load_data(dataset, '0')
[array([1])]
>>> db.load_data(dataset, ['0', '1'])
[array([1]), array([42])]
>>> db.load_dataset(dataset)
({'0': array([1]), '1': array([42])}, Metadata(CurrentVoltageCharacteristic, Agilent4156C, MA8X8))
```

The {class}`~cohesivm.database.Database` class also implements methods for filtering datasets based on
{attr}`~cohesivm.measurements.Measurement.settings` of the {class}`~cohesivm.measurements.Measurement`. Check out the 
documentation of the {meth}`~cohesivm.database.Database.filter_by_settings` and 
{meth}`~cohesivm.database.Database.filter_by_settings_batch` to learn more.
