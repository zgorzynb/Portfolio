import LLVMActions
from DataManager import DataManager

class LLVMGenerator:

    header_text = ""
    main_text = ""
    footer_text =""
    functions = ""
    structs = ""
    global_values = ""
    str_i = 1
    if_num = 1
    read_used = False
    label = []

    @staticmethod
    def print_id(data_manager):
        name = LLVMGenerator.load(data_manager)
        var_type = data_manager.var_type
        LLVMGenerator.main_text += "%" + str(LLVMGenerator.str_i) + " = call i32(i8*,...) @printf({}, {} {})\n".format(data_manager.get_format(), var_type, name)
        LLVMGenerator.str_i += 1

    @staticmethod
    def read(data_manager):
        LLVMGenerator.read_used = True
        if data_manager.var_type is "double":
            LLVMGenerator.main_text += "%{} = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @scan_double, i64 0, i64 0), double* {})\n".format(LLVMGenerator.str_i, data_manager.llvm_name)
        elif data_manager.var_type is "i32":
            LLVMGenerator.main_text += "%{} = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @scan_int, i64 0, i64 0), i32* {})\n".format(LLVMGenerator.str_i, data_manager.llvm_name)
        else:
            raise RuntimeError("Variable has wrong type")
        LLVMGenerator.str_i += 1

    @staticmethod
    def ao(ctx, data_manager_1, data_manager_2):
        v1 = LLVMGenerator.load(data_manager_1)
        v2 = LLVMGenerator.load(data_manager_2)

        if ctx.ADD() is not None:
            data_manager_3, value = LLVMGenerator.add(data_manager_1, data_manager_2, v1, v2)

        if ctx.MINUS() is not None:
            data_manager_3, value = LLVMGenerator.sub(data_manager_1, data_manager_2, v1, v2)

        if ctx.MUL() is not None:
            data_manager_3, value = LLVMGenerator.mul(data_manager_1, data_manager_2, v1, v2)

        if ctx.DIV() is not None:
            data_manager_3, value = LLVMGenerator.div(data_manager_1, data_manager_2, v1, v2)

        if ctx.POW() is not None:
            pass

        LLVMGenerator.allocate(data_manager_3, value)

        return data_manager_3

    @staticmethod
    def allocate(data_manager, value):
        value = str(value)
        LLVMGenerator.alloca(data_manager)
        LLVMGenerator.store(data_manager, value)

    @staticmethod
    def alloca(data_manager):
        name = str(data_manager.llvm_name)
        var_type = str(data_manager.var_type)
        size = str(data_manager.size)
        LLVMGenerator.main_text += name + " = alloca " + var_type + ", align " + size + "\n"
        LLVMGenerator.str_i += 1

    def allocate_array(data_manager, values):
        LLVMGenerator.alloca(data_manager=data_manager)
        llvm_name = "%{}".format(LLVMGenerator.str_i)
        LLVMGenerator.main_text += "{} = getelementptr inbounds {}, {}* {}, i64 0, i64 0\n".format(llvm_name,
                                                                                                  data_manager.var_type,
                                                                                                  data_manager.var_type,
                                                                                                  data_manager.llvm_name)
        LLVMGenerator.str_i += 1
        id = LLVMGenerator.load(values[0].data_manager)
        LLVMGenerator.main_text += "store {} {}, {}* {}, align {}\n".format(data_manager.sub_type,
                                                                            id,
                                                                            data_manager.sub_type,
                                                                            llvm_name,
                                                                            data_manager.size)

        for i in range(1,len(values)):
            last_llvm_name = llvm_name
            llvm_name = "%{}".format(LLVMGenerator.str_i)
            LLVMGenerator.main_text += "{} = getelementptr inbounds {}, {}* {}, i64 1\n".format(llvm_name,
                                                                                              data_manager.sub_type,
                                                                                              data_manager.sub_type,
                                                                                              last_llvm_name)
            LLVMGenerator.str_i += 1
            id = LLVMGenerator.load(values[i].data_manager)
            LLVMGenerator.main_text += "store {} {}, {}* {}, align {}\n".format(data_manager.sub_type,
                                                                                id,
                                                                                data_manager.sub_type,
                                                                                llvm_name,
                                                                                data_manager.size)

    def allocate_string(data_manager, string):
        LLVMGenerator.header_text += "{} =  constant {} c\"{}\\0A\\00\"\n".format(data_manager.llvm_name,
                                                                                data_manager.var_type,
                                                                                string)

    def get_elem(id_dm, value_dm):
        id = LLVMGenerator.load(value_dm)
        LLVMGenerator.main_text += "%{} = sext i32 {} to i64\n".format(LLVMGenerator.str_i, id)
        LLVMGenerator.str_i += 1
        LLVMGenerator.main_text += "%{} = getelementptr inbounds {}, {}* {}, i64 0, i64 {}\n".format(LLVMGenerator.str_i,
                                                                                                   id_dm.var_type,
                                                                                                   id_dm.var_type,
                                                                                                   id_dm.llvm_name,
                                                                                                   "%{}".format(LLVMGenerator.str_i-1))
        LLVMGenerator.str_i += 1
        return "%{}".format(LLVMGenerator.str_i-1)


    @staticmethod
    def store(data_manager, value):
        name = str(data_manager.llvm_name)
        var_type = str(data_manager.var_type)
        size = str(data_manager.size)
        value = str(value)
        LLVMGenerator.main_text += "store " + var_type + " " + value + ", " + var_type + "* " + name + ", align " + size + "\n"

    @staticmethod
    def load(data_manager):
        name = "%" + str(LLVMGenerator.str_i)
        llvm_name = str(data_manager.llvm_name)
        var_type = str(data_manager.var_type)
        size = str(data_manager.size)
        LLVMGenerator.main_text += name + " = load " + var_type + ", " + var_type + "* " + llvm_name + ", align " + size + "\n"
        LLVMGenerator.str_i += 1
        return name


    def add(data_manager_1, data_manager_2, v1, v2):
        type_1 = data_manager_1.var_type
        type_2 = data_manager_2.var_type

        if type_1 is "i32" and type_2 is "i32":
            LLVMGenerator.main_text += "%{} = add nsw i32 {}, {}\n".format(LLVMGenerator.str_i, v1, v2)
            var_type = "i32"
            size = "4"
        elif type_1 is "double" and type_2 is "i32":
            temp = "%{}".format(LLVMGenerator.str_i)
            LLVMGenerator.str_i += 1
            LLVMGenerator.main_text += "{} = sitofp i32 {} to double\n".format(temp, v2)
            LLVMGenerator.main_text += "%{} = fadd double {}, {}\n".format(LLVMGenerator.str_i, v1, temp)
            var_type = "double"
            size = "8"
        elif type_1 is "i32" and type_2 is "double":
            temp = "%{}".format(LLVMGenerator.str_i)
            LLVMGenerator.str_i += 1
            LLVMGenerator.main_text += "{} = sitofp i32 {} to double\n".format(temp, v1)
            LLVMGenerator.main_text += "%{} = fadd double {}, {}\n".format(LLVMGenerator.str_i, temp, v2)
            var_type = "double"
            size = "8"
        elif type_1 is "double" and type_2 is "double":
            LLVMGenerator.main_text += "%{} = fadd double {}, {}\n".format(LLVMGenerator.str_i, v1, v2)
            var_type = "double"
            size = "8"
        else:
            raise RuntimeError("Wrong data types")

        value = llvm_name = "%{}".format(LLVMGenerator.str_i)
        LLVMGenerator.str_i += 1
        llvm_name = "%{}".format(LLVMGenerator.str_i)
        python_name = llvm_name
        is_const = True

        data_manager_3 = DataManager(llvm_name, python_name, var_type, size, is_const)
        return data_manager_3, value

    def sub(data_manager_1, data_manager_2, v1, v2):
        type_1 = data_manager_1.var_type
        type_2 = data_manager_2.var_type

        if type_1 is "i32" and type_2 is "i32":
            LLVMGenerator.main_text += "%{} = sub nsw i32 {}, {}\n".format(LLVMGenerator.str_i, v1, v2)
            var_type = "i32"
            size = "4"
        elif type_1 is "double" and type_2 is "i32":
            temp = "%{}".format(LLVMGenerator.str_i)
            LLVMGenerator.str_i += 1
            LLVMGenerator.main_text += "{} = sitofp i32 {} to double\n".format(temp, v2)
            LLVMGenerator.main_text += "%{} = fsub double {}, {}\n".format(LLVMGenerator.str_i, v1, temp)
            var_type = "double"
            size = "8"
        elif type_1 is "i32" and type_2 is "double":
            temp = "%{}".format(LLVMGenerator.str_i)
            LLVMGenerator.str_i += 1
            LLVMGenerator.main_text += "{} = sitofp i32 {} to double\n".format(temp, v1)
            LLVMGenerator.main_text += "%{} = fsub double {}, {}\n".format(LLVMGenerator.str_i, temp, v2)
            var_type = "double"
            size = "8"
        elif type_1 is "double" and type_2 is "double":
            LLVMGenerator.main_text += "%{} = fsub double {}, {}\n".format(LLVMGenerator.str_i, v1, v2)
            var_type = "double"
            size = "8"
        else:
            raise RuntimeError("Wrong data types")

        value = llvm_name = "%{}".format(LLVMGenerator.str_i)
        LLVMGenerator.str_i += 1
        llvm_name = "%{}".format(LLVMGenerator.str_i)
        python_name = llvm_name
        is_const = True

        data_manager_3 = DataManager(llvm_name, python_name, var_type, size, is_const)
        return data_manager_3, value

    def mul(data_manager_1, data_manager_2, v1, v2):
        type_1 = data_manager_1.var_type
        type_2 = data_manager_2.var_type

        if type_1 is "i32" and type_2 is "i32":
            LLVMGenerator.main_text += "%{} = mul nsw i32 {}, {}\n".format(LLVMGenerator.str_i, v1, v2)
            var_type = "i32"
            size = "4"
        elif type_1 is "double" and type_2 is "i32":
            temp = "%{}".format(LLVMGenerator.str_i)
            LLVMGenerator.str_i += 1
            LLVMGenerator.main_text += "{} = sitofp i32 {} to double\n".format(temp, v2)
            LLVMGenerator.main_text += "%{} = fmul double {}, {}\n".format(LLVMGenerator.str_i, v1, temp)
            var_type = "double"
            size = "8"
        elif type_1 is "i32" and type_2 is "double":
            temp = "%{}".format(LLVMGenerator.str_i)
            LLVMGenerator.str_i += 1
            LLVMGenerator.main_text += "{} = sitofp i32 {} to double\n".format(temp, v1)
            LLVMGenerator.main_text += "%{} = fmul double {}, {}\n".format(LLVMGenerator.str_i, temp, v2)
            var_type = "double"
            size = "8"
        elif type_1 is "double" and type_2 is "double":
            LLVMGenerator.main_text += "%{} = fmul double {}, {}\n".format(LLVMGenerator.str_i, v1, v2)
            var_type = "double"
            size = "8"
        else:
            raise RuntimeError("Wrong data types")

        value = llvm_name = "%{}".format(LLVMGenerator.str_i)
        LLVMGenerator.str_i += 1
        llvm_name = "%{}".format(LLVMGenerator.str_i)
        python_name = llvm_name
        is_const = True

        data_manager_3 = DataManager(llvm_name, python_name, var_type, size, is_const)
        return data_manager_3, value

    def div(data_manager_1, data_manager_2, v1, v2):
        type_1 = data_manager_1.var_type
        type_2 = data_manager_2.var_type

        if type_1 is "i32" or "double" and type_2 is "i32" or "double":
            if type_1 is "i32":
                temp = "%{}".format(LLVMGenerator.str_i)
                LLVMGenerator.str_i += 1
                LLVMGenerator.main_text += "{} = sitofp i32 {} to double\n".format(temp, v1)
                v1 = temp
            if type_2 is "i32":
                temp = "%{}".format(LLVMGenerator.str_i)
                LLVMGenerator.str_i += 1
                LLVMGenerator.main_text += "{} = sitofp i32 {} to double\n".format(temp, v2)
                v2 = temp

            LLVMGenerator.main_text += "%{} = fdiv double {}, {}\n".format(LLVMGenerator.str_i, v1, v2)
            var_type = "double"
            size = "8"
            value = llvm_name = "%{}".format(LLVMGenerator.str_i)
            LLVMGenerator.str_i += 1
            llvm_name = "%{}".format(LLVMGenerator.str_i)
            python_name = llvm_name
            is_const = True

        else:
            raise RuntimeError("Wrong data types")

        data_manager_3 = DataManager(llvm_name, python_name, var_type, size, is_const)
        return data_manager_3, value

    @staticmethod
    def generate():
        text = "declare i32 @printf(i8*, ...)\n\n"

        text += "@print_int = constant [4 x i8] c\"%d\\0A\\00\"\n"
        text += "@print_double = constant [4 x i8] c\"%f\\0A\\00\"\n"
        text += "$scan_double = comdat any\n"
        text += "@scan_double = linkonce_odr dso_local unnamed_addr constant [4 x i8] c\"%lf\00\", comdat, align 1\n"
        text += "$scan_int = comdat any\n"
        text += "@scan_int = linkonce_odr dso_local unnamed_addr constant [3 x i8] c\"%d\00\", comdat, align 1\n\n"

        text += LLVMGenerator.header_text
        text += LLVMGenerator.global_values
        text += LLVMGenerator.structs
        text += LLVMGenerator.functions
        text += "define i32 @main() nounwind{\n"
        text += LLVMGenerator.main_text
        text += "ret i32 0 }\n\n\n"
        if LLVMGenerator.read_used:
            text += LLVMGenerator.footer_text
        return text

