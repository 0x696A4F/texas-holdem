from pygame.locals import *
from s_logo import *
from s_selectmode import *
from s_mode_ai import *

import pygame
import constants as c


def FILL():
    pygame.display.set_caption(c.GUITITLE)
    clock = pygame.time.Clock()
    while True:
        c.SCREEN.fill(c.WHITE)
        c.MOUSE_POS = pygame.mouse.get_pos()
        if c.WHERE == "LOGO":
            LOGO_SCREEN()
        elif c.WHERE == "MODE":
            MODE_SCREEN()
        elif c.WHERE == "GAME_AI_HARD":
            GAME_AI_SCREEN("HARD")
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit(0)
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    c.MOUSE_CLICKED = True
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    c.MOUSE_CLICKED = False
        pygame.display.flip()
        clock.tick(60) # FPS 60