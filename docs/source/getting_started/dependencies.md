# Dependencies

The current core version of COHESIVM is tested for Python 3.9–3.12 and requires the following dependencies:

- h5py (~=3.8)
- numpy (~=1.21)
- matplotlib (~=3.7)
- tqdm (~=4.65)

Apart from the core package, [extras](https://packaging.python.org/en/latest/tutorials/installing-packages/#installing-extras) 
exist for modules with additional dependencies (check the [``pyproject.toml``](https://github.com/mxwalbert/cohesivm/blob/main/pyproject.toml) for a complete listing):

| Extra   | Module                    | Dependency       |
|---------|---------------------------|------------------|
| gui     | cohesivm.gui              | bqplot~=0.12     |
| ma8x8   | cohesivm.interfaces.ma8x8 | pyserial~=3.5    |
| ossila  | cohesivm.devices.ossila   | xtralien~=2.10   |
| agilent | cohesivm.devices.agilent  | pyvisa~=1.13     |
| full    | –                         | *all from above* |
