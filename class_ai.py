class ai:
    def __init__(self, name, chips, mode):
        self.__name = name
        self.__chips = chips
        self.__mode = mode

        #default
        self.__cards = []
        self.__opened = False

    @property
    def get_name(self):
        return self.__name

    @property
    def get_chips(self):
        return self.__chips

    @property
    def get_opened(self):
        return self.__opened

    def get_card(self,index):
        return self.__cards[index]

    def give_card(self, card):
        self.__cards.append(card)

    @property
    def card_open(self):
        if not self.__opened:
            self.__cards[0].show(False,True)
            self.__cards[1].show(False,True)
        if self.__cards[0].get_faced and self.__cards[1].get_faced:
            self.__opened = True

    @property
    def card_show(self):
        self.__cards[0].show()
        self.__cards[1].show()

    def bet(self, chips):
        self.__chips -= chips