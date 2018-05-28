import constants as c


class button:
    def __init__(self, xy, iNormal, iOver=False, iClick=False):
        self.x = xy[0]
        self.y = xy[1]
        self.iNormal = iNormal
        self.iOver = iOver
        self.iClick = iClick

        # 기본값 설정
        self.iWidth = iNormal.get_width()
        self.iHeight = iNormal.get_height()
        self.clicked = False
        self.motion = False
        self.disabled = False

    @property
    def reset(self):
        self.clicked = False
        self.motion = False
        self.disabled = False

    @property
    def on_button(self):
        if (self.x <= c.MOUSE_POS[0] <= self.x + self.iWidth) and (self.y <= c.MOUSE_POS[1] <= self.y + self.iHeight):
            return True
        return False

    @property
    def clicked_button(self):
        if (not self.clicked) and self.on_button and c.MOUSE_CLICKED: # 버튼 누른상태 아니고, 마우스로 버튼위를 클릭했을때
            self.clicked = True
            return True
        elif self.clicked and c.MOUSE_CLICKED: # 버튼을 누른상태에서 여전히 마우스도 누른상태 일때
            return True
        elif self.clicked and not (c.MOUSE_CLICKED or self.on_button): # 클릭한 상태에서 버튼 밖에서 마우스 왼쪽버튼 뗏을때
            self.clicked = False
        elif self.clicked and self.on_button and not c.MOUSE_CLICKED: # 클릭한 상태에서 버튼 안에서 마우스 왼쪽버튼 뗏을때
            self.clicked = False
            self.motion = not self.motion
            return True
        return False

    def __call__(self):
        if not self.disabled: # 버튼이 비활성화가 아닐 때
            if self.on_button and not (self.clicked_button or self.motion): # 버튼 위에있고, 클릭 X, 모션실행 X
                if self.iOver:
                    c.SCREEN.blit(self.iOver, (self.x, self.y))
                else:
                    c.SCREEN.blit(self.iNormal, (self.x, self.y))
            elif self.clicked_button or self.motion:
                if self.iClick:
                    c.SCREEN.blit(self.iClick, (self.x, self.y))
                else:
                    c.SCREEN.blit(self.iNormal, (self.x, self.y))
            else:
                if self.on_button and self.iOver: # 오차나서 다시 넣어줌
                    c.SCREEN.blit(self.iOver, (self.x, self.y))
                else:
                    c.SCREEN.blit(self.iNormal, (self.x, self.y))
        else: # 버튼이 비활성화 일때
            c.SCREEN.blit(self.iNormal, (self.x, self.y))