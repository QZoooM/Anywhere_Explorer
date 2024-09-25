'''
读写模式
要了解文件读写模式,需要了解几种模式的区别,以及对应指针
r:读取文件,若文件不存在则会报错
w:写入文件,若文件不存在则会先创建再写入,会覆盖原文件
a:写入文件,若文件不存在则会先创建再写入,但不会覆盖原文件,而是追加在文件未尾
rb,wb:分别与r,w类似,但是用于读写二进制文件
r+:可读、可写,文件不存在也会报错,写操作时会覆盖
w+:可读,可写,文件不存在先创建,会覆盖
a+:可读、可写,文件不存在先创建,不会覆盖,追加在未尾
'''
#read extended files

path = "config/cfg.ini"
# path1 = "saveport/sav000.dat"
# with open(path,"a") as f:
#     f.write('\n\n')
#     for z_ in range(0,5):
#         z = 4 - z_
#         for x in range(0,64):
#             f.write('\n' + '''block(stone,''' + str(x) + ',1,' + str(z) + ')')

with open(path) as f:
    for line in f.readlines():
        line = line.strip("\n")
        print(line)

#先声明一下a
a=[]

try:

    #打开文件
    fp=open(path,"r")
    print('%s 文件打开成功'% path)

    for line in fp.readlines():

        # 当你读取文件数据时会经常遇见一种问题,
        # 那就是每行数据末尾都会多个换行符'\n',
        # 所以我们需要先把它们去掉

        line=line.replace('\n','')
        #或者line=line.strip('\n')
        #但是这种只能去掉两头的,可以根据情况选择使用哪一种

        line=line.split(',')
        #以逗号为分隔符把数据转化为列表

        a.append(line)
    fp.close()
    print('文件内容为:')
    print(a)
except IOError:
    print("文件打开失败,%s文件不存在"%path)
# sct = '''print("This is a script")
# print(1.1+1)
# print(True)'''
# print(sct)
# exec(sct)
# a = [100,123]
# b = [211,985]
# a += b
# print(a)