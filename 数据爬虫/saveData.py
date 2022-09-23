import pandas as pd
import os


def saveData(path, filename, data):
    # 如果路径不存在，就创建路径
    if not os.path.exists(path):
        os.makedirs(path)

    # 保存文件
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(path + filename, encoding='utf_8',mode = 'a' ,index=False, sep=',', header=False)