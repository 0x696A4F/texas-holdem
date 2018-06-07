import pygame


pygame.font.init()

# GUI
GUIWIDTH = 1280
GUIHEIGHT = 800
GUITITLE = "BSIK TEXAS HOLDEM"
SCREEN = pygame.display.set_mode((GUIWIDTH, GUIHEIGHT))

MOUSE_POS = (0,0)
MOUSE_CLICKED = False # 마우스 왼쪽버튼
MSG_ACTIVE = False

# FONT
FONT_TYPE = "font/NanumBarunGothicBold.ttf"
FONT = pygame.font.Font(FONT_TYPE, 36)

# COLOUR
WHITE = (255,255,255)
BLACK = (0,0,0)
LOGO_GREEN = (11,148,68)
EASY_COLOUR = (210,200,0)

# SCREEN WHERE
WHERE = "LOGO" # FIRST = LOGO

# LOGO
TEXAS_LOGO = pygame.image.load("img/logo/holdem_logo.png")
CARD_IN_LOGO = pygame.image.load("img/logo/card_in_logo.png")
HAND_IN_LOGO = pygame.image.load("img/logo/hand_in_logo.png")

SELECT_MODE = pygame.image.load("img/logo/button/select_mode.png")
SELECT_MODE_O = pygame.image.load("img/logo/button/select_mode_o.png")
SELECT_MODE_C = pygame.image.load("img/logo/button/select_mode_c.png")

DEVELOPER = pygame.image.load("img/logo/button/developer.png")
DEVELOPER_O = pygame.image.load("img/logo/button/developer_o.png")
DEVELOPER_C = pygame.image.load("img/logo/button/developer_c.png")

D_SCROLL = pygame.image.load("img/logo/scroll.png")
SCROLL_OK = pygame.image.load("img/logo/button/ok.png")
SCROLL_OK_O = pygame.image.load("img/logo/button/ok_o.png")
SCROLL_OK_C = pygame.image.load("img/logo/button/ok_c.png")

FIXED_HAND_X = 950
FIXED_HAND_Y = 400
HAND_X = 950
HAND_Y = 400
HAND_BACK = False

# SELECT MODE
MODE_BACK = pygame.image.load("img/mode/back.png")

MODE_AI = pygame.image.load("img/mode/button/mode_ai.png")
MODE_AI_O = pygame.image.load("img/mode/button/mode_ai_o.png")
MODE_AI_C = pygame.image.load("img/mode/button/mode_ai_c.png")

AI_EASY = pygame.image.load("img/mode/button/ai_easy/easy.png")
AI_EASY_O = pygame.image.load("img/mode/button/ai_easy/easy_o.png")
AI_EASY_C = pygame.image.load("img/mode/button/ai_easy/easy_c.png")

# CHIPS
CHIP1 = pygame.image.load("img/chips/1.png")
CHIP1_O = pygame.image.load("img/chips/1_o.png")
CHIP2 = pygame.image.load("img/chips/2.png")
CHIP2_O = pygame.image.load("img/chips/2_o.png")
CHIP3 = pygame.image.load("img/chips/3.png")
CHIP3_O = pygame.image.load("img/chips/3_o.png")
CHIP4 = pygame.image.load("img/chips/4.png")
CHIP4_O = pygame.image.load("img/chips/4_o.png")

PLUS1 = pygame.image.load("img/chips/add/1.png")
PLUS5 = pygame.image.load("img/chips/add/5.png")
PLUS10 = pygame.image.load("img/chips/add/10.png")
MINUS1 = pygame.image.load("img/chips/minus/1.png")
MINUS5 = pygame.image.load("img/chips/minus/5.png")
MINUS10 = pygame.image.load("img/chips/minus/10.png")

BET = pygame.image.load("img/chips/motion/bet.png")
BET_O = pygame.image.load("img/chips/motion/bet_o.png")
BET_C = pygame.image.load("img/chips/motion/bet_c.png")
FOLD = pygame.image.load("img/chips/motion/fold.png")
FOLD_O = pygame.image.load("img/chips/motion/fold_o.png")
FOLD_C = pygame.image.load("img/chips/motion/fold_c.png")

# RESULTS
PLAYER_FOLD = pygame.image.load("img/results/fold.png")

# MODE_AI
AI_EASY_BACK = pygame.image.load("img/ai/easy/back.png")