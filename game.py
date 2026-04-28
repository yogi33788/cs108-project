import pygame, sys
pygame.init()

#game conditions

intro = True
game1 = False
game2 = False
game3 = False

#colors for intro screen

c1 = (61,82,160)
c2 = (112,145,230)
c3 = (134,151,196)
c4 = (173,187,218)
c5 = (237,232,245)

#variables defined
clock = pygame.time.Clock()

#constants

display_width = 800
display_height = 800

#screen

screen = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
pygame.display.set_caption('Game')

#fonts

font1 = pygame.font.Font('1.ttf',(display_height//10))
font2 = pygame.font.Font('2.ttf',(display_height//16))
font3 = pygame.font.Font('3.ttf',(display_height//20))
player_surf = pygame.image.load('CS.png').convert_alpha()
while True:

    mouse_pos = pygame.mouse.get_pos()

    #border animation

    curr_height = screen.get_height()
    curr_width = screen.get_width()

    x = curr_height
    y = curr_width

    if curr_height != display_height:
        display_height = curr_height
        font1 = pygame.font.Font('1.ttf',(display_height//10))
        font2 = pygame.font.Font('2.ttf',(display_height//16))
        font3 = pygame.font.Font('3.ttf',(display_height//20))
        
    #border



    #text surfaces and rectangles for intro

    text1_surf = font1.render('Game Hub', False, c4).convert_alpha()
    text1_rect = text1_surf.get_rect(center = (curr_width//2,curr_height//8))

    text2_surf = font2.render('Click on a game to play', False, 'Grey').convert_alpha()
    text2_rect = text2_surf.get_rect(center = (curr_width//2,(curr_height//8)*3))

    player_rect = player_surf.get_rect(midleft = (0,curr_height//8))

    surf1 = pygame.Surface((curr_width,curr_height//4))
    surf2 = pygame.Surface((curr_width,(curr_height)*3))
    surf1.fill(c1)
    surf2.fill(c2)

    screen.blit(surf1, (0,0))
    screen.blit(surf2, (0,curr_height//4))
    pygame.draw.line(screen,'White',(0,curr_height//4),(curr_width,curr_height/4),8)
    screen.blit(text1_surf,text1_rect)
    screen.blit(text2_surf, text2_rect)
    screen.blit(player_surf, player_rect)

    
    #defining options outline

    opt1 = pygame.Rect(curr_width//24,curr_height//2,(curr_width//12)*11,curr_height//8)
    opt2 = pygame.Rect(curr_width//24,(curr_height//3)*2,(curr_width//12)*11,curr_height//8)
    opt3 = pygame.Rect(curr_width//24,(curr_height//6)*5,(curr_width//12)*11,curr_height//8)


    if opt1.collidepoint(mouse_pos):
        pygame.draw.rect(screen, c4, opt1, border_radius = 20)
        pygame.draw.rect(screen, 'White', opt1,3, border_radius = 20)
    else:
        pygame.draw.rect(screen, c3, opt1, border_radius = 10)
        pygame.draw.rect(screen, 'White', opt1,5, border_radius = 10)

    if opt2.collidepoint(mouse_pos):
        pygame.draw.rect(screen, c4, opt2, border_radius = 20)
        pygame.draw.rect(screen, 'White', opt2,5, border_radius = 20)
    else:
        pygame.draw.rect(screen, c3, opt2, border_radius = 10)
        pygame.draw.rect(screen, 'White', opt2,5, border_radius = 10)

    if opt3.collidepoint(mouse_pos):
        pygame.draw.rect(screen, c4, opt3, border_radius = 20)
        pygame.draw.rect(screen, 'White', opt3,5, border_radius = 20)
    else:
        pygame.draw.rect(screen, c3, opt3, border_radius = 10)
        pygame.draw.rect(screen, 'White', opt3,5, border_radius = 10)
    
    #option surfaces and rectangles

    opt1_surf = font3.render('Tic Tac Toe', False, c5).convert_alpha()
    opt1_rect = opt1_surf.get_rect(center = opt1.center)

    opt2_surf = font3.render('Othello', False, c5).convert_alpha()
    opt2_rect = opt2_surf.get_rect(center = opt2.center)

    opt3_surf = font3.render('Connect4', False, c5).convert_alpha()
    opt3_rect = opt3_surf.get_rect(center = opt3.center)

    screen.blit(opt1_surf, opt1_rect)
    screen.blit(opt2_surf, opt2_rect)
    screen.blit(opt3_surf, opt3_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(120)
