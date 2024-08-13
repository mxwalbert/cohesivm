# Installation

## Using pip
To install the core COHESIVM package from the Python Package Index (PyPI), simply run:

```console
pip install cohesivm
```

This command will download and install the latest stable version of COHESIVM and its core dependencies.

````{important}

If you want to use the GUIs inside your [Jupyter](https://jupyter.org/) environment, make sure to specify the 
``gui`` extra:

```console
pip install cohesivm[gui]
```
````

Further extras exist for the implemented devices and for developers (refer to the ``pyproject.toml`` to get a listing 
of all available optional dependencies).

## Cloning from GitHub
If you want to install the development version of the package from the GitHub repository, follow these steps:
1. **Clone** the repository to your local machine:
    ```console
    git clone https://github.com/mxwalbert/cohesivm.git
    ```
2. **Navigate** into the cloned directory:
    ```console
    cd cohesivm
    ```
3. **Install** the package and its dependencies:
    ```console
    pip install .
    ```
