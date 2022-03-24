import socket

sk = socket.socket(type=socket.SOCK_DGRAM)
sk.bind(("", 12345))
sk.settimeout(1)

c = ()


def waitClient():
    print("等待客户端")
    global c
    while True:
        try:
            data, client = sk.recvfrom(1024)
            if data == b"ready":
                c = client
                print("找到了！", "{0}:{1}".format(*client))
                break
        except TimeoutError:
            print("等待客户端")


def sendData(data):
    if len(c) == 2:
        sk.sendto(data, c)
    else:
        print("发送失败，请先调用waitClient获取客户端")


if __name__ == "__main__":
    print(waitClient())
    sendData(bytes(255))
