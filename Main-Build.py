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
（基本）界面：---to do50%
    开始动画&互动[Done]
    菜单[Done]
    设置界面---to do
    选图界面---to do75%
    游戏界面(2.5D)---to do30%
（基本）
（基本）元素：
    按钮：
        点击按钮[Done]
        托条&滑动---to do
    探险者··-89%
    方块·--05%
    遮挡物透明化渲染---to do
    （增强）特殊生物：就像Boss一样的
（基本）镜头移动··-80%
（基本）将设计背景和方块构成地图的部分(地图前后5;高度3;宽度视情况而定(先128)))---to do
（基本）地图格式：5*3*16n[Done] --> 16*4*16n --> 16n*4*16n --> 16∞*256*16∞
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
import pygame,random,time,os,threading,math,ast #导入运行库
from pygame.locals import *
from math import floor
pygame.init() #初始化Pygame模块
#渲染基本信息(非常重要)，也包括基础音频信息，也是程序的默认信息
class BaseINF(object):
    fps = tfps = 0
    fpsLT = 0
    fpsITV = 1
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
    if basefam == -1:
        RenderInterval = 0
    else:
        RenderInterval = 1/(basefam+10)
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
Wood_img.append(pygame.transform.scale(raw_Wood_img[0],(48, 48)))
Wood_img.append(pygame.transform.scale(raw_Wood_img[1],(48, 32)))
Shadow_img=[]
Shadow_img.append(pygame.transform.scale(pygame.image.load(BlkPth+"Shadow.png").convert_alpha(),(48, 48)))
#--角色
Char00_img=[]
Slt_img=[]
Char00Path="resource/img/Char/"
Char00_img.append(pygame.image.load(Char00Path+"Char00.png").convert_alpha())
Char00_img.append(pygame.image.load(Char00Path+"Char00_Body.png").convert_alpha())
Char00_img.append(pygame.image.load(Char00Path+"Char00_Head.png").convert_alpha())
Slt_img.append(pygame.transform.scale(pygame.image.load(Char00Path+"slt_0.png").convert_alpha(),(48, 48)))
Slt_img.append(pygame.transform.scale(pygame.image.load(Char00Path+"slt_0.png").convert_alpha(),(48, 32)))
Slt_img.append(pygame.transform.scale(pygame.image.load(Char00Path+"slt_1.png").convert_alpha(),(48, 48)))
Slt_img.append(pygame.transform.scale(pygame.image.load(Char00Path+"slt_1.png").convert_alpha(),(48, 32)))
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

#--方块(大类)
class Blocks(object): #48x48,46*32;x-->width,y-->height,z-->depth
    def __init__(self,ID,name,x,y,z,surf,ckpos,box=(1,1,1)):
        self.ID = ID
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.surf = surf
        self.ckpos = ckpos
        self.l_x = box[0]
        self.l_y = box[1]
        self.l_z = box[2]
        self.ptab_abv = self.ptab_fnt = 1
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
        if self.ptab_abv == 1:
            window.blit(surf[0],(paint_x,paint_y))
            window.blit(Shadow_img[0],(paint_x,paint_y))
        if self.ptab_fnt == 1:
            window.blit(surf[1],(paint_x,paint_y-32))

