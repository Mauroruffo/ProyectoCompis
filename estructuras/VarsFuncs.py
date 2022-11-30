class Variable:
    def __init__(self, varName, varType, varDir):
        self.__varName = varName
        self.__varType = varType
        self.__varDir = varDir
        self.__varValue = None
        self.__varSize = None

    def name(self):
        return self.__varName

    def type(self):
        return self.__varType

    def value(self):
        return self.__varValue

    def size(self):
        return self.__varSize
    
    def varDir(self):
        return self.__varDir

    def __repr__(self):
        print(self.__varName + ' ' + self.__varType + ' ' + self.__varValue + ' ' + self.__varSize)

class Function:
    def __init__(self):
        # Lista vacia en la que se guarda informacion en el siguiente orden
        # ScopeExterno -> ScopeInterno -> Tabla de variables 
        #                              ->  workspaces (cantidades por tipo de dato)
        self.table = {}

    def genScope(self, name):
        self.table[name] = {}

    def intScope(self, general_name, name):
        self.table[general_name][name] = {
            "vars_table" : {},
            "param_signature": [],
            "workspace": {}
            }
        
    def setVarsTable(self, general_name, internal_name, varsTable):
        self.table[general_name][internal_name][varsTable]

    def paramType(self, general_name, internal_name, n):
        # Regresa tipo de parametro
        param_signature_arr = self.table[general_name][internal_name]['param_signature']
        if n >= len(param_signature_arr):
            error_msg = "Flop de cantidad de parametros '" + internal_name + \
                "' se esperaban " + str(len(param_signature_arr))
            raise Exception(error_msg)
        else:
            return param_signature_arr[n]

    def paramLength(self, general_name, internal_name):
        # Regresa cantidad de parametros
        return len(self.table[general_name][internal_name]['param_signature'])
    
    def varDir(self, general_name, internal_name, var_name):
        # Regresa la direccion virtual de la variable
        return self.table[general_name][internal_name]['vars_table'][var_name]['var_virtual_address']

    def varType(self, general_name, internal_name, var_name):
        # Regresa el tipo de la variable 
        return self.table[general_name][internal_name]['vars_table'][var_name]['var_data_type']

    def dimSize(self, general_name, internal_name, var_name, dim):
        # Regresa el valor del tamano de la dimension
        return self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'][dim-1]['size']

    def groupSize(self, general_name, internal_name, var_name):
        # Regresa el valor del conjunto de la dimension (ya sea una o dos dimensiones)
        return self.table[general_name][internal_name]['vars_table'][var_name]['group_size']

    def get_group_dimensions(self, general_name, internal_name, var_name):
        # Cantidad de dimensiones de una variable
        if 'dim_list' in self.table[general_name][internal_name]['vars_table'][var_name].keys():
            return len(self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'])
        else:
            return 0

    def genDimMs(self, general_name, internal_name, var_name):

        size = self.table[general_name][internal_name]['vars_table'][var_name]['r']

        for dim in self.table[general_name][internal_name]['vars_table'][var_name]['dim_list']:
            r = self.table[general_name][internal_name]['vars_table'][var_name]['r']
            print("Esto es el dimSize")
            dim_size = dim['size']
            print(dim_size)
            dim['m'] = r / dim_size
            self.table[general_name][internal_name]['vars_table'][var_name]['r'] = dim['m']

        self.table[general_name][internal_name]['vars_table'][var_name]['group_size'] = size

    def dimM(self, general_name, internal_name, var_name, dim):
        # Funcion que regresa el valor M de una dimension
        # if 'm' not in self.table[general_name][internal_name]['vars_table'][var_name]['dim_list']:
        #     self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'] = {}
        #     self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'][dim - 1]['m']
        print("Esto contiene la lista")
        print(self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'][dim-1])
        return self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'][dim-1]['m']
        
    def tempInfo(self, general_name, internal_name, temps_workspace):
        # Funcion para crear el workspace de temporales
        self.table[general_name][internal_name]['workspace']['temps_workspace'] = temps_workspace

    def tipoFunc(self, general_name, internal_name, type):
        # Funcion para agregar el tipo de dato que regresa una funcion
        self.table[general_name][internal_name]['function_type'] = type

    def addVar(self, general_name, internal_name, var_name, var_type, var_data_type, var_virtual_address):
        # Funcion para agregar la informacion sobre una variable
        if var_name in self.table[general_name][internal_name]['vars_table'].keys():
            raise Exception(
                "Variable named " + var_name + " has already been declared in the same scope.")
        else:
            self.table[general_name][internal_name]['vars_table'][var_name] = {
                'var_type': var_type,
                'var_data_type': var_data_type,
                'var_virtual_address': var_virtual_address
            }

    def add_dim1_list(self, general_name, internal_name, vars_table, var_name):
        # Funcion para establecer la primera dimension
        self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'] = [{'dim': 1, 'size': None}]
        self.table[general_name][internal_name]['vars_table'][var_name]['r'] = 1
        vars

    def generalScopeExists(self, name):
        return (name in self.table.keys())

    def internalScopeExists(self, general_name, internal_name):
        return (internal_name in self.table[general_name].keys())

    def varExists(self, general_name, internal_name, var_name):
        return (var_name in self.table[general_name][internal_name]['vars_table'].keys())

    def genVarInfo(self, general_name, internal_name, vars_table):
        # Funcion para agregar un workspace para variables
        variable_workspace = {"int": 0, "float": 0, "string": 0, "bool": 0}
        for var_name, var_dict in vars_table.items():
            if var_dict['var_type'] != 'list':
                variable_workspace[var_dict['var_data_type']] += 1
            else:
                print("Group size")
                print(var_dict['group_size'])
                variable_workspace[var_dict['var_data_type']] += var_dict['group_size']
        self.table[general_name][internal_name]['workspace']['variables_workspace'] = variable_workspace
    
    def editSizeAndR(self, general_name, internal_name, var_name, index, size):
        r = self.table[general_name][internal_name]['vars_table'][var_name]['r']
        self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'][index]['size'] = size
        self.table[general_name][internal_name]['vars_table'][var_name]['r'] = r * size

class Function1:
    def __init__(self, funcName, funcType):
        self.__funcName = funcName
        self.__funcType = funcType

    def name(self):
        return self.__funcName
    
    def type(self):
        return self.__funcType


class Constant:
    def __init__(self):
        self.table = {'int': {}, 'float': {}, 'bool': {}, 'string': {}}


    def add_const(self, type, virtual_address, constant):
        self.table[type][constant] = virtual_address


    def const_exists(self, type, constant):
        return constant in self.table[type].keys()

    def const_address(self, type, constant):
        return self.table[type][constant]