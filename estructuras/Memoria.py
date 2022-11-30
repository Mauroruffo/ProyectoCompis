class MemoriaVirtual:
    def __init__(self):

        # Establecer rangos de memoria para scope, temporales y constantes

        self.table = {
            'globals': {'int': [0, 0, 1999], 'float': [2000, 2000, 3999], 'bool': [4000, 4000, 5999], 'string': [6000, 6000, 7999]},
            'temps': {'int': [16000, 16000, 17999], 'float': [18000, 18000, 19999], 'bool': [20000, 20000, 21999], 'string': [22000, 22000, 23999]},
            'constants': {'int': [24000, 24000, 25999], 'float': [26000, 26000, 27999], 'bool': [28000, 28000, 29999], 'string': [30000, 30000, 31999]}
        }

    def nueva_dir(self, type, block):
        # Funcion para crear nueva direccion para cierto tipo de dato
        print("Esto es block")
        print(block)
        if self.table[block][type][0] > self.table[block][type][2]:
            raise Exception("Too many variables for type " + type)
        else:
            current_address = self.table[block][type][0]
            self.table[block][type][0] += 1
            return current_address


    def nuevo_temp(self, type):
        # Funcion para crear nueva direccion para temporales
        if self.table['temps'][type][0] == self.table['temps'][type][2]:
            raise Exception("Too many variables for type " + type)
        else:
            temp_tuple = (self.table['temps'][type][0], type)
            self.table['temps'][type][0] += 1
            return temp_tuple


    def nuevo_global(self, type):
        # Funcion para crear nueva direccion para temporales
        if self.table['globals'][type][0] == self.table['globals'][type][2]:
            raise Exception("Too many variables for type " + type)
        else:
            global_address = self.table['globals'][type][0]
            self.table['globals'][type][0] += 1
            return global_address

    def cont_info(self, block):
        # Generar informacion sobre las constantes
        type_counters = self.table[block]
        counter_summary = {data_type: dt_array[0] - dt_array[1]
                           for data_type, dt_array in type_counters.items()}
        return counter_summary

    def getListDir(self, type, block, size):
        if self.table[block][type][0] + size - 1 > self.table[block][type][2]:
            raise Exception("Flop por cantidad de variables tipo " + type)
        else:
            current_address = self.table[block][type][0]
            self.table[block][type][0] += size
            return current_address