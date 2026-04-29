import pygame,sys
from games.base_game import Base 
from games.tictactoe import Tictactoe
from games.connect4 import Connect4
from games.othello import Othello 
import subprocess 

class Menu:
    def __init__(self,width,height,p1, p2):
        # basic screen intialization and background
        pygame.init() 
        self.font1 = pygame.font.Font('1.ttf',30)
        self.p1 = p1
        self.p2 = p2
        self.base_width = width
        self.base_height = height
        self.font3 = pygame.font.Font('3.ttf',(self.base_height//20))
        self.clock = pygame.time.Clock()
        self.real_screen = pygame.display.set_mode((self.base_width, self.base_height), pygame.RESIZABLE)
        pygame.display.set_caption('GAME HUB')
        self.virtual_screen = pygame.Surface((self.base_width, self.base_height))
        self.background_surf = pygame.image.load('background.png').convert_alpha()
        self.background_rect = self.background_surf.get_rect(center = (self.base_width/2,self.base_height/2))
        self.opt1 = pygame.Rect(self.base_width/3.8,250,self.base_width/2,self.base_width/8)
        self.opt2 = pygame.Rect(self.base_width/3.8,400,self.base_width/2,self.base_width/8)
        self.opt3 = pygame.Rect(self.base_width/3.8,550,self.base_width/2,self.base_width/8)
        self.opt4 = pygame.Rect(self.base_width/3.8,9*(self.base_width/10)-10,self.base_width/4,self.base_width/10)       
        self.selected_game = None
        self.outro_surf = pygame.image.load('outro.png')
        self.outro_rect = self.outro_surf.get_rect(center = (self.base_width/2,self.base_height/2))
        self.text_surf = self.font1.render('#sort by::', False, 'White')
        self.text_rect = self.text_surf.get_rect(center = (self.base_width/2, 200))

    def gameloop(self):
        #game loop
        while True:
            current_width = self.real_screen.get_width()
            current_height = self.real_screen.get_height()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.virtual_mouse_x = ((mouse_x*self.base_width)/current_width)
            self.virtual_mouse_y = ((mouse_y*self.base_height)/current_height)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.selected_game:
                        if not self.selected_game.gameover:
                            if not self.selected_game.animate:
                                self.selected_game.handle_event(event, (self.virtual_mouse_x, self.virtual_mouse_y))
                        else:
                            self.Outro_click() 
                    else:
                        self.selection()
            
            if self.selected_game == None:  
                self.virtual_screen.blit(self.background_surf,self.background_rect)
            if self.selected_game:
                if not self.selected_game.gameover:
                    self.selected_game.update(self.virtual_screen)
                    self.selected_game.draw(self.virtual_screen,self.virtual_mouse_x,self.virtual_mouse_y)
                else:
                    self.Outro()
            else:    
                self.hover()

            scaled_screen = pygame.transform.smoothscale(self.virtual_screen,(current_width,current_height))
            self.real_screen.blit(scaled_screen,(0,0))
            pygame.display.update()
            self.clock.tick(60)

    def hover(self):  
        if self.opt1.collidepoint((self.virtual_mouse_x,self.virtual_mouse_y)):
            pygame.draw.rect(self.virtual_screen, (80, 140, 180), self.opt1, border_radius = 20)
            pygame.draw.rect(self.virtual_screen, 'White', self.opt1,3, border_radius = 20)
        else:
            pygame.draw.rect(self.virtual_screen, (40, 60, 80), self.opt1, border_radius = 10)
            pygame.draw.rect(self.virtual_screen, 'White',self.opt1,3, border_radius = 10)

        if self.opt2.collidepoint((self.virtual_mouse_x,self.virtual_mouse_y)):
            pygame.draw.rect(self.virtual_screen, (80, 140, 180), self.opt2, border_radius = 20)
            pygame.draw.rect(self.virtual_screen, 'White', self.opt2,3, border_radius = 20)
        else:
            pygame.draw.rect(self.virtual_screen, (40, 60, 80), self.opt2, border_radius = 10)
            pygame.draw.rect(self.virtual_screen, 'White',self.opt2,3, border_radius = 10)

        if self.opt3.collidepoint((self.virtual_mouse_x,self.virtual_mouse_y)):
            pygame.draw.rect(self.virtual_screen, (80, 140, 180), self.opt3, border_radius = 20)
            pygame.draw.rect(self.virtual_screen, 'White', self.opt3,3, border_radius = 20)
        else:
            pygame.draw.rect(self.virtual_screen, (40, 60, 80), self.opt3, border_radius = 10)
            pygame.draw.rect(self.virtual_screen, 'White',self.opt3,3, border_radius = 10)

        self.opt1_surf = self.font3.render('Tic Tac Toe', False, 'White').convert_alpha()
        opt1_rect = self.opt1_surf.get_rect(center = self.opt1.center)

        self.opt2_surf = self.font3.render('Othello', False, 'White').convert_alpha()
        opt2_rect = self.opt2_surf.get_rect(center = self.opt2.center)

        self.opt3_surf = self.font3.render('Connect4', False, 'White').convert_alpha()
        opt3_rect = self.opt3_surf.get_rect(center = self.opt3.center)
        self.virtual_screen.blit(self.opt1_surf,opt1_rect)
        self.virtual_screen.blit(self.opt2_surf,opt2_rect)
        self.virtual_screen.blit(self.opt3_surf,opt3_rect)

    def Outro_click(self):
        if self.opt4.collidepoint(self.virtual_mouse_x, self.virtual_mouse_y):
            self.selected_game = None

        elif self.opt1.collidepoint(self.virtual_mouse_x, self.virtual_mouse_y):
            self.run_leaderboard('wins')

        elif self.opt2.collidepoint(self.virtual_mouse_x, self.virtual_mouse_y):
            self.run_leaderboard('losses')

        elif self.opt3.collidepoint(self.virtual_mouse_x, self.virtual_mouse_y):
            self.run_leaderboard('wbyl')

    def run_leaderboard(self, sort_by,player):
        pygame.quit()
        subprocess.run(['bash', 'leaderboard.sh', sort_by])
        sys.exit()

    def selection(self):
        if self.opt1.collidepoint(self.virtual_mouse_x,self.virtual_mouse_y):
            self.selected_game = Tictactoe(self.p1,self.p2)
        elif self.opt2.collidepoint(self.virtual_mouse_x,self.virtual_mouse_y):
            self.selected_game = Othello(self.p1,self.p2)
        elif self.opt3.collidepoint(self.virtual_mouse_x,self.virtual_mouse_y):
            self.selected_game = Connect4(self.p1,self.p2)
        else:
            pass
        
    def Outro(self):
        self.virtual_screen.blit(self.outro_surf,self.outro_rect)
        if self.opt1.collidepoint((self.virtual_mouse_x,self.virtual_mouse_y)):
            pygame.draw.rect(self.virtual_screen, (80, 140, 180), self.opt1, border_radius = 20)
            pygame.draw.rect(self.virtual_screen, 'White', self.opt1,3, border_radius = 20)
        else:
            pygame.draw.rect(self.virtual_screen, (40, 60, 80), self.opt1, border_radius = 10)
            pygame.draw.rect(self.virtual_screen, 'White',self.opt1,3, border_radius = 10)

        if self.opt2.collidepoint((self.virtual_mouse_x,self.virtual_mouse_y)):
            pygame.draw.rect(self.virtual_screen, (80, 140, 180), self.opt2, border_radius = 20)
            pygame.draw.rect(self.virtual_screen, 'White', self.opt2,3, border_radius = 20)
        else:
            pygame.draw.rect(self.virtual_screen, (40, 60, 80), self.opt2, border_radius = 10)
            pygame.draw.rect(self.virtual_screen, 'White',self.opt2,3, border_radius = 10)

        if self.opt3.collidepoint((self.virtual_mouse_x,self.virtual_mouse_y)):
            pygame.draw.rect(self.virtual_screen, (80, 140, 180), self.opt3, border_radius = 20)
            pygame.draw.rect(self.virtual_screen, 'White', self.opt3,3, border_radius = 20)
        else:
            pygame.draw.rect(self.virtual_screen, (40, 60, 80), self.opt3, border_radius = 10)
            pygame.draw.rect(self.virtual_screen, 'White',self.opt3,3, border_radius = 10)

        self.opt1_surf = self.font3.render('Wins', False, 'White').convert_alpha()
        opt1_rect = self.opt1_surf.get_rect(center = self.opt1.center)

        self.opt2_surf = self.font3.render('Losses', False, 'White').convert_alpha()
        opt2_rect = self.opt2_surf.get_rect(center = self.opt2.center)

        self.opt3_surf = self.font3.render('Win/Loss Ratio', False, 'White').convert_alpha()
        opt3_rect = self.opt3_surf.get_rect(center = self.opt3.center)
        self.virtual_screen.blit(self.opt1_surf,opt1_rect)
        self.virtual_screen.blit(self.opt2_surf,opt2_rect)
        self.virtual_screen.blit(self.opt3_surf,opt3_rect)
        
        self.virtual_screen.blit(self.text_surf,self.text_rect)

        if self.opt4.collidepoint((self.virtual_mouse_x,self.virtual_mouse_y)):
            pygame.draw.rect(self.virtual_screen, (134,151,196), self.opt4, border_radius = 20)
            pygame.draw.rect(self.virtual_screen, 'White', self.opt4,3, border_radius = 20)
        else:
            pygame.draw.rect(self.virtual_screen, (61,82,160), self.opt4, border_radius = 10)
            pygame.draw.rect(self.virtual_screen, 'White',self.opt4,3, border_radius = 10)

        self.opt4_surf = self.font1.render('PLAY  AGAIN', False, 'White').convert_alpha()
        self.opt4_rect = self.opt4_surf.get_rect(center = self.opt4.center)
        self.virtual_screen.blit(self.opt4_surf,self.opt4_rect)

menu = Menu(800,800,'hello','bye')
menu.gameloop()
