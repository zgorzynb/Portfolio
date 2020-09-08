class Struct:

    def __init__(self, name, types, names):
        self.name = name
        self.types = types
        self.names = names



    def get_number(self, name):
        if name in self.names:
            return self.names.index(name)
        else:
            raise RuntimeError("Field doesnt exist!")

    def get_types(self):
        return ', '.join(self.types)
