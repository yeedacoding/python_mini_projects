# 바이러스를 피해라
# 랜덤한 방향으로 바이러스를 생성시킴(위에서 아래로)
# 바이러스를 발생시키는 적을 향해 주사기를 발사
# 바이러스를 피할 때마다 or 시간이 지날 때마다 백신 게이지 상승
# 게이지가 100%가 되면 백신 주사기 발사
# 주사기를 맞은 적 목숨 -1 (총 목숨 5개)
# 나의 목숨 총 3개

import pygame
from pygame.rect import *
import random


# game restart
def restart():
    global isActive, isGameOver, score, recPlayer, recVirus, virus, SCREEN_WIDTH, SCREEN_HEIGHT, enemy_hp
    isGameOver = False
    isActive = 0
    score = 0  # 점수 초기화
    enemy_hp = 5  # 적 목숨 초기화

    for i in range(len(virus)):  # 바이러스 위치 초기화
        recVirus[i].y = -1

    recPlayer.centerx = (SCREEN_WIDTH/2)  # player 위치 초기화
    recPlayer.centery = (SCREEN_HEIGHT-50)

    for j in range(len(hp)):  # player hp img 초기화
        recHp[j].x = SCREEN_WIDTH - 50 - (j*30)
        recHp[j].y = SCREEN_HEIGHT - recHp[j].height

    for j in range(len(hpe)):  # enemy hp img 초기화
        recHpe[j].x = SCREEN_WIDTH - 30 - (j*30)
        recHpe[j].y = recHpe[j].height - 10


# event 함수
def keyEvent():
    global score
    for event in pygame.event.get():  # pygame.event.get() -> 리스트 형태로 event를 전달
        if event.type == pygame.KEYDOWN:  # 아래방향이 아니라 키를 눌렀을 때 (땠을 때는 KEYUP)
            if event.key == pygame.K_ESCAPE:
                pygame.quit()  # esc를 눌렀을 때 게임을 quit
            elif event.key == pygame.K_LEFT:
                move.x = -1
            elif event.key == pygame.K_RIGHT:
                move.x = 1
            elif event.key == pygame.K_UP:
                move.y = -1
            elif event.key == pygame.K_DOWN:
                move.y = 1
            elif event.key == pygame.K_r:  # player hp =0 이 되었을 때 r 을 누르면 restart()
                restart()
            elif score == 2500:  # score(create vaccine) = 2500이 되면
                if event.key == pygame.K_SPACE:  # space bar를 눌러 vaccine shoot
                    makeSyringe()
                    score = 0

        elif event.type == pygame.KEYUP:            # 키보드를 누르지 않으면 움직임 멈추게 하기
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                move.x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                move.y = 0


##############################################################################################
##############################################################################################
# screen에 아이템들을 넣어주는 함수

def movePlayer():
    global isGameOver
    if not isGameOver:
        recPlayer.x += move.x
        recPlayer.y += move.y

    if recPlayer.x < 0:  # player의 움직임이 screen밖으로 벗어나지 않게 하기
        recPlayer.x = 0
    elif recPlayer.x > SCREEN_WIDTH - recPlayer.width:  # SCREEN_WIDTH = 400이고 player width = 40이기 때문에
        # player의 x좌표가 400을 넘어가서 멈추면 440이기 때문에 전체 너비에서 player width만큼 빼줘야한다
        recPlayer.x = SCREEN_WIDTH - recPlayer.width

    if recPlayer.y < 0:
        recPlayer.y = 0
    if recPlayer.y > SCREEN_HEIGHT-50:
        recPlayer.y = SCREEN_HEIGHT-50
    SCREEN.blit(player, recPlayer)

##############################################################################################
##############################################################################################
# 바이러스의 위치를 random하게 생성


def timeDelay():
    global time_delay

    if time_delay > 20:
        time_delay = 0
        return True

    time_delay += 1
    return False


def randomVirus():
    global isGameOver
    if isGameOver:
        return

    if timeDelay() == True:
        idex = random.randint(0, len(virus)-1)
        if recVirus[idex].y == -1:
            recVirus[idex].y = 40
            recVirus[idex].x = random.randrange(
                SCREEN_WIDTH-recVirus[0].width)


def moveVirus():
    global isGameOver

    randomVirus()

    for i in range(len(virus)):  # 여러개의 바이러스를 만들어주기
        if recVirus[i].y == -1:
            continue
        if not isGameOver:
            recVirus[i].y += 1
        if recVirus[i].y > SCREEN_HEIGHT:
            recVirus[i].y = 40
            recVirus[i].x = random.randrange(
                SCREEN_WIDTH-recVirus[0].width)  # x좌표를 다시 생성하기

        SCREEN.blit(virus[i], recVirus[i])

