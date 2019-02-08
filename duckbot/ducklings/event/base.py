# Duckbot util modules
import util.moduleLoader as modloader

# Event management class
# Receives and handles Slack events for Duckbot. Events are classified into
# different event types and dispatched to specific event handlers
class EventManager:

    # Constructor for event manager
    # Params: None
    # Return: EventManager instance
    def __init__(self):
        self.commands = self._initCommands()

    # Loads and initializes bot commands
    # Params: None
    # Return: Dictionary of module names mapped to their modules
    def _initCommands(self):
        # Load in command modules
        mods = modloader.loadBotCommands()
        # Give HELP command access to modules for help messages
        mods['HELP'].COMMANDS = mods
