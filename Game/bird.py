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

class Boss(pygame.sprite.Sprite):
    def __init__(self,boss_surface,boss_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = boss_position
        self.speed = 1
        self.health = 49
        self.isDead = False
        self.jiguangs = pygame.sprite.Group()
    def move(self):
        position_x = self.rect.left + self.speed
        if position_x >370:
            self.rect.left = 370
            self.speed = -1
        elif position_x <-40:
            self.rect.left = -40
            self.speed = 1
        else:
            self.rect.left = position_x
    def singleShot_Left(self,jiguang1_image):
        jiguang1 =Jiguang(jiguang1_image,(self.rect.left-50,self.rect.top+45))#控制发射位置
        self.jiguangs.add(jiguang1)
    def singleShot_Right(self,jiguang1_image):
        jiguang1 = Jiguang(jiguang1_image, (self.rect.right + 50, self.rect.top + 45))  # 控制发射位置
        self.jiguangs.add(jiguang1)


class Jiguang(pygame.sprite.Sprite):
    def __init__(self,shots_surface,shots_position):
        pygame.sprite.Sprite.__init__(self)
        self.image = shots_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = shots_position
        self.speed = 5
    def update(self):
        self.rect.top += self.speed
        if self.rect.top>SCREEN_HEIGHT+50:
            self.kill()

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
        bsk1 = Basketball(bsk1_image,(self.rect.left+33,self.rect.top+40))#控制发射位置
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
#载入游戏胜利画面
win = pygame.image.load('resources/images/win.png')
#载入弟弟画面
didi = pygame.image.load('resources/images/didi.png')
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
#载入boss画面
boss_image = pygame.image.load('resources/images/xc.png')
boss_dead_image = pygame.image.load('resources/images/heibai_xc.png')
#载入激光图片
jiguang_image = pygame.image.load('resources/images/timg.gif')
#设置字体
score = 0
pygame.font.init()
score_font = pygame.font.SysFont(None,32)
score_font.set_bold(True)
#载入各种音效
ji_sound = pygame.mixer.Sound('resources/audios/ji.ogg')
si_sound = pygame.mixer.Sound('resources/audios/si.ogg')
#载入背景音乐
pygame.mixer.music.load('resources/audios/bgm.mp3')
pygame.mixer.music.play(-1)
#设置错过的灭霸数量
missed = 0
missed_font = pygame.font.SysFont(None,32)
missed_font.set_bold(True)
#将boss实例化
sxc = Boss(boss_image,(1,50))
#设置一个变量来判断结局的显示
#0表示变鸡结局，1表示胜利结局，2表示被boss打败结局
ending = 0

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
    if cxk.isJi:
        cxk.image = ji_image
        si_sound.play()
        countdown+=1
        if countdown == 40:
            pygame.mixer.music.stop()#结束游戏后停止背景音乐
            ending = 0
            break#变成鸡后退出循环
    else:
        cxk.image = cxk_image
    #更新篮球图片
    cxk.bsks.update()
    cxk.bsks.draw(screen)
    #产生灭霸图片
    if ticks % 60 == 0 and score<990:
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
        t.speed = 0
        #绑定孙笑川图片
        screen.blit(sxc.image,sxc.rect)
        # 绑定激光画面
        sxc.jiguangs.update()
        sxc.jiguangs.draw(screen)
        #移动
        sxc.move()
        #发射激光
        if ticks % 90==0:
            sxc.singleShot_Left(jiguang_image)
            sxc.singleShot_Right(jiguang_image)
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
    #解决boss
    bossdead_down_list = pygame.sprite.spritecollide(sxc,cxk.bsks,True)
    if len(bossdead_down_list) > 0:
        sxc.health-=1
        if sxc.health == 0:
            sxc.isDead = True
            ending = 1
            sxc.health = 10
    if sxc.isDead:
        sxc.image = boss_dead_image
        countdown += 1
        if countdown == 40:
            pygame.mixer.music.stop()  # 结束游戏后停止背景音乐
            ending = 1
            break  #打败boss后退出循环,并将结局画面设为1
    else:
        sxc.image = boss_image
    #被哥哥打死
    bosswin_down_list = pygame.sprite.spritecollide(cxk,sxc.jiguangs,True)
    if len(bosswin_down_list)>0:
        ending = 2
        break  # 被打败boss后退出循环,并将结局画面设为2

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
if ending==0:
    screen.blit(gameover,(0,0))
    pygame.mixer.music.load('resources/audios/dead.mp3')
    pygame.mixer.music.play()
elif ending==1:
    screen.blit(win, (0, 0))
    pygame.mixer.music.load('resources/audios/fuchou.mp3')
    pygame.mixer.music.play()
else:
    screen.blit(didi, (0, 0))
    pygame.mixer.music.load('resources/audios/loneliness.ogg')
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