#--实体(大类)
class Entity(object): #Whole:27x45;Head:27x21;Body:27x24.
    basicTimeCount = 0
    def __init__(self,x,y,z,width,height,up,surf,type,life,speed=1,faceleft=0):
        self.x = self.tx = x
        self.y = y
        self.ty = None
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
    def hitbox(self): #x&z碰撞判定并限定位移
        scan = 1
        x = floor(self.x)
        y = floor(self.y)
        z = floor(self.z)
        if x!=self.tx or y!=self.ty or z!=self.tz: #载入附近方块
            self.recentBlocks.clear()
            for i in GameVar.blocks:
                if i.x >= x - scan and i.y >= y - scan and i.z >= z-scan and i.x <= x+scan and i.y <= y+scan and i.z <= z+scan:
                    self.recentBlocks.append(i)
            self.tx = floor(self.x)
            self.ty = floor(self.y)
            self.tz = floor(self.z)
        #碰撞:x26,y40,z16-->x0.45,y0.8,z0.45
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
            if i.y <= self.y - 0.5:
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
                        # 上方判定真则速度为零，假则pass。
        for i in self.recentBlocks:
            if i.y >= self.y + 0.4:
                BlkD = i.y
                CON0 = laf[0] < i.x + i.l_x and laf[0] > i.x and laf[2] < i.z + i.l_z and laf[2] > i.z
                CON1 = lab[0] < i.x + i.l_x and lab[0] > i.x and lab[2] < i.z + i.l_z and lab[2] > i.z
                CON2 = raf[0] < i.x + i.l_x and raf[0] > i.x and raf[2] < i.z + i.l_z and raf[2] > i.z
                CON3 = rab[0] < i.x + i.l_x and rab[0] > i.x and rab[2] < i.z + i.l_z and rab[2] > i.z
                if CON0 or CON1 or CON2 or CON3:
                    if laf[1] == BlkD or lab[1] == BlkD or raf[1] == BlkD or rab[1] == BlkD:
                        self.v_y = 0
                    elif laf[1] > BlkD or lab[1] > BlkD or raf[1] > BlkD or rab[1] > BlkD:
                        self.v_y = 0
                        self.y = i.y - self.box_y
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
                if i.x <= self.x - 0.7:
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
                    if i.x >= self.x - 0.3:
                        BlkL = i.x
                        CON0 = rdf[1] < i.y + i.l_y and rdf[1] > i.y and rdf[2] < i.z + i.l_z and rdf[2] > i.z
                        CON1 = rdb[1] < i.y + i.l_y and rdb[1] > i.y and rdb[2] < i.z + i.l_z and rdb[2] > i.z
                        CON2 = raf[1] < i.y + i.l_y and raf[1] > i.y and raf[2] < i.z + i.l_z and raf[2] > i.z
                        CON3 = rab[1] < i.y + i.l_y and rab[1] > i.y and rab[2] < i.z + i.l_z and rab[2] > i.z
                        if CON0 or CON1 or CON2 or CON3:
                            if rdf[0] == BlkL or rdb[0] == BlkL or raf[0] == BlkL or rab[0] == BlkL:
                                self.rtuab += 1
                            elif rdf[0] > BlkL or rdb[0] > BlkL or raf[0] > BlkL or rab[0] > BlkL:
                                self.rtuab += 1
                                self.x = i.x - self.box_x/2
            # 前方判定真则不前，假则pass。
            for i in self.recentBlocks:
                if i.z <= self.z - 0.7:
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
                    if i.z >= self.z - 0.3:
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
            # print((x,y,z))
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

#--控制按钮(大类)
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
class Savings(object): #角色,背包,可用合成表信息存储在sav.dat
    def __init__(self,FolderName,name,ChTime):
        self.FolderName = FolderName
        self.name = name
        self.ChTime = ChTime
        self.T = self.F = self.D = self.O = self.G = self.I = self.M = self.ChunckFilesList = [] #区块文件列表
        self.rdWorldList=['T']
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
        aim = self.FolderName = savrd.slt_sav
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
                        if L == 4:
                            pass
                        L += 1
        self.ChunckFilesList = os.listdir('saveport/'+ aim + '/Ck/')
        print(self.ChunckFilesList)
        for i in self.ChunckFilesList:
            if i.find('T') > -1:
                self.T.append(i)
    def write(self): #存档
        path = 'saveport/sav' + self.FolderName + '.dat'
        with open(path) as f:
            print("write into a sav")
            #exec(f.write())

