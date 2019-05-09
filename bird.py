import pygame
from pygame.locals import *
from random import randint
from sys import exit

class Basketball(pygame.sprite.Sprite):
    def __init__(self,basket_surface,basket_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = basket_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = basket_position
        self.speed = 8

    def update(self):
        self.rect.top -= self.speed
        if(self.rect.top<-10):
            self.kill()

class Thanos(pygame.sprite.Sprite):
    def __init__(self,thanos_surface,thanos_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = thanos_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = thanos_position
        self.speed = 2
    def update(self):
        self.rect.top += self.speed
        if self.rect.top>SCREEN_HEIGHT:
            self.kill()
            global score
            score-=10
            global missed
            missed+=1


class CXK(pygame.sprite.Sprite):
    def __init__(self,cxk_surface,cxk_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = cxk_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = cxk_position
        self.speed = 5
        self.isJi = False
        self.bsks = pygame.sprite.Group()

    def move(self,offset):
        # 改变cxk的位置，并做边缘判断
        offset_x = offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
        offset_y = offset[pygame.K_DOWN] - offset[pygame.K_UP]
        # 横向边缘判断
        cxk_position_x = cxk.rect.left + offset_x
        if cxk_position_x < 0:
            cxk.rect.left = 0
        elif cxk_position_x > 400:
            cxk.rect.left = 400
        else:
            cxk.rect.left = cxk_position_x
        # 纵向边缘判断
        cxk_position_y = cxk.rect.top + offset_y
        if cxk_position_y < 150:
            cxk.rect.top = 150
        elif cxk_position_y > 700:
            cxk.rect.top = 700
        else:
            cxk.rect.top = cxk_position_y

    def singleShoot(self,bsk1_image):
        bsk1 = Basketball(bsk1_image,(self.rect.left+58,self.rect.top+45))#控制发射位置
        self.bsks.add(bsk1)




SCREEN_WIDTH = 600
SCREEN_HEIGHT = 900

offset={pygame.K_LEFT:0, pygame.K_RIGHT:0, pygame.K_UP:0, pygame.K_DOWN:0}

pygame.init()
pygame.mixer.init()
pygame.time.delay(1000)

clock = pygame.time.Clock()
screen =  pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
pygame.display.set_caption("练习时长两年半的（打飞机）练习生")#标题

ticks = 0
#载入背景
background=pygame.image.load('resources/images/bg.png')
#载入游戏结束画面
gameover = pygame.image.load('resources/images/gameover.png')
#载入主角cxk的图片并设置初始位置
cxk_image = pygame.image.load('resources/images/cxk.png')
cxk_position = [200,650]
#死亡时变鸡的图片及游戏结束倒计时
ji_image = pygame.image.load('resources/images/ji.png')
countdown = 0
#实例化主角cxk
cxk = CXK(cxk_image,cxk_position)
#载入篮球图片
bsk_image = pygame.image.load('resources/images/basket.png')
#载入敌人图片
thanos_image = pygame.image.load('resources/images/thanos.png')
thanos_group = pygame.sprite.Group()
thanos_down_group = pygame.sprite.Group()
#设置字体
score = 0
pygame.font.init()
score_font = pygame.font.SysFont(None,32)
score_font.set_bold(True)
#载入射击
ji_sound = pygame.mixer.Sound('resources/audios/ji.ogg')
si_sound = pygame.mixer.Sound('resources/audios/si.ogg')
#载入背景音乐
pygame.mixer.music.load('resources/audios/bgm.mp3')
pygame.mixer.music.play(-1)
#设置错过的灭霸数量
missed = 0
missed_font = pygame.font.SysFont(None,32)
missed_font.set_bold(True)

while True:


    #设置帧率
    clock.tick(90)
    #绑定背景图片
    screen.blit(background,(0,0))
    #设置分数面板
    ScoreFaceText = score_font.render("Score:"+str(score),True,(0,0,0))
    Scoretext = ScoreFaceText.get_rect()
    Scoretext.topleft = (10,10)
    screen.blit(ScoreFaceText,Scoretext)
    #设置miss面板
    MissedFaceText = missed_font.render("Missed:"+str(missed)+" (5 to die)",True,(0,0,0))
    Missedtext = MissedFaceText.get_rect()
    Missedtext.topleft = (10,40)
    screen.blit(MissedFaceText,Missedtext)
    #绑定人物图片
    if cxk.isJi :
        cxk.image = ji_image
        si_sound.play()
        countdown+=1
        if countdown == 40:
            pygame.mixer.music.stop()#结束游戏后停止背景音乐
            break#变成鸡后退出循环
    else:
        cxk.image = cxk_image
    #更新篮球图片
    cxk.bsks.update()
    cxk.bsks.draw(screen)
    #产生灭霸图片
    if ticks % 60 == 0:
        t = Thanos(thanos_image,[randint(0,SCREEN_WIDTH-thanos_image.get_width()),thanos_image.get_height()])
        thanos_group.add(t)
    #根据得分增加游戏难度
    if 200<=score<=400:
        t.speed = 3
    elif 400<score<=500:
        t.speed = 4
    elif 500<score<=1000:
        t.speed = 5
    elif score>1000:
        t.speed = 8
    thanos_group.update()
    thanos_group.draw(screen)
    #击毁并计分
    pre = len(thanos_down_group)
    thanos_down_group.add(pygame.sprite.groupcollide(thanos_group,cxk.bsks,True,True))
    if len(thanos_down_group)>pre:
        score+=10
    #坠鸡
    thanos_down_list = pygame.sprite.spritecollide(cxk,thanos_group,True)
    if len(thanos_down_list)>0:
        thanos_down_group.add(thanos_down_list)
        cxk.isJi = True
    #当missed大于5时，退出游戏
    if missed>=5:
        cxk.isJi = True
    screen.blit(cxk.image,cxk.rect)
    ticks+=1
    pygame.display.update()

    for event in pygame.event.get():
        #处理游戏退出
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        #检测按键
        if event.type == pygame.KEYDOWN:
            if event.key in offset:
                offset[event.key] = cxk.speed
            elif event.key == pygame.K_a:
                cxk.singleShoot(bsk_image)
                ji_sound.play()
        elif event.type == pygame.KEYUP:
            if event.key in offset:
                offset[event.key] = 0

    cxk.move(offset)

#跳出前一段循环,进入游戏结束画面
screen.blit(gameover,(0,0))
pygame.mixer.music.load('resources/audios/dead.mp3')
pygame.mixer.music.play()
while True:
    pygame.display.update()
    #显示最后得分
    score_font = pygame.font.SysFont(None, 72)
    ScoreFaceText = score_font.render("Final Score:" + str(score), True, (0, 0, 0))
    Scoretext = ScoreFaceText.get_rect()
    Scoretext.topleft = (130, 140)
    screen.blit(ScoreFaceText, Scoretext)
    #退出界面
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
