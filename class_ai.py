class ai:
    def __init__(self, name, chips, mode):
        self.__name = name
        self.__chips = chips
        self.__mode = mode

        #default
        self.__cards = []
        self.__opened = False
        self.__betted = 0
        self.__folded = False
        self.__thinking = False
        self.__thinked = False

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
    def get_thinked(self):
        return self.__thinked

    @property
    def reset_betted(self):
        self.__betted = 0

    @property
    def reset_think(self):
        self.__thinking = False
        self.__thinked = False

    def get_card(self, index):
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
            self.__cards[0].show(False, True)
            self.__cards[1].show(False, True)
        if self.__cards[0].get_faced and self.__cards[1].get_faced:
            self.__opened = True

    @property
    def card_show(self):
        self.__cards[0].show()
        self.__cards[1].show()

    def bet(self, chips):
        self.__chips -= chips
        self.__betted += chips
        self.__thinked = True

    @property
    def get_thinking(self):
        return self.__thinking

    def think(self, cards):
        self.__thinking = True