#世界地图类
class World(object): #区块以及方块信息只存在于WDxxx.ck中
    WDTYPE = {"T","F","D","O","G","I","M"}
    def __init__(self,WdType,T_x,T_y,T_z,LogicType):
        self.WdType = WdType
        self.T_x = T_x
        self.T_y = T_y
        self.T_z = T_z
        self.LogType = LogicType
        self.Chuncks = []#列表装列表
        self.ChuncksChangeList = []
        self.LT=0
        self.ITV=0.02
        self.tcpos = None
    def read(self): #读取世界区块
        with open("saveport/" + GameVar.sav.FolderName + "/Ck/T000.ck") as ck:
            tmpCkNum = -1
            for line in ck.readlines():
                line = line.strip('\n')
                if line == "":
                    continue
                if line.find("chunck") > -1:
                    line = line.replace("chunck","")
                    inf = line.split(";")
                    exec("self.Chuncks.append(Chuncks(%s,(%s)))"%(inf[0], inf[1]))
                    tmpCkPos = ast.literal_eval("(%s)"%inf[1])
                    tmpCkNum += 1
                    continue
                binf = []
                str_inf = line.split(",")
                for i in str_inf:
                    binf.append(int(i))
                self.Chuncks[tmpCkNum].contain[binf[3]-tmpCkPos[1]*16][binf[2]][binf[1]-tmpCkPos[0]*16].append(Block(binf[0],binf[1],binf[2],binf[3],tmpCkPos))
    def load_chunck(self,force=0): #从已载入的区块列表中载入方块
        if not Times_up(self.LT,self.ITV):
            return
        scan = 1 #加载范围，默认为1
        for i in GameVar.chars:
            crx = round(i.x/16)
            crz = round(i.z/16)
            if force == 1:
                self.tcpos = None
            if self.tcpos != (crx,crz): #与上一个坐标不同则重新载入，注意之后可能会发生卡顿!!!
                GameVar.blocks.clear()
                for ck in world.Chuncks:
                    if ck.pos[0] > crx-1-scan and ck.pos[0] < crx+scan and ck.pos[1] > crz-1-scan and ck.pos[1] < crz+scan:
                        for z in ck.contain[::-1]:
                            for y in z:
                                for x in y:
                                    for blk in x:
                                        GameVar.blocks.append(blk)
                self.tcpos = (crx,crz) #更新缓存坐标
    def write(self):
        pass

#区块类用于统一管理方块
class Chuncks(object):
    def __init__(self,ID,pos):
        self.ID = ID
        self.pos = pos #坐标(便于定位)
        self.contain = [] #创建一个不存在重复对象的列表(先前的问题已经解决)
        for z in range(0,16): #创建不重不漏的16个列表z
            self.contain.append([])
        for y in range(0,16): #在每个列表z中，创建不重不漏的16个列表y
            for z in range(0,16):
                self.contain[y].append([])
        for x in range(0,16): #在每个列表z中的每个列表y中，创建不重不漏的16个列表x
            for y in range(0,16):
                for z in range(0,16):
                    self.contain[y][x].append([])
    def TidyUp(self): #自我整理功能(这是个多余的功能，将移除或者转化为新的功能)
        pass

#存档世界功能测试--日后移动到适当位置
#T000为测试的有限地图，F000森林，D000沙漠，O000海洋，G000草原，I000无限，M000混乱
#They're Temp
world = World("T",64,3,8,'w16n35')
rdWorldList=['T']

#-支类
#--单个方块(继承Blocks)
class Block(Blocks):
    with open("dictionary/blocks.dict") as rawDict:
        BlockDict=eval(rawDict.read())
    def __init__(self,ID,x,y,z,ckpos):
        blkInfList = Block.BlockDict[ID]
        Blocks.__init__(self,ID,blkInfList[0],x,y,z,blkInfList[1],ckpos,blkInfList[2])

