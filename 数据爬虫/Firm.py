from saveLog import saveLog
import time
import warnings
import json
warnings.filterwarnings('ignore')

def procBox(string) -> float:
    # moneyType = 1 if string[0] == '$' else -1
    return float(string[1:].replace("," , ""))
def justGetBox(ID)->float:
    import requests
    from bs4 import BeautifulSoup
    url = "https://www.imdb.com/title/" + ID
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
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
        return procBox(raw_box)
    except AttributeError as e:
        saveLog(e.args[0])
        return 0.0

class Firm:

    def __init__(self , name : str,  ID : str , flag = True):
        self.firmName = name   # 公司名称
        self.firmID = ID       # 公司的IMDB的ID

        self.totalFilmBox = 0  # 该公司所prod的所有电影的票房

        self.film = []  # 该公司prod的电影list

        if flag:
            self.crawlFirmInfo(self.firmID)

    # 在构造的时候就应该爬到该Firm全部的信息
    def crawlFirmInfo(self, ID):
        import pandas as pd
        import requests
        from bs4 import BeautifulSoup
        import re

        url = "https://www.imdb.com/search/title/?companies=" + ID + "&sort=year,desc"
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

        main_soup = soup.find("div" , attrs = {"class" : "article"})
        list_soup = main_soup.find("div" , attrs = {"class" : "lister-list"}).find_all("div" , recursive= False)

        movie_list = pd.DataFrame(columns=["ID" , "Name" , "Box"])
        for i , v in enumerate(list_soup):
            year_l = re.findall(r"\d{4}" , v.find("h3").find("span" , attrs = {"class":"lister-item-year text-muted unbold"}).text.strip())
            if len(year_l) == 0:
                continue
            year = int(year_l[0])
            if 2016 < year < 2022:
                temp = {
                    "ID": re.findall(r"tt\d+",v.find("div", attrs={"class": "lister-item-content"}).find("h3").find("a").attrs.get("href"))[0],
                    "Name":v.find("div", attrs={"class": "lister-item-content"}).find("h3").find("a").text,
                    "Box": 0.0
                }
                with open("./ing_data/film.json") as f:
                        current_film = json.load(f)
                if temp['ID'] not in current_film.keys():
                    temp["Box"] = justGetBox(temp["ID"])
                    current_film[temp['ID']] = temp['Box']
                    with open('./ing_data/film.json', 'w') as file:
                        json.dump(current_film, file)
                else :
                    temp['Box'] = current_film[temp['ID']]
                movie_list = movie_list.append(temp , ignore_index=True)
        movie_list = movie_list[movie_list['Box'] != 0]
        self.film.append(movie_list)
        self.totalFilmBox = movie_list["Box"].sum()


    def __str__(self):
        return "Name: " + self.firmName + " ,ID: " + self.firmID

# f1 = Firm("Beijing Culture" , "co0707720")
#
# i=0