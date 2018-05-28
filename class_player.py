class player:
    def __init__(self, name, chips):
        self.__name = name
        self.__chips = chips

        # default
        self.__cards = []
        self.__opened = False
        self.__betted = 0
        self.__folded = False

    @property
    def get_name(self):
        return self.__name

    @property
    def get_chips(self):
        return self.__chips

    @property
    def get_opened(self):
        return self.__opened

    @property
    def get_betted(self):
        return self.__betted

    @property
    def get_folded(self):
        return self.__folded

    @property
    def reset_betted(self):
        self.__betted = 0

    def get_card(self,index):
        return self.__cards[index]

    def give_card(self, card):
        self.__cards.append(card)

    @property
    def card_reset(self):
        self.__opened = False
        self.__cards = []

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
        if chips == -1:
            self.__folded = True
        else:
            self.__chips -= chips
            self.__betted += chips