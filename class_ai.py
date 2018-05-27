class ai:
    def __init__(self, name, chips, mode):
        self.__name = name
        self.__chips = chips
        self.__mode = mode

    def bet(self, chips):
        self.__chips -= chips