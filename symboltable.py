class SymbolTable: # таблица символов
    def __init__(self):
        self.symbols = [] #List

    def set(self, name, symbol_type, symbol_type_two = None): #add
        symbol_list
        self.symbols[name] = symbol_type

    def get(self, name): #return
        return self.symbols.get(name, None)

    def check(self, name): #bool check
        return name


    """
    1) Имя
    2) Тип
    3) 2 Тип
    """



