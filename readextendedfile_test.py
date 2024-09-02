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
TO_DO_LIST
（基本）素材---to do05%
（基本）渲染帧机制---to do??%
（基本）界面：---to do20%
    开始动画&互动[Done]
    菜单[Done]
    设置界面---to do
    选图界面---to do
    游戏界面(2.5D)
（基本）界面图形动画---to do??%
（基本）元素：
    按钮[Done]
    探险者··-75%
    方块---to do
    遮挡物透明化渲染---to do
    （增强）特殊生物：就像Boss一样的
（基本）将设计背景和方块构成地图的部分(地图前后5;高度3;宽度视情况而定(先128)))---to do
（基本）地图格式：5*3*16n --> 16*4*16n --> 16n*4*16n --> 16∞*256*16∞
（基本）存档系统---to do
（基本）经验与商店系统---to do
（增强）地图外部储存---to do
（增强）探险者将有多个可选外观
（增强）按钮交互动画
（增强）2DLive
（增强）随机地图16∞*256*16∞设计
（增强）‘混乱’地图16n*4*16n设计
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
        self.EnTkSpd = 0
        self.maxtick = 10000 #默认为“10000”
        self.tickspeed = 100 #默认为“100”,可在游戏内更改(1~10000)
        self.famcount = 0
        self.window_x = 720
        self.window_y = 480
        self.transparency = 100
        self.flowanime = 1 #过渡动画倍速
renderbase = Renderbase()
#基础音频信息
class Ifpl(object):
    def __init__(self):
        self.pl = 1
ifpl = Ifpl()
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
    ifpl.pl = 1
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
#-类
class DevVar(object):
    def __init__(self):
        self.DevMode = 1
devvar = DevVar()

class Background(object):
    def __init__(self,fill_cl,x,y,width,height,surf,movespeed):
        self.fill_cl = fill_cl
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surf = surf
        self.movespeed = movespeed
    def move(self):

        pass

class Blocks(object): #48x48,46*32;x-->width,y-->height,z-->depth
    def __init__(self,x,y,z,width,height,depth,surf):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.depth = depth
        self.surf = surf

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
        window.blit(self.surf[0],(self.x*48 - self.width/2,renderbase.window_y - self.z*32 - self.y*48 - self.height + 1))
    #角色碰撞:26x40下横边&中纵轴
    def hitbox(self):
        hit_up = renderbase.window_y - self.z*32 - 10
        if hit_up <= renderbase.window_y - 160:
            self.upab = 0
        hit_dw = renderbase.window_y - self.z*32 + 6
        if hit_dw >= renderbase.window_y:
            self.dwab = 0
        hit_lf = self.x*48 - 13
        if hit_lf <= 0:
            self.lfab = 0
        hit_rt = self.x*48 + 13
        if hit_rt >= renderbase.window_x:
            self.rtab = 0
    def move(self):
        if self.upab == 1:
            self.z += 0.02
        if self.dwab == 1:
            self.z -= 0.02
        if self.lfab == 1:
            self.x -= 0.02
        if self.rtab == 1:
            self.x += 0.02
        #print((self.x,self.y,self.z))

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

class Txts(object):
    def __init__(self,text,cl,A,position,size,fot = fot[0],view = window):
        self.text = text
        self.cl = cl
        self.A = A
        self.position = position
        self.size = size
        self.fot = fot
        self.view = view
txts=[]
#-支类
#--单个方块
class Block(Blocks):
    def __init__(self,x,y,z,width,height,depth,):
        Blocks.__init__(self,x,y,z,width,height,depth,)
block = Block

#--按钮
class Buttons(ButtonCTRL):
    def __init__(self,x,y,width,height,surf,func="",text="",txtcl=(0,0,0),alpha=250,rfkey=None):
        ButtonCTRL.__init__(self,x,y,width,height,surf,func,text,txtcl,alpha,rfkey)
    def paint(self):
        i = self
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
buttons=[] #按钮列表

#使用类属性存储游戏中的变量，以减少全局变量的数量
class GameVar(object):
    wait = 0
    bg = None
    blocks = None
    chars = None
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

GameVar.bg = Background((0,0,0),0,0,960,480,empty[0],0)
GameVar.blocks = Block
GameVar.blocks=[]
#GameVar.chars = Chars
GameVar.chars=[]
#-零散的(尽量少)

#创建的函数

#工具方法-判断时间间隔是否到了
def isActionTime(lastTime,interval):
    if lastTime == 0:
        return True
    currentTime = time.time()
    return currentTime - lastTime >= interval

#-效果
class RenderEffect(object):
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

#-输入控制器-预期WASD和箭头两种控制选项
class Mvab(object):
    def __init__(self,charmvx_ad,charmvx_mi,charmvy_ad,charmvy_mi):
        self.charmvx_ad = charmvx_ad
        self.charmvx_mi = charmvx_mi
        self.charmvy_ad = charmvy_ad
        self.charmvy_mi = charmvy_mi
