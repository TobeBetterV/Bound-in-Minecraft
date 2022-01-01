from mcpi.minecraft import Minecraft
import threading
import time
from mcpi import block
from mcpi.vec3 import Vec3

mc = Minecraft.create()

wool = block.WOOL.id    #羊毛,15:黑色,13: 绿色,14: 红色
wood = block.WOOD.id    #木头,0:Oak,12:Oak (only bark)
air = block.AIR.id      #空气
snow = block.SNOW_BLOCK.id #雪

# 设置背景
def background_layout():
    # 木头填充开始位置
    x_wood1, y_wood1, z_wood1 = x+10,y+2,z+10
    # 木头填充结束位置
    x_wood2, y_wood2, z_wood2 = x-10,y+22,z+10
    # 木头填充（效果为外圈）
    mc.setBlocks(x_wood1, y_wood1, z_wood1,x_wood2, y_wood2, z_wood2,wood,7)
    # 黑色羊毛填充开始位置
    x_wool1, y_wool1, z_wool1 = x+9,y+3,z+10
    # 黑色羊毛填充结束位置
    x_wool2, y_wool2, z_wool2 = x-9,y+21,z+10
    # 黑色羊毛填充
    mc.setBlocks(x_wool1, y_wool1, z_wool1,x_wool2, y_wool2, z_wool2,wool,7)

    return x_wool1,x_wool2,y_wool1,y_wool2

# 更新球拍位置
def update_Paddle():
    mc2 = Minecraft.create()
    x, y, z = mc2.player.getTilePos()
    # 球拍初始坐标
    paddle_x1, paddle_y1, paddle_z1 = x - 3, y + 3, z + 9
    # 球拍结束坐标
    paddle_x2, paddle_y2, paddle_z2 = x + 3, y + 3, z + 9
    # 创建球拍
    mc2.setBlocks(paddle_x1, paddle_y1, paddle_z1, paddle_x2, paddle_y2, paddle_z2, wool, 13)
    # 更新球拍位置
    while True:
        # 获取新的位置
        x, y, z = mc2.player.getTilePos()
        #判断位置是否更新、是否越界
        if paddle_x1 != x - 3 and x + 3 <= x_wool1 and x - 2 >= x_wool2:
            mc2.setBlocks(paddle_x1, paddle_y1, paddle_z1, paddle_x2, paddle_y2, paddle_z2, air)
            # 球拍坐标
            paddle_x1 = x - 3
            paddle_x2 = x + 3
            mc2.setBlocks(paddle_x1, paddle_y1, paddle_z1, paddle_x2, paddle_y2, paddle_z2, wool, 13)

# 更新球位置
def update_Ball():
    mc3 = Minecraft.create()
    x, y, z = mc3.player.getTilePos()

    # 设置初始位置，y+5是为了避免下方第二个方块为羊毛，游戏可能直接结束。
    x_ball, y_ball, z_ball = x - 3, y + 5, z + 9
    mc.setBlocks(x_ball, y_ball, z_ball,wool,1)
    print("x:"+str(x_ball)+" y:"+str(y_ball)+" z:"+str(z_ball))
    # 水平移动速度
    speed_x=1
    # 垂直移动速度
    speed_y=1

    while True:
        #获取下方方块id，判断是否为羊毛，是则碰上球拍,因为此时y坐标已经减1，所以要判断方块无需减一
        low_block = mc3.getBlock(Vec3(x_ball, y_ball, z_ball))
        #判断小球是否碰到左右两边的木头边框
        if x_ball > x_wool1 or x_ball < x_wool2:
            print("碰到左/右边框")
            speed_x = -speed_x
            x_ball += speed_x
        #判断小球是否碰到上边的木头边框或者球拍
        elif y_ball > y_wool2 or low_block == wool:
            print("碰到上边框/球拍")
            speed_y = -speed_y
            y_ball += speed_y

        elif y_ball < y_wool1:
            background_error()
            mc.postToChat("游戏结束")
            break
        else:
            mc.setBlock(x_ball, y_ball, z_ball,wool,1)
            print("x:" + str(x_ball) + " y:" + str(y_ball) + " z:" + str(z_ball))
            time.sleep(0.3)
            mc3.setBlock(x_ball, y_ball, z_ball,air)
            x_ball += speed_x
            y_ball += speed_y
# 设置游戏结束背景
def background_error():
    # 填充开始位置
    x_wool1, y_wool1, z_wool1 = x+9,y+3,z+10
    # 红色方块位置
    red_wool_num = [8,9,10,11,12,24,25,26,27,28,29,30,31,32,33,42,43,44,45,46,47,48,49,
                    50,51,52,53,54,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,78,79,
                    80,84,85,86,87,88,92,93,97,98,99,104,105,106,111,112,113,115,116,117,
                    118,124,130,131,132,134,135,136,137,138,148,149,150,151,152,153,154,
                    155,156,157,158,166,167,168,169,170,171,172,173,174,175,176,177,178,
                    184,185,186,187,188,189,190,191,192,193,194,195,196,204,205,206,207,
                    208,209,210,211,212,213,214,224,225,226,227,228,229,230,231,232,238,
                    244,245,246,249,250,251,256,257,258,263,264,265,268,269,270,274,275,
                    276,277,278,282,283,284,288,289,290,291,292,293,294,295,296,297,298,
                    299,300,301,302,308,309,310,311,312,313,314,315,316,317,318,319,320,
                    328,329,330,331,332,333,334,335,336,337,338,349,350,351,352,353,354,355,]
    for i in range(1, 362):

        if i in red_wool_num:
            mc.setBlock(x_wool1, y_wool1, z_wool1, wool, 14)
            x_wool1 -= 1
        else:
            mc.setBlock(x_wool1, y_wool1, z_wool1, snow, 1)
            x_wool1 -= 1

        if i % 19 == 0:
            #切换下一行
            y_wool1 += 1
            #x位置归零
            x_wool1 = x+9


# 获取人物位置
x, y, z = mc.player.getPos()
# 建立背景板
x_wool1,x_wool2,y_wool1,y_wool2 = background_layout()
#更新小球位置的线程
T1 = threading.Thread(target = update_Ball,name="T1")
#更新球拍位置的线程
T2 = threading.Thread(target = update_Paddle,name="T2")
T1.start()
T2.start()
