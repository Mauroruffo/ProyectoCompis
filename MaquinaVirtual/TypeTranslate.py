class Translator:
    def __init__(self):
        ...

    def cast(self, value, type):
        # Funcion que sirve para castear los tipos de datos
        if type == 'int':
            return int(value)
        if type == 'float':
            return float(value)
        if type == 'bool':
            if isinstance(value, str):
                return value == 'true'
        if type == 'string':
            return str(value)