import cv2
import numpy as np
from communicate import waitClient, sendData
from compress import compress

# 定义屏幕宽度
w = 128
h = 64


# 转换矩阵，原图像乘这个矩阵之后，每行每8个字节字节合成一个字节，
# 之后每行都这样
# 即 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0  转成 255 00
# 若原图大小为64行128列转为64行16列
# 也就是横向每8个压缩成一个
# 原因是Adafruit drawBitmap 需要这样的解构
def getConvertMat():
    # 每8位 存到一个字节，计算有多少个字节存到b
    b = w // 8
    zeros = np.zeros((b, w), dtype=np.int32)
    for i, row in enumerate(zeros):
        for offset in range(8):
            row[i * 8 + offset] = 2 ** (7 - offset)
    return zeros.T


# 转换矩阵，原图像乘这个矩阵之后，第一列前8行合成一个，然后是第二列前八行。。。。。
#                             然后是第一列8-16行  然后是第二列8-16行
# 之后每行都这样
# 若原图大小为64行128列转为8行128列
# 纵向每8个压缩成一个
# 原因是Adafruit 的 buffer，也是ssd1306的buffer就是这样的解构，这就不用转换了，直接内存拷贝进去，节省时间
def getConvertMatB():
    # 每8位 存到一个字节，计算有多少个字节存到b
    b = h // 8
    zeros = np.zeros((b, h), dtype=np.int32)
    for i, row in enumerate(zeros):
        for offset in range(8):
            row[i * 8 + offset] = 2 ** offset
    return zeros


waitClient()

operator = getConvertMatB()
cap = cv2.VideoCapture("badapple60.mp4")

while (1):
    # get a frame
    _, frame = cap.read()
    if frame is None:
        break
    # show a frame
    res = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)
    img_gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    _, binaryImg = cv2.threshold(img_gray, 100, 1, 0)
    # bytes_mat = np.dot(binaryImg, operator)
    bytes_mat = np.dot(operator, binaryImg)
    sendData(compress(list(bytes_mat.flat)))
    cv2.imshow("capture", binaryImg * 255)
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()
