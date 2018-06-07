import s_mode_ai as s

class player:
    def __init__(self, name, chips):
        self.__name = name
        self.__chips = chips

        # default
        self.__cards = []
        self.__opened = False
        self.__betted = 0
        self.__folded = False
        self.__thinked = False
        self.__rank = ()

    @property
    def get_name(self):
        return self.__name

    @property
    def get_chips(self):
        return self.__chips

    def give_chips(self, chips):
        self.__chips += chips

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
    def reset_folded(self):
        self.__folded = False

    @property
    def get_thinked(self):
        return self.__thinked

    @property
    def reset_think(self):
        self.__thinked = False

    @property
    def reset_betted(self):
        self.__betted = 0

    def set_chips(self, chips):
        self.__chips = chips

    def get_card(self,index):
        return self.__cards[index]

    def give_card(self, card):
        self.__cards.append(card)

    @property
    def card_reset(self):
        self.__opened = False
        self.__cards = []
        self.__rank = ()

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
        self.__thinked = True

    def my_rank(self, cards):
        card_list = []
        for i in self.__cards + cards:
            card_list.append(list(i.get_card))
        self.__rank = s.get_rank(s.str_to_int(card_list))
        return self.__rank