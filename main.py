import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800,600))
background = pygame.image.load('assets/bg.jpg')

mixer.music.load('assets/background.wav')
mixer.music.play(-1)

score_val = 0
font = pygame.font.Font('freesansbold.ttf', 24)
bigFont = pygame.font.Font('freesansbold.ttf', 60)
font_X = 20
font_y = 20

playerImg = pygame.image.load('assets/player2.png')
playerX = 370
playerY = 480
veloX = 0
veloY = 0

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('assets/galaxyIcon.png')
pygame.display.set_icon(icon)

enemyImg = pygame.image.load('assets/space-invaders.png')
enemyX = random.randint(100 , 700)
enemyY = random.randint(50 , 150)
enemy_vel = []

enemyX = []
enemyY = []

for x in range(5):
    enemyX.append(random.randint(100 , 700))
    enemyY.append(random.randint(50 , 150))
    enemy_vel.append(0.5)

bulletImg = pygame.image.load('assets/bullet.png')
bulletX = playerX
bulletY = playerY
bulletVel = 0.75
bullet_state = False

def game_over_screen():
    display = bigFont.render("GAME OVER", True, (255, 255, 255))
    display_Two = bigFont.render("Score: " + str(score_val), True, (255, 255, 255))
    screen.blit(display, (200 , 240))
    screen.blit(display_Two, (220, 300))

def show_score(x , y):
    score = font.render("Score: " + str(score_val),True,(255 , 255 ,255))
    screen.blit(score, (x , y))

def player(x , y):
    screen.blit(playerImg, (x , y))

def enemy(x , y):
    screen.blit(enemyImg, (x , y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = True
    screen.blit(bulletImg, (x + 16,y + 10))

def isCollision(bulletY , enemyY, bulletX , enemyX):
    colDist = math.sqrt(((bulletX - enemyX) ** 2) + ((bulletY - enemyY) ** 2))
    if colDist < 35:
        return True
    else:
        return False

running = True

while running:
    screen.fill((0 , 0 ,0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_DOWN:
            #     veloY = 0.25
            # if event.key == pygame.K_UP:
            #     veloY = -0.25
            if event.key == pygame.K_LEFT:
                veloX = -0.35
            if event.key == pygame.K_RIGHT:
                veloX = 0.35
            if event.key == pygame.K_SPACE and not bullet_state:
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
                shoot_sound = mixer.Sound('assets/laser.wav')
                shoot_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                veloX = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                veloY = 0

    playerX = playerX + veloX
    playerY = playerY + veloY

    if bullet_state:
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletVel
        if bulletY <= 0:
            bullet_state = False
            bulletY = playerY

    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736
    if playerY >= 536:
        playerY = 536
    if playerY <= 0:
        playerY = 0

    player(playerX , playerY)
    for x in range(len(enemyX)):

        if enemyY[x] > 400:
            for j in range(len(enemyX)):
                enemyY[j] = 2000
            game_over_screen()

        enemy(enemyX[x], enemyY[x])
        enemyX[x] = enemyX[x] + enemy_vel[x]

        if (enemyX[x] >= 736):
            enemy_vel[x] = -0.5
            enemyY[x] += 15

        if (enemyX[x] <= 0):
            enemy_vel[x] = 0.5
            enemyY[x] += 15

        if isCollision(bulletY , enemyY[x], bulletX , enemyX[x]):
            bullet_state = False
            bulletY = playerY
            explode_sound = mixer.Sound('assets/explosion.wav')
            explode_sound.play()
            score_val += 30
            enemyX[x] = random.randint(100, 700)
            enemyY[x] = random.randint(50, 150)
            enemy_vel[x] += 0.1

    show_score(font_X, font_y)
    pygame.display.update()