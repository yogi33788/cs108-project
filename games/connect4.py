import numpy as np 
import pygame,sys
from games.base_game import Base 

class Connect4(Base):
    def __init__(self,p1,p2):
        super().__init__(p1,p2)

        # colors
        self.c1 = (61,82,160)
        self.c2 = (112,145,230)
        self.c3 = (134,151,196)
        self.c4 = (173,187,218)

        # fonts
        self.font1 = pygame.font.Font('1.ttf',50)
        self.font2 = pygame.font.Font('2.ttf',40)

        # player
        self.player = 1
        self.col = None
        self.base_width = 800
        self.base_height = 800
        self.columns = 7
        self.rows = 7
        self.x_margin = 50
        self.ty_margin = 100
        self.side = 100
        self.text1_surf = self.font2.render('((Connect 4))', False, (255,255,255))
        self.text1_rect = self.text1_surf.get_rect(center = (self.base_width/2, self.ty_margin/2))
        self.rectangle = np.full((self.rows,self.columns),None)
        self.used = np.full((self.rows,self.columns),None)
        self.level = np.full(8,0)
        self.ypos = self.ty_margin + self.side/2
        self.board_surf = self.create_board()

        for i in range(self.rows):
            for j in range(self.columns):
                self.rectangle[i][j] = pygame.Rect((j)*(self.side)+self.x_margin, (i)*(self.side)+self.ty_margin, self.side, self.side)


    def draw(self, virtual_screen,mx,my):
        virtual_screen.fill(self.c1)
        virtual_screen.blit(self.text1_surf, self.text1_rect)

        color = 'Red' if self.player == 1 else 'Black'
        if mx <= self.x_margin + self.side/2:
            pygame.draw.circle(virtual_screen,color,(self.x_margin+self.side/2, self.ty_margin/2),48)
        elif mx >= self.base_width - self.x_margin-self.side/2:
            pygame.draw.circle(virtual_screen,color,(self.base_width - self.x_margin-self.side/2, self.ty_margin/2),48)
        else:
            pygame.draw.circle(virtual_screen,color,(mx, self.ty_margin/2),48)

        if self.animate:
            if self.player == 1:
                pygame.draw.circle(virtual_screen,'Red',(self.x_margin+self.col*self.side+self.side/2,self.ypos),int(self.side/2-3))
            if self.player == 0:
                pygame.draw.circle(virtual_screen,'Black',(self.x_margin+self.col*self.side+self.side/2,self.ypos),int(self.side/2-3))

        for i in range(self.rows):
            for j in range(self.columns):
                if self.used[i][j] != None:
                    if self.used[i][j] == 1:
                        pygame.draw.circle(virtual_screen,'Red',self.rectangle[i][j].center,48)
                    else:
                        pygame.draw.circle(virtual_screen,'Black',self.rectangle[i][j].center,48)


        virtual_screen.blit(self.board_surf,(self.x_margin, self.ty_margin))
        
        self.winner() 

    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:

            mx, my = mouse_pos
            if mx <= self.x_margin and self.level[0] <=6:
                self.animate = True
                self.col = 0

            elif mx >= self.base_width-self.x_margin and self.level[6] <= 6:
                self.animate = True
                self.col = 6

            else:
                self.col = int((mx - self.x_margin) //(self.side))
                b = self.col
                if int(self.level[b]) <= 6:
                    self.animate = True
                        
        
    def update(self,virtual_screen):
        if self.animate:
            self.ypos += 5
            target_y = self.ty_margin + (self.rows - 1 - self.level[self.col]) * self.side + self.side / 2
            if self.ypos >= target_y:
                self.used[6-self.level[self.col]][self.col] = self.player
                self.player = 1-self.player
                self.level[self.col] += 1
                self.animate = False
                self.ypos = self.ty_margin + self.side/2


    def create_board(self):
        board_surf = pygame.Surface((self.columns*self.side, self.rows*self.side), pygame.SRCALPHA)
        board_surf.fill((0, 0, 0, 0))  # fully transparent

        for i in range(self.rows):
            for j in range(self.columns):
                rect = pygame.Rect(j * self.side, i * self.side, self.side, self.side)
                pygame.draw.rect(board_surf, self.c2, rect)
                cx = j * self.side + self.side//2 
                cy = i * self.side + self.side//2 
                pygame.draw.circle(board_surf, (0, 0, 0, 0), (cx, cy), 48)

        return board_surf
        
    
    def winner(self):
        x = (self.used == 1-self.player)

        # row check
        row_0 = x[:, 0:4].all(axis=1)
        row_1 = x[:, 1:5].all(axis=1)
        row_2 = x[:, 2:6].all(axis=1)
        row_3 = x[:, 3:7].all(axis=1)

        if np.any(row_0 | row_1 | row_2 | row_3 ):
            self.gameover = True
            return 


        # column check
        col_0 = x[0:4,:].all(axis=0)
        col_1 = x[1:5,:].all(axis=0)
        col_2 = x[2:6,:].all(axis=0)
        col_3 = x[3:7,:].all(axis=0)

        if np.any(col_0 | col_1 | col_2 | col_3 ):
            self.gameover = True
            return 
        
        # diagonal check \
        square_0 = x[0:4, 0:4]
        square_1 = x[1:5, 1:5]
        square_2 = x[2:6, 2:6]
        square_3 = x[3:7, 3:7]

        arr = (square_0 & square_1 & square_2 & square_3 )
        if np.any(arr):
            self.gameover = True
            return 
        
        # diagonal check /
        sq0 = x[0:4, 3:7]
        sq1 = x[1:5, 2:6]
        sq2 = x[2:6, 1:5] 
        sq3 = x[3:7, 0:4] 

        ar = (sq0 & sq1 & sq2 & sq3 ) 
        if np.any(ar):     
            self.gameover = True
            return
