import s_mode_ai as s
import random

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

    def give_chips(self, chips):
        self.__chips += chips
        print(self.__chips)

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

    @property
    def get_thinking(self):
        return self.__thinking

    def think(self, cards, step, bet_state):
        # 순위(순위가 같은 경우 추후에 계산)
        # 000 ~ 001 Royal Flush
        # 002 ~ 010 Straight Flush
        # 011 ~ 023 Four Card
        # 024 ~ 036 Full House
        # 037 ~ 044 Flush
        # 045 ~ 054 Straight
        # 055 ~ 067 Triple
        # 068 ~ 145 Two Pair
        # 146 ~ 158 One Pair
        # 159 ~ 166 High Card
        self.__thinking = True
        card_list = []
        for i in self.__cards + cards:
            card_list.append(list(i.get_card))
        tree = s.get_rank(s.str_to_int(card_list))
        rand = random.randint(1,100)
        expected = bet_state - self.__betted
        print(tree)
        if step == 1:
            if tree[1] in ("HIGH CARD", "ONE PAIR"):
                if 30 < rand <= 60:
                    self.bet(expected)
                else:
                    self.__folded = True
            elif tree[1] == "TWO PAIR":
                if 10 < rand <= 30 or 50 < rand <= 90:
                    self.bet(expected)
                else:
                    self.__folded = True
            else:
                self.bet(expected)
        self.__thinked = True