##############################################################################################
##############################################################################################
# syringe와 중국국기, virus와의 충돌


def checkCollisionSy():
    global score, isGameOver

    if isGameOver:
        return

    for rec in recVirus:
        if rec.y == -1:
            continue
        for recS in recSy:
            if rec.top < recS.bottom \
                    and recS.top < rec.bottom \
                    and rec.left < recS.right \
                    and recS.left < rec.right:
                rec.y = -1
                break


def makeSyringe():
    if isGameOver:
        return
    for i in range(len(syringe)):
        if recSy[i].y == -500:
            recSy[i].x = recPlayer.x-70
            recSy[i].y = recPlayer.y
            break


def moveSyringe():
    global enemy_hp
    for i in range(len(syringe)):  # 여러개의 바이러스를 만들어주기
        if recSy[i].y == -500:
            continue
        hpeImg()
        if not isGameOver:
            recSy[i].y -= 3  # 주사기가 날아가는 속도는 조금 더 빠르게
        if recSy[i].y < 0:
            recSy[i].y = -500
            enemy_hp -= 1
        if enemy_hp == 4:
            # 리스트에서 remove,delete가 안되서 enemy hp img 위치 다른 곳으로 날려버리기
            recHpe[4].y = 800
        if enemy_hp == 3:
            recHpe[3].y = 800
        if enemy_hp == 2:
            recHpe[2].y = 800
        if enemy_hp == 1:
            recHpe[1].y = 800
        if enemy_hp == 0:
            recHpe[0].y = 800
            # endingImg()
            # enemy_hp = 5

        SCREEN.blit(syringe[i], recSy[i])

##############################################################################################
##############################################################################################
# player와 virus의 충돌


def checkCollision():
    global score, isGameOver, player_hp, SCREEN_HEIGHT
    if isGameOver:
        return
    for rec in recVirus:

        if rec.y == -1:
            continue
        hpImg()

        if rec.top < recPlayer.bottom \
                and recPlayer.top < rec.bottom \
                and rec.left < recPlayer.right \
                and recPlayer.left < rec.right:  # recPlayer와 recVirus의 네모칸 위치 비교
            recPlayer.centerx = (SCREEN_WIDTH/2)  # 처음 시작 시 player의 x 좌표
            recPlayer.centery = (SCREEN_HEIGHT-50)
            player_hp -= 1  # 부딪히면 player 목숨 -1
            # 떨어지는 virus의 갯수가 많아지면 부딪힌 후 초기화된 player의 위치에 이미 virus가 있을 수도 있어 목숨을 바로 잃을 수도 있기 때문에
            # 부딪힌 후 초기화된 player위치 주변의 virus 지워주기
            for rec in recVirus:
                if rec.y > 350 and rec.x in range(100, 300):
                    rec.y = -1
        if player_hp == 2:
            recHp[0].y = 800
        if player_hp == 1:
            recHp[1].y = 800
        if player_hp == 0:
            recHp[2].y = 800
            isGameOver = True
            player_hp = 3


##############################################################################################
##############################################################################################
# gameover, score 화면에 표시

def setText():
    global isGameOver, score
    mFont = pygame.font.SysFont("arial", 20, True, False)  # 게임 내에서 사용될 기본 font

    if isGameOver:  # game over가 되면 안내문 생성
        SCREEN.blit(mFont.render(
            'Game Over!!', True, True, "red"), (150, 300, 0, 0))
        SCREEN.blit(mFont.render(
            'Press R - Restart', True, True, "red"), (140, 320, 0, 0))


def shootSy():
    global isGameOver, score
    mFont = pygame.font.SysFont("arial", 20, True, False)
    if isGameOver:
        return

    if score < 2500:
        score += 1
        SCREEN.blit(mFont.render(
            f'Creating Vaccine... : {round((score/2500)*100)}%', True, True, "green"), (10, SCREEN_HEIGHT-25, 0, 0))
    elif score == 2500:
        SCREEN.blit(mFont.render(
            f'Shoot Vaccine!!', True, "red", "yellow"), (10, SCREEN_HEIGHT-25, 0, 0))

##############################################################################################
##############################################################################################
# start 배경, 게임 중 배경, 플레이어와 적의 목숨 이미지, ending 배경


