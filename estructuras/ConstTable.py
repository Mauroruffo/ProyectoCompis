class Constants:

    def __init__(self):
        self.table = {'int': {}, 'float': {}, 'bool': {}, 'string': {}}

    def add_constant(self, type, virtual_address, constant):
        self.table[type][constant] = virtual_address

    def has_constant(self, type, constant):
        return constant in self.table[type].keys()

    def get_constant_address(self, type, constant):
        return self.table[type][constant]
    
class Variables:

    def __init__(self):
        self.table = {}