class player:
    def __init__(self, name, chips):
        self.__name = name
        self.__chips = chips

    @property
    def get_name(self):
        return self.__name

    @property
    def get_chips(self):
        return self.__chips

    def bet(self, chips):
        self.__chips -= chips