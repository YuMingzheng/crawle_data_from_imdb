from saveLog import saveLog
import time
import warnings
import json
warnings.filterwarnings('ignore')

def procBox(string , IMDBID) -> float:
    # moneyType = 1 if string[0] == '$' else -1
    if string[0] != "$":
        saveLog(IMDBID + "不是美元")
    return float(string[1:].replace(",", ""))

def justGetBox(ID , IMDBID)->float:
    with open("./ing_data/film.json") as f:
        current_film = json.load(f)
    if ID in current_film.keys():
        return current_film[ID]

    import requests
    from bs4 import BeautifulSoup
    url = "https://www.imdb.com/title/" + ID  # 拼接得到URL
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'cookie': 'uu=eyJpZCI6InV1Yzc2M2Q0ZWI2YmQ3NGRiZGFmM2EiLCJwcmVmZXJlbmNlcyI6eyJmaW5kX2luY2x1ZGVfYWR1bHQiOmZhbHNlfX0=; adblk=adblk_no; session-id=132-5398336-5861824; session-id-time=2082787201l; ubid-main=134-4497815-6177129; session-token=VuAAEN7JmW2km1JuyfTtrf0mKknQ+XG/SVU+EhOyEepD0XraTZhxdwfK0jX1ru8rzjz7DUeE/JT98u6Sj8nrZxHKXsBcAK6wmSQzJaYyWSmS3olZPaw0sdYpGiG6s5zG3qRYREK7dyt92g7/lEQH5MoalaR4/9LdcXxtVMFsB6TmvDni3+lVggpCh8k17mLYaPuGe9eRHt+AHLwXQeuRdg==; csm-hit=tb:M6XPNMWR67C4FRHDZE47+s-M6XPNMWR67C4FRHDZE47|1664064346523&t:1664064346523&adb:adblk_no',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1'
    }
    try:
        resp = requests.get(url=url, headers=header)
    except requests.exceptions.ConnectionError as e:
        time.sleep(10)
        resp = requests.get(url=url, headers=header)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    try:
        raw_box = soup.find("section" , attrs = {"data-testid":"BoxOffice"}).find("li" , attrs = {"data-testid":"title-boxoffice-cumulativeworldwidegross"}).find("ul").text
        box = procBox(raw_box , IMDBID)
        current_film[ID] = box
        with open('./ing_data/film.json', 'w') as file:
            json.dump(current_film, file)

        return box
    except AttributeError as e:
        saveLog(e.args[0])
        return 0.0

def getAllRelateMovie(soup , IMDBID):
    '''
    :param IMDBID:
    :param soup:
    :return: DataFrame(cols = ["ID" , "Name" , "Box"])
    '''
    import pandas as pd
    import re
    all_movie = soup.find_all("div" , recursive= False)
    df = pd.DataFrame(columns=["ID" , "Name" , "Box"])
    count = 0
    for i, v in enumerate(all_movie):
        if count > 5:
            break
        try:
            year = v.find("span").text.strip()
            if year == "":
                continue
            if 2016 < int(re.findall(r"\d+" , year)[0])< 2022:
                temp_dict = {
                    "ID":  re.findall(r'tt[0-9]+' , v.attrs.get('id'))[0],
                    "Name": v.find("b").text,
                    "Box": 0.0
                }
                temp_dict["Box"] = justGetBox(temp_dict['ID'] , IMDBID)
                df = df.append(temp_dict, ignore_index=True)
                count +=1
        except ValueError as e:
            continue

    df = df[df['Box'] != 0.0]
    return df

class Person:

    def __init__(self , name : str , ID : str , flag = True):
        self.personName = name  # 人名
        self.personID = ID      # 人的ID

        self.totalActorFilmBox = 0  # 这个人所主演的电影的票房
        self.totalDirectFilmBox = 0  # 这个人所指导的电影的票房

        self.actorFilm = []  # 参演的电影
        self.directFilm = []  # 导演的电影

        if flag:
            self.crawlPersonInfo(self.personID)

    # 在构造的时候就应该爬到该Person全部的信息
    def crawlPersonInfo(self , ID):
        # print("  crawlPersonInfo...of " , self.personName)
        import requests
        from bs4 import BeautifulSoup

        url = "https://www.imdb.com/name/" + ID
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",

        }
        try:
            resp = requests.get(url=url, headers=header)
        except requests.exceptions.ConnectionError as e:
            time.sleep(10)
            resp = requests.get(url=url, headers=header)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text)

        l = soup.find("div" , attrs = {"id":"filmography"}).find_all("div" , recursive= False)
        for i , v in enumerate(l):
            if v.attrs.get('id') == "filmo-head-actor" or v.attrs.get('id') == "filmo-head-actress":
                df = getAllRelateMovie(l[i+1] , IMDBID = ID)
                self.actorFilm.append(df)
                self.totalActorFilmBox = df["Box"].sum()
            elif v.attrs.get('id') == "filmo-head-director":
                df = getAllRelateMovie(l[i+1] , IMDBID = ID)
                self.directFilm.append(df)
                self.totalDirectFilmBox = df["Box"].sum()

    def addActorFilm(self , actorFilm):
        self.actorFilm.append(actorFilm)

    def addDirectFilm(self , directFilm):
        self.directFilm.append(directFilm)


    # def calcTotalActorFilmBox(self):
    #     temp = 0
    #     for i in self.actorFilm:
    #         temp += i.grossBoxoffice
    #     self.totalActorFilmBox = temp
    #
    # def calcTotalDirectFilmBox(self):
    #     temp = 0
    #     for i in self.directFilm:
    #         temp += i.grossBoxoffice
    #     self.totalDirectFilmBox = temp
    #
    # def calcTotalWriteFilmBox(self):
    #     temp = 0
    #     for i in self.writeFilm:
    #         temp += i.grossBoxoffice
    #     self.totalWriteFilmBox = temp
    #
    # def calcTotalProduceFilmBox(self):
    #     temp = 0
    #     for i in self.produceFilm:
    #         temp += i.grossBoxoffice
    #     self.totalProduceFilmBox = temp
    #
    # def calcAll(self):
    #     self.calcTotalActorFilmBox()
    #     self.calcTotalDirectFilmBox()
    #     self.calcTotalWriteFilmBox()
    #     self.calcTotalProduceFilmBox()

    def __str__(self):
        return "Name: " + self.personName + ",ID: " + self.personID

# xuzheng = Person("Zheng Xu" , "nm1905770")
#
# i = 0