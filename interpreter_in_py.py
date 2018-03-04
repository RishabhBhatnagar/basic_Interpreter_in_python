import re
import ast
variables = {}
type = {}
def interpret(command):

    def expr(code, context = None):
        if not context:
            context = {}
        code = code.format(**context)
        code = re.sub('%', "", code)
        expr = ast.parse(code, mode = 'eval')
        code_object = compile(expr, '<string>', 'eval')
        return eval(code_object)

    def check_int_string_float_variable(string):
        if string[0] in {'"', "'"}:
            return "string"
        try:
            int_num = int(string)
            return "int"
        except:
            try:
                float_num = float(string)
                return "float"
            except:
                return 'variable'

    def add(chunks):
        sum = 0
        add_num = []
        breaks = False
        for i in chunks[1:]:
            add_num = add_num + i.split(',')
        for i in add_num:
            if i:
                try :
                    num = int(i)
                    sum = sum + int(i)
                except:
                    if i in variables:
                        sum = sum + variables[i]
                    else:
                        breaks = True
        if not breaks : return sum
        else:print("Undefined variables accessed")

    def show(chunks):

        #Printing a string.
        if chunks[1][0] in ['"', "'"]:
            if chunks[-1][-1] != chunks[1][0]:
                print("String quotes should be same.")
            else:
                chunks[1] = chunks[1][1:]
                chunks[-1] = chunks[-1][:-1]
                print(" ".join(chunks[1:]))
        #Printing a variable value.
        else:
            try:
                #checking if int is called to show.
                int_num = int(" ".join(chunks[1:]))
                print(int_num)
            except:
                #number maybe either var or float
                try:
                    #checking if float
                    float_num = float(" ".join(chunks[1:]))
                    print(float_num)
                except:
                    #pakka variable h.
                    try:
                        print(variables[" ".join(chunks[1:])])
                    except:
                        if " ".join(chunks[1:]) == 'variables':
                            print(variables)
                        else : print("variable", " ".join(chunks[1:]), "not found")


    def assignment(lhs, rhs):
        #checking if the lhs is not a basic primitives.
        data_type_lhs = check_int_string_float_variable(lhs)
        if data_type_lhs == 'variable':
            #Is rhs a variable??
            try:
                data_type_rhs = check_int_string_float_variable(rhs)
                if data_type_rhs == 'variable':
                    variables[lhs.strip()] = variables[rhs.strip()]
                else:
                    variables[lhs.strip()] = int(rhs.strip())
            except : print("Cannot assign", data_type, "any value")

            
    def delete_variable(variable_list):
        vars = []
        can_delete_all = True
        for i in variable_list:
            vars = vars + i.split(',')

        try : vars.remove('')
        except:pass
        try: vars.remove(' ')
        except:pass
        
        for var in vars:
            if check_int_string_float_variable(var) != 'variable':
                can_delete_all = False
        if can_delete_all:
            for var in vars:
                try:
                    del(variables[var])
                except:
                    print(var, "not declared")
        else:
            print("Cannot delete a non variable")
    chunks = command.split()

    #switch cases for commands
    if chunks[0] == 'show':
        show(chunks)
    elif chunks[0] == 'add':
        sumV = add(chunks)
        if sumV : print(sumV)
    elif "=" in command:
        lhs, rhs = command.split("=", 1)
        assignment(lhs, rhs)
    elif chunks[0] == 'del':
        delete_variable(chunks[1:])
    else :
        try:
            print(expr(command))
        except:
            print("command", chunks[0], "not found.")
while True:
    command = input(">>>")
    interpret(command)
