import pygame, sys
import numpy as np

pygame.init()

clock = pygame.time.Clock()

green = (34,139,34)
black = (0,0,0)
c1 = (61,82,160)
c2 = (112,145,230)
c4 = (173,187,218)

active = True

# font 
font1 = pygame.font.Font('1.ttf', 50)
font2 = pygame.font.Font('2.ttf', 40)

player = 0 # Starting with Black

# black and white discs
b_disc = pygame.image.load('black.png')
b_disc = pygame.transform.scale(b_disc, (60, 60))
w_disc = pygame.image.load('white.png')
w_disc = pygame.transform.scale(w_disc, (60, 60))

# virtual screen
base_width = 645
base_height = 645
columns = 8
rows = 8
x_margin = 60
y_margin = 60
gap = 5
side = 60

text1_surf = font1.render('((O T H E L L O))', False, (255,255,255))
text1_rect = text1_surf.get_rect(center = (base_width/2, y_margin/2))
text2_surf = font2.render('WHITE turn', False, c2)
text2_rect = text2_surf.get_rect(midbottom = (base_width/2, base_height - 10))
text3_surf = font2.render('BLACK turn', False, c2)
text3_rect = text3_surf.get_rect(midbottom = (base_width/2, base_height - 10))

real_screen = pygame.display.set_mode((base_width, base_height), pygame.RESIZABLE)
virtual_screen = pygame.Surface((base_width, base_height))
pygame.display.set_caption('OTHELLO')

rectangle = np.full((rows, columns), None)
used = np.full((rows, columns), None)

# Initial discs 
used[3][3], used[4][4] = 1, 1
used[3][4], used[4][3] = 0, 0

for i in range(rows):
    for j in range(columns):
        rectangle[i][j] = pygame.Rect(j * (gap + side) + x_margin, i * (gap + side) + y_margin, side, side)

def checkline(line, i, player):
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

def hor_check(i,j,used,player):
    line = used[i,:]
    return checkline(line,j,player)
    
def ver_check(i,j,used,player):
    line = used[:,j]
    return checkline(line,i,player)

# diagonal check \
def diag1_check(i, j, used, player):
    line = np.diagonal(used, offset=j-i).copy() 
    d = min(i, j)
    check = checkline(line, d, player)
    if check:
        n = len(line)
        r = np.arange(max(0, i-j), max(0, i-j) + n)
        c = np.arange(max(0, j-i), max(0, j-i) + n)
        used[r, c] = line
    return check

# diagonal check /        
def diag2_check(i, j, used, player):
    used_fliplr = np.fliplr(used).copy() 
    line = np.diagonal(used_fliplr, offset=7-(i+j)).copy() 
    d = min(i, 7-j)
    check = checkline(line, d, player)
    if check:
        n = len(line)
        r = np.arange(max(0, i-(7-j)), max(0, i-(7-j)) + n)
        c = np.arange(max(0, (7-j)-i), max(0, (7-j)-i) + n)
        used_fliplr[r, c] = line
        used[:] = np.fliplr(used_fliplr)
    return check
    
#check and  flip 
def check_and_flip(i,j,used,player):
    if used[i,j] is not None :
        return False
    hor = hor_check(i,j,used,player)
    ver = ver_check(i,j,used,player)
    diag1 = diag1_check(i,j,used,player)
    diag2 = diag2_check(i,j,used,player)
    return (hor|ver|diag1|diag2)

def has_any_valid_move(used,player):
    i,j = np.where(used == None )

    def valid(n):
        if n >= len(i):
            return False
        if check_and_flip(i[n],j[n],used.copy(),player):
            return True
        return valid(n+1)
    
    if len(i) == 0 :
        return False
    return valid(0)
    
def score(used,player):
    black_score = np.sum(used == 0)
    white_score = np.sum(used == 1)
    print(f"Black:{black_score}  White:{white_score}")


while True:
    cur_width = real_screen.get_width()
    cur_height = real_screen.get_height()
    mouse_pos = pygame.mouse.get_pos()
    virtual_mouse_x = (mouse_pos[0] * base_width) / cur_width
    virtual_mouse_y = (mouse_pos[1] * base_height) / cur_height

    virtual_screen.fill(c1)
    virtual_screen.blit(text1_surf, text1_rect)
    
    if player == 1: virtual_screen.blit(text2_surf, text2_rect)
    else: virtual_screen.blit(text3_surf, text3_rect)

    for i in range(rows):
        for j in range(columns):
            if rectangle[i][j].collidepoint((virtual_mouse_x, virtual_mouse_y)) and used[i][j] == None:
                pygame.draw.rect(virtual_screen, c4, rectangle[i][j]) 
            else:
                pygame.draw.rect(virtual_screen, green, rectangle[i][j])
            
            pygame.draw.rect(virtual_screen, black, rectangle[i][j], 1)

            if used[i][j] == 1:
                virtual_screen.blit(w_disc, rectangle[i][j])
            elif used[i][j] == 0:
                virtual_screen.blit(b_disc, rectangle[i][j])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(rows):
                for j in range(columns):
                    if rectangle[i][j].collidepoint(virtual_mouse_x, virtual_mouse_y):
                        if check_and_flip(i,j,used,player):
                            used[i][j] = player
                            score(used, player)
                            if has_any_valid_move(used, 1 - player):
                                player = 1 - player
                            elif not has_any_valid_move(used, player):
                                print("Game Over")

    scaled_screen = pygame.transform.smoothscale(virtual_screen, (cur_width, cur_height))
    real_screen.blit(scaled_screen, (0,0))

    pygame.display.update()
    clock.tick(60)