def startImg():
    nFont = pygame.font.SysFont('arial', 40, True, False)
    mFont = pygame.font.SysFont("arial", 20, True, False)  # 왜 글로벌로 안 가져와지냐..
    SCREEN.blit(start, recStart)
    SCREEN.blit(nFont.render(
        f'AVOID FUCKING VIRUS', True, "Red", False), (15, 60, 0, 0))
    SCREEN.blit(player1, recPlayer1)
    SCREEN.blit(mFont.render(
        f': player', True, "black"), (85, 150, 0, 0))
    SCREEN.blit(virus1, recVirus1)
    SCREEN.blit(mFont.render(
        f' : avoid this virus!', True, "black"), (80, 210, 0, 0))
    SCREEN.blit(hp1, recHp1)
    SCREEN.blit(mFont.render(
        f' : player\'s life X 3', True, "black"), (80, 280, 0, 0))
    SCREEN.blit(hpe1, recHpe1)
    SCREEN.blit(mFont.render(
        f': enemy\'s life X 5', True, "black"), (80, 350, 0, 0))
    SCREEN.blit(syringe1, recSy1)
    SCREEN.blit(mFont.render(
        f': Shoot Super Vaccine!(Press Space-bar)', True, "black"), (70, 420, 0, 0))
    SCREEN.blit(mFont.render(
        f'Press Enter to Start', True, "red", False), (125, 500, 0, 0))


def backgroundImg():
    SCREEN.blit(background, recBackground)


def hpImg():
    SCREEN.blit(hp[0], recHp[0])
    SCREEN.blit(hp[1], recHp[1])
    SCREEN.blit(hp[2], recHp[2])


def hpeImg():
    SCREEN.blit(hpe[0], recHpe[0])
    SCREEN.blit(hpe[1], recHpe[1])
    SCREEN.blit(hpe[2], recHpe[2])
    SCREEN.blit(hpe[3], recHpe[3])
    SCREEN.blit(hpe[4], recHpe[4])


def enemyImg():
    SCREEN.blit(enemy, recEnemy)


def endingImg():
    nFont = pygame.font.SysFont('arial', 40, True, False)
    mFont = pygame.font.SysFont("arial", 20, True, False)
    SCREEN.blit(ending, recEnding)
    SCREEN.blit(nFont.render(
        f' You Win!!', True, "black"), (140, 150, 0, 0))
    SCREEN.blit(mFont.render(
        f' Do you want to restart the game?', True, "black"), (80, 330, 0, 0))
    SCREEN.blit(mFont.render(
        f' Press Enter! ', True, "black"), (160, 350, 0, 0))


##############################################################################################
##############################################################################################

# 전역변수 만들기
gameLoop = 0
isActive = 0
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
move = Rect(0, 0, 0, 0)  # x,y,가로,세로
time_delay = 0
score = 0
isGameOver = False  # false면 게임 끝내기
player_hp = 3  # player 목숨은 3개
enemy_hp = 5  # enemy 목숨은 5개

# pygame 초기화
pygame.init()

##############################################################################################
##############################################################################################

# create screen
SCREEN = pygame.display.set_mode((400, 600))  # 튜플 형식으로 화면의 사이즈 설정
pygame.display.set_caption("Avoid Fucking Virus")  # 내 게임 창의 title


# create start Img
start = pygame.image.load(
    "avoidvirus\\img sources\\start.png")
start = pygame.transform.scale(start, (400, 600))
recStart = start.get_rect()

# create background
background = pygame.image.load(
    "avoidvirus\\img sources\\background.jpg")
recBackground = background.get_rect()
background_size = background.get_rect().size
background_width = background_size[0]
background_height = background_size[1]

# create ending Img
ending = pygame.image.load(
    "avoidvirus\\img sources\\ending.jpg")
ending = pygame.transform.scale(ending, (400, 600))
recEnding = ending.get_rect()

# make enemy
enemy = pygame.image.load(
    "avoidvirus\\img sources\\enemy.png")  # 이미지를 불러오기
enemy = pygame.transform.scale(enemy, (400, 80))  # 이미지 사이즈 설정(튜플)
recEnemy = enemy.get_rect()
recEnemy.centerx = SCREEN_WIDTH-200  # 처음 시작 시 player의 x 좌표
recEnemy.centery = 30

# make player
player = pygame.image.load(
    "avoidvirus\\img sources\\me.png")  # 이미지를 불러오기
player = pygame.transform.scale(player, (20, 20))  # 이미지 사이즈 설정(튜플)
recPlayer = player.get_rect()
recPlayer.centerx = (SCREEN_WIDTH/2)  # 처음 시작 시 player의 x 좌표
recPlayer.centery = (SCREEN_HEIGHT-50)         # y 좌표

player1 = pygame.image.load(
    "avoidvirus\\img sources\\me.png")  # start img에 쓰일 사진
player1 = pygame.transform.scale(player1, (50, 50))
recPlayer1 = player.get_rect()
recPlayer1.centerx = (45)
recPlayer1.centery = (150)


# make virus
virus = [pygame.image.load(
    "avoidvirus\\img sources\\virus.png") for i in range(50)]  # 이미지를 불러오기