#--角色(继承实体Entity)
class Chars(Entity): #Whole:27x45;Head:27x21;Body:27x24.
    basicTimeCount = 0
    slt_xz_dict = {0:(1,0),1:(1,-1),2:(0,-1),3:(-1,-1),4:(-1,0),5:(-1,1),6:(0,1),7:(1,1)}
    slt_y_dict = {0:-1,1:-1,2:0,3:1,4:1}
    def __init__(self,x,y,z,width,height,up,surf,type,life,speed=1,faceleft=0):
        Entity.__init__(self,x,y,z,width,height,up,surf,type,life,speed,faceleft)
        self.slt_xz = 22.5
        self.slt_y = 90
        self.shapab = 1
        self.slt_pos = None
    def shapeWorld(self):
        xz = Chars.slt_xz_dict[floor(self.slt_xz/45)]
        y = Chars.slt_y_dict[floor(self.slt_y/36)]
        if floor(self.slt_y/36) == 0:
            self.slt_pos = (floor(self.x),floor(self.y)-1,floor(self.z))
        elif floor(self.slt_y/36) == 4:
            self.slt_pos = (floor(self.x),floor(self.y)+1,floor(self.z))
        else:
            self.slt_pos = (floor(self.x)+xz[0],floor(self.y)+y,floor(self.z)+xz[1])
    def paint_slt(self):
        paint_y = BaseINF.window_y -(self.slt_pos[1]*48 + self.slt_pos[2]*32)
        paint_x = self.slt_pos[0]*48
        if self.x <= world.T_x - 7.5 and self.x >= 7.5:
            paint_x += (-GameVar.chars[0].x+7.5)*48
        elif GameVar.chars[0].x > world.T_x - 7.5:
            paint_x += (15 - world.T_x)*48
        elif GameVar.chars[0].x < 7.5:
            pass
        if self.shapab == 1:
            i = 2
        elif self.shapab == 0:
            i = 0
        else:
            return
        window.blit(Slt_img[i+1],(paint_x,paint_y-32))
        window.blit(Slt_img[i],(paint_x,paint_y))

#--按钮(继承控制按钮ButtonCTRL)
class Buttons(ButtonCTRL):
    def __init__(self,x,y,width,height,surf,func="",text="",txtcl=(0,0,0),alpha=250,rfkey=None):
        self.surf = pygame.Surface((width,height),pygame.SRCALPHA)
        self.surf.fill((0,0,0,0))
        my_font = pygame.font.Font(fot[1],round(height*0.5))
        text = my_font.render(text,True,(50,50,50))
        siz = text.get_size()
        if siz[0] > width - 10:
            scltext=pygame.transform.scale(text,(width-10, (width-10)*siz[1]/siz[0]))
        if siz[1] > height - 6:
            scltext=pygame.transform.scale(text,((height-6)*siz[0]/siz[1], height-6))
        if siz[0] <= width - 10 and siz[1] <= height - 6:
            scltext=text
        sclsiz = scltext.get_size()
        pos = (width/2-sclsiz[0]/2,height/2-sclsiz[1]/2)
        self.surf.blit(pygame.transform.scale(surf,(width,height)),(0,0))
        self.surf.blit(scltext,pos)
        ButtonCTRL.__init__(self,x,y,width,height,self.surf,func,text,txtcl,alpha,rfkey)
    def paint(self):
        self.surf.set_alpha(self.alpha)
        window.blit(self.surf,(self.x,self.y))
buttons=[] #按钮列表

#使用类属性存储游戏中的变量，以减少全局变量的数量
class GameVar(object):
    wait = 0 #渲染等待以减少性能消耗
    bg = Background((0,0,0),0,0,960,480,empty[0],0) #初始的背景配置
    blocks = [] #方块缓冲区
    sav = Savings('','','') #存档信息初始化以及寄存位点
    world = None #地图寄存位点
    chars = [] #角色列表
    tmpchars = [] #角色缓存列表
    lastTime = 0
    interval = 1 #单位为秒
    #控制游戏状态
    STATES = {"END_UP":0,"START_UP":1,"MENU":2,"SAV":3,"GAMING":4,"STORE":5,"PAUSE":6,"FLOW_ANIMA":100,}
    state = STATES["START_UP"]

#线程
class Render_Thread(threading.Thread): #继承父类threading.Thread
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self): #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        Err_Times = 0 
        while True:
            try:
                render_window()
            except:
                if Err_Times >= 10:
                    break
                Err_Times += 1
        print("Stop Rendering")

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

#-效果(需要补充&重写)
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

