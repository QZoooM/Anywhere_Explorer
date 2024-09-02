#小游戏-探险类
#Author:QZoooM
#This game is based on Pygame.
#if it leaks Pygame, it will go wrong. :(

'''
简单思路：
    这是一个冒险游戏，有四个有限长度的地图（丛林，沙漠，海洋，草原）
    还有一个无限随机地图和‘混乱’地图（仅供测试，后期也可以在开发者模式中打开）
    玩家将扮演探险者在提供的地图中冒险，获得探险经验
    创建新存档有初始图纸，得到的探险经验用于购买其他道具图纸，制作道具需要采集素材
'''
'''
（基本）元素：
    探险者(角色)·--to do33%
'''


#导入运行库
import pygame,random,time
from pygame.locals import *
#初始化Pygame模块
pygame.init()
#渲染基本信息(非常重要)
class Renderbase(object):
    def __init__(self):
        self.basefam = 72
        self.basetick = 0
        self.maxtick = 10000 #默认为“10000”
        self.tickspeed = 100 #默认为“100”,可在游戏内更改(1~10000)
        self.famcount = 0
        self.window_x = 720
        self.window_y = 480
        self.transparency = 100
        self.flowanime = 1 #过渡动画倍速
renderbase = Renderbase()
#创建窗口（视野）
pygame.display.set_caption("Anywhere Explorer")
window_size = (renderbase.window_x,renderbase.window_y)
window = pygame.display.set_mode(window_size)
#导入资源
print('Load images')
#-图组
#--背景
BGPath = "resource/img/BG/"
raw_BG_img=[]
BG_img=[]
raw_BG_img.append(pygame.image.load(BGPath+"Main_menu.png").convert_alpha())
for i in raw_BG_img:
    BG_img.append(pygame.transform.scale(i,(960, 480)))
#--方块
BlkPth="resource/img/Block/"
raw_Grass_img=[]
Grass_img=[]
raw_Grass_img.append(pygame.image.load(BlkPth+"Grass_Side.png").convert_alpha())
for i in raw_Grass_img:
    Grass_img.append(pygame.transform.scale(i,(48, 48)))
raw_Stone_img=[]
Stone_img=[]
raw_Stone_img.append(pygame.image.load(BlkPth+"Stone_Side.png").convert_alpha())
raw_Stone_img.append(pygame.image.load(BlkPth+"Stone_Up.png").convert_alpha())
Stone_img.append(pygame.transform.scale(raw_Stone_img[0],(48, 48)))
Stone_img.append(pygame.transform.scale(raw_Stone_img[1],(48, 32)))
raw_Wood_img=[]
Wood_img=[]
raw_Wood_img.append(pygame.image.load(BlkPth+"Wood_Side.png").convert_alpha())
for i in raw_Wood_img:
    Wood_img.append(pygame.transform.scale(i,(48, 48)))
#--角色
Char00_img=[]
Char00Path="resource/img/Char/Char00"
Char00_img.append(pygame.image.load(Char00Path+".png").convert_alpha())
Char00_img.append(pygame.image.load(Char00Path+"_Body.png").convert_alpha())
Char00_img.append(pygame.image.load(Char00Path+"_Head.png").convert_alpha())
#设置图片透明度
#image.set_alpha(128)
#--按钮
BtnPath="resource/img/Button/"
empty=[]
empty.append(pygame.image.load(BtnPath+"empty.png"))
raw_Btn_img=[]
Btn_img=[]
raw_Btn_img.append(pygame.image.load(BtnPath+"Button0.png"))
for i in raw_Btn_img:
    Btn_img.append(pygame.transform.scale(i,(144, 48)))
Btn_img.append(pygame.image.load(BtnPath+"Box_ui.png"))

#-音频
print('Load audio')
DA="resource/ado/Dream_Away.mp3"
def StopThanStartAudio(DA):
    if pygame.mixer.get_busy() == True:
        pygame.mixer.stop()
    BGM=pygame.mixer.Sound(DA)
    channal=BGM.play(-1)
    BGM.set_volume(0.195)
