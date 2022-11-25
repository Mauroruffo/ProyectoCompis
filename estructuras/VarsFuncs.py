class Variable:
    def __init__(self, varName, varType):
        self.__varName = varName
        self.__varType = varType
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

    def __repr__(self):
        print(self.__varName + ' ' + self.__varType + ' ' + self.__varValue + ' ' + self.__varSize)

class Function:
    def __init__(self):
        self.table = {}

    def genScope(self, name):
        self.table[name] = {}

    def intScope(self, general_name, name):
        self.table[general_name][name] = {
            "vars_table": {},
            "param_signature": [],
            "workspace": {}
            }


    def paramType(self, general_name, internal_name, n):
        # Raise error if n is bigger than array size
        param_signature_arr = self.table[general_name][internal_name]['param_signature']
        if n >= len(param_signature_arr):
            error_msg = "Sending too many parameters for function '" + internal_name + \
                "' when " + str(len(param_signature_arr)) + " are expected."
            raise Exception(error_msg)
        else:
            return param_signature_arr[n]

    def paramLength(self, general_name, internal_name):
        return len(self.table[general_name][internal_name]['param_signature'])

    def init_funcCuad(self, general_name, internal_name):
        return self.table[general_name][internal_name]['start_quad']

    def funcType(self, general_name, internal_name):
        return self.table[general_name][internal_name]['function_type']

    def funcDir(self, general_name, internal_name, function_name):
        return self.table[general_name][internal_name]['vars_table'][function_name]['var_virtual_address']
    
    def varDir(self, general_name, internal_name, var_name):
        return self.table[general_name][internal_name]['vars_table'][var_name]['var_virtual_address']

    def varType(self, general_name, internal_name, var_name):
        return self.table[general_name][internal_name]['vars_table'][var_name]['var_data_type']

    def get_group_size(self, general_name, internal_name, var_name):
        return self.table[general_name][internal_name]['vars_table'][var_name]['group_size']

    def dimSize(self, general_name, internal_name, var_name, dim):
        return self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'][dim-1]['size']

    def get_group_dimensions(self, general_name, internal_name, var_name):
        if 'dim_list' in self.table[general_name][internal_name]['vars_table'][var_name].keys():
            return len(self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'])
        else:
            return 0

    def dimM(self, general_name, internal_name, var_name, dim):
        return self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'][dim-1]['m']
        
    def tempInfo(self, general_name, internal_name, temps_workspace):
        self.table[general_name][internal_name]['workspace']['temps_workspace'] = temps_workspace

    def tipoFunc(self, general_name, internal_name, type):
        self.table[general_name][internal_name]['function_type'] = type

    def initCuad(self, general_name, internal_name, quad_id):
        self.table[general_name][internal_name]['start_quad'] = quad_id

    def addVar(self, general_name, internal_name, var_name, var_type, var_data_type, var_virtual_address):
        if var_name in self.table[general_name][internal_name]['vars_table'].keys():
            raise Exception(
                "Variable named " + var_name + " has already been declared in the same scope.")
        else:
            print("La variable " + var_name + " ha sido agregada")
            self.table[general_name][internal_name]['vars_table'][var_name] = {
                'var_type': var_type,
                'var_data_type': var_data_type,
                'var_virtual_address': var_virtual_address,
                'var_name': var_name
            }

    def addParam(self, general_name, internal_name, parameter_type):
        self.table[general_name][internal_name]['param_signature'].append(parameter_type)

    def add_dim1_list(self, general_name, internal_name, var_name):
        self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'] = [{
            'dim': 1, 'size': None}]
        self.table[general_name][internal_name]['vars_table'][var_name]['r'] = 1

    def edit_dimSize(self, general_name, internal_name, var_name, index, size):
        r = self.table[general_name][internal_name]['vars_table'][var_name]['r']
        self.table[general_name][internal_name]['vars_table'][var_name]['dim_list'][index]['size'] = size
        self.table[general_name][internal_name]['vars_table'][var_name]['r'] = r * size

    def generalScopeExists(self, name):
        return (name in self.table.keys())

    def internalScopeExists(self, general_name, internal_name):
        return (internal_name in self.table[general_name].keys())

    def varExists(self, general_name, internal_name, var_name):
        return (var_name in self.table[general_name][internal_name]['vars_table'].keys())

    def genVarInfo(self, general_name, internal_name):
        variable_workspace = {"int": 0, "float": 0, "string": 0, "bool": 0}
        # ir por todo el var table y sumar cada tipo
        vars_table = self.table[general_name][internal_name]['vars_table']
        for var_name, var_dict in vars_table.items():
            if var_dict['var_type'] != 'list':
                variable_workspace[var_dict['var_data_type']] += 1
            else:
                variable_workspace[var_dict['var_data_type']
                                   ] += var_dict['group_size']
        self.table[general_name][internal_name]['workspace']['variables_workspace'] = variable_workspace

    def gen_dimM(self, general_name, internal_name, var_name):
        size = self.table[general_name][internal_name]['vars_table'][var_name]['r']

        for dim in self.table[general_name][internal_name]['vars_table'][var_name]['dim_list']:
            r = self.table[general_name][internal_name]['vars_table'][var_name]['r']
            dim_size = dim['size']
            dim['m'] = r / dim_size
            self.table[general_name][internal_name]['vars_table'][var_name]['r'] = dim['m']

        self.table[general_name][internal_name]['vars_table'][var_name]['group_size'] = size

    def delete_varTable(self, general_name, internal_name):
        self.table[general_name][internal_name]['vars_table'] = {}

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