############################################################################################################
############################################ 2 część #######################################################
############################################################################################################
    @staticmethod
    def check_bool(dm1, dm2, sign):

        var_1 = LLVMGenerator.load(dm1)
        var_2 = LLVMGenerator.load(dm2)

        LLVMGenerator.main_text += '%{} = {} {} {},{}\n'.format(LLVMGenerator.str_i,sign,dm1.var_type, var_1, var_2)
        LLVMGenerator.main_text += 'br i1 %{}, label %True{}, label %False{}\n'.format(LLVMGenerator.str_i, LLVMGenerator.if_num, LLVMGenerator.if_num)

        LLVMGenerator.str_i += 1
        LLVMGenerator.if_num += 2
        LLVMGenerator.label.append('False')
        LLVMGenerator.label.append('True')
        return LLVMGenerator.if_num

    @staticmethod
    def new_block(id):
        LLVMGenerator.main_text += '{}{}:\n'.format(LLVMGenerator.label.pop(-1), id-2)

    #Functions
    @staticmethod
    def function_header(fun_name):
        LLVMGenerator.functions += "\n"
        LLVMGenerator.functions += "; Function Attrs: nounwind uwtable\n"
        LLVMGenerator.functions += "define i32 @{}() #0 ".format(fun_name)
        LLVMGenerator.functions += "{\n"

    @staticmethod
    def function_footer(x):
        LLVMGenerator.functions += '{}\n'.format(x)
        LLVMGenerator.functions += "}\n\n"

    @staticmethod
    def call_fun(fun_name):
        id = "%" + str(LLVMGenerator.str_i)
        LLVMGenerator.main_text += "{} = call i32 @{}()\n".format(id, fun_name)
        LLVMGenerator.str_i += 1
        return id

    #Struktury
    @staticmethod
    def struct_header(struct):
        LLVMGenerator.structs += '%struct.{} = '.format(struct.name)
        LLVMGenerator.structs += "type {"
        LLVMGenerator.structs += struct.get_types()
        LLVMGenerator.structs += "}\n"

    @staticmethod
    def allocate_struct(struct):
        id = "%{}".format(LLVMGenerator.str_i)
        LLVMGenerator.main_text += "{} = alloca %struct.{}, align 8\n".format(id, struct.name)
        LLVMGenerator.str_i +=1
        return id

    @staticmethod
    def get_struct_elem(struct, struct_obj, index):
        id = "%{}".format(LLVMGenerator.str_i)
        LLVMGenerator.main_text += "{} = getelementptr inbounds %struct.{}, %struct.{}* {}, i32 0, i32 {}\n".format(id,
                                                                                                                  struct.name,
                                                                                                                  struct.name,
                                                                                                                  struct_obj.id,
                                                                                                                 index)
        LLVMGenerator.str_i +=1
        return id

    @staticmethod
    def store_struct_elem(type, id_to_store, id):

        LLVMGenerator.main_text += "store {} {}, {}* {}, align 8\n".format(type,id_to_store,type, id)


    @staticmethod
    def assing_global(name, dm, value):
        LLVMGenerator.global_values += "@{} = global {} {}, align {}\n".format(name, dm.var_type, value, dm.size)





    footer_text = """%struct._iobuf = type { i8* }
%struct.__crt_locale_pointers = type { %struct.__crt_locale_data*, %struct.__crt_multibyte_data* }
%struct.__crt_multibyte_data = type opaque
%struct.__crt_locale_data = type opaque
declare dso_local %struct._iobuf* @__acrt_iob_func(i32) #3

@__local_stdio_scanf_options._OptionsStorage = internal global i64 0, align 8

$_vfscanf_l = comdat any
$scanf = comdat any
$__local_stdio_scanf_options = comdat any


define linkonce_odr dso_local i32 @scanf(i8* %0, ...) #0 comdat {
  %2 = alloca i8*, align 8
  %3 = alloca i32, align 4
  %4 = alloca i8*, align 8
  store i8* %0, i8** %2, align 8
  %5 = bitcast i8** %4 to i8*
  call void @llvm.va_start(i8* %5)
  %6 = load i8*, i8** %4, align 8
  %7 = load i8*, i8** %2, align 8
  %8 = call %struct._iobuf* @__acrt_iob_func(i32 0)
  %9 = call i32 @_vfscanf_l(%struct._iobuf* %8, i8* %7, %struct.__crt_locale_pointers* null, i8* %6)
  store i32 %9, i32* %3, align 4
  %10 = bitcast i8** %4 to i8*
  call void @llvm.va_end(i8* %10)
  %11 = load i32, i32* %3, align 4
  ret i32 %11
}

define linkonce_odr dso_local i64* @__local_stdio_scanf_options() #1 comdat {
  ret i64* @__local_stdio_scanf_options._OptionsStorage
}

declare void @llvm.va_start(i8*) #2
declare void @llvm.va_end(i8*) #2
declare dso_local i32 @__stdio_common_vfscanf(i64, %struct._iobuf*, i8*, %struct.__crt_locale_pointers*, i8*) #3

define linkonce_odr dso_local i32 @_vfscanf_l(%struct._iobuf* %0, i8* %1, %struct.__crt_locale_pointers* %2, i8* %3) #1 comdat {
  %5 = alloca i8*, align 8
  %6 = alloca %struct.__crt_locale_pointers*, align 8
  %7 = alloca i8*, align 8
  %8 = alloca %struct._iobuf*, align 8
  store i8* %3, i8** %5, align 8
  store %struct.__crt_locale_pointers* %2, %struct.__crt_locale_pointers** %6, align 8
  store i8* %1, i8** %7, align 8
  store %struct._iobuf* %0, %struct._iobuf** %8, align 8
  %9 = load i8*, i8** %5, align 8
  %10 = load %struct.__crt_locale_pointers*, %struct.__crt_locale_pointers** %6, align 8
  %11 = load i8*, i8** %7, align 8
  %12 = load %struct._iobuf*, %struct._iobuf** %8, align 8
  %13 = call i64* @__local_stdio_scanf_options()
  %14 = load i64, i64* %13, align 8
  %15 = call i32 @__stdio_common_vfscanf(i64 %14, %struct._iobuf* %12, i8* %11, %struct.__crt_locale_pointers* %10, i8* %9)
  ret i32 %15
}\n"""