#-字体
print('Load fonts...')
fotPath = "resource/fot/"
fotList=["minisimple","web85W"]
fot=[]
for i in fotList:
    fot.append(fotPath+i+".ttf")
print('Done!')
pygame.display.set_icon(Char00_img[0])
#创建的对象/变量
#-大类
class DevVar(object):
    def __init__(self):
        self.DevMode = 1
devvar = DevVar()
#0=就绪/正在执行;1=完成;2=等待
class Startrd(object):
    def __init__(self):
        self.window = 0
        self.dtext = 2
        self.text = "Click to start!!"
        self.sttick = 0
        self.tomn = 2
startrd = Startrd()
class Menurd(object):
    def __init__(self):
        self.window = 0
        self.mntick = 0
        self.inma = 0
        self.main = 2
        self.goto = 0
menurd = Menurd()

class Blocks(object): #48x48
    def __init__(self,x,y,width,height,type,life,score,ticks,baseTickCount):
        self.x = x

change = 1
class Chars(object): #Whole:27x45;Head:27x21;Body:27x24.
    def __init__(self,x,y,z,width,height,up,surf,type,life,upab=0,dwab=0,lfab=0,rtab=0,speed=1):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.up = up
        self.surf = surf
        self.type = type
        self.life = life
        self.upab = upab
        self.dwab = dwab
        self.lfab = lfab
        self.rtab = rtab
        self.speed = speed
    #绘制角色
    def paint(self):
        window.blit(self.surf[0],(self.x - self.width/2,self.z - self.height))
    #角色碰撞:26x40下横边&中纵轴
    def hitbox(self):
        hit_up = self.z - self.height + 7
        if hit_up <= 240:
            self.upab = 0
        hit_dw = self.z
        if hit_dw >= renderbase.window_y - 48:
            self.dwab = 0
        hit_lf = self.x - self.width/2 + 0.5
        if hit_lf <= 0:
            self.lfab = 0
        hit_rt = self.x + self.width/2 - 0.5
        if hit_rt >= renderbase.window_x:
            self.rtab = 0
    def move(self):
        if self.upab == 1:
            self.z -= 0.66
        if self.dwab == 1:
            self.z += 0.66
        if self.lfab == 1:
            self.x -= 1
        if self.rtab == 1:
            self.x += 1
        #print((self.x,self.y))
        
    def anima(self):
        pass


class Background(object):
    def __init__(self,x,y,width,height,movespeed) -> None:
        pass

