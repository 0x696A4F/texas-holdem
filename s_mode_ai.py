from class_card import *
from class_ai import *
from class_player import *

import random
import pygame
import constants as c
import buttons as b
import sendmsg as sm

c_cards = []
p1_hand = []
p2_hand = []
small_blind = 0
p_list = [0, player(1, 1000), ai(2, 1000, "HARD")] # 플레이어 리스트
max_player = 2 # 최대 플레이어
divided = False # 카드를 배분했는지
continued = False # 게임을 계속 하는지
race_step = 0
bet_turn = 0
count_turn = 0
bet_state = 0
stake_chips = 0
will_bet = 0
selected_chip = 0
def fresh_deck(mode):
    global c_cards, p1_hand, p2_hand
    new = []
    p1 = []
    p2 = []
    suits = ["SPADE", "HEART", "DIAMOND", "CLUB"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

    for i in range(len(suits)):
        for j in range(len(ranks)):
            new.append((suits[i], ranks[j]))
    random.shuffle(new)

    # 플레이어에게 배분
    for i in range(2):
        for j in range(max_player):
            give = (small_blind + (i*2 + j)) % max_player
            if give == 0:
                give = max_player
            p_list[give].give_card(card(new[i*2 + j], give, i+1, mode))
            if give == 1:
                p1.append(new[i*2 + j])
            if give == 2:
                p2.append(new[i*2 + j])
    for i in range(2):
        p1_hand.append(list(p1[i]))
        p2_hand.append(list(p2[i]))
    p1_hand = str_to_int(p1_hand)
    p2_hand = str_to_int(p2_hand)

    # 커뮤니티 카드
    for i in range(max_player*2 + 1, max_player*2 + 6):
        c_cards.append(card(new[i], "COMMUNITY", i - (max_player * 2), mode))

def div_animation():
    i = small_blind
    card_index = 0
    count = 0
    while count <= max_player * 2: # divide player card
        if p_list[i].get_card(card_index).get_moved:
            p_list[i].get_card(card_index).show()
            i += 1
            if i > max_player:
                i = 1
        else:
            c_cards[0].show() # 커뮤니티 카드 한장 깔아 놓기
            p_list[i].get_card(card_index).show(True)
            break
        count += 1
        if count == max_player + 1:
            card_index = 1
            i = small_blind

    if count == max_player * 2 + 1: # divide community card
        for i in range(5):
            if c_cards[i].get_moved:
                c_cards[i].show()
                if i == 4:
                    global divided
                    divided = True
            else:
                if not i == 4:
                    c_cards[4].show()
                c_cards[i].show(True)
                break

def change_chip():
    global selected_chip
    check = 0
    for i in range(4):
        if selected_chip != b.b_chip[i][1] and b.b_chip[i][0].motion:
            selected_chip = b.b_chip[i][1]
            for j in range(4):
                if not i == j:
                    b.b_chip[j][0].motion = False
        if not b.b_chip[i][0].motion:
            check += 1

    if check == 4:
        selected_chip = 0

def count_chip(multiple):
    global will_bet
    for i in range(3):
        if b.b_plus[i][0].motion:
            will_bet += b.b_plus[i][1] * multiple
            if will_bet > p_list[1].get_chips:
                will_bet = p_list[1].get_chips
            if will_bet > bet_state - p_list[1].get_betted + p_list[2].get_chips:
                will_bet = bet_state - p_list[1].get_betted + p_list[2].get_chips
            b.b_plus[i][0].motion = False
        elif b.b_minus[i][0].motion:
            will_bet -= b.b_minus[i][1] * multiple
            if will_bet < 0:
                will_bet = 0
            b.b_minus[i][0].motion = False

def str_to_int(card_list):  # 카드순위를 계산하기 쉽게 문양도 숫자로 변환
    for card in card_list:
        if card[0] == "SPADE":
            card[0] = 0
        elif card[0] == "HEART":
            card[0] = 1
        elif card[0] == "DIAMOND":
            card[0] = 2
        elif card[0] == "CLUB":
            card[0] = 3
        if card[1] == "A":  # ACE가 가장 높은 카드이므로 14로 배정
            card[1] = 14
        elif card[1] == "K":
            card[1] = 13
        elif card[1] == "Q":
            card[1] = 12
        elif card[1] == "J":
            card[1] = 11
        else:
            card[1] = int(card[1])
    return card_list

def get_rank(card_list):
    hand = sorted(card_list)
    rank_list = []
    for x in hand:
        rank_list.append(x[1])
    rank_list.sort()
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

    rank_name = "HIGH CARD"
    rank = 173 - max(rank_list)

    Four_card = False
    Full_House = False

    Four_card_number = 0
    Triple_list = []
    Pair_list = []

    for x in range(15, 1, -1):
        if rank_list.count(x) == 4:    # 같은 숫자가 4개
            Four_card_number = x
        if rank_list.count(x) == 3:    # 같은 숫자가 3개 (2개 이상일 수 있으므로 리스트)
            Triple_list.append(x)
        if rank_list.count(x) == 2:    # 같은 숫자가 2개 (2개 이상일 수 있으므로 리스트)
            Pair_list.append(x)

    if Four_card_number > 0:
        Four_card = True
        rank = 25 - Four_card_number
        rank_name = "FOUR CARD"

    elif Triple_list != []:
        if Pair_list != []:             # Full House
            Full_House = True
            rank = 38 - Triple_list[0]
            rank_name = "FULL HOUSE"
        else:
            rank = 69 - Triple_list[0]
            rank_name = "TRIPLE"

    elif Pair_list != []:
        if len(Pair_list) >= 2:
            rank_name = "TWO PAIR"
            if Pair_list[0] == 14:
                rank = 81 - Pair_list[1]
            elif Pair_list[0] == 13:
                rank = 92 - Pair_list[1]
            elif Pair_list[0] == 12:
                rank = 102 - Pair_list[1]
            elif Pair_list[0] == 11:
                rank = 111 - Pair_list[1]
            elif Pair_list[0] == 10:
                rank = 119 - Pair_list[1]
            elif Pair_list[0] == 9:
                rank = 126 - Pair_list[1]
            elif Pair_list[0] == 8:
                rank = 132 - Pair_list[1]
            elif Pair_list[0] == 7:
                rank = 137 - Pair_list[1]
            elif Pair_list[0] == 6:
                rank = 141 - Pair_list[1]
            elif Pair_list[0] == 5:
                rank = 144 - Pair_list[1]
            elif Pair_list[0] == 4:
                rank = 146 - Pair_list[1]
            elif Pair_list[0] == 3:
                rank = 145
        elif len(Pair_list) == 1:
            if rank > 146:
                rank = 160 - Pair_list[0]
                rank_name = "ONE PAIR"
    for x in range(0, len(hand) -1):
        if rank_list[len(hand)-1-x] == rank_list[len(hand)-2-x]:
                    del rank_list[len(hand)-1-x]

    if len(rank_list) >= 5:
        Straight = False
        top_number = 0
        for i in range(len(rank_list)-4):
            if rank_list[i+1]-rank_list[i] == 1 and \
                rank_list[i+2]-rank_list[i+1] == 1 and \
                rank_list[i+3]-rank_list[i+2] == 1 and \
                rank_list[i+4]-rank_list[i+3] == 1:
                Straight = True
                top_number = rank_list[i+4]
        if Straight:
            if top_number == 14:
                rank = 45
                rank_name = "STRAIGHT"
            else:
                rank = 59 - top_number
                rank_name = "STRAIGHT"
        if 2 in rank_list and 3 in rank_list and \
            4 in rank_list and 5 in rank_list and \
            14 in rank_list:                          # A 2 3 4 5 스트레이트는 숫자상으로 2 3 4 5 14 이므로 이렇게 표현
            rank = 54
            rank_name = "STRAIGHT"

    suit_list = []
    for x in hand:
        suit_list.append(x[0])

    if Four_card or Full_House:                # Flush보다 높은 족보
        pass
    else:
        Flush = False
        num = []
        if suit_list.count(0) >= 5:
            Flush = True
            pattern_num = 0
            for x in range(0, len(hand)):                     # 문양이 다른 카드는 삭제한다.
                if suit_list[len(hand)-1-x] != pattern_num:
                    del hand[len(hand)-1-x]
            for x in hand:
                num.append(x[1])
            rank = 51 - max(num)
            rank_name = "FLUSH"
        elif suit_list.count(1) >= 5:
            Flush = True
            pattern_num = 1
            for x in range(0, len(hand)):
                if suit_list[len(hand) - 1 - x] != pattern_num:
                    del hand[len(hand) - 1 - x]
            for x in hand:
                num.append(x[1])
            rank = 51 - max(num)
            rank_name = "FLUSH"
        elif suit_list.count(2) >= 5:
            Flush = True
            pattern_num = 2
            for x in range(0, len(hand)):
                if suit_list[len(hand) - 1 - x] != pattern_num:
                    del hand[len(hand) - 1 - x]
            for x in hand:
                num.append(x[1])
            rank = 51 - max(num)
            rank_name = "FLUSH"
        elif suit_list.count(3) >= 5:
            Flush = True
            pattern_num = 3
            for x in range(0, len(hand)):
                if suit_list[len(hand) - 1 - x] != pattern_num:
                    del hand[len(hand) - 1 - x]
            for x in hand:
                num.append(x[1])
            rank = 51 - max(num)
            rank_name = "FLUSH"
        num_len = len(num)
        if Flush:
            for x in range(0, num_len - 1):
                if num[num_len - 1 - x] == num[num_len - 2 - x]:
                    del num[num_len - 1 - x]
            num.sort()
            if len(num) >= 5:
                if num[1]-num[0] == 1 and \
                    num[2]-num[1] == 1 and \
                    num[3]-num[2] == 1 and \
                    num[4]-num[3] == 1:
                    if max(num) == 14:
                        rank = 1
                        rank_name = "ROYAL FLUSH"
                    else:
                        rank = 15 - max(num)
                        rank_name = "STRAIGHT FLUSH"
                if num == [2, 3, 4, 5, 14]:
                    rank = 10
                    rank_name = "STRAIGHT FLUSH"

    return (rank, rank_name)


def get_potential_rank(card_list):
    hand = sorted(card_list)
    rank_list = []
    for x in hand:
        rank_list.append(x[1])
    rank_list.sort()  # 숫자만을 오름차순으로 정렬

    rank_name = "High_Card"

    if (2 in rank_list and 3 in rank_list and 4 in rank_list and 5 in rank_list) or \
            (3 in rank_list and 4 in rank_list and 5 in rank_list and 6 in rank_list) or \
            (4 in rank_list and 5 in rank_list and 6 in rank_list and 7 in rank_list) or \
            (5 in rank_list and 6 in rank_list and 7 in rank_list and 8 in rank_list) or \
            (6 in rank_list and 7 in rank_list and 8 in rank_list and 9 in rank_list) or \
            (7 in rank_list and 8 in rank_list and 9 in rank_list and 10 in rank_list) or \
            (8 in rank_list and 9 in rank_list and 10 in rank_list and 11 in rank_list) or \
            (9 in rank_list and 10 in rank_list and 11 in rank_list and 12 in rank_list) or \
            (10 in rank_list and 11 in rank_list and 12 in rank_list and 13 in rank_list) or \
            (11 in rank_list and 12 in rank_list and 14 in rank_list and 14 in rank_list) or \
            (14 in rank_list and 2 in rank_list and 3 in rank_list and 4 in rank_list) or \
            (2 in rank_list and 4 in rank_list and 5 in rank_list and 6 in rank_list) or \
            (3 in rank_list and 5 in rank_list and 6 in rank_list and 7 in rank_list) or \
            (4 in rank_list and 6 in rank_list and 7 in rank_list and 8 in rank_list) or \
            (5 in rank_list and 7 in rank_list and 8 in rank_list and 9 in rank_list) or \
            (6 in rank_list and 8 in rank_list and 9 in rank_list and 10 in rank_list) or \
            (7 in rank_list and 9 in rank_list and 10 in rank_list and 11 in rank_list) or \
            (8 in rank_list and 10 in rank_list and 11 in rank_list and 12 in rank_list) or \
            (9 in rank_list and 11 in rank_list and 12 in rank_list and 13 in rank_list) or \
            (10 in rank_list and 12 in rank_list and 13 in rank_list and 14 in rank_list) or \
            (14 in rank_list and 3 in rank_list and 4 in rank_list and 5 in rank_list) or \
            (2 in rank_list and 3 in rank_list and 5 in rank_list and 6 in rank_list) or \
            (3 in rank_list and 4 in rank_list and 6 in rank_list and 7 in rank_list) or \
            (4 in rank_list and 5 in rank_list and 7 in rank_list and 8 in rank_list) or \
            (5 in rank_list and 6 in rank_list and 8 in rank_list and 9 in rank_list) or \
            (6 in rank_list and 7 in rank_list and 9 in rank_list and 10 in rank_list) or \
            (7 in rank_list and 8 in rank_list and 10 in rank_list and 11 in rank_list) or \
            (8 in rank_list and 9 in rank_list and 11 in rank_list and 12 in rank_list) or \
            (9 in rank_list and 10 in rank_list and 12 in rank_list and 13 in rank_list) or \
            (10 in rank_list and 11 in rank_list and 13 in rank_list and 14 in rank_list) or \
            (14 in rank_list and 2 in rank_list and 4 in rank_list and 5 in rank_list) or \
            (2 in rank_list and 3 in rank_list and 4 in rank_list and 6 in rank_list) or \
            (3 in rank_list and 4 in rank_list and 5 in rank_list and 7 in rank_list) or \
            (4 in rank_list and 5 in rank_list and 6 in rank_list and 8 in rank_list) or \
            (5 in rank_list and 6 in rank_list and 7 in rank_list and 9 in rank_list) or \
            (6 in rank_list and 7 in rank_list and 8 in rank_list and 10 in rank_list) or \
            (7 in rank_list and 8 in rank_list and 9 in rank_list and 11 in rank_list) or \
            (8 in rank_list and 9 in rank_list and 10 in rank_list and 12 in rank_list) or \
            (9 in rank_list and 10 in rank_list and 11 in rank_list and 13 in rank_list) or \
            (10 in rank_list and 11 in rank_list and 12 in rank_list and 14 in rank_list) or \
            (14 in rank_list and 2 in rank_list and 3 in rank_list and 5 in rank_list):
        rank_name = "P_Straight"

        suit_list = []
        for x in hand:
            suit_list.append(x[0])  # 문양만 추가
        for i in range(4):
            if suit_list.count(i) == 4:
                rank_name = "P_Flush"

    return rank_name

def GAME_AI_SCREEN(mode):
    global p_list, stake_chips, bet_state, race_step, bet_turn, count_turn, small_blind, will_bet, p1_hand, p2_hand, c_cards, divided, selected_chip, continued
    if mode == "EASY":
        c.SCREEN.blit(c.AI_EASY_BACK, (0, 0))
    elif mode == "NORMAL":
        pass
    elif mode == "HARD":
        pass

    if race_step == 0:
        if not c_cards:  # 덱이 비었을때
            bet_turn = 0
            count_turn = 0
            bet_state = 0
            stake_chips = 0
            will_bet = 0
            selected_chip = 0
            divided = False
            for i in range(1, max_player+1):
                p_list[i].card_reset
                p_list[i].reset_think
                p_list[i].reset_betted
                p_list[i].reset_folded
            fresh_deck(mode)
        if small_blind == 0: # 처음 게임시작 하는경우
            small_blind = random.randint(1,2) # 재시작인 경우 재시작하기전에 조정
            bet_turn = small_blind+2 if small_blind+2 <= max_player else small_blind+2-max_player
        elif not c.MSG_ACTIVE:
            small_blind += 1
            if small_blind > max_player: small_blind = 1
            bet_turn = small_blind
        # 카드 순서대로 보여주기
        for i in range(5):
            c_cards[i].show()
        show_player = small_blind
        for i in range(2):
            for _ in range(max_player * 2):
                p_list[show_player].get_card(i).show()
                show_player += 1
                if show_player > max_player:
                    show_player = 1
        if continued:
            if p_list[small_blind].get_chips < 25: #SB 지불비용 X일시
                text = ("당신이 " if small_blind == 2 else "컴퓨터가 ") + "이겼습니다. 처음부터 다시 시작하겠습니까?"
                ask = sm.YesNo(text)
                if ask == "YES":
                    race_step = 0
                    small_blind = 0
                    p_list[1].set_chips(1000)
                    p_list[2].set_chips(1000)
                    continued = False
                elif ask == "NO":
                    c.WHERE = "LOGO"
                    p_list[1].set_chips(1000)
                    p_list[2].set_chips(1000)
                    continued = False
            elif p_list[2 if small_blind == 1 else 1].get_chips < 50: # 빅블 지불비용 X일시
                text = ("당신이 " if small_blind == 1 else "컴퓨터가 ") + "이겼습니다. 처음부터 다시 시작하겠습니까?"
                ask = sm.YesNo(text)
                if ask == "YES":
                    race_step = 0
                    small_blind = 0
                    p_list[1].set_chips(1000)
                    p_list[2].set_chips(1000)
                    continued = False
                elif ask == "NO":
                    c.WHERE = "LOGO"
                    p_list[1].set_chips(1000)
                    p_list[2].set_chips(1000)
                    continued = False
            else:
                race_step = 1
                p_list[small_blind].bet(25)
                p_list[small_blind + 1 if small_blind + 1 <= max_player else 1].bet(50)
                # count_turn += 2 #2인용 초과할때
                bet_state = 50
        else:
            start = sm.YesNo(mode + " 난이도의 게임을 시작하시겠습니까?")
            if start == "YES":
                race_step = 1
                p_list[small_blind].bet(25)
                p_list[small_blind + 1 if small_blind + 1 <= max_player else 1].bet(50)
                #count_turn += 2 #2인용 초과할때
                bet_state = 50
            elif start == "NO":
                c.WHERE = "LOGO"
    elif race_step == 1 and not divided:
        div_animation()
    else:
        opened = False
        check = 0 # 앞면 개수
        if not p_list[1].get_opened: # 나의 카드가 오픈이 안되어 있다면
            p_list[1].card_open
            for i in range(2, max_player+1):
                p_list[i].card_show
            for i in range(5):
                c_cards[i].show()
        else:
            for i in range(1, max_player+1):
                if not (p_list[1].get_folded or p_list[2].get_folded or p_list[i].get_opened) and race_step == 5:
                    p_list[i].card_open
                else:
                    p_list[i].card_show
                if p_list[i].get_opened:
                    check += 2
                if p_list[i].get_folded:
                    p_1 = p_list[i].get_card(0).get_pos
                    p_2 = p_list[i].get_card(1).get_pos
                    f_pos = (int((p_1[0] + p_2[0] - c.PLAYER_FOLD.get_width()) / 2 + 56),
                             int((p_1[1] + p_2[1] - c.PLAYER_FOLD.get_height()) / 2 + 74))
                    c.SCREEN.blit(c.PLAYER_FOLD, f_pos)
            for i in range(5):
                if 1 < race_step and i <= race_step:
                    c_cards[i].show(False,True)
                else:
                    c_cards[i].show()
                if c_cards[i].get_faced:
                    check += 1

        if race_step < 5 and check == 2 + (0 if race_step == 1 else race_step+1): # 스텝5이하이고 애니메이션 처리완료되면
            opened = True
            
        if race_step == 5: # 승패 처리 (2인용으로 우선제작)
            if p_list[1].get_folded:
                play_more = sm.YesNo("컴퓨터가 <" + str(stake_chips) + "> 를 가져갑니다. 더 하시겠습니까?")
                if play_more == "YES":
                    p_list[2].give_chips(stake_chips)
                    c_cards = []
                    p1_hand = []
                    p2_hand = []
                    race_step = 0
                    continued = True
                    p_list[1].card_reset
                    p_list[2].card_reset
                elif play_more == "NO":
                    c.WHERE = "LOGO"
            elif p_list[2].get_folded:
                play_more = sm.YesNo("당신이 <" + str(stake_chips) + "> 를 가져갑니다. 더 하시겠습니까?")
                if play_more == "YES":
                    p_list[1].give_chips(stake_chips)
                    c_cards = []
                    p1_hand = []
                    p2_hand = []
                    race_step = 0
                    continued = True
                    p_list[1].card_reset
                    p_list[2].card_reset
                elif play_more == "NO":
                    c.WHERE = "LOGO"
            else: # 모두 폴드 X
                rankFont = pygame.font.Font(c.FONT_TYPE, 50)
                p1_rank = rankFont.render(p_list[1].my_rank(c_cards)[1], True, (255, 31, 31))
                p2_rank = rankFont.render(p_list[2].my_rank(c_cards)[1], True, (255, 31, 31))
                c.SCREEN.blit(p1_rank, (550, 630))
                c.SCREEN.blit(p2_rank, (370, 120))
                if p_list[1].my_rank(c_cards)[0] < p_list[2].my_rank(c_cards)[0]:
                    play_more = sm.YesNo("당신이 <" + str(stake_chips) + "> 를 가져갑니다. 더 하시겠습니까?")
                elif p_list[1].my_rank(c_cards)[0] > p_list[2].my_rank(c_cards)[0]:
                    play_more = sm.YesNo("컴퓨터가 <" + str(stake_chips) + "> 를 가져갑니다. 더 하시겠습니까?")
                elif p_list[1].my_rank(c_cards)[0] == p_list[2].my_rank(c_cards)[0]:
                    p1_hand.sort(key=lambda x:x[1])
                    p2_hand.sort(key=lambda x:x[1])
                    if p1_hand[1][1] > p2_hand[1][1]:
                        play_more = sm.YesNo("당신이 <" + str(stake_chips) + "> 를 가져갑니다. 더 하시겠습니까?")
                    elif p1_hand[1][1] < p2_hand[1][1]:
                        play_more = sm.YesNo("컴퓨터가 <" + str(stake_chips) + "> 를 가져갑니다. 더 하시겠습니까?")
                    elif p1_hand[1][1] == p2_hand[1][1]:
                        if p1_hand[0][1] > p2_hand[0][1]:
                            play_more = sm.YesNo("당신이 <" + str(stake_chips) + "> 를 가져갑니다. 더 하시겠습니까?")
                        elif p1_hand[0][1] < p2_hand[0][1]:
                            play_more = sm.YesNo("컴퓨터가 <" + str(stake_chips) + "> 를 가져갑니다. 더 하시겠습니까?")
                        elif p1_hand[0][1] == p2_hand[0][1]:
                            if p1_hand[1][0] < p2_hand[1][0]:
                                play_more = sm.YesNo("당신이 <" + str(stake_chips) + "> 를 가져갑니다. 더 하시겠습니까?")
                            elif p1_hand[1][0] > p2_hand[1][0]:
                                play_more = sm.YesNo("컴퓨터가 <" + str(stake_chips) + "> 를 가져갑니다. 더 하시겠습니까?")
                if play_more == "YES":
                    if p_list[1].my_rank(c_cards)[0] < p_list[2].my_rank(c_cards)[0]:
                        p_list[1].give_chips(stake_chips)
                    elif p_list[1].my_rank(c_cards)[0] > p_list[2].my_rank(c_cards)[0]:
                        p_list[2].give_chips(stake_chips)
                    elif p_list[1].my_rank(c_cards)[0] == p_list[2].my_rank(c_cards)[0]:
                        p1_hand.sort(key=lambda x: x[1])
                        p2_hand.sort(key=lambda x: x[1])
                        if p1_hand[1][1] > p2_hand[1][1]:
                            p_list[1].give_chips(stake_chips)
                        elif p1_hand[1][1] < p2_hand[1][1]:
                            p_list[2].give_chips(stake_chips)
                        elif p1_hand[1][1] == p2_hand[1][1]:
                            if p1_hand[0][1] > p2_hand[0][1]:
                                p_list[1].give_chips(stake_chips)
                            elif p1_hand[0][1] < p2_hand[0][1]:
                                p_list[2].give_chips(stake_chips)
                            elif p1_hand[0][1] == p2_hand[0][1]:
                                if p1_hand[1][0] < p2_hand[1][0]:
                                    p_list[1].give_chips(stake_chips)
                                elif p1_hand[1][0] > p2_hand[1][0]:
                                    p_list[2].give_chips(stake_chips)
                    c_cards = []
                    p1_hand = []
                    p2_hand = []
                    race_step = 0
                    continued = True
                    p_list[1].card_reset
                    p_list[2].card_reset
                elif play_more == "NO":
                    c.WHERE = "LOGO"

        if opened:
            betted = [0] + [p_list[i].get_betted for i in range(1, max_player + 1)]
            if bet_turn == 1 and p_list[1].get_thinked:
                count_turn += 1
                bet_turn += 1
            elif bet_turn == 1 and not p_list[1].get_folded: # 나의 턴일때
                for i in range(4): # 칩생성
                    b.b_chip[i][0]()
                    if c.MSG_ACTIVE:
                        b.b_chip[i][0].disabled = True
                    else:
                        b.b_chip[i][0].disabled = False
                b.b_bet()
                b.b_fold()
                if c.MSG_ACTIVE:
                    b.b_bet.disabled = b.b_fold.disabled = True
                else:
                    b.b_bet.disabled = b.b_fold.disabled = False
                change_chip()
                if selected_chip:
                    for i in range(3): # 버튼 생성
                        b.b_plus[i][0]()
                        b.b_minus[i][0]()
                        if c.MSG_ACTIVE:
                            b.b_plus[i][0].disabled = b.b_minus[i][0].disabled = True
                        else:
                            b.b_plus[i][0].disabled = b.b_minus[i][0].disabled = False
                count_chip(selected_chip)
            elif bet_turn == 2: # AI THINKING
                if (betted[2] == bet_state and p_list[2].get_thinked) or p_list[2].get_folded:
                    count_turn += 1
                    bet_turn = bet_turn + 1 if bet_turn + 1 <= max_player else 1
                elif not p_list[bet_turn].get_thinking or (betted[2] != bet_state and p_list[2].get_thinked):
                    p_list[2].think(c_cards, race_step, bet_state, p_list[1].get_chips)

            rFont = pygame.font.Font(c.FONT_TYPE, 50)
            now_round = rFont.render("<" + mode + " ROUND " + str(race_step) + ">", True, (255,31,31))
            c.SCREEN.blit(now_round, (30,30))
            if bet_turn == 1:
                my_bet_state = c.FONT.render("누적:" + str(betted[1]) + " / 예정:" + str(will_bet) + "  보유량:" + str(p_list[1].get_chips), True, (0,0,0))
            else:
                my_bet_state = c.FONT.render("누적:" + str(betted[1]) + "  보유량:" + str(p_list[1].get_chips), True, (0,0,0))
            c.SCREEN.blit(my_bet_state, (130,748))
            ai_bet_state = c.FONT.render("누적:" + str(betted[2]) + "  보유량:" + str(p_list[2].get_chips), True, (0,0,0))
            c.SCREEN.blit(ai_bet_state, (874,25))
            stake_text = c.FONT.render("총 누적된 칩", True, (0,0,0))
            stake_chips_state = c.FONT.render(str(stake_chips), True, (0,0,0))
            c.SCREEN.blit(stake_text, (940, 345))
            c.SCREEN.blit(stake_chips_state, (940, 385))

            if b.b_bet.motion:
                if will_bet == 0:
                    if bet_state == 0:
                        msg = "체크 하시겠습니까?"
                    else:
                        msg = "<" + str(bet_state - betted[1]) + "> 내고 콜 하시겠습니까?"
                else:
                    if will_bet + betted[1] <= bet_state:
                        msg = "<" + str(bet_state - betted[1]) + "> 내고 콜 하시겠습니까?"
                    else:
                        if bet_state > 0:
                            msg = "<" + str(bet_state - betted[1]) + "> 내고 <"+\
                                  str(will_bet + betted[1] - bet_state) +"> 레이즈 하시겠습니까?"
                        else:
                            msg = "<" + str(will_bet) + "> 베팅 하시겠습니까?"
                motion = sm.YesNo(msg)
                if motion == "YES":
                    p_list[1].bet(bet_state - betted[1] if will_bet+betted[1] <= bet_state else will_bet)
                    bet_state += 0 if will_bet+betted[1] <= bet_state else betted[1]+will_bet-bet_state
                    bet_turn = bet_turn+1 if bet_turn+1 <= max_player else 1
                    count_turn += 1
                    b.b_bet.reset
                elif motion == "NO":
                    b.b_bet.reset
            betted = [0] + [p_list[i].get_betted for i in range(1, max_player + 1)]
            if count_turn == max_player: # 턴이 한번씩 다 돌았을 때
                bet_check = 0
                fold_check = 0
                collect_betted = 0
                for i in range(1,max_player+1): # 베팅상황 체크
                    if (betted[i] == bet_state and p_list[i].get_thinked) or p_list[i].get_folded:
                        bet_check += 1
                        collect_betted += betted[i]
                        if p_list[i].get_folded:
                            fold_check += 1
                    elif betted[i] != bet_state:
                        p_list[i].reset_think
                if bet_check == max_player: # 모두 콜하거나 폴드 되었다면
                    stake_chips += collect_betted
                    if fold_check == max_player - 1: # 한명빼고 나머지가 모두 폴드 했을 때
                        race_step = 5
                    else:
                        race_step += 1
                        bet_state = 0
                        will_bet = 0
                        p_list[1].reset_betted
                        p_list[1].reset_think
                        p_list[2].reset_betted
                        p_list[2].reset_think # AI 재설정
                bet_turn = small_blind
                will_bet = 0
                count_turn = 0

            if b.b_fold.motion:
                motion = sm.YesNo("정말로 폴드 하시겠습니까?")
                if motion == "YES":
                    p_list[1].bet(-1)
                    b.b_fold.reset
                elif motion == "NO":
                    b.b_fold.reset