#-独立输入控制器(将要移除)
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
        # print(event)
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == WINDOWMINIMIZED:
            pygame.mixer.pause()
        elif event.type == WINDOWRESTORED:
            pygame.mixer.unpause()
        #按钮交互[点击后松开]   
        if menurd.inma == 0: #完成亮屏后才允许操作
            return
        if event.type==pygame.MOUSEMOTION:
            if GameVar.state == GameVar.STATES["GAMING"] and gamingrd.run == 0:
                GameVar.chars[0].slt_xz += event.rel[0]*2
                GameVar.chars[0].slt_y -= event.rel[1]*2
                if GameVar.chars[0].slt_xz >= 360:
                    GameVar.chars[0].slt_xz -=360
                elif GameVar.chars[0].slt_xz < 0:
                    GameVar.chars[0].slt_xz +=360
                if GameVar.chars[0].slt_y > 150:
                    GameVar.chars[0].slt_y = 150
                elif GameVar.chars[0].slt_y < 30:
                    GameVar.chars[0].slt_y = 30
        if event.type == MOUSEBUTTONDOWN:
            if event.button==1:
                if GameVar.state == GameVar.STATES["START_UP"] and startrd.dtext == 1: #点击左键切换为运行状态
                    startrd.dtext = 2
                    startrd.sttick = 0
                    startrd.tomn = 0
                    GameVar.wait = 0
                if GameVar.state == GameVar.STATES["GAMING"] and gamingrd.run == 0:
                    ti = None
                    for i in range(0,len(GameVar.blocks)):
                        tblk = GameVar.blocks[i]
                        if (tblk.x,tblk.y,tblk.z) == GameVar.chars[0].slt_pos:
                            if GameVar.chars[0].shapab == 1:
                                ti = i
                                break
                    if ti == None:
                        continue
                    for ck in world.Chuncks:
                        if ck.pos == tblk.ckpos:
                            ck.contain[tblk.z-tblk.ckpos[1]*16][tblk.y][tblk.x-tblk.ckpos[0]*16].pop(0)
                    GameVar.blocks.pop(ti)
            if event.button==3:
                if GameVar.state == GameVar.STATES["GAMING"] and gamingrd.run == 0:
                    pos = GameVar.chars[0].slt_pos
                    tshp = GameVar.chars[0].shapab
                    for i in range(0,len(GameVar.blocks)):
                        tblk = GameVar.blocks[i]
                        if (tblk.x,tblk.y,tblk.z) == pos:
                            GameVar.chars[0].shapab = 0
                            break
                    if pos[1] > 15:
                        GameVar.chars[0].shapab = 0
                        print("The Y limitation is 15")
                    if GameVar.chars[0].shapab == 1:
                        pos = GameVar.chars[0].slt_pos
                        tckpos = (floor(pos[0]/16),floor(pos[2]/16))
                        for ck in world.Chuncks:
                            if ck.pos == tckpos:
                                ck.contain[pos[2]-tckpos[1]*16][pos[1]][pos[0]-tckpos[0]*16].append(Block(2,pos[0],pos[1],pos[2],tckpos))
                        GameVar.blocks.clear()
                        world.load_chunck(1)
                    GameVar.chars[0].shapab = tshp
        if event.type == MOUSEBUTTONUP and event.button==1:
            for i in buttons:
                if event.pos[0] > i.x and event.pos[0] < i.x+i.width and event.pos[1] > i.y and event.pos[1] <i.y+i.height:
                    exec(i.func)
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
                    if event.key == K_v:
                        if i.shapab == 1:
                            i.shapab = 0
                        elif i.shapab == 0:
                            i.shapab = 1
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

#游戏内信息处理
def InGameProc():
    world.load_chunck()
    GameVar.chars[0].shapeWorld()

#碰撞侦测

