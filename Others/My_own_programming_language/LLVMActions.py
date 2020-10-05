from PLwypiszListener import PLwypiszListener
from LLVMGenerator import LLVMGenerator
from DataManager import DataManager
from Scope import Scope
from Struct import Struct
from Struct_Object import Struct_Object

class LLVMActions(PLwypiszListener):

    value = ""
    ao = ""
    memory = dict()
    structures = dict()
    structures_obj = dict()
    functions = []
    global_var = []
    ifs = []

    def exitAo(self, ctx):
        data_manager_1 = ctx.value()[0].data_manager
        data_manager_2 = ctx.value()[1].data_manager
        data_manager_3 = LLVMGenerator.ao(ctx=ctx, data_manager_1=data_manager_1, data_manager_2=data_manager_2)
        self.memory[data_manager_3.python_name] = data_manager_3
        ctx.data_manager = data_manager_3

    def exitRead(self, ctx):
        data_manager = self.memory[ctx.ID().getText()]
        LLVMGenerator.read(data_manager)

    def exitAssign(self, ctx):
        #done
        if ctx.ID().getText() not in self.memory:
            #alokacja
            if ctx.value() is not None:
                data_manager = ctx.value().data_manager

            if ctx.ao() is not None:
                data_manager = ctx.ao().data_manager

            del self.memory[data_manager.python_name]
            python_name = ctx.ID().getText()
            data_manager.python_name = python_name
            data_manager.is_const = False
            self.memory[python_name] = data_manager
        else:
            raise RuntimeError("Variable already created")

    def exitNextassign(self, ctx):
        if ctx.ID().getText() in self.memory:
            if ctx.value() is not None:
                out_data_manager = ctx.value().data_manager

            if ctx.ao() is not None:
                out_data_manager = ctx.ao().data_manager


            data_manager = self.memory[ctx.ID().getText()]

            if data_manager.var_type is out_data_manager.var_type:
                x = LLVMGenerator.load(out_data_manager)
                LLVMGenerator.main_text += "store {} {}, {}* {}, align {}\n".format(data_manager.var_type, x,data_manager.var_type, data_manager.llvm_name,data_manager.size)
            else:
                raise RuntimeError("Variable type doesnt match")

        else:
            raise RuntimeError("Variable doesn`t exist")

    def exitValue(self, ctx):
        if ctx.ID() is not None:
            if ctx.ID().getText() in self.memory:
                ctx.data_manager = self.memory[ctx.ID().getText()]
            elif ctx.ID().getText() in self.functions:
                value = LLVMGenerator.call_fun(ctx.ID().getText())
                llvm_name = "%" + str(LLVMGenerator.str_i)
                python_name = llvm_name
                var_type = "i32"
                size = "4"
                is_const = True
                data_manager = DataManager(llvm_name=llvm_name, python_name=python_name, var_type=var_type, size=size,
                                           is_const=is_const)
                ctx.data_manager = data_manager
                self.memory[python_name] = data_manager
                LLVMGenerator.allocate(data_manager=data_manager, value=value)
            else:
                raise RuntimeError("Variable: '" + str(ctx.ID().getText()) +"' not recognized")
        if ctx.INT() is not None:
            llvm_name = "%" + str(LLVMGenerator.str_i)
            python_name = llvm_name
            var_type = "i32"
            size = "4"
            is_const = True
            data_manager = DataManager(llvm_name=llvm_name, python_name= python_name, var_type = var_type, size = size,
                                       is_const= is_const)
            ctx.data_manager = data_manager
            self.memory[python_name] = data_manager
            value = ctx.INT().getText()
            LLVMGenerator.allocate(data_manager=data_manager, value=value)

        if ctx.DOUBLE() is not None:
            llvm_name = "%" + str(LLVMGenerator.str_i)
            python_name = llvm_name
            var_type = "double"
            size = "8"
            is_const = True
            data_manager = DataManager(llvm_name=llvm_name, python_name= python_name, var_type = var_type, size = size,
                                       is_const= is_const)
            ctx.data_manager = data_manager
            self.memory[python_name] = data_manager
            value = ctx.DOUBLE().getText()
            LLVMGenerator.allocate(data_manager=data_manager, value=value)

        if ctx.STRING() is not None:
            llvm_name = "@str" + str(LLVMGenerator.str_i)
            python_name = llvm_name
            string = ctx.STRING().getText()[1:-1]
            length = len(string)+2
            var_type = "[{} x i8]".format(length)
            size = "1"
            is_const = True
            data_manager = DataManager(llvm_name=llvm_name, python_name=python_name, var_type=var_type, size=size,
                                       is_const=is_const, length=length)
            ctx.data_manager = data_manager
            self.memory[python_name] = data_manager
            LLVMGenerator.allocate_string(data_manager=data_manager, string=string)

        if ctx.arr() is not None:
            llvm_name = "%" + str(LLVMGenerator.str_i)
            python_name = llvm_name
            length = len(ctx.arr().value())
            sub_type = ctx.arr().value()[0].data_manager.var_type
            var_type = "[{} x {}]".format(length, sub_type)
            size = ctx.arr().value()[0].data_manager.size
            is_const = True

            data_manager = DataManager(llvm_name=llvm_name, python_name=python_name, var_type=var_type, size=size,
                                       is_const=is_const, sub_type=sub_type, length=length)
            ctx.data_manager = data_manager
            self.memory[python_name] = data_manager
            values = ctx.arr().value()
            LLVMGenerator.allocate_array(data_manager=data_manager, values=values)

        if ctx.arr_element() is not None:
            if ctx.arr_element().ID().getText() in self.memory:
                id_dm = self.memory[ctx.arr_element().ID().getText()]
                value_dm = ctx.arr_element().value().data_manager
                llvm_name = LLVMGenerator.get_elem(id_dm=id_dm, value_dm=value_dm)
                python_name = llvm_name
                var_type = id_dm.sub_type
                size = id_dm.size
                is_const = True
                data_manager = DataManager(llvm_name=llvm_name, python_name=python_name, var_type=var_type, size=size,
                                           is_const=is_const)
                self.memory[python_name]= data_manager
                ctx.data_manager = data_manager
            else:
                raise RuntimeError("Array not recognized")

        if ctx.struct_elem() is not None:
            id_1 = ctx.struct_elem().ID()[0].getText()
            id_2 = ctx.struct_elem().ID()[1].getText()
            struct = self.structures_obj[id_1]
            parent = struct.parent
            index = parent.get_number(id_2)
            id = LLVMGenerator.get_struct_elem(parent, struct, index)

            llvm_name = id
            python_name = llvm_name
            var_type = parent.types[index]
            size = 4
            is_const = False
            data_manager = DataManager(llvm_name, python_name,var_type,size,is_const)
            ctx.data_manager = data_manager


    def exitPrint(self, ctx):
        if ctx.value() is not None:
            data_manager = ctx.value().data_manager
            LLVMGenerator.print_id(data_manager)

        if ctx.ao() is not None:
            data_manager = ctx.ao().data_manager
            LLVMGenerator.print_id(data_manager)

    def exitProg(self, ctx):
        print(LLVMGenerator.generate())
