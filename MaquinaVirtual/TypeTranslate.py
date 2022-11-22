class Translator:
    def __init__(self):
        ...

    def cast(self, value, type):
        if type == 'int':
            return int(value)
        if type == 'float':
            return float(value)
        if type == 'bool':
            return bool(value)
        if type == 'string':
            return str(value)