class ButtonCTRL(object):
    def __init__(self,x,y,width,height,surf,func="",text="",txtcl=(0,0,0),alpha=255,rfkey=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surf = surf
        self.func = func
        self.text = text
        self.txtcl = txtcl
        self.alpha = alpha
        self.rfkey = rfkey
        self.behave = 0
        self.ticks = 0
        self.baseTickCount = 0
        self.BEHAVE = {"TO_MENU":0}
    def bhv(self):
        if self.behave == self.BEHAVE[0]:
            pass

#-小类（定义方法的地方）
#--单个方块
class block():
    def __init__(self,x,y,width,height,up,type,life,score,ticks,baseTickCount):
        Blocks.__init__(self,x,y,width,height,up,life,ticks,baseTickCount)
        self.x = x
        self.y = y
        self.width = 48 #方块长
        self.height = 48 #方块高
        self.up = 36
        self.type = type
        self.score = score 

#--初始角色
change = 1
class Char(Chars):
    def __init__(self,x,y,z,width,height,up,surf,type,life,upab,dwab,lfab,rtab,speed):
        Chars.__init__(self,x,y,z,width,height,up,surf,type,life,upab,dwab,lfab,rtab,speed)

#--按钮
class Buttons(ButtonCTRL):
    def __init__(self,x,y,width,height,surf,func,text,txtcl,alpha,rfkey):
        ButtonCTRL.__init__(self,x,y,width,height,surf,func,text,txtcl,alpha,rfkey)
buttons = Buttons
buttons=[]


#使用类属性存储游戏中的变量，以减少全局变量的数量
change = 1
class GameVar(object):
    wait = 0
    sky = None
    blocks = []
    chars = []
    lastTime = 0
    interval = 1#单位为秒
    paintLastTime = 0
    paintInterval = 0.04
    #分数和生命值
    score = 0
    lives = 5
    #控制游戏状态
    STATES = {"START_UP":1,"MENU":2,"SELECT":3,"STORE":4,"GAMING":5,"PAUSE":6,"FLOW_ANIMA":100,}
    state = STATES["START_UP"]

GameVar.chars = Char
GameVar.chars=[]

class R_W_Saves():
    read = None
    write = None

#-零散的(尽量少)
j1 = 0

#创建的函数

#工具方法-判断时间间隔是否到了
def isActionTime(lastTime,interval):
    if lastTime == 0:
        return True
    currentTime = time.time()
    return currentTime - lastTime >= interval

#-效果
class RenderEffect():
    def __init__(self):
        self.crtimes = 0
        self.ot_x = -10000
        self.ot_y = -10000
    #--闪烁(带频率，幅度，变化模式，次数，单位刻输入)
    def twinkling(self):
        #if 
        pass
    #--震动(频率，x位，y位，x幅度，y幅度，变化模式，单位刻输入)
    def vibrating(self,freq,x,y,amount_x,amount_y,mode,tick):
        if mode == 1:
            yestick = round(((1/freq)*renderbase.maxtick*renderbase.tickspeed*self.crtimes)/300)
            if yestick <= tick:
                self.ot_x = x + random.randint(-amount_x,amount_x)
                self.ot_y = y + random.randint(-amount_y,amount_y)
                self.crtimes = self.crtimes + 1
                position = (int(self.ot_x),int(self.ot_y))
                return position
            else:
                position = (int(self.ot_x),int(self.ot_y))
                return position

rendereffect = RenderEffect()

change = 1
BtFunc=[]
BtFunc000='''startrd.tomn = 0
startrd.sttick = 256
GameVar.wait = 0
startrd.dtext = 1'''
BtFunc001='''menurd.goto = 1'''
BtFunc002='''menurd.goto = 0'''
BtFunc003=''''''
BtFunc004='''GameVar.state = GameVar.STATES["GAMING"]\ngamingrd.init = 0'''
BtFunc005='''gamingrd.tosl = 0\ngamingrd.tomn = 0'''

BtFunc.append(BtFunc000)
BtFunc.append(BtFunc001)
BtFunc.append(BtFunc002)
BtFunc.append(BtFunc003)
BtFunc.append(BtFunc004)
BtFunc.append(BtFunc005)

#-事件侦测总线
def handleEvent():
    for event in pygame.event.get():
        #print(event)
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == WINDOWMINIMIZED:
            pygame.mixer.pause()
        elif event.type == WINDOWRESTORED:
            pygame.mixer.unpause()
        #按钮交互[点击后松开]
        if event.type == MOUSEBUTTONUP and event.button==1:
            for i in buttons:
                if event.pos[0] > i.x and event.pos[0] < i.x+i.width and event.pos[1] > i.y and event.pos[1] <i.y+i.height:
                    exec(i.func)
        #点击左键切换为运行状态
        if event.type == MOUSEBUTTONDOWN and event.button==1:
            pass
        if event.type==KEYDOWN:
            for i in buttons:
                if i.rfkey == event.key:
                    exec(i.func)
            #根据键盘的操作控制角色的坐标并触发相应的动画-输入控制器-预期WASD和箭头两种控制选项
            for i in GameVar.chars:
                if GameVar.state == GameVar.STATES["GAMING"] and gamingrd.run == 0:
                    if event.key == K_w:
                        i.upab = 1
                    if event.key == K_a:
                        i.lfab = 1
                    if event.key == K_s:
                        i.dwab = 1
                    if event.key == K_d:
                        i.rtab = 1
        if event.type==KEYUP:
            for i in GameVar.chars:
                if GameVar.state == GameVar.STATES["GAMING"] and gamingrd.run == 0:
                    if event.key == K_w:
                        i.upab = 0
                    if event.key == K_a:
                        i.lfab = 0
                    if event.key == K_s:
                        i.dwab = 0
                    if event.key == K_d:
                        i.rtab = 0




#碰撞侦测

#碰撞侦测总线
def CheckHit():
    #角色碰撞
    for i in GameVar.chars:
        Char.hitbox(i)




#组件移动

#组件移动总线
def element_move():
    #角色移动
    for i in GameVar.chars:
        Char.move(i)


#渲染文本
def renderText(text,cl,A,position,size,fot = fot[0],view = window):
    my_font = pygame.font.Font(fot,size)
    text = my_font.render(text,True,cl).convert_alpha()
    text.set_alpha(A)
    view.blit(text,position)


#元素绘制
#-背景绘制

#-组件绘制
#--按钮绘制
def renderButtons():
    for i in buttons:
        img = pygame.transform.scale(i.surf,(i.width,i.height))
        img.set_alpha(i.alpha)
        my_font = pygame.font.Font(fot[1],round(i.height*0.5))
        text = my_font.render(i.text,True,(50,50,50)).convert_alpha()
        siz = text.get_size()
        if siz[0] >= i.width - 4:
            scltext=pygame.transform.scale(text,(i.width-4, (i.width-4)*siz[1]/siz[0]))
        if siz[1] >= i.height - 2:
            scltext=pygame.transform.scale(text,((i.height-2)*siz[0]/siz[1], i.height-2))
        if not siz[0] >= i.width - 4 or not siz[1] >= i.height - 2:
            scltext=text
        sclsiz = scltext.get_size()
        pos = (i.x+i.width/2-sclsiz[0]/2,i.y+i.height/2-sclsiz[1]/2)
        scltext.set_alpha(i.alpha)
        window.blit(img,(i.x,i.y))
        window.blit(text,pos)


def rendercomponents():
    renderButtons()
    


#元素绘制总线
def renderelement():
    rendercomponents()


#-渲染启动界面
buttons.append(ButtonCTRL(658,0,64,32,empty[0],BtFunc[0],'Skip>>',(150,150,150)))
def render_start_up():
    if GameVar.state == GameVar.STATES["START_UP"]:
        startrd.window = 1
        buttons.clear()
        ta = 255
        Stone_img[0].set_alpha(ta)
        Stone_img[1].set_alpha(ta)
        Btn_img[0].set_alpha(0)
        BG_img[0].set_alpha(ta*2/3)
        #StopThanStartAudio(DA)
        GameVar.state = GameVar.STATES["MENU"]
        GameVar.wait = 0
        menurd.main = 0

#-渲染菜单2界面
def render_menu():
    if GameVar.state == GameVar.STATES["MENU"]:
        if menurd.main == 0:
            buttons.clear()
            buttons.append(ButtonCTRL(40,40,640,430,Btn_img[1]))
            buttons.append(ButtonCTRL(70,65,580,80,Btn_img[1],BtFunc[4],"Char Test",(50,50,50),255,K_1))
            buttons.append(ButtonCTRL(70,150,580,80,Btn_img[1],"print('Being Built now!!!')","Save Test",(50,50,50),255,K_2))
            buttons.append(ButtonCTRL(70,235,580,80,Btn_img[1],"print('Being Built now!!!')","Save 01",(50,50,50),255,K_3))
            buttons.append(ButtonCTRL(70,320,580,80,Btn_img[1],"print('Being Built now!!!')","++Add New One++",(50,50,50),255,K_4))
            #buttons.append(ButtonCTRL(40,5,60,30,Btn_img[0],BtFunc[2],"<Back",(50,50,50),255,K_ESCAPE))
            menurd.goto = 1
            menurd.main = 1
        if menurd.main == 1 and menurd.goto == 1:
            cl=255
            window.fill((cl,cl,cl))
            window.blit(BG_img[0],(0,0))
        # elif menurd.main == 1 and menurd.goto == 0:
        #     buttons.clear()
        #     buttons.append(ButtonCTRL(286,180,144,48,Btn_img[0],BtFunc[1],"Start",(50,50,50)))
        #     menurd.main = 0

change = 1
#-临时TEST存档

change = 1
class Selectrd(object):
    def __init__(self):
        self.reading = 2
        self.writing = 2
selectrd = Selectrd()
#-渲染存档操作3界面
def render_select():
    if GameVar.state == GameVar.STATES["SELECT"]:
        #扫描对应存档

        pass

class Gamingrd(object):
    def __init__(self):
        self.init = 0
        self.window = 2
        self.run = 2
        self.tomn = 2
        self.tosl = 2
gamingrd = Gamingrd()
#-渲染游戏4界面
def render_gaming():
    if GameVar.state == GameVar.STATES["GAMING"]:
        if gamingrd.init == 0:
            buttons.clear()
            buttons.append(ButtonCTRL(5,5,60,30,Btn_img[0],BtFunc[5],"<Back",(50,50,50),255,K_ESCAPE))
            GameVar.chars.append(Chars(120,0,432,27,45,26,Char00_img,0,1))
            gamingrd.init = 1
        elif gamingrd.init == 1:
            gamingrd.run = 0
        if gamingrd.run == 0:
            window.fill((250,250,250))
            window.blit(BG_img[0],(0,0))
            for i in range(0,15):
                for j in range(0,6):
                    if j < 5:
                        window.blit(Stone_img[1],(0+48*i,272+32*j))
                    if j == 5:
                        window.blit(Stone_img[0],(0+48*i,432))
        if gamingrd.tomn == 0:
            buttons.clear()
            GameVar.chars.clear()
            buttons.append(ButtonCTRL(40,40,640,430,Btn_img[1]))
            buttons.append(ButtonCTRL(70,65,580,80,Btn_img[1],BtFunc[4],"Char Test",(50,50,50),255,K_1))
            buttons.append(ButtonCTRL(70,150,580,80,Btn_img[1],"print('Being Built now!!!')","Save Test",(50,50,50),255,K_2))
            buttons.append(ButtonCTRL(70,235,580,80,Btn_img[1],"print('Being Built now!!!')","Save 01",(50,50,50),255,K_3))
            buttons.append(ButtonCTRL(70,320,580,80,Btn_img[1],"print('Being Built now!!!')","++Add New One++",(50,50,50),255,K_4))
            gamingrd.tomn = 1
            GameVar.state = GameVar.STATES["MENU"]
            menurd.goto = 1
            menurd.main = 1

            


change = 1
#角色渲染Char
def renderChars():
    for i in GameVar.chars:
        #print(i.surf[0])
        Char.paint(i)



#-游戏内图层渲染先后
def gamingrender():
    renderChars()
    pass


#-渲染窗口总线
def renderwindow():
    #界面渲染控制
    if GameVar.wait == 0:
        render_start_up()
        render_menu()
        render_gaming()
    #组件渲染（此if便于停止）
    if GameVar.wait == 0:
        renderelement()
        gamingrender()
    frameupd(renderbase.basefam)
#帧更新
def frameupd(fps):
    pygame.display.update()
    fps = fps

#总线(尽量简洁)
while True:
    handleEvent()
    CheckHit()
    element_move()
    renderwindow()
    if j1 == 1:
        exit()
    #time.sleep((1/renderbase.maxtick)/renderbase.tickspeed)


