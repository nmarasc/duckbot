# Event class
# This may affect response time negatively, see how it goes
class Event:

    # Constructor for Event
    # Params: event_p - incoming slack event to parse
    # Return: Event instance
    def __init__(self, event_p):
    #{{{

        if "type" in event_p:
            self.type = event_p["type"]
        else:
            self.type = None

        # Call the parser based on the event type
        if self.type in self.EVENT_PARSERS:
            self.EVENT_PARSERS[self.type](self, event_p)
    #}}}

    # Parser for message type events
    # Params: event_new - Event instance to add field data to
    #         event_old - slack event to extract data from
    # Return: None
    def parseMessageEvent(event_new, event_old):
    #{{{
#         print(event_old)
        # Ignore slackbot's messages
        if "user" in event_old and event_old["user"] == "USLACKBOT":
            event_new.type = None
            return

        event_new.channel = event_old["channel"]
        if "subtype" not in event_old:
            event_new.user = event_old["user"]
            event_new.text = event_old["text"]
            event_new.ts   = event_old["ts"]
        elif event_old["subtype"] == "message_changed":
            event_new.user = event_old["message"]["user"]
            event_new.text = event_old["message"]["text"]
            event_new.ts   = event_old["message"]["ts"]
        elif event_old["subtype"] == "channel_purpose":
            event_new.user = event_old["user"]
            event_new.text = event_old["purpose"]
            event_new.ts   = event_old["ts"]
            event_new.type = "update"
            event_new.subtype = "channel_purpose"
        elif event_old["subtype"] == "bot_message":
            event_new.type = "bot_message"
            event_new.text = event_old["text"]
            event_new.user = event_old["bot_id"]
            event_new.name = event_old["username"]
            event_new.ts   = event_old["ts"]
        # Ignore subtypes not handled
        else:
            event_new.type = None
    #}}}

    # Parser for reaction added events
    # Params: event_new - Event instance to add field data to
    #         event_old - slack event to extract data from
    # Return: None
    def parseReactionAddedEvent(event_new, event_old):
    #{{{
        event_new.user     = event_old["user"]
        event_new.reaction = {
             "emoji" : event_old["reaction"]
            ,"type"  : event_old["item"]["type"]
        }
        if event_new.reaction["type"] == "message":
            event_new.channel = event_old["item"]["channel"]
            event_new.ts      = event_old["item"]["ts"]

        elif (event_new.reaction["type"] == "file" or
              event_new.reaction["type"] == "file_comment"):
            event_new.file = event_old["item"]["file"]
    #}}}

    # Parser for team join events
    # Params: event_new - Event instance to add field data to
    #         event_old - slack event to extract data from
    # Return: None
    def parseTeamJoinEvent(event_new, event_old):
        event_new.user = event_old["user"]["id"]

    # Parser for channel joined events
    # Params: event_new - Event instance to add field data to
    #         event_old - slack event to extract data from
    # Return: None
    def parseChannelJoinedEvent(event_new, event_old):
    #{{{
        event_new.type    = "update"
        event_new.subtype = "channel_joined"
        event_new.channel = event_old["channel"]["id"]
        event_new.channel_data = event_old["channel"]
    #}}}

    #{{{ - EVENT_PARSERS
    EVENT_PARSERS = {
         "message"        : parseMessageEvent
        ,"reaction_added" : parseReactionAddedEvent
        ,"team_join"      : parseTeamJoinEvent
        ,"channel_joined" : parseChannelJoinedEvent
    }
    #}}}
