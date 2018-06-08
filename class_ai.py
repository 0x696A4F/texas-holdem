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

    def set_chips(self, chips):
        self.__chips = chips

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
        self.__rank = ()

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
        if chips == -1:
            self.__folded = True
        else:
            self.__chips -= chips
            self.__betted += chips
        self.__thinking = False
        self.__thinked = True

    def my_rank(self, cards):
        card_list = []
        for i in self.__cards + cards:
            card_list.append(list(i.get_card))
        self.__rank = s.get_rank(s.str_to_int(card_list))
        return self.__rank

    def community_rank(self, cards):
        card_list = []
        for i in cards:
            card_list.append(list(i.get_card))
        self.__rank = s.get_rank(s.str_to_int(card_list))
        return s.get_rank(s.str_to_int(card_list))

    def portential_community_rank(self, cards):
        card_list = []
        for i in cards:
            card_list.append(list(i.get_card))
        return s.get_potential_rank(s.str_to_int(card_list))

    @property
    def get_thinking(self):
        return self.__thinking

    def think(self, cards, step, bet_state, p_chips): # p_chips 은 플레이어1의 칩개수.
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
        #### 베팅할때 플레이어 1의 칩 개수를 넘기면 안됨. ####
        self.__thinking = True
        if step == 1:
            c_tree = self.community_rank(cards[:5])
            tree = self.my_rank(cards[:5])
            P_c_tree = self.portential_community_rank(cards[:5])
        elif step == 2:
            c_tree = self.community_rank(cards[:4])
            tree = self.my_rank(cards[:4])
            P_c_tree = self.portential_community_rank(cards[:4])
        else:
            c_tree = self.community_rank(cards)           # 투페어이상 해당 step2부터 사용
            tree = self.my_rank(cards)
            P_c_tree = self.portential_community_rank(cards)             # 스트레이트와 플러쉬만 해당 step 4부터 사용
        betting = [10, 10, 10, 10, 20, 20, 20, 30, 30, 50, 50, 100]
        rand = random.randint(1,100)
        bluffing = random.randint(1,random.randint(50,100))
        bluffing_list = [50, 50, 50, 100, 100, 200, 300]
        expected = bet_state - self.__betted
        random.shuffle(betting)
        random.shuffle(bluffing_list)

        if betting[0] > self.__chips:
            betting[0] = self.__chips
        if bluffing_list[0] > self.__chips:
            bluffing_list[0] = self.__chips

        # 배팅
        if step == 1:
            if tree[1] in ("HIGH CARD", "ONE PAIR", "TWO PAIR"):
                if bet_state < 100:
                    if 10 < rand <= 90:
                        if expected <= 100:
                            self.bet(expected)
                        else:
                            if 40 < rand <= 55:
                                self.bet(expected)
                            else:
                                self.bet(-1)
                    else:
                        self.bet(-1)
                else:
                    if rand == 35:
                        self.bet(expected)
                    else:
                        self.bet(-1)
                    '''
                    if 30 < rand <= 40:
                        self.bet(expected)
                    else:
                        self.bet(-1)
                    '''
            else:
                self.bet(expected)

        elif step == 2:
            if tree[1] == "HIGH CARD":
                if bet_state < 100:
                    if 40 < bluffing <= 50:
                        if expected + bluffing_list[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + bluffing_list[0])
                    else:
                        if 20 < rand <= 80:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                else:
                    if 40 < bluffing <= 50:
                        if expected + bluffing_list[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + bluffing_list[0])
                    else:
                        self.bet(-1)
            elif tree[1] == "ONE PAIR":
                if bet_state < 150:
                    if 40 < bluffing <= 50:
                        if expected + bluffing_list[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + bluffing_list[0])
                    else:
                        if 10 < rand <= 90:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                else:
                    if 40 < bluffing <= 50:
                        if expected + bluffing_list[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + bluffing_list[0])
                    else:
                        self.bet(-1)
            elif tree[1] == "TWO PAIR":
                if 40 < bluffing <= 50:
                    if expected + bluffing_list[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + bluffing_list[0])
                else:
                    if c_tree[1] == "TWO PAIR":
                        if 30 < rand <= 70:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                    else:
                        if 25 < rand <= 75:
                            if expected + betting[0] > p_chips:
                                self.bet(p_chips)
                            else:
                                self.bet(expected + betting[0])
                        else:
                            self.bet(expected)
            elif tree[1] == "TRIPLE":
                if 40 < bluffing <= 50:
                    if expected + bluffing_list[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + bluffing_list[0])
                else:
                    if c_tree[1] == "TRIPLE":
                        if 30 < rand <= 70:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                    else:
                        if 20 < rand <= 80:
                            if expected + betting[0] > p_chips:
                                self.bet(p_chips)
                            else:
                                self.bet(expected + betting[0])
                        else:
                            self.bet(expected)
            else:
                if 40 < bluffing <= 50:
                    
                    if expected + bluffing_list[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + bluffing_list[0])
                else:
                    if 15 < rand <= 85:
                        if expected + betting[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + betting[0])
                    else:
                        self.bet(expected)
        elif step == 3:
            if tree[1] == "HIGH CARD":
                if bet_state < 100:
                    if 40 < bluffing <= 50:
                        if expected + bluffing_list[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + bluffing_list[0])
                    else:
                        if 20 < rand <= 80:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                else:
                    if 40 < bluffing <= 50:
                        if expected + bluffing_list[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + bluffing_list[0])
                    else:
                        self.bet(-1)
            elif tree[1] == "ONE PAIR":
                if bet_state < 150:
                    if 40 < bluffing <= 50:
                        
                        if expected + bluffing_list[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + bluffing_list[0])
                    else:
                        if 10 < rand <= 90:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                else:
                    if 40 < bluffing <= 50:
                        
                        if expected + bluffing_list[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + bluffing_list[0])
                    else:
                        self.bet(-1)
            elif tree[1] == "TWO PAIR":
                if 40 < bluffing <= 50:
                    
                    if expected + bluffing_list[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + bluffing_list[0])
                else:
                    if c_tree[1] == "TWO PAIR":
                        if 30 < rand <= 70:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                    else:
                        if 30 < rand <= 70:
                            if expected + betting[0] > p_chips:
                                self.bet(p_chips)
                            else:
                                self.bet(expected + betting[0])
                        else:
                            self.bet(expected)
            elif tree[1] == "TRIPLE":
                if 40 < bluffing <= 50:
                    
                    if expected + bluffing_list[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + bluffing_list[0])
                else:
                    if c_tree[1] == "TRIPLE":
                        if 30 < rand <= 70:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                    else:
                        if 25 < rand <= 75:
                            if expected + betting[0] > p_chips:
                                self.bet(p_chips)
                            else:
                                self.bet(expected + betting[0])
                        else:
                            self.bet(expected)
            elif tree[1] == "STRAIGHT":
                if 40 < bluffing <= 50:
                    
                    if expected + bluffing_list[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + bluffing_list[0])
                else:
                    if c_tree[1] == "STRAIGHT":
                        if 30 < rand <= 70:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                    else:
                        if 20 < rand <= 80:
                            if expected + betting[0] > p_chips:
                                self.bet(p_chips)
                            else:
                                self.bet(expected + betting[0])
                        else:
                            self.bet(expected)
            elif tree[1] == "FLUSH":
                if 40 < bluffing <= 50:
                    if expected + bluffing_list[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + bluffing_list[0])
                else:
                    if c_tree[1] == "FLUSH":
                        if 30 < rand <= 70:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                    else:
                        if 20 < rand <= 80:
                            if expected + betting[0] > p_chips:
                                self.bet(p_chips)
                            else:
                                self.bet(expected + betting[0])
                        else:
                            self.bet(expected)
            elif tree[1] == "FULL HOUSE":
                if 40 < bluffing <= 50:
                    if expected + bluffing_list[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + bluffing_list[0])
                else:
                    if c_tree[1] == "FULL HOUSE":
                        if 30 < rand <= 70:
                            self.bet(expected)
                        else:
                            if bet_state == 0:
                                self.bet(0)
                            else:
                                self.bet(-1)
                    else:
                        if 10 < rand <= 90:
                            if expected + betting[0] > p_chips:
                                self.bet(p_chips)
                            else:
                                self.bet(expected + betting[0])
                        else:
                            self.bet(expected)
            else:
                if 40 < bluffing <= 50:
                    if expected + bluffing_list[0] > p_chips:
                        self.bet(p_chips)
                    else:
                        self.bet(expected + bluffing_list[0])
                else:
                    if 10 < rand <= 90:
                        if expected + betting[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + betting[0])
                    else:
                        self.bet(expected)

        elif step == 4:
            if 40 < bluffing <= 50:
                if expected + bluffing_list[0] > p_chips:
                    self.bet(p_chips)
                else:
                    self.bet(expected + bluffing_list[0])
            else:
                if tree[1] == "STRAIGHT":
                    if P_c_tree == "P_Straight":
                        s_betting = [10, 20, 30, 50]
                        if 30 < rand < 70:
                            random.shuffle(s_betting)
                            if s_betting[0] > self.__chips:
                                s_betting[0] = self.__chips
                            if expected + s_betting[0] > p_chips:
                                self.bet(p_chips)
                            else:
                                self.bet(expected + s_betting[0])
                        else:
                            self.bet(expected)
                    else:
                        if 30 < rand <= 70:
                            if expected + betting[0] > p_chips:
                                self.bet(p_chips)
                            else:
                                self.bet(expected + betting[0])
                        else:
                            self.bet(expected)
                elif tree[1] == "FLUSH":
                    if P_c_tree == "P_Flush":
                        s_betting = [10, 20, 30, 50]
                        if 30 < rand < 70:
                            random.shuffle(s_betting)
                            if s_betting[0] > self.__chips:
                                s_betting[0] = self.__chips
                            if expected + s_betting[0] > p_chips:
                                self.bet(p_chips)
                            else:
                                self.bet(expected + s_betting[0])
                        else:
                            self.bet(expected)
                    else:
                        if 30 < rand <= 70:
                            if expected + betting[0] > p_chips:
                                self.bet(p_chips)
                            else:
                                self.bet(expected + betting[0])
                        else:
                            self.bet(expected)
                elif tree[1] in ("TWO PAIR", "TRIPLE", "FULL HOUSE", "STRAIGHT FLUSH", "ROYAL FLUSH"):
                    if 30 < rand <= 70:
                        if expected + betting[0] > p_chips:
                            self.bet(p_chips)
                        else:
                            self.bet(expected + betting[0])
                    else:
                        self.bet(expected)
                else:
                    if bet_state < 100:
                        self.bet(expected)
                    else:
                        if 25 < rand < 75:
                            self.bet(expected)
                        else:
                            self.bet(-1)

        elif step == 5:
            if 50 < bluffing <= 60:
                if expected + bluffing_list[0] > p_chips:
                    self.bet(p_chips)
                else:
                    self.bet(expected + bluffing_list[0])
            else:
                if tree[1] in ("TRIPLE", "STRAIGHT", "FLUSH", "FULL HOUSE", "STRAIGHT FLUSH", "ROYAL FLUSH"):
                    self.bet(expected)
                else:
                    if bet_state < 100:
                        self.bet(expected)
                    else:
                        if tree[1] == "TWO PAIR":
                            self.bet(expected)
                        if tree[1] == "ONE PAIR":
                            if 40 < rand < 60 or bet_state > 700:
                                self.bet(expected)
                            else:
                                self.bet(-1)
                        if tree[1] == "HIGH CARD":
                            if 45 < rand < 55 or bet_state > 700:
                                self.bet(expected)
                            else:
                                self.bet(-1)

        if self.__chips < 0:
            s.bet_state += self.__chips
            self.__chips = 0

        if s.bet_state < self.__betted:
            s.bet_state = self.__betted
            s.bet_turn = s.bet_turn + 1 if s.bet_turn + 1 <= s.max_player else 1

        self.get__thinked = True