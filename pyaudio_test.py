#A test for pygame audio control
import pygame,easygui,os
pygame.init()

#地址&音频
print('Load audio')
Ad=[]
AdPath = "resource/ado/"
files = os.listdir(AdPath)
for file in files:
    if not os.path.isdir(file):
        Ad.append(AdPath+file)

def StopThanStartAudio(DA):
    ifpl.pl = 1
    if pygame.mixer.get_busy() == True:
        pygame.mixer.stop()
    BGM=pygame.mixer.Sound(DA)
    channal=BGM.play(-1)
    BGM.set_volume(0.195)

Answer=["Dream Away","Vivid Theory"]
class Ifpl(object):
    def __init__(self):
        self.pl = 1
ifpl = Ifpl()
def handleevent():
    rt = easygui.choicebox("Select Music","Audio test",{"Dream Away":1,"Vivid Theory":2,"3":3,"PAUSE":4,"EXIT":4},0)
    print(rt)
    if rt == "EXIT" or rt == None:
        pygame.quit()
        exit()
    if rt == "PAUSE":
        if ifpl.pl == 1:
            pygame.mixer.pause()
            ifpl.pl = 0
        else:
            pygame.mixer.unpause()
            ifpl.pl = 1
    ct = 0
    for i in Answer:
        if rt == i:
            StopThanStartAudio(Ad[ct])
        ct += 1

while True:
    handleevent()
    print(pygame.mixer.get_busy())