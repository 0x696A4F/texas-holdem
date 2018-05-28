from class_button import *

import pygame
import constants as c

iYes = pygame.Surface((60,30))
iYes.fill((255,168,0))
iNo = pygame.Surface((60,30))
iNo.fill((255,168,0))
FONT = pygame.font.Font(c.FONT_TYPE, 20)
tYes = FONT.render("예", True, c.BLACK)
tNo = FONT.render("아니오", True, c.BLACK)
iYes.blit(tYes, (int((60-tYes.get_width())/2),4))
iNo.blit(tNo, (int((60-tNo.get_width())/2),4))
b_Yes = button((550, 430), iYes)
b_No = button((630, 430), iNo)

def YesNo(text):
    c.MSG_ACTIVE = True

    x,y = 400, 300
    back = pygame.Surface((c.GUIWIDTH,200))
    back.fill((92,92,92))
    back.set_alpha(210)

    textF = pygame.font.Font(c.FONT_TYPE, 50)
    text = textF.render(str(text), True, c.BLACK)

    c.SCREEN.blit(back, (0,y))
    c.SCREEN.blit(text, (int((c.GUIWIDTH - text.get_width())/2),y+50))
    b_Yes()
    b_No()
    if b_Yes.motion:
        b_Yes.reset
        c.MSG_ACTIVE = False
        return "YES"
    elif b_No.motion:
        b_No.reset
        c.MSG_ACTIVE = False
        return "NO"