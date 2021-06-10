# -*- coding: utf-8 -*-

__all__ = ['Bidict', 'Rangedict']


class Bidict(dict):
    r"""Bidirectional dictionary."""

    def __init__(self, *args, **kwargs):
        r"""Bidict contructor."""
        super(Bidict, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
            self.inverse.setdefault(value, []).append(key)

    def __setitem__(self, key, value):
        r"""Set value in both directions."""
        if key in self:
            self.inverse[self[key]].remove(key)
        super(Bidict, self).__setitem__(key, value)
        self.inverse.setdefault(value, []).append(key)

    def __delitem__(self, key):
        r"""Remove item from dictionary in both directions."""
        self.inverse.setdefault(self[key], []).remove(key)
        if self[key] in self.inverse and not self.inverse[self[key]]:
            del self.inverse[self[key]]
        super(Bidict, self).__delitem__(key)


class Rangedict(dict):
    r"""Dictionary indexed by a range."""

    def __getitem__(self, item):
        if type(item) != range:
            for key in self:
                if item in key:
                    return self[key]
            raise KeyError
        else:
            return super().__getitem__(item)
