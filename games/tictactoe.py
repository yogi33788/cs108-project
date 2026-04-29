import numpy as np 
import pygame,sys
from games.base_game import Base 

class Tictactoe(Base):
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

        # images
        self.X_surf = pygame.image.load('X.png')
        self.O_surf = pygame.image.load('O.png')

        self.base_width = 800
        self.base_height = 800
        self.columns = 10
        self.rows = 10
        self.x_margin = 55
        self.y_margin = 55
        self.gap = 10
        self.side = 60
        self.text1_surf = self.font1.render('((T i c  T a c  T o e))', False, (255,255,255))
        self.text1_rect = self.text1_surf.get_rect(center = (self.base_width/2, self.y_margin/2))
        self.text2_surf = self.font2.render('Player (X) turn', False, self.c2)
        self.text2_rect = self.text2_surf.get_rect(midbottom = (self.base_width/2, self.base_height))
        self.text3_surf = self.font2.render('Player (O) turn', False, self.c2)
        self.text3_rect = self.text3_surf.get_rect(midbottom = (self.base_width/2, self.base_height))

        self.rectangle = np.full((self.rows,self.columns),None)

        #account for the rectangle usage

        self.used = np.full((self.rows,self.columns),None)
        for i in range(self.rows):
            for j in range(self.columns):
                self.rectangle[i][j] = pygame.Rect((j)*(self.gap+self.side)+self.x_margin, (i)*(self.gap+self.side)+self.y_margin, self.side, self.side)

    def draw(self, virtual_screen,mx,my):
        virtual_screen.fill(self.c1)
        virtual_screen.blit(self.text1_surf, self.text1_rect)

        if self.player == 1:
            virtual_screen.blit(self.text2_surf, self.text2_rect)
        else:
            virtual_screen.blit(self.text3_surf, self.text3_rect)

        for i in range(self.rows):
            for j in range(self.columns):

                rect = self.rectangle[i][j]

                if rect.collidepoint(mx, my) and self.used[i][j] is None:
                    pygame.draw.rect(virtual_screen, self.c4, rect)
                else:
                    if self.used[i][j] == 1:
                        virtual_screen.blit(self.X_surf, rect)
                    elif self.used[i][j] == 0:
                        virtual_screen.blit(self.O_surf, rect)
                    else:
                        pygame.draw.rect(virtual_screen, self.c3, rect)

        self.winner() 
       
    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = mouse_pos

            for i in range(self.rows):
                for j in range(self.columns):
                    if self.rectangle[i][j].collidepoint(mx, my) and self.used[i][j] is None:
                        if self.player == 1:
                            self.used[i][j] = 1
                            self.player = 0
                        else:
                            self.used[i][j] = 0
                            self.player = 1

    def winner(self):
        x = (self.used == 1-self.player)

        # row check
        row_0 = x[:, 0:5].all(axis=1)
        row_1 = x[:, 1:6].all(axis=1)
        row_2 = x[:, 2:7].all(axis=1)
        row_3 = x[:, 3:8].all(axis=1)
        row_4 = x[:, 4:9].all(axis=1)
        row_5 = x[:,5:10].all(axis=1)

        if np.any(row_0 | row_1 | row_2 | row_3 | row_4 | row_5):
            self.gameover = True
            return 


        # column check
        col_0 = x[0:5,:].all(axis=0)
        col_1 = x[1:6,:].all(axis=0)
        col_2 = x[2:7,:].all(axis=0)
        col_3 = x[3:8,:].all(axis=0)
        col_4 = x[4:9,:].all(axis=0)
        col_5 = x[5:10,:].all(axis=0)

        if np.any(col_0 | col_1 | col_2 | col_3 | col_4 | col_5):
            self.gameover = True
            return 
        
        # diagonal check \
        square_0 = x[0:6, 0:6]
        square_1 = x[1:7, 1:7]
        square_2 = x[2:8, 2:8]
        square_3 = x[3:9, 3:9]
        square_4 = x[4:10, 4:10]

        arr = (square_0 & square_1 & square_2 & square_3 & square_4)
        if np.any(arr):
            self.gameover = True
            return 
        
        # diagonal check /
        sq0 = x[0:6, 4:10]
        sq1 = x[1:7, 3:9]
        sq2 = x[2:8, 2:8] 
        sq3 = x[3:9, 1:7] 
        sq4 = x[4:10, 0:6]

        ar = (sq0 & sq1 & sq2 & sq3 & sq4) 
        if np.any(ar):     
            self.gameover = True
            return

        #complete board 
    def update(self,screen):
        pass