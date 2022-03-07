import pygame
from pygame.locals import *
from pygame import mixer#音声とかのライブラリ
import sys
import random
import math
pygame.init()#初期化

#ウィンドウの表示
screen=pygame.display.set_mode((800,600))#スクリーンを定義
#screen.fill((150,150,150))#背景の色RGB
pygame.display.set_caption('kawanaka shooting')#タイトル

#player
playerImg=pygame.image.load('player.png')#プレイヤー画像読み込み
playerX,playerY=370,480
playerX_change=0

#Enemy
enemyImg = pygame.image.load('kasuga.png')
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)#ランダムな場所から敵は出現
enemyX_change, enemyY_change = 4, 40

bulletImg = pygame.image.load('bullet.png')
bulletX, bulletY = 0, 480
bulletX_change, bulletY_change = 0, 3
bullet_state = 'ready'

#score
score_value = 0

sound=pygame.mixer.Sound('yorunikakeru.wav')#サウンド読み込み
sound.play()

def player(x,y):    
    screen.blit(playerImg,(x,y))#読み込んだ画像を表示

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False

running=True
while running:#スクリーンを閉じずに開いている
    screen.fill((0,0,0))#黒でスクリーンを上書き

    font=pygame.font.SysFont(None,70)
    message=font.render('Welcome to kasuga shooting!',False,(255,255,255))
    screen.blit(message,(20,50))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:#閉じるをクリックするとウィンドウを閉じる
            running=False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:#左を押したら
                playerX_change = -1.5
            if event.key == pygame.K_RIGHT:#右を押したら
                playerX_change = 1.5
            if event.key == pygame.K_SPACE:#スペースを押したら
                if bullet_state is 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
    
        if event.type == pygame.KEYUP:#キーを離すと
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:#playerの移動制限
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    font=pygame.font.SysFont(None,100)
    over=font.render('GAME OVER',False,(255,0,0))
    
    # Enemy
    if enemyY > 440:
        screen.blit(over,(215,260))
        screen.blit(score, (20,550))
        he = pygame.image.load('he.png')
        screen.blit(he,(600,300))

        pygame.display.update()
        for event in pygame.event.get():
 
                ### 終了処理
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    exit()
        continue
                    
    enemyX += enemyX_change
    if enemyX <= 0: #左端に来たら
        enemyX_change = random.randint(1,8)
        enemyY += enemyY_change
    elif enemyX >=736: #右端に来たら
        enemyX_change = random.randint(-8,-1)
        enemyY += enemyY_change

    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletY = 480
        bullet_state = 'ready'
        score_value += 1
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)

    # Bullet Movement
    if bulletY <=0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    # Score
    font = pygame.font.SysFont(None, 32) # フォントの作成　Noneはデフォルトのfreesansbold.ttf
    score = font.render(f"Score : {str(score_value)}", True, (255,255,255)) # テキストを描画したSurfaceの作成
    screen.blit(score, (20,550))

    player(playerX,playerY)
    enemy(enemyX,enemyY)
    pygame.display.update()#スクリーン上のものを書き換えたときはアップデートが必要









