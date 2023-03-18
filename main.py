import pygame , random
pygame.init()



def hit_detect( ball, wall ):
    '''Collision detection of the ball and the walls that i made.
    The ball is gonna hit pads where they are on the screen'''
    ball_x = ball[0]
    ball_y = ball[1]

    wall_width = 10
    wall_height = 100
    wall_x = wall[0]
    wall_y = wall[1]

    if ball_x > wall_x and ball_x < wall_x + wall_width:
        if ball_y > wall_y and ball_y < wall_y + wall_height:

            ball[2] *= -1

def ball_movement():

    # ball movements
    ball[0]+= ball[2]
    ball[1] += ball[3]

    #ball hit detection with walls
    if ball[1] > screen_height:
        ball[3] *= -1
    if ball[1] < 0:
        ball[3] *= -1



frame = 0
#pygame settings for the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Pong game")  # Set title
clock = pygame.time.Clock()
game_font = pygame.font.Font("freesansbold.ttf",32)



#Settings for game
ball = [screen_width/2,screen_height/2, 5, 5 ]
pad1 = [50,screen_height/2-50]
pad2 = [screen_width - 50, screen_height/2 - 50 ]
pad1_speed = 0
player1_score = 0
player2_score = 0

speed = 10


#Making a Main window for the game.
running= True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        down = True
    if not keys[pygame.K_DOWN]:
        down = False
    if keys[pygame.K_UP]:
        up = True
    if not keys[pygame.K_UP]:
        up = False
    # print(f"up: {up}, down: {down}")
    if up:
       pad1[1] -= speed
    if down:
        pad1[1] += speed

    ball_movement()


    # AI for motstander, the second pad follows the ball
    if pad2[1] >= 0 and pad2[1] + 100 <= screen_height:
        pad2[1] = ball[1] - 50

    # Reposision of pad when i move it so it doesnt move out of the screen
    if pad2[1] <= 0:
        pad2[1] = 1
    if pad2[1] + 100 > screen_height:
        pad2[1] = screen_height - 101

    if pad1[1] <= 0:
        pad1[1] = 1
    if pad1[1] + 100 > screen_height:
        pad1[1] = screen_height - 101


    # HIT DETECTION WITH PADS and the ball
    hit_detect( ball, pad1 )
    hit_detect( ball, pad2 )

    # HIT DETECTION WITH SCORE CALCULATION AND REPOSITION OF BALL
    if ball[0] < 0:
        player2_score += 1
        ball[0] = screen_width/2
        ball[1] = screen_height/2
        ball[2] *= random.randrange(-1,1)
        if ball[2] == 0:
            ball[2] = -3
        else:
            ball[2] = 3

    if ball[1] > screen_width:
        player1_score += 1
        ball[0] = screen_width/2
        ball[1] = screen_height/2
        ball[2] *= random.randrange(-3,1)
        if ball[2] == 0:
            ball[2] = 3
        else:
            ball[2] = -3

    if frame % 100 == 0:
        with open("scores.csv", "a") as f:
            f.write(f"player1 {player1_score} - {player2_score} player2\n")






    # Rendering, drawing of the ball and the pads
    screen.fill((0,0,0))
    pygame.draw.ellipse(screen,(255,255,255),(ball[0],ball[1],10,10))
    pygame.draw.rect(screen,(255,255,255),(pad1[0],pad1[1],10,100))
    pygame.draw.rect(screen,(255,255,255),(pad2[0],pad2[1],10,100))
    pygame.draw.aaline(screen,(255,255,255),(screen_width/2,0),(screen_width/2,screen_height))

    score_text = game_font.render(f"{player1_score}",False,(255,255,255))
    screen.blit(score_text,(50,50))

    score_text = game_font.render(f"{player2_score}", False, (255,255 ,255 ))
    screen.blit(score_text, (screen_width-50,50))
    frame += 1
    pygame.display.update()
    clock.tick(60)