import cv2
import numpy as np
from communicate import waitClient, sendData

# 定义屏幕宽度
w = 128
h = 64


# 转换矩阵，原图像乘这个矩阵之后，每行每8个字节字节合成一个字节，
# 之后每行都这样
# 即 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0  转成 255 00
# 若原图大小为64行128列转为64行
# 原因是Adafruit drawBitmap 需要这样的解构
def getConvertMat():
    # 每8位 存到一个字节，计算有多少个字节存到b
    b = w // 8
    zeros = np.zeros((b, w), dtype=np.int32)
    for i, row in enumerate(zeros):
        for offset in range(8):
            row[i * 8 + offset] = 2 ** (7 - offset)
    return zeros.T


waitClient()

operator = getConvertMat()
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
    _, show = cv2.threshold(img_gray, 100, 255, 0)
    bytes_mat = np.dot(binaryImg, operator)
    sendData(bytes(list(bytes_mat.flat)))
    cv2.imshow("capture", binaryImg*255)
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()
