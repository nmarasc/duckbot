# Python imports
import importlib
import os

SRC_ROOT = getcwd()
MOD_ROOT = path.join(SRC_ROOT, 'ducklings')
CMD_ROOT = paht.join(MOD_ROOT, 'command')

# Load the bot command modules
# Params: None
# Return: Dictionary containing command names mapped to modules
def loadBotCommands():
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

def loadFrom(path):
    full_path = os.path.join(os.getcwd(), path)
    print(path)
    print(os.listdir(path))
    modules = [f.replace('.py', '') for f in os.listdir(full_path) if
               os.path.isfile(os.path.join(full_path, f)) and
               f != '__init__.py']
    print(modules)
    loaded = {}
    for mod_name in modules:
        mod = importlib.import_module(f"{path.replace('/', '.')}.{mod_name}")
        loaded = {**{name:mod for name in mod.NAMES}, **loaded}
    return loaded

def getPackageNames(path):
    _, _, filenames = next(os.walk(path))
    modules = [fn.replace('.py', '') for fn in filenames]
    return modules.remove('__init__')
