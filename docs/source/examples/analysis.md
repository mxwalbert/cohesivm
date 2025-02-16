# Analyse the Results

The {class}`~cohesivm.analysis.Analysis` is tightly bound with the {class}`~cohesivm.measurements.Measurement` because
this will determine how the data is shaped and which features you want to extract from it. Therefore, the base class
should be extended as explained in this tutorial:

- {doc}`Implement an Analysis</tutorials/analysis>`

However, in the following example, the base class will be used to show the basic functionality.

## Generate Data

Since the {class}`~cohesivm.interfaces.MA8X8` interface was used in the previous examples, the initialized
{class}`~cohesivm.database.Dataset` should be filled with data accordingly. With the HDF5 file from 
the {doc}`Basic Usage</getting_started/basic_usage>` example, this script should do the job:

```python
import numpy as np
from cohesivm.database import Database

# load existing data and corresponding metadata
db = Database('Test.h5')
dataset = db.filter_by_sample_id('test_sample_42')[0]
metadata = db.load_metadata(dataset)

# create a new dataset to not interfere with previous examples
dataset = db.initialize_dataset(metadata)

# iterate over contact_ids and save data arrays
for contact_id in metadata.contact_ids:
    db.save_data(np.array(range(10), dtype=[('Voltage (V)', float)]), dataset, contact_id)

# load the data
data, metadata = db.load_dataset(dataset)
```

## Define Functions

Next, {attr}`~cohesivm.analysis.Analysis.functions` and {attr}`~cohesivm.analysis.Analysis.plots` must be defined:

```pycon
>>> def maximum(contact_id: str) -> float:
...     return max(data[contact_id]['Voltage (V)'])
>>> functions = {'Maximum': maximum}
>>> plots = {}  # will be spared for simplicity (refer to the tutorial instead)
```

This approach seems too complex for what the function does, but it makes sense if you consider that this should be
implemented in a separate {class}`~cohesivm.analysis.Analysis` class. There, the data is stored as a property and the
{attr}`~cohesivm.analysis.Analysis.functions` (i.e., methods) have direct access to it. Due to the use of 
[structured arrays](https://numpy.org/doc/stable/user/basics.rec.html), the label also needs to be stated explicitly. But, again, this will normally be available as 
a property of the class.

## With vs. without Metadata

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

## Use the Class

The main purposes of the {class}`~cohesivm.analysis.Analysis` are bundling functions for quick data analysis 
and providing the framework for the {doc}`Analysis GUI</guis/analysis>`. But it is also useful to generate maps 
of analysis results:

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
