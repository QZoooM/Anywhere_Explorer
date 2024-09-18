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
（基本）渲染帧机制---[Done]
（基本）界面：---to do20%
    开始动画&互动[Done]
    菜单[Done]
    设置界面---to do
    选图界面---to do75%
    游戏界面(2.5D)---to do25%
（基本）
（基本）元素：
    按钮：
        点击按钮[Done]
        托条&滑动---to do
    探险者··-89%
    方块---to do
    遮挡物透明化渲染---to do
    （增强）特殊生物：就像Boss一样的
（基本）镜头移动··-80%
（基本）将设计背景和方块构成地图的部分(地图前后5;高度3;宽度视情况而定(先128)))---to do
（基本）地图格式：5*3*16n --> 16*4*16n --> 16n*4*16n --> 16∞*256*16∞
（基本）存档系统，世界不可写入，每次都加载初始地图---to do
（基本）经验与商店系统---to do
（增强）地图外部储存，可写入---to do
（增强）探险者将有多个可选外观
（增强）按钮交互动画
（增强）界面图形动画---to do??%
（增强）2DLive
（增强）随机地图（丛林，沙漠，海洋，草原）&种子机制
（增强）随机地图16∞*256*16∞设计
（增强）‘混乱’地图16n*4*16n设计
'''
import pygame,random,time,os,threading,math #导入运行库
from pygame.locals import *
pygame.init() #初始化Pygame模块
#渲染基本信息(非常重要)，也包括基础音频信息，也是程序的默认信息
class BaseINF(object):
    basefam = 60 #基础帧率;;144-->6.64s;60-->7.29
    basetick = 0 #（可能没用）
    EnTkSpd = 1 #默认为“1”
    maxtick = 10000 #默认为“10000”
    tickspeed = 100 #默认为“100”,可在游戏内更改(1~10000)
    famcount = 0 #（可能没用）
    window_x = 720 #窗口宽
    window_y = 480 #窗口高
    transparency = 100 #（可能没用）
    flowanime = 1 #过渡动画倍速
    vol = 0.195 #音量
    ado_on = 1 #音频开关
    ado_mt = 0 #静音
    #导入用户配置信息
    try:
        with open('config/cfg.ini') as cfg:
            L = 1
            for line in cfg.readlines():
                try:
                    line = float(line.strip('\n'))
                except:
                    pass
                if L == 2:
                    basefam = line
                elif L == 3:
                    basetick = line
                elif L == 4:
                    EnTkSpd = line
                elif L == 5:
                    maxtick = line
                elif L == 6:
                    tickspeed = line
                elif L == 7:
                    famcount = line
                elif L == 8:
                    window_x = line
                elif L == 9:
                    window_y = line
                elif L == 10:
                    transparency = line
                elif L == 11:
                    flowanime = line
                elif L == 12:
                    vol = line
                elif L == 13:
                    ado_on = line
                elif L == 14:
                    ado_mt = line
                elif L == 15:
                    break
                L += 1
    except:
        print("This User has yet created cfg.ini, automatically run with default config.")
    #时间计算使用的变量(不会改变)
    RenderLastTime = 0
    RenderInterval = 1/(basefam)
    LoadLastTime = 0
    LoadInterval = EnTkSpd/maxtick/tickspeed #1/1008
#创建窗口（视野）
pygame.display.set_caption("Anywhere Explorer")
window_size = (BaseINF.window_x,BaseINF.window_y)
window = pygame.display.set_mode(window_size)
#补帧技术(待定)
#framp_0 = pygame.Surface(window_size)
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
raw_Grass_img.append(pygame.image.load(BlkPth+"Grass_Up.png").convert_alpha())
#for i in raw_Grass_img:
Grass_img.append(pygame.transform.scale(raw_Grass_img[0],(48, 48)))
Grass_img.append(pygame.transform.scale(raw_Grass_img[1],(48, 32)))
raw_Stone_img=[]
Stone_img=[]
raw_Stone_img.append(pygame.image.load(BlkPth+"Stone_Side.png").convert_alpha())
raw_Stone_img.append(pygame.image.load(BlkPth+"Stone_Up.png").convert_alpha())
Stone_img.append(pygame.transform.scale(raw_Stone_img[0],(48, 48)))
Stone_img.append(pygame.transform.scale(raw_Stone_img[1],(48, 32)))
raw_Wood_img=[]
Wood_img=[]
raw_Wood_img.append(pygame.image.load(BlkPth+"Wood_Side.png").convert_alpha())
raw_Wood_img.append(pygame.image.load(BlkPth+"Wood_Up.png").convert_alpha())
for i in raw_Wood_img:
    Wood_img.append(pygame.transform.scale(i,(48, 48)))
Shadow_img=[]
Shadow_img.append(pygame.transform.scale(pygame.image.load(BlkPth+"Shadow.png").convert_alpha(),(48, 48)))
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
    if BaseINF.ado_on == 0:
        return
    if pygame.mixer.get_busy() == True:
        pygame.mixer.stop()
    BGM=pygame.mixer.Sound(DA)
    channal=BGM.play(-1)
    if BaseINF.ado_mt == 0:
        BGM.set_volume(BaseINF.vol)
    else:
        BGM.set_volume(0)
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
#-类概括
'''
类-主类-支类
  |-开发者=DevVar
  |-物理=PhyAgri
  |-背景=Background
  |-方块(主)=Blocks
  |   |-方块(支)=Block
  |-角色=Chars
  |-控制按钮=ButtonCTRL
  |   |-点击式按钮=Buttons
  |   |-拖动滑块=None
  |-文本=Txts
  |-Camera=Camera
  |-存档=Savings
  |-地图世界=World
  |-butto=Buttons
  |-GameVar=GameVar
