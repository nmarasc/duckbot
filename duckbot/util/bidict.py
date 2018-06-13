# Bidirectional dictionary class
# Credit belongs to a dude on stackoverflow
class bidict(dict):
    # Constructor for bidict
    # Params: same as regular dict
    # Return: bidict instance
    def __init__(self, *args, **kwargs):
    #{{{
        super(bidict, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
            self.inverse.setdefault(value,[]).append(key)
    #}}}

    # Set value in both directions
    # Params: key   - index to map value to
    #         value - value to map key to
    # Return: None
    def __setitem__(self, key, value):
    #{{{
        if key in self:
            self.inverse[self[key]].remove(key)
        super(bidict, self).__setitem__(key, value)
        self.inverse.setdefault(value,[]).append(key)
    #}}}

    # Remove key from dict
    # Params: key - key to remove
    # Return: None
    def __delitem__(self, key):
    #{{{
        self.inverse.setdefault(self[key],[]).remove(key)
        if self[key] in self.inverse and not self.inverse[self[key]]:
            del self.inverse[self[key]]
        super(bidict, self).__delitem__(key)
    #}}}
