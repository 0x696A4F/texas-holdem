from class_button import *

import constants as c

# button in logo
b_select = button((485, 600), c.SELECT_MODE, c.SELECT_MODE_O, c.SELECT_MODE_C)
b_developer = button((485,690), c.DEVELOPER, c.DEVELOPER_O, c.DEVELOPER_C)
b_scroll_ok = button((598,515), c.SCROLL_OK, c.SCROLL_OK_O, c.SCROLL_OK_C)

# button in select mode
b_mode_ai = button((178,116), c.MODE_AI, c.MODE_AI_O, c.MODE_AI_C)
b_ai_easy = button((178,542), c.AI_EASY, c.AI_EASY_O, c.AI_EASY_C)

# button about chips
b_chip = [[button((430,575), c.CHIP1, False, c.CHIP1_O),1], [button((485,575), c.CHIP2, False, c.CHIP2_O),5],
          [button((540,575), c.CHIP3, False, c.CHIP3_O),25], [button((595,575), c.CHIP4, False, c.CHIP4_O),100]]

b_plus = [[button((439,630), c.PLUS1),1], [button((509,630), c.PLUS5),5], [button((579,630), c.PLUS10),10]]
b_minus = [[button((439, 670), c.MINUS1),1], [button((509, 670), c.MINUS5),5], [button((579, 670), c.MINUS10),10]]

b_fold = button((660,630), c.FOLD, c.FOLD_O, c.FOLD_C)
b_bet = button((660,686), c.BET, c.BET_O, c.BET_C)