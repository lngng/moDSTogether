import os
import pathlib
import re
import sys

SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

D_COMMANDS = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Don't Starve Together\\data\\scripts\\debugcommands.lua"
D_KEYS = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Don't Starve Together\\data\\scripts\\debugkeys.lua"


def list_print(list, numbered=False):
    c = 0 
    for each in list:
        if numbered:
            print(c,each)
        else:
            print(each)
        c+=1


class Summary:
    def __init__(self, path):
        self.path = path
        with open(path, "r", encoding="utf-8") as file_object:
            self.data = file_object.readlines()

    @property
    def name(self):
        src_filename = os.path.basename(self.path)
        return src_filename[:src_filename.find('.')]

    @property
    def functions(self):
        functions = []
        function_lines = self._get_fn_lines()
        for each in function_lines:
            functions.append(Function(each))        
        return functions

    
    def _get_fn_lines(self):
        fn_lines = []
        for each in self.data:
            if each.startswith("function") or each.startswith("local function"):
                each.strip()
                fn_lines.append(each)
        return fn_lines


    def log_pretty(self):
        print("FUNCTIONS\n")
        for fn in self.functions:
            print(' name: ', fn.name)
            print(' params: ', fn.params)
            print(' scope: ', fn.scope)
            print('\n')
    

    def log_csv(self, destination_dir, toconsole=False):
        if destination_dir == ".":
            destination_dir = os.getcwd()
        destination = os.path.join(str(destination_dir), self.name + '.csv')
        with open(destination, "w", encoding='utf-8') as dest_file:
            dest_file.write("Name,Parameters,Scope\n")
            for fn in self.functions:
                if toconsole:
                    print(line)
                line = fn.name + "," + str(fn.params) + "," + fn.scope
                dest_file.write(line + '\n')


class Function:
    def __init__(self, line_str:str):
        self.str = line_str
        self.name = self._get_name()
        self.scope = self._get_scope()
        self.params = self._get_params()

    def __str__(self):
        return self.str

    def _get_name(self):
        name_start = self.str.find("function ") + len("function")
        name_end = self.str.find("(", name_start) 
        name = self.str[name_start:name_end]
        return name
        
    def _get_scope(self):
        if "local " in self.str:
            scope = "local"
        else:
            scope = "global"
        return scope

    def _get_params(self):
        params_start = self.str.find("(") + 1
        params_end = self.str.find(")", params_start) 
        params_str = self.str[params_start:params_end]
        params_str = params_str.strip()
        params_str = params_str.replace(" ", "")
        params_str = params_str.replace(", ", ",")
        params_str = params_str.replace(",", " | ")

        return params_str



if __name__ == "__main__":

    try:
        src = sys.argv[1]
        dest = sys.argv[2]
    except:
        src = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Don't Starve Together\\data\\scripts\\debugcommands.lua"
        dest = "."

    summary = Summary(src)
    summary.log_csv(dest)


