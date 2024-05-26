import os
import importlib


class CompatibilityError(Exception):
    """Raised if the components/parameters of a composite class are not compatible with each other."""
    pass


# Get a list of all the files and directories in the current directory
current_dir = os.path.dirname(__file__)
file_list = os.listdir(current_dir)

# Iterate through the files and directories
for item in file_list:
    # Skip special files and directories (e.g., __init__.py, __pycache__)
    if not item.startswith('__') and item.endswith('.py') and item != 'main.py':
        # Remove the '.py' extension to get the module/package name
        module_name = item[:-3]

        # Import the module/package dynamically
        module = importlib.import_module(f'{__name__}.{module_name}')
        globals()[module_name] = module
