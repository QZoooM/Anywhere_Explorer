#AutoRange_Test
import ast,time
#列表自动规整排列
FnumList=[]
path = "Test/AutoSort.txt"
with open(path) as file:
    RnumList = file.read().split("\n")
    for i in RnumList:
        FnumList.append(float(i))
    # print(RnumList)
    # print(FnumList)

#先扫描出不符合排序的后一个数
def At_Sort(arr):
    n = 1
    print("Before is %s%s"%(arr,type(arr)))
    while n != 0:
        n = 0
        for i in range(0,len(arr)-1):
            if arr[i] <= arr[i+1]:
                continue
            else:
                tmp = arr[i]
                arr[i] = arr[i+1]
                arr[i+1] = tmp
                n += 1
    print("After is %s%s"%(arr,type(arr)))

def mergeSort(arr):
    import math
    if(len(arr)<2):
        return arr
    middle = math.floor(len(arr)/2)
    left, right = arr[0:middle], arr[middle:]
    return merge(mergeSort(left), mergeSort(right))

def merge(left,right):
    result = []
    while left and right:
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    while left:
        result.append(left.pop(0))
    while right:
        result.append(right.pop(0))
    return result


At_Sort(FnumList)
for i in range(0,0):
    print(i)
# Dict={1:13, 2:134}
# print(Dict)
BlockType={0:"'air';empty;(0,0,0)",1:"'grass';Grass_img;(1,1,1)",2:"'stone';Stone_img;(1,1,1)",3:"'wood';Wood_img;(1,1,1)"}
# ty="135"
# mm=113
# nn="mm"
# tmp=[]
# tmp.append(ty)
# tmp.append(eval(ty))
# tmp.append(nn)
# tmp.append(eval(nn))
# print(tmp)

with open("dictionary/blocks.dict") as rawDict:
    tmplst=[]
    strDict = rawDict.read()
    Dict = ast.literal_eval(strDict)
    print(Dict)
    Dict.update({2: Dict[1], 1: Dict[2]})
    print(Dict)
    #Dict[]
    #BlockDict






#clm    纵列
#row    横行
#level  层排

# class Blocks(object):
#     def __init__(self,x,y,z,surf,l_x=1,l_y=1,l_z=1):
#         self.x = x
#         self.y = y
#         self.z = z
#         self.surf = surf
#         self.l_x = l_x
#         self.l_y = l_y
#         self.l_z = l_z
# class Block(Blocks):
#     BlockType = {}
#     def __init__(self,type,x,y,z,l_x=1,l_y=1,l_z=1):
#         Blocks.__init__(self,x,y,z,"",l_x,l_y,l_z)
# block = Block
# class World(object):
#     WDTYPE = {"T","F","D","O","G","I","M"}
#     def __init__(self,WdType,T_x,T_y,T_z,LogicType,Chuncks):
#         self.WdType = WdType
#         self.T_x = T_x
#         self.T_y = T_y
#         self.T_z = T_z
#         self.LogType = LogicType
#         self.Chuncks = Chuncks#列表装列表
#     def read(self):
#         with open("saveport/aaaaaa/Ck/T000AutoRange.ck") as ck:
#             for line in ck.readlines():
#                 line = line.strip('\n')
#                 try:
#                     exec("blocks.append(block(" + line +"))")
#                 except:
#                     pass
#                 #print(line)

# blocks = []
# world = World("T",64,3,5,'w16n35',[])
# world.read()
# for block in blocks:
#     print("This Block locates at %s, %s, %s"  %(block.x, block.y, block.z))
# a = []