mvab = Mvab(0,0,0,0)

#设置布局变量类，作为layout.ini的规范
class Layout(object):
    def __init__(self,start,menu,sav,store,gaming,pause):
        self.start=start
        self.menu=menu
        self.sav=sav
        self.store=store
        self.gaming=gaming
        self.pause=pause
layout = Layout([],[],[],[],[],[]) #列表打包导入的layout，通过layout.~[~]调用指令
#按钮功能存储
BtFunc=[]
BtTest=[]
BtTest000='''GameVar.state = GameVar.STATES["GAMING"]\ngamingrd.init = 0'''
BtTest001='''gamingrd.tosv = 0\ngamingrd.tomn = 0'''
BtTest002=''''''
BtTest003=''''''
BtTest.append(BtTest000)
BtTest.append(BtTest001)
with open("config/layout.ini") as f: #读取layout.ini，存储各布局初始化的指令，比如：向列表加入背景、按钮、文字
    exec(f.read()) #layout.ini由指令构成

#-事件侦测总线
def handle_event():
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
            if GameVar.state == GameVar.STATES["START_UP"] and startrd.dtext == 1:
                startrd.dtext = 2
                startrd.sttick = 0
                startrd.tomn = 0
                GameVar.wait = 0
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
        #
        #按下ESC进入[PUASE]或者仅唤出暂停的界面

#碰撞侦测

#碰撞侦测总线
def check_hit():
    #角色碰撞
    for i in GameVar.chars:
        i.hitbox()

#组件移动总线
def element_move():
    #角色移动
    for i in GameVar.chars:
        i.move()


#渲染文本
def renderText(text,cl,A,position,size,fot = fot[0],view = window):
    my_font = pygame.font.Font(fot,size)
    text = my_font.render(text,True,cl).convert_alpha()
    text.set_alpha(A)
    view.blit(text,position)

def renderTexts():
    for i in txts:
        renderText(i.text,i.cl,i.A,i.position,i.size,i.fot,i.view)

#元素绘制
#-背景绘制

#-组件绘制
def rendercomponents():
    #--按钮绘制
    for i in buttons:
        i.paint()
    

#元素绘制总线
def renderelement():
    rendercomponents()
    renderTexts()

#-启动界面变量[状态量]（0=就绪/正在执行;1=完成;2=等待///同下）
class Startrd(object):
    def __init__(self):
        self.window = 0
        self.dtext = 2
        self.text = "Click to start!!"
        self.sttick = 0
        self.tomn = 2
startrd = Startrd()
#-渲染启动界面
exec(layout.start[0])
#buttons.append(ButtonCTRL(658,0,64,32,empty[0],BtFunc[0],'Skip>>',(150,150,150)))
def render_start_up():
    if GameVar.state == GameVar.STATES["START_UP"]:
        if startrd.window == 0 and startrd.sttick <= 255:
            cl = ta = round(startrd.sttick)
            GameVar.bg.fill_cl=(cl,cl,cl)
            for i in buttons:
                i.alpha = ta
            startrd.sttick = startrd.sttick + 0.8*renderbase.flowanime
        elif startrd.dtext == 2 and startrd.window == 0:
            startrd.window = 1
            startrd.dtext = startrd.sttick = 0
            txts.append(Txts(startrd.text,(255,255,255),255,(150,100),45))
        if startrd.dtext == 0 and startrd.sttick <= 255:
            tmptk = round(startrd.sttick)
            cl1 = 255 - tmptk
            ta = tmptk
            Stone_img[0].set_alpha(ta)
            Stone_img[1].set_alpha(ta)
            txts[0].cl = (cl1,cl1,cl1)
            startrd.sttick = startrd.sttick + 0.4*renderbase.flowanime
        elif startrd.dtext == 0:
            startrd.dtext = 1
            GameVar.wait = 1
        if startrd.tomn == 0 and startrd.sttick <= 255:
            tmptk = round(startrd.sttick)
            cl = 255 - tmptk
            ta = round(cl/1.2)
            txts[0].position = rendereffect.vibrating(450,150,100,7,5,1,tmptk)
            Btn_img[0].set_alpha(ta)
            Stone_img[0].set_alpha(ta)
            Stone_img[1].set_alpha(ta)
            GameVar.bg.fill_cl=(cl,cl,cl)
            for i in buttons:
                i.alpha = ta
            startrd.sttick = startrd.sttick + 0.5*renderbase.flowanime
        elif startrd.tomn == 0:
            startrd.tomn = 1
            startrd.sttick = 0
            txts.clear()
            Stone_img[0].set_alpha(255)
            Stone_img[1].set_alpha(255)
            Btn_img[0].set_alpha(0)
            GameVar.bg.surf = BG_img[0]
            exec(layout.menu[0])
            txts.append(Txts("Anywhere",(56,60,171),0,(4,4),75))
            txts.append(Txts("  Explorer",(56,60,171),0,(4,60),75))
            StopThanStartAudio(DA)
            GameVar.state = GameVar.STATES["MENU"]

