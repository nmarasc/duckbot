# Duckbot util modules
from duckbot.util.event import Event

# Event management class
# Receives and handles events for Duckbot. Events are classified into
# different types and dispatched to specific handlers
class EventManager:

    ERROR = {
        'NO_PROCESS_FN' :
            'no process function defined for event type: {}'
    }

    # Constructor for event manager
    # Params: None
    # Return: EventManager instance
    def __init__(self):
        # Load event handlers
        self.event_handlers = modloader.loadFrom('ducklings.event')
        # Give command references to message handler
        self.event_handlers['message'].COMMANDS = command_modules

    # Standardizes events and gives them to the proper event handler
    # Params: event - non standardized event
    # Return: String response from event handlers
    def dispatch(self, event):

