class Translator:
    def __init__(self):
        ...

    def cast(self, value, type):
        if type == 'int':
            return int(value)
        if type == 'float':
            return float(value)
        if type == 'bool':
            if isinstance(value, str):
                return value == 'true'
        if type == 'string':
            return str(value)