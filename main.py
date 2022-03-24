# created by Huang Lu
# 27/08/2016 17:05:45 
# Department of EE, Tsinghua Univ.

import cv2
import numpy as np
import socket

# 定义屏幕宽度
w = 128
h = 64

# 每8位 存到一个字节，计算有多少个字节存到b
b = w // 8
zeros = np.zeros((b, w), dtype=np.int32)
for i, row in enumerate(zeros):
    for offset in range(8):
        row[i * 8 + offset] = 2 ** (7 - offset)

mat = zeros.T
print(zeros)
sk = socket.socket(type=socket.SOCK_DGRAM)

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
    bytes_mat = np.dot(binaryImg, mat)
    # print(list(bytes_mat.flat))
    for c in bytes_mat.flat:
        print('%x'%c,end=" ")
    print()
    sk.sendto(bytes(list(bytes_mat.flat)), ("1.1.1.101", 9527))
    cv2.imshow("capture", show)

    # cv2.waitKey(1)

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
cap.release()
cv2.destroyAllWindows()
