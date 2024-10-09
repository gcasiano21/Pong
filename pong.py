import pygame, sys

pygame.init()
clock = pygame.time.Clock()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 960
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Pong')

ball = pygame.Rect(WINDOW_WIDTH / 2, 5, 15, 15)

dink = pygame.mixer.Sound('../Audio/dink.wav')
donk = pygame.mixer.Sound('../Audio/donk.wav')
scored = pygame.mixer.Sound('../Audio/scored.wav')
music = pygame.mixer.Sound('../Audio/menu.wav')
music.play(-1)
music.set_volume(.15)

player1Score = 0
player2Score = 0

player1 = pygame.Rect(10, WINDOW_HEIGHT / 2 - 50, 10, 100)
player2 = pygame.Rect(WINDOW_WIDTH - 20, WINDOW_HEIGHT / 2 - 50, 10, 100)

ballX = 10
ballY = 10

player_speed = 10
ai_speed = 10

def ballLogic():
    global ballX, ballY
    ball.x += ballX
    ball.y += ballY
    if ball.top <= 0 or ball.bottom >= WINDOW_HEIGHT:
        ballY *= -1
        donk.play()
    if ball.colliderect(player1) or ball.colliderect(player2):
        ballX *= -1
        dink.play()

def playerMovement():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= player_speed
    elif keys[pygame.K_s] and player1.bottom < WINDOW_HEIGHT:
        player1.y += player_speed

def aiMovement():
    if ball.right > (WINDOW_WIDTH / 2 + WINDOW_WIDTH / 4 + WINDOW_WIDTH / 16):
        if player2.top < ball.top:
            player2.top += ai_speed
        if player2.bottom > ball.bottom:
            player2.bottom -= ai_speed

def ballReset():
    global ballY
    ballY = 10
    ball.midtop = (WINDOW_WIDTH / 2, 5)
    player1.y = WINDOW_HEIGHT / 2 - 50
    player2.y = WINDOW_HEIGHT / 2 - 50

def score():
    global player1Score, player2Score
    if ball.left < 10:
        scored.play()
        pygame.time.delay(2000)
        ballReset()
        player2Score += 1
    if ball.right > WINDOW_WIDTH - 10:
        scored.play()
        pygame.time.delay(2000)
        ballReset()
        player1Score += 1
    if player1Score == 7:
        drawWinner('Player 1')
    elif player2Score == 7:
        drawWinner('Player 2')

def displayScore():
    global player1Score, player2Score
    font = pygame.font.SysFont('freesansbold.ttf', 35)
    text_surf1 = font.render(str(player1Score), True, (255, 255, 255))
    text_rect1 = text_surf1.get_rect(midtop = (WINDOW_WIDTH / 4 , 43))
    display_surface.blit(text_surf1, text_rect1)
    text_surf2 = font.render(str(player2Score), True, (255, 255, 255))
    text_rect2 = text_surf2.get_rect(midtop =  ((WINDOW_WIDTH / 2) + (WINDOW_WIDTH / 4), 43))
    display_surface.blit(text_surf2, text_rect2)

def drawWinner(player):
    font = pygame.font.SysFont('freesansbold.ttf', 100)
    win_surf = font.render(f'{player} Wins!', True, (255, 255, 255))
    win_rect = win_surf.get_rect(midtop = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2 - WINDOW_HEIGHT / 4)))
    display_surface.fill((0, 0, 0))
    display_surface.blit(win_surf, win_rect)
    pygame.display.update()
    pygame.time.delay(5000)
    pygame.quit()
    sys.exit()

def paused():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                paused = False
            
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            paused()
    
    display_surface.fill((0, 0, 0))
    pygame.draw.aaline(display_surface, (255, 255, 255), (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT))
    font = pygame.font.SysFont('freesansbold.ttf', 35)
    header_surf1 = font.render(str('Player 1'), True, (255, 255, 255))
    header_rect1 = header_surf1.get_rect(midtop = (WINDOW_WIDTH / 4 , 10))
    display_surface.blit(header_surf1, header_rect1)
    header_surf2 = font.render(str('Player 2'), True, (255, 255, 255))
    header_rect2 = header_surf2.get_rect(midtop =  ((WINDOW_WIDTH / 2) + (WINDOW_WIDTH / 4), 10))
    display_surface.blit(header_surf2, header_rect2)

    pygame.draw.rect(display_surface, (255, 255, 255), player1)
    pygame.draw.rect(display_surface, (255, 255, 255), player2)

    pygame.draw.ellipse(display_surface, (255, 255, 255), ball)

    ballLogic()

    playerMovement()
    aiMovement()

    score()
    displayScore()
    
    clock.tick(60)

    pygame.display.flip()
