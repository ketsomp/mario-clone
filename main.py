import pygame
import random
import math

from pygame.sprite import DirtySprite

pygame.init()

# fps
clock = pygame.time.Clock()
fps = 60

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 16)

textX = 10
textY = 10

# file paths
IconPath = 'assets/mario.png'
SpriteImagePath = 'assets/firemario.png'
Enemy1ImagePath = 'assets/goomba.png'
MusicPath = 'assets/mario_soundtrack.mp3'
ProjectilePath = 'assets/fireball.png'
ProjectileSoundEffectPath = 'assets/fireball.mp3'
BackgroundPath = 'assets/grass_background.png'
ShootingSoundEffectPath = 'assets/fireball.mp3'

shootingSound = pygame.mixer.Sound(ShootingSoundEffectPath)

iconImg = pygame.image.load(IconPath)

# defines screen dimensions
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Hexham's Reckoning")
pygame.display.set_icon(iconImg)

# background
bgpic = pygame.image.load(BackgroundPath)
background = pygame.transform.scale(bgpic, (1000, 800))

# plays music
pygame.mixer.music.load(MusicPath)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# main sprite
# class Sprite(pygame.sprite.Sprite):
#	def __init__(self,picture_path):
#		pygame.image.load(r(SpriteImagePath))

# player dimensions
SpriteImage = pygame.image.load(SpriteImagePath)
playerImg = pygame.transform.scale(SpriteImage, (64, 64))
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
    screen.blit(playerImg, (x, y))

# drawing first enemy sprite


def enemy1(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# drawing projectile


def fire_projectile(x, y):
    global proj_state
    proj_state = False
    screen.blit(projImg, (x+16, y+10))

# detect collision


def isCollision(enemy1X, enemy1Y, projX, projY):
    distance = math.sqrt((math.pow(enemy1X-projX, 2)) +
                         (math.pow(enemy1Y-projY, 2)))
    if distance < 27:
        return True
    else:
        return False


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
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
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
        collision = isCollision(enemy1X[i], enemy1Y[i], projX, projY)
        if collision:
            projX = playerX
            projY = playerY
            proj_state = True
            score += 1
            enemy1X[i] =5000
            #enemy1Y[i] = random.randint(100, 736)
        enemy1(enemy1X[i], enemy1Y[i], i)

    # projectile movement
    if projX >= 1000:
        projX = 450
        proj_state = True

    if proj_state == False:
        fire_projectile(projX, projY)
        projX -= projX_change

    # collision

    player(playerX, playerY)
    show_score(textX, textY)
    # logger()
    pygame.display.update()
