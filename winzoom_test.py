import pygame,time,threading
from pygame.locals import *
from math import floor
# 初始化 Pygame
pygame.init()

# 设置窗口大小
class Base_INF():
    window_size = (400, 400)

# 创建窗口
window = pygame.display.set_mode(Base_INF.window_size,pygame.RESIZABLE)

# 加载图像
BlkPth="resource/img/Block/"
image = pygame.transform.scale(pygame.image.load(BlkPth+"Grass_Side.png"), Base_INF.window_size).convert_alpha()

def Times_up(lastTime,interval):
    if lastTime == 0:
        return True
    currentTime = time.time()
    return currentTime - lastTime >= interval

class Render_Thread(threading.Thread): #继承父类threading.Thread
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self): #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        Err_Times = 0 
        while True:
            try:
                RD_window()
            except:
                if Err_Times >= 3:
                    break
                Err_Times += 1
        print("Stop Rendering")

class Clock():
    RD_LT = 0
    RD_ITV = 1/60
    LD_LT = 0
    LD_ITV = 1/10000
def RD_window():
    if Times_up(Clock.RD_LT,Clock.RD_ITV):
        Clock.RD_LT = time.time()
        window.fill((0,0,0))
        sc_siz = scaled_image.get_size()
        window.blit(scaled_image, (0, (Base_INF.window_size[1]-sc_siz[1])/2))
        pygame.display.update()

class Char():
    FaceLeft = 0

tx = ty = txz = None
ag = 0
ud = 180
thread_render_window = Render_Thread(1,"render_window")
thread_render_window.start()
# 游戏循环
running = True
while running:
    if not Times_up(Clock.LD_LT,Clock.LD_ITV):
        continue
    Clock.LD_LT = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        if event.type==pygame.MOUSEMOTION:
            if ud > 0:
                ag += event.rel[0]*2
            else:
                ag -= event.rel[0]*2
            ud -= event.rel[1]*0.5
            if ud > 180:
                ud = 180
            elif ud < -180:
                ud = -180
    cursize = pygame.display.get_surface().get_size()
    if cursize[0] != tx:
        tx = ty = cursize[0]
        Base_INF.window_size = (cursize[0],cursize[0])
        window = pygame.display.set_mode(Base_INF.window_size,pygame.RESIZABLE)
    elif cursize[1] != ty:
        tx = ty = cursize[1]
        Base_INF.window_size = (cursize[1],cursize[1])
        window = pygame.display.set_mode(Base_INF.window_size,pygame.RESIZABLE)
    if ag >= 360:
        ag -= 360
    elif ag < 0:
        ag += 360
    rotate_img = pygame.transform.rotate(image,ag)
    if ud > 0:
        flip_img = pygame.transform.flip(rotate_img, 1, 0) #图，转x轴，转y轴
    else:
        flip_img = rotate_img
    scaled_image = pygame.transform.scale(flip_img,(Base_INF.window_size[0],Base_INF.window_size[1]*abs(ud/180)))
    slt_xz = floor(ag/45)
    if slt_xz != txz:
        print(slt_xz)
        txz = slt_xz

# 退出 Pygame
pygame.quit()