#碰撞侦测总线
def check_hit():
    #角色碰撞
    for i in GameVar.chars:
        i.hitbox()

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
'''
规范：
???
'''
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
        self.togm = 2
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
            if self.togm == 0:
                #将于此处插入地图选择的判定参数
                GameVar.state = GameVar.STATES["GAMING"]
                world.tcpos = None
                self.togm = 1
                pass
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
        self.posLastTime = 0
        self.posInterval = 0.05
    #-渲染游戏4界面
    def render(self):
        if GameVar.state == GameVar.STATES["GAMING"]:
            if self.init == 0:
                if len(GameVar.tmpchars) > 0:
                    GameVar.chars += GameVar.tmpchars
                    GameVar.tmpchars.clear()
                else:
                    GameVar.chars.append(Chars(1.75,4,0.5,27,45,26,Char00_img,0,1))
                exec(layout.gaming[0])
                self.init = 1
            elif self.init == 1:
                self.run = 0
            if self.run == 0:
                InGameProc()
                try:
                    if Times_up(self.posLastTime,self.posInterval):
                        txts[0].text = str((floor(GameVar.chars[0].x),floor(GameVar.chars[0].y),floor(GameVar.chars[0].z)))
                        self.posLastTime = time.time()
                except:
                    pass
            if self.tomn == 0:
                # 此处应插入存档写入，或跳转至存档写入的步骤
                GameVar.tmpchars += GameVar.chars
                GameVar.chars.clear()
                GameVar.blocks.clear()
                world.Chuncks.clear()
                GameVar.state = GameVar.STATES["MENU"]
                menurd.goto = 1
                menurd.main = 1
                self.tomn = 1
            if self.tops == 0:
                exec(layout.pause[0])
                self.run = 1
                self.tops = 1
                self.paus = 0
            if self.paus == 0:#执行暂停
                return
            if self.paus == 1:
                exec(layout.gaming[0])
                self.run = 0
                self.paus = 2
gamingrd = Gamingrd()

#元素绘制
#-组件绘制
def rendercomponents():
    for i in buttons: #按钮绘制
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
        scan_x = 14 #14
        scan_y = 7 #7
        for i in GameVar.blocks:
            if i.x >= GameVar.chars[0].x-scan_x-1 and i.x <= GameVar.chars[0].x+scan_x and i.z >= GameVar.chars[0].z-scan_y-1 and i.z <= GameVar.chars[0].z+scan_y:
                i.paint()
    
#渲染角色
def renderChars():
    for i in GameVar.chars:
        i.paint()
        i.paint_slt()

#-游戏内图层渲染先后(仅仅针对实体和方块)
def TrueRenderGameEngine():
    print("TrueRenderEngine is on building")
    # for i in GameVar.blocks:
    #     if 1:
    #         pass


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
    if Times_up(BaseINF.RenderLastTime,BaseINF.RenderInterval):
        BaseINF.RenderLastTime = time.time()
        if GameVar.wait == 0: #此if便于停止
            renderBG()
            renderBlocks()
            renderChars()
            # TrueRenderGameEngine()
            renderelement()
            # renderText("PFS:%s"%BaseINF.fps,(50,255,0),255,(345,0),15,fot[1])
            #帧更新
            pygame.display.update()
            BaseINF.tfps += 1

#加载总线
def Load_():
    if Times_up(BaseINF.LoadLastTime,BaseINF.LoadInterval):
        BaseINF.LoadLastTime = time.time()
        #碰撞侦测
        check_hit()
        #组件移动
        element_move()
        #渲染控制
        render_control()
        #帧率计算(日后移到合适位置)
    if Times_up(BaseINF.fpsLT,BaseINF.fpsITV):
        BaseINF.fpsLT = time.time()
        BaseINF.fps = BaseINF.tfps
        print(BaseINF.fps)
        BaseINF.tfps = 0

#加入线程并启动
thread_render_window = Render_Thread(1,"render_window")
thread_render_window_2 = Render_Thread(2,"render_window")
thread_render_window.start()
#time.sleep(BaseINF.RenderInterval/2)
#thread_render_window_2.start()

#统一的终止操作(预计移除)
def IF_END_UP_GAME():
    if GameVar.state == GameVar.STATES["END_UP"]:
        pygame.quit()
        exit()

#总线
while True:
    #操作侦测
    handle_event()
    #加载
    Load_()