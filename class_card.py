import pygame
import constants as c


class card:
    def __init__(self, stat, owner, sequence, mode):
        self.__suit = stat[0]
        self.__rank = stat[1]
        self.__owner = owner
        self.__seq = sequence
        self.__mode = mode

        # default value
        self.__imgFront = pygame.image.load("img/cards/" + self.__suit.lower() + "/" + self.__rank + ".png")
        self.__imgBack = pygame.image.load("img/cards/back/" + self.__mode.lower() + ".png")
        self.__faced = False
        self.__facing = False
        self.__h_size = self.__imgBack.get_height()
        self.__w_size = self.__imgBack.get_width()
        self.__moved = False
        self.__pos = (974, 328)

    @property
    def get_card(self):
        return self.__suit, self.__rank

    @property
    def get_moved(self):
        return self.__moved

    @property
    def get_owner(self):
        return self.__owner

    @property
    def get_faced(self):
        return self.__faced

    @property
    def get_pos(self):
        return self.__pos

    @property
    def faced_up(self):
        if not self.__facing:
            self.__w_size -= 10
            if self.__w_size < 0:
                self.__w_size = 0
                self.__facing = True
            return pygame.transform.scale(self.__imgBack, (self.__w_size, self.__h_size))
        else:
            self.__w_size += 10
            if self.__w_size > 115:
                self.__w_size = 115
                self.__faced = True
            return pygame.transform.scale(self.__imgFront, (self.__w_size, self.__h_size))

    @property
    def scatter(self): # 카드 뿌려주는 함수
        if self.__owner == 1:
            pos_f = (130 + (151 * (self.__seq - 1)), 571)
        elif self.__owner == 2:
            pos_f = (1025 - (151 * (self.__seq - 1)), 85)
        else:
            pos_f = (130 + (151 * (self.__seq - 1)), 328)
        add_x, add_y = int((pos_f[0] - 974) / 8), int((pos_f[1] - 328) / 8) # 좌표 더해주는 값
        self.__pos = (self.__pos[0] + add_x, self.__pos[1] + add_y) # 좌표 조정
        under = lambda a, b: abs(self.__pos[a] - pos_f[a]) < abs(b)
        if under(0, add_x) or under(1, add_y):
            self.__pos = pos_f
            self.__moved = True

    def show(self, scatter=False, faced_up=False):
        if (self.__faced or self.__facing) and self.__moved: # 이동됐고, 앞면상태일 때
            if self.__facing:
                c.SCREEN.blit(self.faced_up, self.__pos)
            else:
                c.SCREEN.blit(self.__imgFront, self.__pos)
        else:
            if not self.__moved and scatter:
                self.scatter
            if faced_up:
                c.SCREEN.blit(self.faced_up, self.__pos)
            else:
                c.SCREEN.blit(self.__imgBack, self.__pos)