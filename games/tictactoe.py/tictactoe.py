import pygame, sys
import numpy as np

pygame.init()

clock = pygame.time.Clock()

c1 = (61,82,160)
c2 = (112,145,230)
c3 = (134,151,196)
c4 = (173,187,218)
c5 = (237,232,245)

#game active

active = True

#font
font1 = pygame.font.Font('1.ttf',50)
font2 = pygame.font.Font('2.ttf',40)

#player
player = 1

#X and O
X_surf = pygame.image.load('tictactoe.py/X.png')
O_surf = pygame.image.load('/tictactoe.py/O.png')

#virtual screen
base_width = 800
base_height = 800
columns = 10
rows = 10
x_margin = 55
y_margin = 55
gap = 10
side = 60

#text surf
text1_surf = font1.render('((T i c  T a c  T o e))', False, (255,255,255))
text1_rect = text1_surf.get_rect(center = (base_width/2, y_margin/2))
text2_surf = font2.render('Player (X) turn', False, c2)
text2_rect = text2_surf.get_rect(midbottom = (base_width/2, base_height))
text3_surf = font2.render('Player (O) turn', False, c2)
text3_rect = text3_surf.get_rect(midbottom = (base_width/2, base_height))

#screen
real_screen = pygame.display.set_mode((base_width, base_height), pygame.RESIZABLE)
virtual_screen = pygame.Surface((base_width, base_height))

pygame.display.set_caption('Tic Tac Toe')

#rectangle grid

rectangle = np.full((rows,columns),None)

#account for the rectangle usage

used = np.full((rows,columns),None)

for i in range(rows):
        for j in range(columns):
            rectangle[i][j] = pygame.Rect((i)*(gap+side)+x_margin, (j)*(gap+side)+y_margin, side, side)

def Win(used, i, j, player):
    #row check
    row_limit = j-4
    if row_limit < 0:
        row_limit = 0
    for r in range(row_limit, j+1):
        if r+4 <= 9:
            window = used[i,r:r+5]
            if np.all(window == player):
                print('True')
                return

    #column check
    column_limit = i-4
    if column_limit < 0:
        column_limit = 0
    for c in range(column_limit, i+1):
        if c+4 <=9:
            window = used[c:c+5,j]
            if np.all(window == player):
                print('True')
                return

    #diagonal check
    if i >= j:
        minimum = j
    else:
        minimum = i
    if minimum <= 4:
        diagonal = minimum 
    else:
        diagonal = 4
    for d in range(0,diagonal):
        if i-diagonal+d+5<=9 and j-diagonal+d+5<=9:
            window = used[i-diagonal+d:i-diagonal+d+5,j-diagonal+d:j-diagonal+d+5].diagonal()
            if np.all(window == player):
                print('True')
                return
    if i >= 9-j:
        minimum = 9-j
    else:
        minimum = i
    if minimum <= 4:
        diagonal = minimum
    else:
        diagonal = 4
    for d in range(0,diagonal):
        if i-diagonal+d+5 <= 9 and j+diagonal-d-5 >=0:
            window = np.fliplr(used[i-diagonal+d:i-diagonal+d+5,j+diagonal-d:j+diagonal-d-5]).diagonal()
            if np.all(window == player):
                print('True')
                return
    
while True:

    cur_width = real_screen.get_width()
    cur_height = real_screen.get_height()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    virtual_mouse_x = ((mouse_x*base_width)/cur_width)
    virtual_mouse_y = ((mouse_y*base_height)/cur_height)

    virtual_screen.fill(c1)
    virtual_screen.blit(text1_surf, text1_rect)
    if player == 1:
        virtual_screen.blit(text2_surf, text2_rect)
    else:
        virtual_screen.blit(text3_surf, text3_rect)

    for i in range(rows):
        for j in range(columns):
            if rectangle[i][j].collidepoint((virtual_mouse_x, virtual_mouse_y)) and used[i][j] == None:
                pygame.draw.rect(virtual_screen, c4, rectangle[i][j])
            else:
                if used[i][j]!= None:
                    if used[i][j] == 1:
                        virtual_screen.blit(X_surf, rectangle[i][j])
                    else:
                        virtual_screen.blit(O_surf, rectangle[i][j])
                else:
                    pygame.draw.rect(virtual_screen, c3, rectangle[i][j])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(rows):
                for j in range(columns):
                    if rectangle[i][j].collidepoint(virtual_mouse_x, virtual_mouse_y) and used[i][j] == None:
                        if player == 1:
                            used[i][j] = 1
                            Win(used, i, j, player)
                            player = 0
                        else:
                            used[i][j] = 0
                            Win(used, i, j, player)
                            player = 1
                            

    scaled_screen = pygame.transform.smoothscale(virtual_screen, (cur_width, cur_height))
    real_screen.blit(scaled_screen, (0,0))

    pygame.display.update()
    clock.tick(60)
        
