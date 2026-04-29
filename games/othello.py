import pygame, sys
import numpy as np
from games.base_game import Base

class Othello(Base):
    def __init__(self, p1, p2):
        super().__init__(p1, p2)

        # colours
        self.green = (34, 139, 34)
        self.c1 = (61, 82, 160)
        self.c2 = (112, 145, 230)
        self.c4 = (173, 187, 218)

        # fonts 
        self.font1 = pygame.font.Font('1.ttf', 40)
        self.font2 = pygame.font.SysFont("Arial", 30)
        self.score_font = pygame.font.SysFont("Arial", 30)

        # player (0 = Black, 1 = White)
        self.player = 0

        # black and white discs
        self.b_disc = pygame.image.load('black.png')
        self.w_disc = pygame.image.load('white.png')

        # virtual screen
        self.columns = 8
        self.rows = 8
        self.x_margin = 45/2
        self.y_margin = 45
        self.gap = 5
        self.side = 90

        self.text1_surf = self.font1.render('((O T H E L L O))', False, 'White')
        self.text1_rect = self.text1_surf.get_rect(center=(self.base_width / 2, 45/2.5))
        
        self.text2_surf = self.font2.render('White\'s turn :', False,'White')
        self.text2_rect = self.text2_surf.get_rect(topleft =(20, 15))
        self.text3_surf = self.font2.render('Black\'s turn :', False, 'White')
        self.text3_rect = self.text3_surf.get_rect(topleft =(20, 15))

        self.rectangle = np.full((self.rows, self.columns), None)
        self.used = np.full((self.rows, self.columns), None)

        # Initial discs setup
        self.used[3][3], self.used[4][4] = 1, 1
        self.used[3][4], self.used[4][3] = 0, 0

        for i in range(self.rows):
            for j in range(self.columns):
                self.rectangle[i][j] = pygame.Rect(j * (self.gap + self.side) + self.x_margin, 
                                                  i * (self.gap + self.side) + self.y_margin, 
                                                  self.side, self.side)

    def draw(self, virtual_screen, mx, my):
        virtual_screen.fill('Black')
        virtual_screen.blit(self.text1_surf, self.text1_rect)

        # Dynamic Score on Screen
        b_score = np.sum(self.used == 0)
        w_score = np.sum(self.used == 1)
        score1_surf = self.score_font.render(f"Black: {b_score}", True, 'Red')
        score2_surf = self.score_font.render(f"White: {w_score}", True, 'Blue')
        score1_rect = score1_surf.get_rect(topright= (self.base_width-10,15))
        score2_rect = score2_surf.get_rect(topright= (self.base_width-150,15))
        virtual_screen.blit(score1_surf, score1_rect)
        virtual_screen.blit(score2_surf, score2_rect)

        if self.player == 1:
            virtual_screen.blit(self.text2_surf, self.text2_rect)
        else:
            virtual_screen.blit(self.text3_surf, self.text3_rect)

        for i in range(self.rows):
            for j in range(self.columns):
                rect = self.rectangle[i][j]
                # Hover effect
                if rect.collidepoint((mx, my)) and self.used[i][j] is None:
                    pygame.draw.rect(virtual_screen, (117,250,141), rect)
                else:
                    pygame.draw.rect(virtual_screen, self.green, rect)
                
                # Draw Discs
                if self.used[i][j] == 1:
                    virtual_screen.blit(self.w_disc, rect)
                elif self.used[i][j] == 0:
                    virtual_screen.blit(self.b_disc, rect)

                elif self.used[i][j] == None:
                    if self.check_and_flip(i,j,self.used.copy(),self.player):
                        if self.player == 0:
                            pygame.draw.circle(virtual_screen,'Black',rect.center,40,2)
                        else:
                            pygame.draw.circle(virtual_screen,'White',rect.center,40,2)

    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = mouse_pos
            for i in range(self.rows):
                for j in range(self.columns):
                    if self.rectangle[i][j].collidepoint(mx, my):
                        # Attempt move
                        if self.check_and_flip(i, j, self.used, self.player):
                            self.used[i][j] = self.player
                            
                            # Switch Turn Logic
                            if self.has_any_valid_move(self.used, 1 - self.player):
                                self.player = 1 - self.player
                            elif not self.has_any_valid_move(self.used, self.player):
                                # Game Over logic
                                self.gameover = True
                                b_score = np.sum(self.used == 0)
                                w_score = np.sum(self.used == 1)
                                if b_score > w_score: self.player = 1
                                elif w_score > b_score: self.player = 0
                                else: self.player = 2 # Draw

    def update(self,screen):
        pass
    
    def checkline(self,line, i, player):
        check = False
        other_player = 1 - player
        if i >= len(line) - 1:
            front = np.array([])
        
        else:
            front = line[i+1:]

        not_opp_disc = np.where(front != other_player)[0]
        if not_opp_disc.size != 0:
            x = not_opp_disc[0]
            if x > 0 and (i + 1 + x) < len(line) and line[i + 1 + x] == player:
                line[i+1:i+1+x] = player
                check = True

        if i <= 0:
            back = np.array([])
        else:
            back = line[:i][::-1]

        not_opp_disc = np.where(back != other_player)[0]
        if not_opp_disc.size != 0:
            x = not_opp_disc[0]
            if x > 0 and (i - 1 - x) >= 0 and line[i - 1 - x] == player:
                line[i-x:i] = player
                check = True

        return check

    def hor_check(self,i,j,used,player):
        line = used[i,:]
        return self.checkline(line,j,player)
        
    def ver_check(self,i,j,used,player):
        line = used[:,j]
        return self.checkline(line,i,player)

    # diagonal check \
    def diag1_check(self,i, j, used, player):
        line = np.diagonal(used, offset=j-i).copy() 
        d = min(i, j)
        check = self.checkline(line, d, player)
        if check:
            n = len(line)
            r = np.arange(max(0, i-j), max(0, i-j) + n)
            c = np.arange(max(0, j-i), max(0, j-i) + n)
            used[r, c] = line
        return check

    # diagonal check /        
    def diag2_check(self,i, j, used, player):
        used_fliplr = np.fliplr(used).copy() 
        line = np.diagonal(used_fliplr, offset=7-(i+j)).copy() 
        d = min(i, 7-j)
        check = self.checkline(line, d, player)
        if check:
            n = len(line)
            r = np.arange(max(0, i-(7-j)), max(0, i-(7-j)) + n)
            c = np.arange(max(0, (7-j)-i), max(0, (7-j)-i) + n)
            used_fliplr[r, c] = line
            used[:] = np.fliplr(used_fliplr)
        return check
        
    #check and  flip 
    def check_and_flip(self,i,j,used,player):
        if used[i,j] is not None :
            return False
        hor = self.hor_check(i,j,used,player)
        ver = self.ver_check(i,j,used,player)
        diag1 = self.diag1_check(i,j,used,player)
        diag2 = self.diag2_check(i,j,used,player)
        return (hor|ver|diag1|diag2)

    def has_any_valid_move(self,used,player):
        i,j = np.where(used == None )

        def valid(n):
            if n >= len(i):
                return False
            if self.check_and_flip(i[n],j[n],used.copy(),player):
                return True
            return valid(n+1)
        
        if len(i) == 0 :
            return False
        return valid(0)