recVirus = [None for i in range(len(virus))]
for i in range(len(virus)):
    virus[i] = pygame.transform.scale(virus[i], (20, 20))  # 이미지 사이즈 설정(튜플)
    recVirus[i] = virus[i].get_rect()
    # 처음 바이러스의 y값은 -1이다 떨어지는 virus가 랜덤한 idex를 돌면서 recVirus[idex].y == 0이 되게 바꿔준다 -> 안바뀌면 recVirus.y== -1 ="moveStar()에 걸려서 continue, 즉 떨어지지 않는다"
    recVirus[i].y = -1

virus1 = pygame.image.load(
    "avoidvirus\\img sources\\virus.png")
virus1 = pygame.transform.scale(virus1, (50, 50))
recVirus1 = virus1.get_rect()
recVirus1.centerx = (60)
recVirus1.centery = (220)

# make syringe
syringe = [pygame.image.load(
    "avoidvirus\\img sources\\syringe.png") for i in range(1)]  # 이미지를 불러오기
recSy = [None for i in range(len(syringe))]
for i in range(len(syringe)):
    syringe[i] = pygame.transform.scale(
        syringe[i], (150, 150))  # 이미지 사이즈 설정(튜플)
    recSy[i] = syringe[i].get_rect()
    recSy[i].y = -500

syringe1 = pygame.image.load(
    "avoidvirus\\img sources\\syringe.png")
syringe1 = pygame.transform.scale(syringe1, (50, 50))
recSy1 = syringe1.get_rect()
recSy1.centerx = (60)
recSy1.centery = (430)


# make player's hp
hp = [pygame.image.load(
    "avoidvirus\\img sources\\hp.png") for i in range(3)]
recHp = [None for i in range(len(hp))]
for i in range(len(hp)):
    hp[i] = pygame.transform.scale(hp[i], (25, 25))
    recHp[i] = hp[i].get_rect()
for j in range(len(hp)):
    recHp[j].x = SCREEN_WIDTH - 50 - (j*30)
    recHp[j].y = SCREEN_HEIGHT - recHp[j].height

hp1 = pygame.image.load(
    "avoidvirus\\img sources\\hp.png")
hp1 = pygame.transform.scale(hp1, (50, 50))
recHp1 = hp1.get_rect()
recHp1.centerx = (65)
recHp1.centery = (290)


# make enemy's hp
hpe = [pygame.image.load(
    "avoidvirus\\img sources\\virus2.png") for i in range(5)]
recHpe = [None for i in range(len(hpe))]
for i in range(len(hpe)):
    hpe[i] = pygame.transform.scale(hpe[i], (20, 20))
    recHpe[i] = hpe[i].get_rect()
for j in range(len(hpe)):
    recHpe[j].x = SCREEN_WIDTH - 30 - (j*30)
    recHpe[j].y = recHpe[j].height - 10

hpe1 = pygame.image.load(
    "avoidvirus\\img sources\\virus2.png")
hpe1 = pygame.transform.scale(hpe1, (50, 50))
recHpe1 = hpe1.get_rect()
recHpe1.centerx = (60)
recHpe1.centery = (360)


# necesaary code
# pygame에 시간을 부여해주는 Clock()   # pygame이 active될 때 cycle이 빨리 돌기 때문에 시간을 delay해 줄 필요가 있다.
clock = pygame.time.Clock()

##############################################################################################
##############################################################################################
while gameLoop == 0:
    while isActive == 0:
        startImg()
        restart()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif event.key == pygame.K_RETURN:
                    isActive = 1
        clock.tick(120)
        pygame.display.flip()

    while isActive == 1:
        # active events
        keyEvent()
        # active start img
        # active background img
        backgroundImg()
        # active enemy img
        enemyImg()
        # active enemy's hp img
        hpeImg()
        # active player move
        movePlayer()
        # active virus move
        moveVirus()
        # active missile(syringe)
        moveSyringe()
        # 충돌 감지
        checkCollisionSy()
        checkCollision()
        # score text
        shootSy()
        setText()
        if player_hp == 0:  # player의 목숨이 0이 되었을 때 r을 누르면 게임 다시 시작
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        restart()
        if enemy_hp == 0:
            isActive = 2
        clock.tick(120)  # milisecond 단위로 pygame을 delay시킴
        pygame.display.flip()

    while isActive == 2:  # ending 화면 보여주기
        endingImg()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif event.key == pygame.K_RETURN:      # enter 누르면 첫 화면으로 돌아가기
                    restart()
            if event.type == pygame.KEYUP:  # ending을 본 후 게임을 다시 시작하면 키보드를 누르고 있지 않아도 player가 움직이는 것을 방지
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    move.x = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    move.y = 0
        clock.tick(120)
        pygame.display.flip()
