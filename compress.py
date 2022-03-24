import lz4.block


# lz4压缩
def compress(data):
    # 这里pycharm不知道为啥不识别store_size参数，垃圾pycharm
    compressed = lz4.block.compress(bytes(data), store_size=False)
    return compressed
