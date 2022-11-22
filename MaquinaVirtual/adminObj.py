import json

class adminObj:
    def __init__(self):

        with open('obj.json') as json_file:
            self.obj = json.load(json_file)

        if 'error' in self.obj.keys():
            raise Exception(self.obj['Error'])
        
        self.func_dir = self.obj['func_dir']
        self.cuads = self.obj['cuads']
        self.const_sum = self.obj['constants_summary']

    def varWorkspace(self, genScope, intScope):
        return self.func_dir[genScope][intScope]['workspace']['variables_workspace']
    
    def tempWorkspace(self, genScope, intScope):
        return self.func_dir[genScope][intScope]['workspace']['temps_workpace']
    
    def constSum(self):
        return self.const_sum
    
    def constTable(self):
        return self.constTable