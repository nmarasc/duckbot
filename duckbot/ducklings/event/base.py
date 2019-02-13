# Duckbot util modules
import util.moduleLoader as modloader
import ducklings.event.message as message_handler
from util.event import Event

# Event management class
# Receives and handles Slack events for Duckbot. Events are classified into
# different event types and dispatched to specific event handlers
class EventManager:

    # Constructor for event manager
    # Params: None
    # Return: EventManager instance
    def __init__(self):
        # Initialize bot commands
        self.commands = self._initCommands()
        # Load event handlers
        self.event_handlers = modloader.loadFrom('ducklings.event')
        # Give command references to message handler
        self.event_handlers['message'].COMMANDS = self.commands

    # Loads and initializes bot commands
    # Params: None
    # Return: Dictionary of module names mapped to their modules
    def _initCommands(self):
        # Load in command modules
        mods = modloader.loadBotCommands()
        # Give HELP command access to modules for help messages
        mods['HELP'].COMMANDS = mods

    # Standardizes events and gives them to the proper event handler
    # Params: event - non standardized event
    # Return: String response from event handlers
    def dispatch(self, event):
        # Create standardized event
        event = Event(event)
        try: # Call event handler for event type
            response = self.event_handlers[event.type].act(event)
        except KeyError: # Unrecognized event type, ignore
            response = ""
        return response
