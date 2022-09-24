import pandas as pd
import os


def save_film_data(film , path, filename):
    import os
    # 如果路径不存在，就创建路径
    if not os.path.exists(path):
        os.makedirs(path)

    # 保存文件
    data_l = [
        film.filmID,
        film.filmName,
        film.releaseDate,
        str(film.duration),
        "|".join(film.filmType),
        str(film.grossBoxoffice),
        str(film.totalActorBox),
        str(film.totalDirectBox),
        str(film.totalWriteBox),
        # str(self.totalProducBox),
        str(film.totalProducFirmBox),
        str(film.totalDistributeFirmBox)

    ]
    print(data_l)

    with open(path + filename, encoding='utf_8', mode='a') as f:
        f.write(",".join(data_l) + "\n")

def saveData(path, filename, data):
    # 如果路径不存在，就创建路径
    if not os.path.exists(path):
        os.makedirs(path)

    # 保存文件
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(path + filename, encoding='utf_8',mode = 'a' ,index=False, sep=',', header=False)
