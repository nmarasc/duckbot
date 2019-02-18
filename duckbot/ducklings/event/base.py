# Duckbot util modules
import util.moduleLoader as modloader
from util.event import Event

# Event management class
# Receives and handles events for Duckbot. Events are classified into
# different types and dispatched to specific handlers
class EventManager:

    # Constructor for event manager
    # Params: None
    # Return: EventManager instance
    def __init__(self):
        # Load event handlers
        self.event_handlers = modloader.loadFrom('ducklings.event')
        # Initialize bot commands
        command_modules = self._initCommands()
        # Give command references to message handler
        self.event_handlers['message'].COMMANDS = command_modules

    # Standardizes events and gives them to the proper event handler
    # Params: event - non standardized event
    # Return: String response from event handlers
    def dispatch(self, event):
        response = {'return_code': 0}
        # Create standardized event
        event = Event(event)
        try: # Call event handler for event type
            response = self.event_handlers[event.type].process(event)
            #TODO: Check rc maybe
        except KeyError: # Unrecognized event type, ignore
            response['return_code'] = -1
            response['message'] = None
        except AttributeError: # No process function defined
            response['return_code'] = 1
        return response

    # Loads and initializes bot commands
    # Params: None
    # Return: Dictionary of module names mapped to their modules
    def _initCommands(self):
        # Load in command modules
        mods = modloader.loadBotCommands()
        # Give HELP command access to modules for help messages
        mods['HELP'].COMMANDS = mods
