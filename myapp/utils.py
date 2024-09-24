import numpy as np
import cv2
from matplotlib import pyplot as plt
import time
import threading
from django.utils import timezone
from myapp.models import TongueColor

# 函数功能:求出输入矩阵中所有不为0元素的最大值与最小值
# 输入:矩阵 
# 输出:最大值与最小值
def getMyMaxAndMin(I):
    myMax = 0
    myMin = 255
    rows,columns= I.shape
    for i in range(rows):
        for j in range(columns):
            if I[i][j] != 0:
                if I[i][j] > myMax:
                    myMax = I[i][j]
                if I[i][j] < myMin:
                    myMin = I[i][j]
    return myMax,myMin

# 函数功能:迭代法确定色度法中的阈值，忽略矩阵中所有为0的元素
# 输入:矩阵 
# 输出:符合要求的阈值
def iterativeThreshold(I):
    rows,columns= I.shape
    myMax,myMin = getMyMaxAndMin(I)
    T = (myMax + myMin) / 2
    temp = T

    while True:
        #计算所有小于temp且不为0元素的平均值
        leftCount = 0
        leftSum = 0
        for i in range(rows):
            for j in range(columns):
                if I[i][j] != 0 and I[i][j] < temp:
                    leftCount += 1
                    leftSum += I[i][j]
        if leftCount != 0:
            leftAvg = leftSum / leftCount
        else:
            leftAvg = 0

        #计算所有大于temp且不为0元素的平均值
        rightCount = 0
        rightSum = 0
        for i in range(rows):
            for j in range(columns):
                if I[i][j] != 0 and I[i][j] >= temp:
                    rightCount += 1
                    rightSum += I[i][j]
        if rightCount != 0:
            rightAvg = rightSum / rightCount
        else:
            rightAvg = 0

        T = (leftAvg + rightAvg) / 2
        if temp == T:
            break
        temp = T

    return T

# 函数功能:将输入图像拆分为H,S,V通道,并进行一系列处理提出舌头的轮廓
# 输入:原始图像 
# 输出:二值化的closing矩阵，舌头区域为255，非舌头区域为0
def hsvDeal(img):
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h = hsv[:,:,0]
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    #二值化H通道与V通道
    _,thresh_h = cv2.threshold(h,127,255,cv2.THRESH_BINARY)
    _,thresh_v = cv2.threshold(v,127,255,cv2.THRESH_BINARY)
    #对H通道与V通道进行“与”运算
    hAndV = cv2.bitwise_and(thresh_h,thresh_v)
    #进行形态学“闭”运算，先膨胀后腐蚀
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(hAndV, cv2.MORPH_CLOSE, kernel)
    #返回提取出的舌头轮廓
    return closing

# 函数功能:色度阈值法判断图像是否是舌头
# 输入:原图像
# 输出:bool值
def tongueColorDetect(img):
    #提取出舌头区域
    closing = hsvDeal(img)
    #舌头的掩膜,舌头区域为1，非舌头区域为0
    mask = closing.copy() / 255
    #计算“舌头”区域的占整个图像的比例，太低的话说明不是舌头
    effectiveRate = np.sum(mask == 1) / (mask.shape[0] * mask.shape[1])
    #非舌头区域置为白色
    tongueArea = img.copy()
    tongueArea[mask == 0] = [255,255,255]
    cv2.imshow('Tongue',tongueArea)

    #色度阈值法，I = R - (G + B) / 2
    #分离舌质与舌苔
    I = tongueArea[:,:,2] - (tongueArea[:,:,0] + tongueArea[:,:,1]) / 2
    I = I * mask

    iterT = iterativeThreshold(I)   #调用函数获得阈值
    colorResult = tongueArea.copy()
    colorResult[I >= iterT] = [255,255,255]
    # cv2.imshow("Split",colorResult)
    avg_r = np.mean(tongueArea[(I > 0) & (I < iterT),2])
    avg_g = np.mean(tongueArea[I >= iterT,1])
    avg_compare = np.mean(I[(I > 0) & (I < iterT)])
    # print("The average value of compare is:" + str(avg_compare))
    # print("The average value of r is:" + str(avg_r))
    # print("The average value of g is:" + str(avg_g))
    # print("The rate of the effective area is:" + str(effectiveRate))
    # 新增：分析舌头颜色
    hsv = cv2.cvtColor(tongueArea, cv2.COLOR_BGR2HSV)
    avg_hue = np.mean(hsv[mask == 1, 0])
    avg_sat = np.mean(hsv[mask == 1, 1])
    avg_val = np.mean(hsv[mask == 1, 2])

    # 计算相对亮度
    overall_brightness = np.mean(img)
    relative_brightness = avg_val / overall_brightness

    # 调试输出
    # print(f"avg_hue: {avg_hue}, avg_sat: {avg_sat}, avg_val: {avg_val}")
    # print(f"relative_brightness: {relative_brightness}")

    # 定义颜色范围（这些值可能需要根据实际情况调整）
    if relative_brightness > 1.3 and avg_sat < 50:  # 相对亮度高且饱和度低表示过白
        color = "white"
    elif 0 <= avg_hue < 20 or 330 <= avg_hue <= 360:  # 红色的色相范围
        if avg_sat > 100:  # 高饱和度表示过红
            color = "red"
        else:
            color = "pink"
    else:
        color = "pink"

    # 可以调节的四个参数
    if avg_r >= 120 and avg_compare >= 20 and avg_g < 200 and effectiveRate >= 0.1:
        return (True, color)
    else:
        return (False, None)

def run_tongue_detection(user):
    WIDTH = 320
    HEIGHT = 240
    cap = cv2.VideoCapture(0)
    cap.set(3, WIDTH)
    cap.set(4, HEIGHT)

    last_color = None
    color_start_time = None

    while True:
        ret, frame = cap.read()
        cv2.rectangle(frame, (WIDTH // 3 - 5, HEIGHT // 5 * 3 - 5), (WIDTH // 3 * 2, HEIGHT), [0, 255, 0], 1)
        isTongue, tongue_color = tongueColorDetect(frame[HEIGHT // 5 * 3:HEIGHT, WIDTH // 3:WIDTH // 3 * 2, :])

        if isTongue:
            if tongue_color:
                cv2.putText(frame, f' {tongue_color}', (5, 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2, 8, 0)
                if last_color == tongue_color:
                    if time.time() - color_start_time >= 2:
                        save_color_to_db(tongue_color, user)
                        break
                else:
                    last_color = tongue_color
                    color_start_time = time.time()
            else:
                cv2.putText(frame, 'ok', (5, 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2, 8, 0)
        else:
            cv2.putText(frame, 'cant found tongue', (5, 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2, 8, 0)

        cv2.imshow('Frame', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def save_color_to_db(color, user):
        customer_id = user.customer_id if user.is_authenticated else '0'
        # 使用Django ORM存储颜色数据
        TongueColor.objects.create(customer_id=customer_id, color=color)