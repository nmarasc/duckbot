# Python imports
import importlib
import os

SRC_ROOT = os.getcwd()
MOD_ROOT = os.path.join(SRC_ROOT, 'ducklings')
UTL_ROOT = os.path.join(SRC_ROOT, 'util')
CMD_ROOT = os.path.join(MOD_ROOT, 'command')
EVT_ROOT = os.path.join(MOD_ROOT, 'event')

# Load the bot command modules
# Params: None
# Return: Dictionary containing command names mapped to modules
def loadBotCommands():
    path = '{}.{}'.format(
        os.path.basename(MOD_ROOT),
        os.path.basename(CMD_ROOT)
    )
    return loadFrom(path)

# Load bot subcommand modules from given package
# Params: package - name of subcommand package
# Return: Dictionary with modules mapped to their names or
#         None if the package does not exist
def loadSubCommands(package):
    path = f'{{}}.{{}}.sub_{package}'.format(
        os.path.basename(MOD_ROOT),
        os.path.basename(CMD_ROOT)
    )
    return loadFrom(path)

# Load modules from a specific package
# Params: package - dot qualified package path, e.g. ducklings.command
# Return: Dictionary with module defined names mapped to modules
def loadFrom(package):
    # Build os path from package path
    pkg_path = os.path.join(*package.split('.'))
    pkg_path = os.path.join(SRC_ROOT, pkg_path)
    if os.path.isdir(pkg_path):  # Confirm package exists
        # Get contained module names
        module_names = _getModuleNames(pkg_path)
        # Attach modules to anchor
        paths = [f'{package}.{name}' for name in module_names]
        # Load the modules
        modules = _loadModules(paths)
    else:  # Package did not exist
        modules = None
    return modules

# Find module names from given path
# Params: path - absolute package path to check for modules
# Return: list of contained module names
# Note  : Assumes that the package exists and is not empty
def _getModuleNames(path):
    # Get file names contained in the path
    _, _, filenames = next(os.walk(path))
    # Remove file extensions
    modules = [fn.replace('.py', '') for fn in filenames]
    # Remove init since it isn't a real module and never will be
    # This line can go when it finally proves itself
    modules.remove('__init__')
    return modules

# Import modules and map them to their names in a dictionary
# Params: mod_paths - list of dot qualified module paths to be imported
# Return: Dictionary with module names mapped to the module
def _loadModules(mod_paths):
    loaded = {}
    for path in mod_paths:
        # Import the module
        module = importlib.import_module(path)
        try:  # See if the module defined its own names
            loaded = {**{name:module for name in module.NAMES}, **loaded}
        except AttributeError:  # Otherwise use the path basename
            loaded[path.split('.')[-1]] = module
    return loaded
