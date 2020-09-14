class DataManager:

    def __init__(self, llvm_name, python_name, var_type, size, is_const=False, sub_type=None, length=None):
        self.llvm_name = llvm_name
        self.python_name = python_name
        self.var_type = var_type
        self.size = size
        self.is_const = is_const
        self.sub_type = sub_type
        self.length = length

    def get_format(self):
        if self.var_type is "i32":
            text = "i8* getelementptr([4 x i8], [4 x i8]* @print_int, i32 0, i32 0)"
        elif self.var_type is "double":
            text = "i8* getelementptr([4 x i8], [4 x i8]* @print_double, i32 0, i32 0)"
        else:
            text = "i8* getelementptr inbounds ( "+str(self.var_type)+", "+str(self.var_type)+ "* " + str(self.llvm_name)+", i32 0, i32 0)"
        return text

