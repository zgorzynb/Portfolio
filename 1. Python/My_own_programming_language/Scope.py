class Scope:

    main_text = ""
    local_variables = dict()

    def __init__(self, obj, obj2, type):
        self.generator = obj
        self.actions = obj2
        self.main_text = obj.main_text
        self.type = type
        self.memory = obj2.memory.copy()
        self.str_i = obj.str_i
        if type is 'function':
            obj2.memory = dict()
            for var in obj2.global_var:
                obj2.memory[var] = self.memory[var]


    def end_block(self):
        self.old_memory = self.actions.memory
        self.actions.memory = self.memory.copy()

        if self.type is 'function':
            text = self.generator.main_text[len(self.main_text):]
            text = self.generate_text(text)
            self.generator.functions += text
            self.generator.main_text = self.main_text
            self.generator.str_i = self.str_i


    def generate_text(self, text):
        text = text.replace('%', '%fun')
        text = text.replace('%funT', '%T')
        text = text.replace('%funF', '%F')
        text = text.replace('%funt', '%t')
        text = text.replace('%funf', '%f')
        return text