#-菜单界面变量[状态量]
class Menurd(object):
    def __init__(self):
        self.window = 0
        self.mntick = 0
        self.inma = 0
        self.main = 2
        self.goto = 0
menurd = Menurd()
#-渲染菜单2界面
def render_menu():
    if GameVar.state == GameVar.STATES["MENU"]:
        if menurd.inma == 0 and menurd.mntick <= 255:
            tmptk = round(menurd.mntick)
            GameVar.bg.fill_cl = (tmptk,tmptk,tmptk)
            ta = tmptk
            BG_img[0].set_alpha(ta/3*2)
            for i in buttons:
                i.alpha = ta
            for i in txts:
                i.A = ta
            menurd.mntick = menurd.mntick + 0.9*renderbase.flowanime
        elif menurd.inma == 0:
            menurd.inma = 1
            menurd.main = 0
            menurd.mntick = 0
        if menurd.main == 0 and menurd.goto == 0:
            cl=255
            ta=255
        elif menurd.main == 0 and menurd.goto == 1:
            txts.clear()
            exec(layout.menu[2])
            menurd.main = 1
        if menurd.main == 1 and menurd.goto == 0:
            txts.clear()
            txts.append(Txts("Anywhere",(56,60,171),255,(4,4),75))
            txts.append(Txts("  Explorer",(56,60,171),255,(4,60),75))
            exec(layout.menu[1])
            menurd.main = 0
            
class Selectrd(object):
    def __init__(self):
        self.reading = 2
        self.writing = 2
selectrd = Selectrd()
#-渲染存档操作3界面
def render_sav():
    if GameVar.state == GameVar.STATES["SAV"]:
        #扫描对应存档

        pass

class Gamingrd(object):
    def __init__(self):
        self.init = 0
        self.window = 2
        self.run = 2
        self.tomn = 2
        self.tosv = 2
        self.paus = 2
gamingrd = Gamingrd()
#-渲染游戏4界面
def render_gaming():
    if GameVar.state == GameVar.STATES["GAMING"]:
        if gamingrd.init == 0:
            buttons.clear()
            buttons.append(Buttons(5,5,80,30,Btn_img[0],BtTest[1],"Pause II",(50,50,50),255,K_ESCAPE))
            GameVar.chars.append(Chars(0.5,1,0.5,27,45,26,Char00_img,0,1))
            gamingrd.init = 1
        elif gamingrd.init == 1:
            gamingrd.run = 0
        if gamingrd.tomn == 0:
            GameVar.chars.clear()
            exec(layout.menu[2])
            gamingrd.tomn = 1
            GameVar.state = GameVar.STATES["MENU"]
            menurd.goto = 1
            menurd.main = 1
        if gamingrd.paus == 0:
            gamingrd.paus = 1
            buttons.append(Buttons(5,5,60,30,Btn_img[0],BtTest[1],"Pause II",(50,50,50),255,K_ESCAPE))

#渲染背景
def renderBG():
    i = GameVar.bg
    window.fill(i.fill_cl)
    window.blit(i.surf,(i.x,i.y))

#渲染方块
def renderBlocks():
    if startrd.window != 0 and GameVar.state == GameVar.STATES["START_UP"]:
        for i in range(0,15):
            window.blit(Stone_img[1],(0 + i*48,166))
        for i in range(0,15):
            for j in range(0,7):  
                window.blit(Stone_img[0],(0 + i*48,198 + j*48))
    if GameVar.state == GameVar.STATES["GAMING"] and gamingrd.run == 0:
        for i in range(0,15):
            for j in range(0,6):
                if j < 5:
                    window.blit(Stone_img[1],(0+48*i,272+32*j))
                if j == 5:
                    window.blit(Stone_img[0],(0+48*i,432))

#渲染角色
def renderChars():
    for i in GameVar.chars:
        #print(i.surf[0])
        Chars.paint(i)


#-游戏内图层渲染先后
def rendergaming():
    renderBlocks()
    renderChars()

#-渲染窗口总线
def render_window():
    #界面渲染控制
    if GameVar.wait == 0:
        render_start_up()
        render_menu()
        render_gaming()
    #组件渲染（此if便于停止）
    if GameVar.wait == 0:
        renderBG()
        rendergaming()
        renderelement()
    frameupd(renderbase.basefam)
#帧更新
def frameupd(fps):
    pygame.display.update()
    fps = fps


#总线(尽量简洁)
while True:
    #操作侦测
    handle_event()
    #碰撞侦测
    check_hit()
    #组件移动
    element_move()
    #渲染窗口
    render_window()
    time.sleep((renderbase.EnTkSpd*1/renderbase.maxtick)/renderbase.tickspeed)


