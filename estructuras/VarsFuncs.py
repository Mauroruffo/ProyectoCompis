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

    def intScope(self, genScope, name):
        self.table[genScope][name] = {
            "vars_table" : {},
            "param_signature": [],
            "workspace": {}
            }
        
    def setVarsTable(self, genScope, intScope, varsTable):
        self.table[genScope][intScope][varsTable]

    def paramLength(self, genScope, intScope):
        # Regresa cantidad de parametros
        return len(self.table[genScope][intScope]['param_signature'])
    
    def varDir(self, genScope, intScope, var_name):
        # Regresa la direccion virtual de la variable
        return self.table[genScope][intScope]['vars_table'][var_name]['var_virtual_address']

    def varType(self, genScope, intScope, var_name):
        # Regresa el tipo de la variable 
        return self.table[genScope][intScope]['vars_table'][var_name]['var_data_type']

    def dimSize(self, genScope, intScope, var_name, dim):
        # Regresa el valor del tamano de la dimension
        return self.table[genScope][intScope]['vars_table'][var_name]['dim_list'][dim-1]['size']

    def groupSize(self, genScope, intScope, var_name):
        # Regresa el valor del conjunto de la dimension (ya sea una o dos dimensiones)
        return self.table[genScope][intScope]['vars_table'][var_name]['group_size']

    def get_group_dimensions(self, genScope, intScope, var_name):
        # Cantidad de dimensiones de una variable
        if 'dim_list' in self.table[genScope][intScope]['vars_table'][var_name].keys():
            return len(self.table[genScope][intScope]['vars_table'][var_name]['dim_list'])
        else:
            return 0

    def genDimMs(self, genScope, intScope, var_name):

        size = self.table[genScope][intScope]['vars_table'][var_name]['r']

        for dim in self.table[genScope][intScope]['vars_table'][var_name]['dim_list']:
            r = self.table[genScope][intScope]['vars_table'][var_name]['r']
            dim_size = dim['size']
            dim['m'] = r / dim_size
            self.table[genScope][intScope]['vars_table'][var_name]['r'] = dim['m']

        self.table[genScope][intScope]['vars_table'][var_name]['group_size'] = size

    def dimM(self, genScope, intScope, var_name, dim):
        # Funcion que regresa el valor M de una dimension
        # if 'm' not in self.table[genScope][intScope]['vars_table'][var_name]['dim_list']:
        #     self.table[genScope][intScope]['vars_table'][var_name]['dim_list'] = {}
        #     self.table[genScope][intScope]['vars_table'][var_name]['dim_list'][dim - 1]['m']
        return self.table[genScope][intScope]['vars_table'][var_name]['dim_list'][dim-1]['m']
        
    def tempInfo(self, genScope, intScope, temps_workspace):
        # Funcion para crear el workspace de temporales
        self.table[genScope][intScope]['workspace']['temps_workspace'] = temps_workspace

    def tipoFunc(self, genScope, intScope, type):
        # Funcion para agregar el tipo de dato que regresa una funcion
        self.table[genScope][intScope]['function_type'] = type

    def addVar(self, genScope, intScope, var_name, var_type, var_data_type, var_virtual_address):
        # Funcion para agregar la informacion sobre una variable
        if var_name in self.table[genScope][intScope]['vars_table'].keys():
            raise Exception(
                "Flop por creacion de la variable " + var_name + ", esta ya fue declarada!")
        else:
            self.table[genScope][intScope]['vars_table'][var_name] = {
                'var_type': var_type,
                'var_data_type': var_data_type,
                'var_virtual_address': var_virtual_address
            }

    def add_dim1_list(self, genScope, intScope, vars_table, var_name):
        # Funcion para establecer la primera dimension
        self.table[genScope][intScope]['vars_table'][var_name]['dim_list'] = [{'dim': 1, 'size': None}]
        self.table[genScope][intScope]['vars_table'][var_name]['r'] = 1
        vars

    def generalScopeExists(self, name):
        return (name in self.table.keys())

    def internalScopeExists(self, genScope, intScope):
        return (intScope in self.table[genScope].keys())

    def genVarInfo(self, genScope, intScope, vars_table):
        # Funcion para agregar un workspace para variables
        variable_workspace = {"int": 0, "float": 0, "string": 0, "bool": 0}
        for var_name, var_dict in vars_table.items():
            if var_dict['var_type'] != 'list':
                variable_workspace[var_dict['var_data_type']] += 1
            else:
                variable_workspace[var_dict['var_data_type']] += var_dict['group_size']
        self.table[genScope][intScope]['workspace']['variables_workspace'] = variable_workspace
    
    def editSizeAndR(self, genScope, intScope, var_name, index, size):
        r = self.table[genScope][intScope]['vars_table'][var_name]['r']
        self.table[genScope][intScope]['vars_table'][var_name]['dim_list'][index]['size'] = size
        self.table[genScope][intScope]['vars_table'][var_name]['r'] = r * size

    def varExistsInScope(self, genScope, intScope, var_name):
        return (var_name in self.table[genScope][intScope]['vars_table'].keys())
    
    def agregarFirma(self, genScope, intScope, parameter_type):
        # Funcion que te permite modificar los parametros de la funcion
        self.table[genScope][intScope]['param_signature'].append(parameter_type)
        
    def cuadInicial(self, genScope, intScope, quad_id):
        # Funcion que sirve para determinar el indice del cuadruplo
        self.table[genScope][intScope]['start_quad'] = quad_id

    def funcDir(self, genScope, intScope, function_name):
        return self.table[genScope][intScope]['vars_table'][function_name]['var_virtual_address']

    def setFuncType(self, genScope, intScope, type):
        self.table[genScope][intScope]['function_type'] = type

    def lenFirmaParam(self, genScope, intScope):
        # Funcion para regresar la firma de los parametros
        return len(self.table[genScope][intScope]['param_signature'])
    
    def getCuadFuncInicial(self, genScope, intScope):
        # Funcion para obtener el indice del primer cuadruplo
        return self.table[genScope][intScope]['start_quad']

    def getTipoFunc(self, genScope, intScope):
        return self.table[genScope][intScope]['function_type']

    def numTipoFirma(self, genScope, intScope, n):
        # Verifica que la n no sea mas grande la cantidad de parametros esperados
        param_signature_arr = self.table[genScope][intScope]['param_signature']
        if n >= len(param_signature_arr):
            raise Exception("Flop por cantidad de parametros en'" + intScope + "' se esperaban " + str(len(param_signature_arr)))
        else:
            return param_signature_arr[n]

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