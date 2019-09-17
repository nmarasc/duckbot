# Python imports
import importlib
import os

UTL_ROOT = os.path.dirname(os.path.realpath(__file__))
SRC_ROOT = os.path.dirname(UTL_ROOT)
MOD_ROOT = os.path.join(SRC_ROOT, 'ducklings')
CMD_ROOT = os.path.join(MOD_ROOT, 'command')
EVT_ROOT = os.path.join(MOD_ROOT, 'event')

# Load the bot command modules
# Params: None
# Return: Dictionary containing command names mapped to modules
def loadBotCommands():
    path = '{}.{}.{}'.format(
        os.path.basename(SRC_ROOT),
        os.path.basename(MOD_ROOT),
        os.path.basename(CMD_ROOT)
    )
    return loadFrom(path)

# Load bot subcommand modules from given package
# Params: package - name of subcommand package
# Return: Dictionary with modules mapped to their names or
#         None if the package does not exist
def loadSubCommands(package):
    path = f'{{}}.{{}}.{{}}.sub_{package}'.format(
        os.path.basename(SRC_ROOT),
        os.path.basename(MOD_ROOT),
        os.path.basename(CMD_ROOT)
    )
    return loadFrom(path)

# Load modules from a specific package
# Params: package - dot qualified path, e.g. duckbot.ducklings.command
# Return: Dictionary with module defined names mapped to modules
def loadFrom(package):
    # Build os path from package path
    pkg_path = os.path.join(*package.split('.'))
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
    # Remove file extensions and modules starting with '_'
    modules = [f[:f.index('.')] for f in filenames if not f.startswith('_')]
    return modules

# Import modules and map them to their names in a dictionary
# Params: mod_paths - list of dot qualified module paths to be imported
# Return: Dictionary with module names mapped to the module
def _loadModules(mod_paths):
    loaded = {}
    for path in mod_paths:
        # Import the module
        module = importlib.import_module(path)
        if not hasattr(module, 'DISABLED') or not module.DISABLED:
            try:  # See if the module defined its own names
                new = {name:module for name in module.NAMES}
                loaded = {**new, **loaded}
            except AttributeError:  # Otherwise use the path basename
                loaded[path.split('.')[-1]] = module
    return loaded
