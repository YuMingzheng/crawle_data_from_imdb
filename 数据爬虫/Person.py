# from ProcessOneFilm import procBox
from saveLog import saveLog
import warnings
warnings.filterwarnings('ignore')

def procBox(string) -> float:
    # moneyType = 1 if string[0] == '$' else -1
    return float(string[1:].replace("," , ""))

def justGetBox(ID)->float:
    import requests
    from bs4 import BeautifulSoup
    url = "https://www.imdb.com/title/" + ID  # 拼接得到URL
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    }
    resp = requests.get(url=url, headers=header)
    resp.raise_for_status()
    # resp.encoding = resp.apparent_encoding

    soup = BeautifulSoup(resp.text, "html.parser")

    try:
        raw_box = soup.find("section" , attrs = {"data-testid":"BoxOffice"}).find("li" , attrs = {"data-testid":"title-boxoffice-cumulativeworldwidegross"}).find("ul").text
        return procBox(raw_box)
    except AttributeError as e:
        saveLog(e.args[0])
        return 0.0

def getAllRelateMovie(soup):
    '''

    :param soup:
    :return: DataFrame(cols = ["ID" , "Name" , "Box"])
    '''
    import pandas as pd
    import re
    all_movie = soup.find_all("div" , recursive= False)
    df = pd.DataFrame(columns=["ID" , "Name" , "Box"])
    for i, v in enumerate(all_movie):
        print("  i = " , i)
        try:
            if 2016 < int(v.find("span").text.strip()) < 2022:
                temp_dict = {
                    "ID":  re.findall('tt[0-9]*' , v.attrs.get('id'))[0],
                    "Name": v.find("b").text,
                    "Box": 0.0
                }
                temp_dict["Box"] = justGetBox(temp_dict['ID'])
                df = df.append(temp_dict, ignore_index=True)
                df = df[df['Box'] != 0]
        except ValueError as e:
            continue

    return df

class Person:

    def __init__(self , name : str , ID : str , flag = True):
        print("__init__...")
        self.personName = name  # 人名
        self.personID = ID      # 人的ID

        self.totalActorFilmBox = 0  # 这个人所主演的电影的票房
        self.totalDirectFilmBox = 0  # 这个人所指导的电影的票房
        self.totalWriteFilmBox = 0  # 这个人所编剧的电影的票房
        # self.totalProduceFilmBox = 0  # 这个人所发行的电影的票房

        self.actorFilm = []  # 参演的电影
        self.directFilm = []  # 导演的电影
        self.writeFilm = []  # 编剧的电影
        self.produceFilm = []  # 发行的电影

        if flag:
            self.crawlPersonInfo(self.personID)

    # 在构造的时候就应该爬到该Person全部的信息
    def crawlPersonInfo(self , ID):
        print("crawlPersonInfo...of " , self.personName)
        import requests
        from bs4 import BeautifulSoup

        url = "https://www.imdb.com/name/" + ID
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        }
        resp = requests.get(url=url, headers=header)
        resp.raise_for_status()
        # resp.encoding = resp.apparent_encoding

        soup = BeautifulSoup(resp.text)

        l = soup.find("div" , attrs = {"id":"filmography"}).find_all("div" , recursive= False)
        for i , v in enumerate(l):
            if v.attrs.get('id') == "filmo-head-actor" or v.attrs.get('id') == "filmo-head-actress":
                print("actor..")
                df = getAllRelateMovie(l[i+1])
                self.actorFilm.append(df)
                self.totalActorFilmBox = df["Box"].mean()
            elif v.attrs.get('id') == "filmo-head-director":
                print("director..")
                df = getAllRelateMovie(l[i+1])
                self.directFilm.append(df)
                self.totalDirectFilmBox = df["Box"].mean()
            elif v.attrs.get('id') == "filmo-head-writer":
                print("writer..")
                df = getAllRelateMovie(l[i+1])
                self.writeFilm.append(df)
                self.totalWriteFilmBox = df["Box"].mean()
            # elif v.attrs.get('id') == "filmo-head-producer":
            #     print("producer...")
            #     df = getAllRelateMovie(l[i+1])
            #     self.produceFilm.append(df)
            #     self.totalProduceFilmBox = df["Box"].sum()





    def addActorFilm(self , actorFilm):
        self.actorFilm.append(actorFilm)

    def addDirectFilm(self , directFilm):
        self.directFilm.append(directFilm)

    def addWriteFilm(self , writeFilm):
        self.writeFilm.append(writeFilm)

    def addProduceFilm(self , produceFilm):
        self.produceFilm.append(produceFilm)

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