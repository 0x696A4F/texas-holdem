from class_card import *
from class_ai import *
from class_player import *

import random
import pygame
import constants as c
import buttons as b
import sendmsg as sm

c_cards = []
small_blind = 0
p_list = [0, player(1,300), ai(2,300,"EASY")]
max_player = len(p_list) - 1
divided = False
race_step = 0
bet_state = 50
my_bet = 25
com_bet = 50
now_bet = 0
selected_chip = 0
def fresh_deck(mode):
    global c_cards
    new = []
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
    global now_bet
    for i in range(3):
        if b.b_plus[i][0].motion:
            now_bet += b.b_plus[i][1] * multiple
            if now_bet > p_list[1].get_chips:
                now_bet = p_list[1].get_chips
            b.b_plus[i][0].motion = False
        elif b.b_minus[i][0].motion:
            now_bet -= b.b_minus[i][1] * multiple
            if now_bet < 0:
                now_bet = 0
            b.b_minus[i][0].motion = False


def GAME_AI_SCREEN(mode):
    global race_step, small_blind
    if mode == "EASY":
        c.SCREEN.blit(c.AI_EASY_BACK, (0,0))
    elif mode == "NORMAL":
        pass
    elif mode == "HARD":
        pass

    if not c_cards: # 덱이 비었을때
        fresh_deck(mode)

    if race_step == 0:
        if small_blind == 0: # 처음 게임시작 하는경우
            small_blind = random.randint(1,2) # 재시작인 경우 재시작하기전에 조정
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
        start = sm.YesNo("게임을 시작하시겠습니까?")
        if start == "YES":
            race_step = 1
    elif race_step == 1 and not divided:
        div_animation()
    else:
        opened = False
        check = 0 # 앞면 개수
        if not p_list[1].get_opened:
            p_list[1].card_open
            for i in range(2, max_player+1):
                p_list[i].card_show
            for i in range(5):
                c_cards[i].show()
        else:
            for i in range(1, max_player+1):
                p_list[i].card_show
                if p_list[i].get_opened:
                    check += 2
            for i in range(5):
                if race_step > 1 and i < 5-race_step:
                    c_cards[i].show(False,True)
                else:
                    c_cards[i].show()
                if c_cards[i].get_faced:
                    check += 1

        if check == 2 + (0 if race_step == 1 else race_step+1):
            opened = True

        if opened:
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
            my_bet_state = c.FONT.render(str(my_bet) + "/" + str(now_bet), True, (0,0,0))
            c.SCREEN.blit(my_bet_state, (439,705))
            ai_bet_state = c.FONT.render(str(com_bet), True, (0,0,0))
            c.SCREEN.blit(ai_bet_state, (750,85))

            if b.b_bet.motion:
                if now_bet == 0:
                    if bet_state == 0:
                        msg = "체크 하시겠습니까?"
                    else:
                        msg = "<" + str(bet_state - my_bet) + "> 콜 하시겠습니까?"
                else:
                    if now_bet + my_bet <= bet_state:
                        msg = "<" + str(bet_state - my_bet) + "> 콜 하시겠습니까?"
                    else:
                        msg = "<" + str(bet_state - my_bet) + "> 내고 <" + str(now_bet + my_bet - bet_state) +"> 레이즈 하시겠습니까?"
                motion = sm.YesNo(msg)
                if motion == "YES":
                    me.bet(bet_state - my_bet + now_bet)
                    b.b_bet.reset
                elif motion == "NO":
                    b.b_bet.reset