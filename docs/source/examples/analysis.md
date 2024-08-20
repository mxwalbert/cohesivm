# Analyse the Results

The {class}`~cohesivm.analysis.Analysis` is tightly bound with the {class}`~cohesivm.measurements.Measurement` because
this will determine how the data is shaped and which features you want to extract from it. Therefore, the base class
should be extended as explained in this tutorial:

- {doc}`Implement an Analysis</tutorials/analysis>`

However, in the following example, the base class will be used to show the basic functionality.

Since the {class}`~cohesivm.interfaces.MA8X8` interface was used in the previous examples, the dataset should be filled
with ``data`` accordingly. If you already have an HDF5 file from following the basic usage example ("Test.h5"), then
this script should do the job:

```python
import numpy as np
from cohesivm.database import Database

# load existing data and corresponding metadata
db = Database('Test.h5')
dataset = db.filter_by_sample_id('test_sample_42')[0]
metadata = db.load_metadata(dataset)

# create a new data to not interfere with previous examples
dataset = db.initialize_dataset(metadata)

# iterate over contact_ids and save data arrays
for contact_id in metadata.contact_ids:
    db.save_data(np.array(range(10), dtype=[('Voltage (V)', float)]), dataset, contact_id)

# load the data
data, metadata = db.load_dataset(dataset)
```

This time, the {meth}`~cohesivm.database.Database.save_data` method was used correctly (contrary to the previous
examples) because the provided ``data`` should always be
a [structured array](https://numpy.org/doc/stable/user/basics.rec.html).

Next, {attr}`~cohesivm.analysis.Analysis.functions` and {attr}`~cohesivm.analysis.Analysis.plots` must be defined:

```pycon
>>> def maximum(contact_id: str) -> float:
...     return max(data[contact_id]['Voltage (V)'])
>>> functions = {'Maximum': maximum}
>>> plots = {}  # will be spared for simplicity (refer to the tutorial instead)
```

This approach seems too complex for what the function does, but it makes sense if you consider that this should be
implemented in a separate {class}`~cohesivm.analysis.Analysis` class. There, the data is stored as a property and the
{attr}`~cohesivm.analysis.Analysis.functions` (i.e., methods) have direct access to it. Due to the use of structured
arrays (which facilitate to store the quantity and the unit alongside the data), the label also needs to be stated
explicitly. But, again, this will normally be available as a property.

In the following, the class is initialized with and without using the {class}`~cohesivm.database.Metadata` from the
dataset. The former approach has the advantage that all available fields could be accessed by the
{attr}`~cohesivm.analysis.Analysis.functions`, e.g., values that are stored in the
{attr}`~cohesivm.database.Metadata.measurement_settings`.

```pycon
>>> from cohesivm.analysis import Analysis
# without metadata, the contact_position_dict must be provided
>>> analysis = Analysis(functions, plots, data, metadata.contact_position_dict)
# with metadata, additional metadata fields can be used in the analysis
>>> analysis = Analysis(functions, plots, (data, metadata))
>>> analysis.metadata.measurement_settings['illuminated']
True
```

The main usage of the {class}`~cohesivm.analysis.Analysis`, besides providing the framework for
the {doc}`Analysis GUI</guis/analysis>`, is to quickly generate maps of analysis results:

```pycon
>>> analysis.generate_result_maps('Maximum')[0]
array([[9., 9., 9., 9., 9., 9., 9., 9.],
       [9., 9., 9., 9., 9., 9., 9., 9.],
       [9., 9., 9., 9., 9., 9., 9., 9.],
       [9., 9., 9., 9., 9., 9., 9., 9.],
       [9., 9., 9., 9., 9., 9., 9., 9.],
       [9., 9., 9., 9., 9., 9., 9., 9.],
       [9., 9., 9., 9., 9., 9., 9., 9.],
       [9., 9., 9., 9., 9., 9., 9., 9.]])
```

As expected, the maximum value of the generated data is placed in a 2D numpy array on locations corresponding to
the {attr}`~interfaces.Interface.contact_positions`.
