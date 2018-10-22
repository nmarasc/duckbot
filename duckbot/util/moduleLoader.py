# Python imports
import os
import importlib

import sys

# Dynamic module and package loader
class ModuleLoader:

    # Module loader contructor
    # Allows for dynamic loading of packages and modules
    # Params: None
    # Return: ModuleLoader instance
    def __init__(self):
        self._setDefaultModulePaths()  # Initialize module paths

    # Load the bot command modules
    # Params: None
    # Return: Dictionary containing command names mapped to modules
    def loadBotCommands(self):
        # Get modules in command root and ignore __init__
        modules = [f.replace('.py', '') for f in os.listdir(self.cmd_root) if
                   os.path.isfile(os.path.join(self.cmd_root, f)) and
                   f != '__init__.py']
        # Build module anchor
        mod_anchor = (os.path.basename(self.mod_root) + "." +
                      os.path.basename(self.cmd_root))
        # Load command modules
        commands = {}
        for mod_name in modules:
            mod = importlib.import_module(mod_anchor + "." + mod_name)
            commands[mod.NAMES[0]] = mod
        return commands

    # Set default paths for bot modules
    # Params: None
    # Return: None
    def _setDefaultModulePaths(self):
        # Expectation: working directory was changed to the source root
        self.src_root = os.getcwd()
        # Default module package
        self.mod_root = os.path.join(self.src_root, "ducklings")
        # Default command package
        self.cmd_root = os.path.join(self.mod_root, "command")

if __name__ == '__main__':
    for p in sys.path:
        print(p)
    print("END")
    try:
        m = ModuleLoader()
    except ValueError as e:
        print('error: ' + str(e))
        sys.exit(-1)
    print(m)
    m.loadBotCommands()