'''

#--开发者
class DevVar(object):
    def __init__(self):
        self.DevMode = 1
devvar = DevVar()

#--物理
class PhyAgri(object):
    PhyLastTime = 0
    PhyInterval = 0.08
    grav_var = 0.000098
    resis = 0.000001

#--背景类
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
    def paint(self):
        if world.T_x > 15:
            if GameVar.chars[0].x <= world.T_x - 7.5 and GameVar.chars[0].x >= 7.5:
                paint_x = (BaseINF.window_x - self.width)*(GameVar.chars[0].x-7.5)/(world.T_x - 15)
            elif GameVar.chars[0].x > world.T_x - 7.5:
                paint_x = self.x - self.width + BaseINF.window_x
            elif self.x < 7.5:
                paint_x = self.x
        elif world.T_x == -1:
            paint_x = 360 - self.width
        paint_y = self.y
        surf = self.surf
        window.blit(surf,(paint_x,paint_y))

#--方块大类
class Blocks(object): #48x48,46*32;x-->width,y-->height,z-->depth
    def __init__(self,x,y,z,surf,l_x=1,l_y=1,l_z=1):
        self.x = x
        self.y = y
        self.z = z
        self.surf = surf
        self.l_x = l_x
        self.l_y = l_y
        self.l_z = l_z
        self.paint_x = (self.x - self.l_x/2+0.5)*48
        self.paint_y = BaseINF.window_y - self.y*48 - self.z*32
    def paint(self):
        # paint_x = self.x*48 - self.l_x/2 + 24
        # paint_y = BaseINF.window_y - self.y*48 + self.z*32
        paint_y = self.paint_y
        if GameVar.chars[0].x <= world.T_x - 7.5 and GameVar.chars[0].x >= 7.5:
            paint_x = self.paint_x + (-GameVar.chars[0].x+7.5)*48
        elif GameVar.chars[0].x > world.T_x - 7.5:
            paint_x = self.paint_x + (15 - world.T_x)*48
        elif GameVar.chars[0].x < 7.5:
            paint_x = self.paint_x
        surf = self.surf
        window.blit(surf[0],(paint_x,paint_y))
        window.blit(Shadow_img[0],(paint_x,paint_y))
        window.blit(surf[1],(paint_x,paint_y-32))


#--实体
class Entity(object): #Whole:27x45;Head:27x21;Body:27x24.
    basicTimeCount = 0
    def __init__(self,x,y,z,width,height,up,surf,type,life,speed=1,faceleft=0):
        self.x = self.tx = x
        self.y = y
        self.ty = -999
        self.z = self.tz = z
        self.box_x = 0.45
        self.box_y = 0.8
        self.box_z = 0.45
        self.width = width
        self.height = height
        self.up = up
        self.surf = surf
        self.type = type
        self.life = life
        self.bkab = self.ftab = self.lfab = self.rtab = 0
        self.bkuab = self.ftuab = self.lfuab = self.rtuab = 0
        self.speed = speed
        self.faceleft = faceleft
        self.felling = 0
        self.landing = 1
        self.v_x = self.v_y = self.v_z = 0
        self.hit_up = self.hit_dw = self.hit_lf = self.hit_rt = None
        self.recentBlocks = []
        self.tmpList = []
        self.tmpVar = 0
    def hitbox(self): #x&z碰撞判定并限定位移
        scan = 1
        x = math.floor(self.x)
        y = math.floor(self.y)
        z = math.floor(self.z)
        if x!=self.tx or y!=self.ty or z!=self.tz: #载入附近方块
            self.recentBlocks.clear()
            for i in GameVar.blocks:
                if i.x >= x - scan and i.y >= y - scan and i.z >= z-scan and i.x <= x+scan and i.y <= y+scan and i.z <= z+scan:
                    self.recentBlocks.append(i)
        self.tx = math.floor(self.x)
        self.ty = math.floor(self.y)
        self.tz = math.floor(self.z)
        #碰撞:x26,y40,z16-->x0.45,y0.8,z0.45
        str()
        #碰撞点阵箱命名规则:xyz-->ldf(左下前)
        L = self.x - self.box_x/2
        R = self.x + self.box_x/2
        D = self.y
        A = self.y + self.box_y
        F = self.z - self.box_z/2
        B = self.z + self.box_z/2
        ldf = (L,D,F)
        ldb = (L,D,B)
        laf = (L,A,F)
        lab = (L,A,B)
        rdf = (R,D,F)
        rdb = (R,D,B)
        raf = (R,A,F)
        rab = (R,A,B)
        Check_WASD = 1
        # 下方判定真则不下落&速度为零，假则下落。
        self.lfuab = self.rtuab = self.ftuab = self.bkuab = ufell = 0 #重置数值
        if self.y > 1:
            self.felling = 1
        for i in self.recentBlocks:
            if i.y <= self.y - 0.6:
                BlkA = i.y + i.l_y
                CON0 = ldf[0] <= i.x + i.l_x and ldf[0] >= i.x and ldf[2] <= i.z + i.l_z and ldf[2] >= i.z
                CON1 = ldb[0] <= i.x + i.l_x and ldb[0] >= i.x and ldb[2] <= i.z + i.l_z and ldb[2] >= i.z
                CON2 = rdf[0] <= i.x + i.l_x and rdf[0] >= i.x and rdf[2] <= i.z + i.l_z and rdf[2] >= i.z
                CON3 = rdb[0] <= i.x + i.l_x and rdb[0] >= i.x and rdb[2] <= i.z + i.l_z and rdb[2] >= i.z
                if CON0 or CON1 or CON2 or CON3:
                    if ldf[1] == BlkA or ldb[1] == BlkA or rdf[1] == BlkA or rdb[1] == BlkA:
                        ufell += 1
                    elif ldf[1] < BlkA or ldb[1] < BlkA or rdf[1] < BlkA or rdb[1] < BlkA:
                        ufell += 1
                        self.y = i.y + i.l_y
        if ufell >= 1:
            self.felling = 0
        if self.felling == 1:
            if self.y == 1:
                self.felling = 0
        if self.y < 1:
                self.felling = 0
                self.v_y = 0
                self.y = 1
        if self.landing == 0:
            if self.felling == 0:
                Check_WASD = 0
        elif self.landing == 1:
            if self.felling == 1:
                Check_WASD = 0
        #当落地瞬间，不启用以下判定
        #[
        if Check_WASD == 1:
            # 左方判定真则不左，假则pass。
            for i in self.recentBlocks:
                if i.x <= self.x - 0.6:
                    BlkR = i.x + i.l_x
                    CON0 = ldf[1] < i.y + i.l_y and ldf[1] > i.y and ldf[2] < i.z + i.l_z and ldf[2] > i.z
                    CON1 = ldb[1] < i.y + i.l_y and ldb[1] > i.y and ldb[2] < i.z + i.l_z and ldb[2] > i.z
                    CON2 = laf[1] < i.y + i.l_y and laf[1] > i.y and laf[2] < i.z + i.l_z and laf[2] > i.z
                    CON3 = lab[1] < i.y + i.l_y and lab[1] > i.y and lab[2] < i.z + i.l_z and lab[2] > i.z
                    if CON0 or CON1 or CON2 or CON3:
                        if ldf[0] == BlkR or ldb[0] == BlkR or laf[0] == BlkR or lab[0] == BlkR:
                            self.lfuab += 1
                        elif ldf[0] < BlkR or ldb[0] < BlkR or laf[0] < BlkR or lab[0] < BlkR:
                            self.lfuab += 1
                            self.x = i.x + i.l_x + self.box_x/2
            if self.lfuab == 0:
                # 右方判定真则不右，假则pass。
                for i in self.recentBlocks:
                    if i.x >= self.x - 0.4:
                        BlkL = i.x
                        CON0 = rdf[1] < i.y + i.l_y and rdf[1] > i.y and rdf[2] < i.z + i.l_z and rdf[2] > i.z
                        CON1 = rdb[1] < i.y + i.l_y and rdb[1] > i.y and rdb[2] < i.z + i.l_z and rdb[2] > i.z
                        CON2 = raf[1] < i.y + i.l_y and raf[1] > i.y and raf[2] < i.z + i.l_z and raf[2] > i.z
                        CON3 = rab[1] < i.y + i.l_y and rab[1] > i.y and rab[2] < i.z + i.l_z and rab[2] > i.z
                        if CON0 or CON1 or CON2 or CON3:
                            if self.tmpVar == 0:
                                self.tmpVar = 1
                                print("初次断点判定，顶点%s，是否下落%s"%((rdf,rdb,raf,rab), ufell==1))
                            if rdf[0] == BlkL or rdb[0] == BlkL or raf[0] == BlkL or rab[0] == BlkL:
                                self.rtuab += 1
                            elif rdf[0] > BlkL or rdb[0] > BlkL or raf[0] > BlkL or rab[0] > BlkL:
                                self.rtuab += 1
                                self.x = i.x - self.box_x/2
            # 前方判定真则不前，假则pass。
            for i in self.recentBlocks:
                if i.z <= self.z - 0.6:
                    BlkB = i.z + i.l_z
                    CON0 = ldf[1] < i.y + i.l_y and ldf[1] > i.y and ldf[0] < i.x + i.l_x and ldf[0] > i.x
                    CON1 = laf[1] < i.y + i.l_y and laf[1] > i.y and laf[0] < i.x + i.l_x and laf[0] > i.x
                    CON2 = raf[1] < i.y + i.l_y and raf[1] > i.y and raf[0] < i.x + i.l_x and raf[0] > i.x
                    CON3 = rdf[1] < i.y + i.l_y and rdf[1] > i.y and rdf[0] < i.x + i.l_x and rdf[0] > i.x
                    if CON0 or CON1 or CON2 or CON3:
                        if ldf[2] == BlkB or laf[2] == BlkB or raf[2] == BlkB or rdf[2] == BlkB:
                            self.ftuab += 1
                        elif ldf[2] < BlkB or laf[2] < BlkB or raf[2] < BlkB or rdf[2] < BlkB:
                            self.ftuab += 1
                            self.z = i.z + i.l_z + self.box_z/2
            if self.ftuab == 0:
                # 后方判定真则不后，假则pass。
                for i in self.recentBlocks:
                    if i.z >= self.z - 0.4:
                        BlkF = i.z
                        CON0 = rdb[1] < i.y + i.l_y and rdb[1] > i.y and rdb[0] < i.x + i.l_x and rdb[0] > i.x
                        CON1 = ldb[1] < i.y + i.l_y and ldb[1] > i.y and ldb[0] < i.x + i.l_x and ldb[0] > i.x
                        CON2 = lab[1] < i.y + i.l_y and lab[1] > i.y and lab[0] < i.x + i.l_x and lab[0] > i.x
                        CON3 = rab[1] < i.y + i.l_y and rab[1] > i.y and rab[0] < i.x + i.l_x and rab[0] > i.x
                        if CON0 or CON1 or CON2 or CON3:
                            if rdb[2] == BlkF or ldb[2] == BlkF or lab[2] == BlkF or rab[2] == BlkF:
                                self.bkuab += 1
                            elif rdb[2] > BlkF or ldb[2] > BlkF or lab[2] > BlkF or rab[2] > BlkF:
                                self.bkuab += 1
                                self.z = i.z - self.box_z/2
            if self.lfuab == 0 and self.rtuab == 0 and self.ftuab == 0 and self.bkuab == 0:
                # 上方判定真则速度为零，假则pass。
                for i in self.recentBlocks:
                    if i.y >= self.y - 0.1:
                        BlkD = i.y + i.l_y
                        CON0 = laf[0] < i.x + i.l_x and laf[0] > i.x and laf[2] < i.z + i.l_z and laf[2] > i.z
                        CON1 = lab[0] < i.x + i.l_x and lab[0] > i.x and lab[2] < i.z + i.l_z and lab[2] > i.z
                        CON2 = raf[0] < i.x + i.l_x and raf[0] > i.x and raf[2] < i.z + i.l_z and raf[2] > i.z
                        CON3 = rab[0] < i.x + i.l_x and rab[0] > i.x and rab[2] < i.z + i.l_z and rab[2] > i.z
                        if CON0 or CON1 or CON2 or CON3:
                            if laf[1] == BlkD or lab[1] == BlkD or raf[1] == BlkD or rab[1] == BlkD:
                                self.v_y = 0
                            elif laf[1] < BlkD or lab[1] < BlkD or raf[1] < BlkD or rab[1] < BlkD:
                                self.v_y = 0
                                self.y = i.y - self.box_y
        #]
        #地图边界判定
        if B == world.T_z:
            self.bkab = 0
        elif B > world.T_z:
            self.bkab = 0
            self.z = world.T_z - self.box_z/2
        if F == 0:
            self.ftab = 0
        elif F < 0:
            self.ftab = 0
            self.z = self.box_z/2
        if L == 0:
            self.lfab = 0
        elif L < 0:
            self.lfab = 0
            self.x = self.box_x/2
        if R == world.T_x:
            self.rtab = 0
        elif R > world.T_x:
            self.rtab = 0
            self.x = world.T_x - self.box_x/2
        #下降&着陆转换
        if self.felling == 1:
            self.v_y -= PhyAgri.grav_var
            self.landing = 0
        elif self.landing == 0:
            if self.felling == 0:
                self.v_y = 0
                self.landing = 1
        #坐标显示以及其他测试功能----For test
        # self.tmpList.append(ufell)
        # print("")
        # print((x,y,z))
        if Times_up(Chars.basicTimeCount,1):
            print((x,y,z))
            # print((self.x,self.y,self.z))
            # print(self.tmpList)
            # self.tmpList.clear()
            Chars.basicTimeCount = time.time()
    def paint(self): #绘制
        if self.lfab == 1:
            if self.faceleft == 0:
                self.faceleft = 1
                self.surf[0] = pygame.transform.flip(self.surf[0],1,0)
        if self.rtab == 1:
            if self.faceleft == 1:
                self.faceleft = 0
                self.surf[0] = pygame.transform.flip(self.surf[0],1,0)
        if world.T_x == -1:
            paint_x = 360 - self.width/2
        elif world.T_x > 15:
            if self.x <= world.T_x - 7.5 and self.x >= 7.5:
                paint_x = 360 - self.width/2
            elif self.x > world.T_x - 7.5:
                paint_x = (self.x - world.T_x + 15)*48 - self.width/2
            elif self.x < 7.5:
                paint_x = self.x*48 - self.width/2
        pygame.draw.ellipse(window,(75,75,75),(paint_x+2-(self.y-1)*0.2,BaseINF.window_y - self.z*32 - 54-(self.y-1)*0.07,self.width-1+(self.y-1)*0.4,16+(self.y-1)*0.14))
        window.blit(self.surf[0],(paint_x,BaseINF.window_y - self.z*32 - (self.y-1)*48 - self.height + 1))
    def gravbox(self): #y轴碰撞判定(防掉底)(已转移至hitbox函数，将要移除)
        # # print(str(self.felling)+'---'+str(self.v_y)) #For test
        # for recentBlock in self.recentBlocks:
        #     if recentBlock == None:
        #         self.felling = 1
        #     if recentBlock.y <= self.y-0.4 and recentBlock.x == self.tx and recentBlock.z == self.tz:
        #         if self.y > recentBlock.y+1:
        #             self.felling = 1
        #         if self.y == recentBlock.y+1:
        #             self.felling = 0
        #             self.v_z = 0
        #         if self.y < recentBlock.y+1:
        #             self.felling = 0
        #             self.v_z = 0
        #             self.y = recentBlock.y+1
        pass
    def move(self):
        if self.bkab == 1:
            if self.bkuab == 0:
                self.z += 0.01*self.speed
        if self.ftab == 1:
            if self.ftuab == 0:
                self.z -= 0.01*self.speed
        if self.lfab == 1:
            if self.lfuab == 0:
                self.x -= 0.01*self.speed
        if self.rtab == 1:
            if self.rtuab == 0:
                self.x += 0.01*self.speed
        self.x += self.v_x
        self.y += self.v_y
        self.z += self.v_z

#--控制按钮
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

#--文本绘制
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

#Camera类
'''
当角色移动至离地图边界大于7.5单位距离(屏幕中央)时，角色位置锁定，地图开始移动
但是该变量暂时由特定算法替代，故搁置
'''
class Camera(object):
    def __init__(self) -> None:
        
        pass

#存档类
class Savings(object):
    def __init__(self,FolderName,name,ChTime,T=[],F=[],D=[],O=[],G=[],I=[],M=[],TotalChunckList=[]):#区块数量
        self.FolderName = FolderName
        self.name = name
        self.ChTime = ChTime
        self.T = T
        self.F = F
        self.D = D
        self.O = O
        self.G = G
        self.I = I
        self.M = M
        self.TotalChunckList = TotalChunckList
    def scan(self): #扫描存档
        menurd.SavPhs.clear()
        menurd.SavFds.clear()
        saving_folder_list = os.listdir('saveport/')
        for fd in saving_folder_list:
            if not os.path.isfile(fd):
                menurd.SavPhs.append(fd)
                with open('saveport/'+ fd + '/sav.dat') as s:
                    L = 1
                    for line in s.readlines():
                        line=line.strip('\n')
                        if L == 1:
                            self.name = line
                        if L == 2:
                            self.ChTime = line
                        if L == 3:
                            break
                        L += 1
                menurd.SavFds.append(self.name + '   ' + self.ChTime)
    def load(self): #扫描选中的存档
        aim = GameVar.sav.FolderName = savrd.slt_sav
        with open('saveport/'+ aim + '/sav.dat') as s:
                    L = 1
                    for line in s.readlines():
                        line=line.strip('\n')
                        if L == 1:
                            self.name = line
                        if L == 2:
                            self.ChTime = line
                        if L == 3:
                            break
                        L += 1
        GameVar.sav.TotalChunckList = os.listdir('saveport/'+ aim + '/Ck/')
        print(GameVar.sav.TotalChunckList)
        for i in GameVar.sav.TotalChunckList:
            if i.find('T') > -1:
                GameVar.sav.T.append(i)
            #exec(f.read())
        pass
    def write(self):
        path = 'saveport/sav' + 'which' + '.dat'
        with open(path) as f:
            print("write into a sav")
            #exec(f.write())

#世界地图类
class World(object):
    WDTYPE = {"T","F","D","O","G","I","M"}
    def __init__(self,WdType,T_x,T_y,T_z,LogicType,Chuncks):
        self.WdType = WdType
        self.T_x = T_x
        self.T_y = T_y
        self.T_z = T_z
        self.LogType = LogicType
        self.Chuncks = Chuncks#列表装列表
        self.ChuncksChangeList = []
    #读取世界
    def read(self):
        with open("saveport/" + GameVar.sav.FolderName + "/Ck/T000.ck") as ck:
            #GameVar.sav.FolderName
            for line in ck.readlines():
                line = line.strip('\n')
                if line == "":
                    continue
                if line.find("chunck") > -1:
                    continue
                try:
                    exec("GameVar.blocks.append(block(" + line +"))")
                except:
                    pass
                #print(line)
    def write(self):
        pass
        

#存档世界功能测试--日后移动到适当位置
#T000为测试的有限地图，F000森林，D000沙漠，O000海洋，G000草原，I000无限，M000混乱
#They're Temp
world = World("T",64,3,5,'w16n35',[])
rdWorldList=['T']

#存档


#-支类
#--单个方块
class Block(Blocks):
    BlockType = {}
    def __init__(self,type,x,y,z,l_x=1,l_y=1,l_z=1):
        if type == "stone":
            surf = Stone_img
        elif type == "grass":
            surf = Grass_img
        elif type == "wood":
            surf = Wood_img
        elif type == "air":
            surf = empty
        Blocks.__init__(self,x,y,z,surf,l_x,l_y,l_z)
block = Block

#--角色(隶属实体)
class Chars(Entity): #Whole:27x45;Head:27x21;Body:27x24.
    basicTimeCount = 0
    def __init__(self,x,y,z,width,height,up,surf,type,life,speed=1,faceleft=0):
        Entity.__init__(self,x,y,z,width,height,up,surf,type,life,speed,faceleft)
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
        if siz[0] > i.width - 10:
            scltext=pygame.transform.scale(text,(i.width-10, (i.width-10)*siz[1]/siz[0]))
        if siz[1] > i.height - 6:
            scltext=pygame.transform.scale(text,((i.height-6)*siz[0]/siz[1], i.height-6))
        if siz[0] <= i.width - 10 and siz[1] <= i.height - 6:
            scltext=text
        sclsiz = scltext.get_size()
        pos = (i.x+i.width/2-sclsiz[0]/2,i.y+i.height/2-sclsiz[1]/2)
        scltext.set_alpha(i.alpha)
        window.blit(img,(i.x,i.y))
        window.blit(scltext,pos)
buttons=[] #按钮列表

#使用类属性存储游戏中的变量，以减少全局变量的数量
class GameVar(object):
    wait = 0 #渲染等待以减少性能消耗
    bg = Background((0,0,0),0,0,960,480,empty[0],0)
    blocks = []
    sav = Savings('','','') #存档信息初始化以及寄存位点
    chars = [] #角色列表
    tmpchars = [] #角色缓存列表
    lastTime = 0
    interval = 1 #单位为秒
    #控制游戏状态
    STATES = {"END_UP":0,"START_UP":1,"MENU":2,"SAV":3,"GAMING":4,"STORE":5,"PAUSE":6,"FLOW_ANIMA":100,}
    state = STATES["START_UP"]
#-零散的(尽量少)

#创建的函数
#线程
class myThread(threading.Thread): #继承父类threading.Thread
    def __init__(self, threadID, name, todo=None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.todo = todo
    def run(self): #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        Err_Times = 0 
        while True:
            try:
                render_window()
            except:
                if Err_Times >= 3:
                    exit()
                Err_Times += 1

#获取日期
def Get_date():
    t = time.localtime()
    return "%s/%s/%s" %(t.tm_year, t.tm_mon, t.tm_mday)

#工具方法-判断时间间隔是否到了
def Times_up(lastTime,interval):
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
            yestick = round(((1/freq)*BaseINF.maxtick*BaseINF.tickspeed*self.crtimes)/300)
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

#-输入控制器(预计移除)
class Mvab(object):
    def __init__(self,charmvx_ad,charmvx_mi,charmvy_ad,charmvy_mi):
        self.charmvx_ad = charmvx_ad
        self.charmvx_mi = charmvx_mi
        self.charmvy_ad = charmvy_ad
        self.charmvy_mi = charmvy_mi
mvab = Mvab(0,0,0,0)

#设置布局变量类，作为layout.ini的规范
class Layout(object):
    def __init__(self,start,menu,sav,store,gaming,pause,option):
        self.start=start
        self.menu=menu
        self.sav=sav
        self.store=store
        self.gaming=gaming
        self.pause=pause
        self.option=option
layout = Layout([],[],[],[],[],[],[]) #列表打包导入的layout，通过layout.~[~]调用指令
#按钮测试功能存储
BtTest=[]
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
        if menurd.inma == 0:
            return
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
                    if event.key == K_SPACE:
                        i.v_y = 0.0142
                    if event.key == K_w:
                        i.bkab = 1
                    if event.key == K_a:
                        i.lfab = 1
                    if event.key == K_s:
                        i.ftab = 1
                    if event.key == K_d:
                        i.rtab = 1
        if event.type==KEYUP:
            for i in GameVar.chars:
                if GameVar.state == GameVar.STATES["GAMING"] and gamingrd.run == 0:
                    if event.key == K_w:
                        i.bkab = 0
                    if event.key == K_a:
                        i.lfab = 0
                    if event.key == K_s:
                        i.ftab = 0
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
        # i.gravbox()

#组件移动总线
def element_move():
    #角色移动
    if GameVar.state != GameVar.STATES["GAMING"]:
        return
    for i in GameVar.chars:
        i.move()

#-渲染启动界面
exec(layout.start[0])
#-启动界面变量[状态量]（0=就绪/正在执行;1=完成;2=等待///同下）
class Startrd(object):
    def __init__(self):
        self.window = 0
        self.dtext = 2
        self.text = "Click to start!!"
        self.sttick = 0
        self.tomn = 2
    def render(self):
        if GameVar.state == GameVar.STATES["START_UP"]:
            if self.window == 0 and self.sttick <= 255:
                cl = ta = round(self.sttick)
                GameVar.bg.fill_cl=(cl,cl,cl)
                for i in buttons:
                    i.alpha = ta
                self.sttick = self.sttick + 0.8*BaseINF.flowanime
            elif self.dtext == 2 and self.window == 0:
                self.window = 1
                self.dtext = self.sttick = 0
                txts.append(Txts(self.text,(255,255,255),255,(150,100),45))
            if self.dtext == 0 and self.sttick <= 255:
                tmptk = round(self.sttick)
                cl1 = 255 - tmptk
                ta = tmptk
                Stone_img[0].set_alpha(ta)
                Stone_img[1].set_alpha(ta)
                txts[0].cl = (cl1,cl1,cl1)
                self.sttick = self.sttick + 0.4*BaseINF.flowanime
            elif self.dtext == 0:
                self.dtext = 1
                GameVar.wait = 1
            if self.tomn == 0 and self.sttick <= 255:
                tmptk = round(self.sttick)
                cl = 255 - tmptk
                ta = round(cl/1.2)
                txts[0].position = rendereffect.vibrating(450,150,100,7,5,1,tmptk)
                Btn_img[0].set_alpha(ta)
                Stone_img[0].set_alpha(ta)
                Stone_img[1].set_alpha(ta)
                GameVar.bg.fill_cl=(cl,cl,cl)
                for i in buttons:
                    i.alpha = ta
                self.sttick = self.sttick + 0.5*BaseINF.flowanime
            elif self.tomn == 0:
                self.tomn = 1
                GameVar.state = GameVar.STATES["MENU"]
                GameVar.bg.fill_cl = (0,0,0)
                BG_img[0].set_alpha(0)
                GameVar.bg.surf = BG_img[0]
                exec(layout.menu[0])
                StopThanStartAudio(DA)
                menurd.inma = 0
                Stone_img[0].set_alpha(255)
                Stone_img[1].set_alpha(255)
                Btn_img[0].set_alpha(0)
                self.sttick = 0
startrd = Startrd()

#-菜单界面变量[状态量]a
class Menurd(object):
    def __init__(self):
        self.window = 0
        self.mntick = 0
        self.inma = 2
        self.main = 2
        self.ppsv = 2
        self.goto = -1
        self.SavPhs = []
        self.SavFds = []
    #-渲染菜单2界面
    def render(self):
        if GameVar.state == GameVar.STATES["MENU"]:
            if self.inma == 0 and self.mntick <= 255:
                tmptk = round(self.mntick)
                GameVar.bg.fill_cl = (tmptk,tmptk,tmptk)
                ta = tmptk
                BG_img[0].set_alpha(ta/3*2)
                for i in buttons:
                    i.alpha = ta
                for i in txts:
                    i.A = ta
                self.mntick = self.mntick + 0.9*BaseINF.flowanime
            elif self.inma == 0:
                self.inma = 1
                self.main = 0
                self.mntick = 0
            if self.main == 0:
                cl=255
                ta=255
            if self.goto == 1:
                GameVar.sav.scan()
                txts.clear()
                exec(layout.menu[2])
                self.main = 1
                self.goto = -1
            if self.goto == 0:
                exec(layout.menu[1])
                self.main = 0
                self.goto = -1
            if self.ppsv == 0:
                self.ppsv = 1
                savrd.reading = 0
                GameVar.state = GameVar.STATES["SAV"]
menurd = Menurd()
            
class Savrd(object):
    def __init__(self):
        self.tomain = 2
        self.main = 2
        self.tomn = 2
        self.reading = 2
        self.writing = 2
        self.clean = 2
        self.slt_sav = -1 #可选0，1，2
        self.wd = 1
        self.slt_wd = "N"
    #-渲染存档操作3界面
    def render(self):
        if GameVar.state == GameVar.STATES["SAV"]:
            if self.reading == 0:
                #扫描对应存档
                try:
                    GameVar.sav.load()
                except:
                    print('Read Save Error!\nCheck spell or whether sav.dat format is correct.')
                self.reading = 1
                self.tomain = 0
            if self.writing == 0:
                #写入对应存档
                try:
                    print("writting sav00"+ str(self.slt_sav) +" ~~~ Doing")
                    GameVar.sav.write()
                    GameVar.chars.clear()
                    print("Done!")
                except IOError:
                    print("This programme has yet had power to write a file!")
                except:
                    print('Write Saving Error!\nCheck spell or whether sav.dat&xxx.ck format is correct.')
                    print('You have to create a new Saving,\nbut dont warry, everything will be sattled.')
                self.writing = 1
            if self.reading == 1 and self.tomain == 0:
                self.tomain = 1
                exec(layout.sav[0])
                self.main = 0
            if self.main == 0:
                
                pass
            if self.clean == 0:
                pass
            if self.tomn == 0:
                self.tomn = 1
                GameVar.state = GameVar.STATES["MENU"]
                menurd.goto = 1
                menurd.main = 1
savrd = Savrd()

class Gamingrd(object):
    def __init__(self):
        self.init = 0
        self.window = 2
        self.run = 2
        self.tomn = 2
        self.tosv = 2
        self.tops = 2
        self.paus = 2
    #-渲染游戏4界面
    def render(self):
        if GameVar.state == GameVar.STATES["GAMING"]:
            if self.init == 0:
                buttons.clear()
                exec(layout.gaming[0])
                if len(GameVar.tmpchars) > 0:
                    GameVar.chars += GameVar.tmpchars
                    GameVar.tmpchars.clear()
                else:
                    GameVar.chars.append(Chars(1.75,4,0.5,27,45,26,Char00_img,0,1))
                self.init = 1
            elif self.init == 1:
                self.run = 0
            if self.tomn == 0:
                # if GameVar.chars[0].faceleft == 1:
                #     ch = GameVar.chars[0]
                #     ch.surf[0] = pygame.transform.flip(ch.surf[0],1,0)
                GameVar.tmpchars += GameVar.chars
                GameVar.chars.clear()
                self.tomn = 1
                GameVar.state = GameVar.STATES["MENU"]
                menurd.goto = 1
                menurd.main = 1
            if self.tops == 0:
                buttons.clear()
                exec(layout.pause[0])
                self.tops = 1
                self.paus = 0
            if self.paus == 0:#执行暂停
                return
            if self.paus == 1:
                buttons.clear()
                exec(layout.gaming[0])
                self.paus = 2
gamingrd = Gamingrd()

#元素绘制

#-组件绘制
def rendercomponents():
    #--按钮绘制
    for i in buttons:
        i.paint()

#渲染文本
def renderText(text,cl,A,position,size,fot = fot[0],view = window):
    my_font = pygame.font.Font(fot,size)
    text = my_font.render(text,True,cl).convert_alpha()
    text.set_alpha(A)
    view.blit(text,position)

def renderTexts():
    for i in txts:
        renderText(i.text,i.cl,i.A,i.position,i.size,i.fot,i.view)

#渲染背景
def renderBG():
    i = GameVar.bg
    window.fill(i.fill_cl)
    if GameVar.state == GameVar.STATES["GAMING"]:
        i.paint()
    else:
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
        for i in GameVar.blocks:
            i.paint()
    
#渲染角色
def renderChars():
    for i in GameVar.chars:
        Chars.paint(i)

#-游戏内图层渲染先后
def TrueRenderGameEngine():
    print("TrueRenderEngine is on building")


def renderingame():
    renderBlocks()
    renderChars()

#元素绘制总线
def renderelement():
    rendercomponents()
    renderTexts()

#-渲染控制总线
def render_control():
    if GameVar.wait == 0:
        startrd.render()
        menurd.render()
        savrd.render()
        gamingrd.render()

#-渲染窗口总线
def render_window():
    #此if便于停止
    if not Times_up(BaseINF.RenderLastTime,BaseINF.RenderInterval):
        return
    BaseINF.RenderLastTime = time.time()
    if GameVar.wait == 0:
        renderBG()
        renderingame()
        renderelement()
        #帧更新
        pygame.display.update()

#加载总线
def Load_():
    if not Times_up(BaseINF.LoadLastTime,BaseINF.LoadInterval):
        return
    BaseINF.LoadLastTime = time.time()
    #碰撞侦测
    check_hit()
    #组件移动
    element_move()
    #渲染控制
    render_control()
#加入线程并启动
thread_render_window_1 = myThread(1,"render_window")
thread_render_window_2 = myThread(2,"render_window")
thread_render_window_1.start()
time.sleep(BaseINF.RenderInterval/2)
#thread_render_window_2.start()
#统一的终止操作(预计移除)
def IF_END_UP_GAME():
    if GameVar.state == GameVar.STATES["END_UP"]:
        pygame.quit()
        exit()
#总线(尽量简洁)
while True:
    #操作侦测
    handle_event()
    #加载
    Load_()
    #渲染窗口
    #render_window()