############################################################################################################
############################################ 2 część #######################################################
############################################################################################################
    #IF

    def exitSign(self, ctx):
        dm1 = ctx.value()[0].data_manager
        dm2 = ctx.value()[1].data_manager
        if dm1.var_type is 'i32':
            if '>' in ctx.getText():
                sign = 'icmp sgt'
            elif '<' in ctx.getText():
                sign = 'icmp slt'
            else:
                sign = 'icmp eq'
        else:
            if '>' in ctx.getText():
                sign = 'fcmp ogt'
            elif '<' in ctx.getText():
                sign = 'fcmp olt'
            else:
                sign = 'fcmp oeq'
        id = LLVMGenerator.check_bool(dm1, dm2, sign)
        LLVMActions.ifs.append(id)


    def exitElse_if(self, ctx):
        id =  LLVMActions.ifs.pop(-1)
        LLVMGenerator.main_text += "false{}:\n".format(id - 1)

    def enterBlock(self, ctx):
        scope = Scope(LLVMGenerator, self, 'if_loop')
        ctx.scope = scope
        id = LLVMActions.ifs[-1]
        LLVMGenerator.new_block(id)

    def exitBlock(self, ctx):
        id = LLVMActions.ifs[-1]
        LLVMGenerator.main_text += "br label %false{}\n".format(id-1)
        ctx.scope.end_block()

    #LOOP

    def enterLoop(self, ctx):
        LLVMGenerator.main_text += 'br label %false{}\n'.format(LLVMGenerator.if_num+1)
        LLVMGenerator.main_text += '\n'
        id = LLVMGenerator.if_num
        LLVMActions.ifs.append(id)
        LLVMGenerator.main_text += 'false{}:\n'.format(id+1)

    def exitLoop(self, ctx):
        id = LLVMActions.ifs.pop(-1)
        LLVMGenerator.main_text += 'False{}:\n'.format(id-2)
        LLVMGenerator.if_num += 1

    #Funkcje

    def enterFunction(self, ctx):
        fun_name = ctx.fparam().getText()
        self.functions.append(fun_name)
        LLVMGenerator.function_header(fun_name)
        ctx.main_text = LLVMGenerator.main_text

    def exitFunction(self, ctx):
        length = len(ctx.main_text)
        x = LLVMGenerator.main_text[length:]
        LLVMGenerator.main_text = ctx.main_text
        LLVMGenerator.function_footer(x)

    def enterFblock(self, ctx):
        scope = Scope(LLVMGenerator, LLVMActions, 'function')
        ctx.scope = scope

    def exitFblock(self, ctx):

        if 'output' in self.memory:
            output = self.memory['output']
            output = LLVMGenerator.load(output)
            LLVMGenerator.main_text += "ret i32 {}".format(output)
        else:
            raise RuntimeError("No output in this function")
        scope = ctx.scope
        scope.end_block()

    def exitCall_function(self, ctx):
        if ctx.ID().getText() in self.functions:
            LLVMGenerator.call_fun(ctx.ID().getText())
        else:
            raise RuntimeError("No function called: " + ctx.ID().getText())

    #Struktury

    def enterStruct(self, ctx):
        struct_name = ctx.ID().getText()
        types = []
        names = []
        for elem in ctx.structblock().structelem():
            if 'double' in elem.getText():
                types.append('double')
                names.append(elem.getText()[6:])
            elif 'int' in elem.getText():
                types.append("i32")
                names.append(elem.getText()[3:])
            else:
                raise RuntimeError("Type not recogized")

        struct = Struct(struct_name, types, names)
        self.structures[struct_name] = struct
        LLVMGenerator.struct_header(struct)

    def exitAllocatestruct(self, ctx):
        struct_name = ctx.ID()[0].getText()
        var_name = ctx.ID()[1].getText()

        if struct_name in self.structures:
            struct = self.structures[ctx.ID()[0].getText()]
            id = LLVMGenerator.allocate_struct(struct)
            struct_object = Struct_Object(var_name, struct, id)
            self.structures_obj[var_name] = struct_object
        else:
            raise RuntimeError("Struct not recognized")

    def exitStorestruct(self, ctx):
        struct_name = ctx.ID()[0].getText()
        var_name = ctx.ID()[1].getText()
        if struct_name in self.structures_obj:
            struct_obj = self.structures_obj[struct_name]
            struct = struct_obj.parent
            if var_name in struct.names:
                index = struct.get_number(var_name)
                id_to_store = LLVMGenerator.load(ctx.value().data_manager)
                id = LLVMGenerator.get_struct_elem(struct, struct_obj, index)
                type = struct.types[index]

                LLVMGenerator.store_struct_elem(type = type, id=id, id_to_store=id_to_store)

            else:
                raise RuntimeError("Structure doesnt have this field")
        else:
            raise RuntimeError("Structure doesnt exist")


    #zmienneglobalne

    def exitAssignglobalvalue(self, ctx):
        dm = ctx.value().data_manager
        value = ctx.value().getText()
        name = ctx.ID().getText()
        LLVMGenerator.assing_global(name, dm, value)

        llvm_name = "@" + name
        python_name = name
        var_type = dm.var_type
        size = dm.size
        is_const = True
        data_manager = DataManager(llvm_name=llvm_name, python_name=python_name, var_type=var_type, size=size,
                                   is_const=is_const)
        self.memory[name] = data_manager
        self.global_var.append(name)
