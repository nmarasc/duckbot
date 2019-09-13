# Last Updated: 2.2
# dictionary that can index on a range
# credit goes to not me
class rangedict(dict):
    # Retrieve item from the dict
    # Params: item - value to get from the dict
    # Return: value mapped to item
    def __getitem__(self, item):
        if type(item) != range:
            for key in self:
                if item in key:
                    return self[key]
            raise KeyError
        else:
            return super().__getitem__(item)
