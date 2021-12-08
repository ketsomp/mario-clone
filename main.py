import pygame
import random
import math

pygame.init()

# fps
clock = pygame.time.Clock()
fps = 60

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 16)

textX = 10
textY = 10

# True - facing right
# False - facing left
pov = True

# file paths
IconPath = 'assets/mario.png'
SpriteRImagePath = 'assets/firemario_R.png'
SpriteLImagePath = 'assets/firemario_L.png'
Enemy1ImagePath = 'assets/goomba.png'
MusicPath = 'assets/mario_soundtrack.mp3'
ProjectilePath = 'assets/fireball.png'
ProjectileSoundEffectPath = 'assets/fireball.mp3'
BackgroundPath = 'assets/grass_background.png'
ShootingSoundEffectPath = 'assets/fireball.mp3'
GameOverSoundEffectPath = 'assets/game_over_sound_effect.mp3'
GameCompleteSoundEffectPath = 'assets/game_complete_sound_effect.mp3'

iconImg = pygame.image.load(IconPath)

# defines screen dimensions
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Hexham's Reckoning")
pygame.display.set_icon(iconImg)

# background
bgpic = pygame.image.load(BackgroundPath)
background = pygame.transform.scale(bgpic, (1000, 800))

#  music
bgmusic = pygame.mixer.Sound(MusicPath)
bgmusic.play(-1)
bgmusic.set_volume(0.1)
shootingSound = pygame.mixer.Sound(ShootingSoundEffectPath)
game_over_music = pygame.mixer.Sound(GameOverSoundEffectPath)
game_over_music.set_volume(0.1)
game_complete_music = pygame.mixer.Sound(GameCompleteSoundEffectPath)
game_complete_music.set_volume(0.1)

# player dimensions
SpriteRImage = pygame.image.load(SpriteRImagePath)
playerRImg = pygame.transform.scale(SpriteRImage, (64, 64))
SpriteLImage = pygame.image.load(SpriteLImagePath)
playerLImg = pygame.transform.scale(SpriteLImage, (64, 64))
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# enemy dimensions
enemyImg = []
enemy1X = []
enemy1Y = []
enemy1X_change = []
enemy1Y_change = []
enemy1Count = 10

for i in range(enemy1Count):
    enemyImg.append(pygame.image.load(Enemy1ImagePath))
    enemy1X.append(random.randint(100, 936))
    enemy1Y.append(random.randint(100, 736))
    enemy1X_change.append(2)
    enemy1Y_change.append(2)

# bullet dimensions
# True = Can't see proj on screen : ready
# False = proj in motion : fire
projpic = pygame.image.load(ProjectilePath)
projImg = pygame.transform.scale(projpic, (32, 32))
projX = 450
projY = 500
projX_change = -10
projY_change = 0
proj_state = True


def show_score(x, y):
    scorerender = font.render('Score:'+str(score), True, (255, 255, 255))
    screen.blit(scorerender, (x, y))

# drawing player sprite


def player(x, y):
    if pov:
        screen.blit(playerRImg, (x, y))
    else:
        screen.blit(playerLImg, (x, y))

# drawing first enemy sprite


def enemy1(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# drawing projectile


def fire_projectile(x, y):
    global proj_state
    proj_state = False
    screen.blit(projImg, (x+16, y+10))

# detect collision


def isCollision(x1, y1, x2, y2):
    distance = math.sqrt((math.pow(x1-x2, 2)) +
                         (math.pow(y1-y2, 2)))
    if distance < 27:
        return True
    else:
        return False


def pov_of_player():
    if pov:
        print('dog')

def logger():
    print(projX, ",", projY)


# game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    # setting frames per second to 60 - standard
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # moving the sprite using keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
                projX_change = 10
                pov = False
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
                projX_change = -10
                pov = True
            if event.key == pygame.K_UP:
                playerY_change = -5
            if event.key == pygame.K_DOWN:
                playerY_change = 5
            if event.key == pygame.K_SPACE:
                if proj_state is True:
                    projX = playerX
                    projY = playerY
                    fire_projectile(projX, projY)
                    shootingSound.play()
        # registering letting go of key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                playerY_change = 0

    # 5+=-0.1 => 5-=0.1
    # 5+=0.1
    playerX += playerX_change
    playerY += playerY_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 936:
        playerX = 936
    if playerY <= 0:
        playerY = 0
    elif playerY >= 736:
        playerY = 736

    # enemy movement pattern
    for i in range(enemy1Count):
        enemy1X[i] += enemy1X_change[i]
        # enemy1Y+=enemy1Y_change
        # preventing from passing out of bounds
        if enemy1X[i] <= 0:
            enemy1X_change[i] = 2
        elif enemy1X[i] >= 936:
            enemy1X_change[i] = -2
        if enemy1Y[i] <= 0:
            enemy1Y_change[i] = 2
        elif enemy1Y[i] >= 736:
            enemy1Y_change[i] = -2

        projectileCollision = isCollision(enemy1X[i], enemy1Y[i], projX, projY)
        if projectileCollision:
            projX = playerX
            projY = playerY
            proj_state = True
            score += 1
            enemy1X[i] = 5000
            #enemy1Y[i] = random.randint(100, 736)
        enemy1(enemy1X[i], enemy1Y[i], i)
        playerCollision = isCollision(enemy1X[i], enemy1Y[i], playerX, playerY)
        if playerCollision:
            playerX = 10000
            playerY = 10000
            game_over_music.play()
            bgmusic.stop()
            # wait for 8 seconds for end of game theme to complete
            pygame.time.wait(7000)
            running = False  # end program
    # projectile movement
    if projX >= 1000 or projX<0:
        projX = 450
        proj_state = True

    if proj_state == False:
        fire_projectile(projX, projY)
        projX -= projX_change

    # game complete sequence
    if score == 10:
        game_complete_music.play()
        bgmusic.stop()
        # wait for 8 seconds for end of game theme to complete
        pygame.time.wait(8000)
        running = False  # end program

    # collision

    player(playerX, playerY)
    show_score(textX, textY)
    # logger()
    pygame.display.update()
