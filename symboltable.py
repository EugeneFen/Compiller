class SymbolTable:
    symbols = {}

    def __init__(self):
        self.symbols = {} #?????


    def set(self, name, symbol_type):
        print(name, "Add")
        if not (name in self.symbols.items()):
            self.symbols[name] = symbol_type
            return True
        return False


    def get(self, name):
        if self.symbols[name]:
            return self.symbols[name]
        return "Not value"

    def check(self, value):
        if value in self.symbols.items():
            return False
        return True
