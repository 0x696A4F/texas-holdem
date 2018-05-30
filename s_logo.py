import pygame
import constants as c
import buttons as b

def LOGO_SCREEN():
    c.SCREEN.fill(c.LOGO_GREEN)

    # 배경 오브젝트 그리기
    c.SCREEN.blit(c.TEXAS_LOGO, (275, -10))
    c.SCREEN.blit(c.CARD_IN_LOGO, (200, 370))
    c.SCREEN.blit(c.HAND_IN_LOGO, (c.HAND_X, c.HAND_Y))

    # 손 애니메이션
    if not c.HAND_BACK:  # 손 앞으로
        c.HAND_X -= 4
        c.HAND_Y -= 2
        if c.FIXED_HAND_X - c.HAND_X == 100:
            c.HAND_BACK = True
    else:  # 손 뒤로
        c.HAND_X += 2
        c.HAND_Y += 1
        if c.FIXED_HAND_X == c.HAND_X:
            c.HAND_BACK = False

    # 버튼 그리기
    b.b_select()
    b.b_developer()
    if b.b_select.motion:
        c.WHERE = "GAME_AI_HARD"
        b.b_select.reset
    if b.b_developer.motion:
        back_dark = pygame.Surface((c.GUIWIDTH, c.GUIHEIGHT))
        back_dark.fill(c.BLACK)
        back_dark.set_alpha(128)
        c.SCREEN.blit(back_dark, (0, 0))
        c.SCREEN.blit(c.D_SCROLL, (445, 100))
        b.b_scroll_ok()
        b.b_select.disabled = True
        b.b_developer.disabled = True
        if b.b_scroll_ok.motion:
            b.b_developer.motion = False
            b.b_scroll_ok.motion = False
            b.b_select.disabled = False
            b.b_developer.disabled = False