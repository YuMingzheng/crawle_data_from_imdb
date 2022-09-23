import json

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

import Firm
import Person
from saveLog import saveLog

import warnings
warnings.filterwarnings("ignore")


def crawleOneFilm(IMDBID : str):
    import Film

    url = "https://www.imdb.com/title/" + IMDBID  # 拼接得到URL
    header = {
        "accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        "sec-ch-us" : '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"'
    }
    resp = requests.get(url = url , headers = header)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding

    soup = BeautifulSoup(resp.text , "html.parser")

    filmName = soup.find("h1" , attrs={"data-testid":"hero-title-block__title"}).text
    film = Film.Film(filmName , IMDBID)

    # release date
    date = findReleaseDate(soup)
    film.setReleaseDate(date)

    # duration
    duration = findDuration(soup)
    film.setDuration(duration)

    # type(genres)
    genres = findGenres(soup)
    film.setFilmType(genres)

    # boxoffice
    boxoffice = findBoxoffice(soup)
    film.setGrossBoxoffice(boxoffice)

    # actor director writer producer productionFirm distributeFirm
    fullCredit = getFullCredits(IMDBID)
    film.actorList = fullCredit['actor']
    film.directList = fullCredit['director']
    film.writerList = fullCredit['writer']

    # 人员的票房
    _act_box = 0
    for i in film.actorList:
        _act_box += i.totalActorFilmBox
    film.totalActorBox = _act_box

    _dir_box = 0
    for i in film.directList:
        _dir_box += i.totalDirectFilmBox
    film.totalDirectBox = _dir_box

    _wri_box = 0
    for i in film.writerList:
        _wri_box += i.totalWriteFilmBox
    film.totalWriteBox = _wri_box

    # 公司的票房
    fullComp = getFullComp(IMDBID)
    film.productionFirm = fullComp['production']
    film.distributeFirm = fullComp['distributors']

    # 公司的票房
    _prod_firm_box = 0
    for i in film.productionFirm:
        _prod_firm_box += i.totalFilmBox
    film.totalProducFirmBox = _prod_firm_box

    _distr_firm_box = 0
    for i in film.distributeFirm:
        _distr_firm_box += i.totalFilmBox
    film.totalDistributeFirmBox = _distr_firm_box

    return film

def findReleaseDate(soup) -> str:
    try:
        return soup.find("section" , attrs={"data-testid":"Details"}).find("li" , attrs = {"data-testid":"title-details-releasedate"}).find("div").text
    except AttributeError as e:
        saveLog(e.args)
        return ""

def findDuration(soup) -> int:
    try:
        raw_dura = soup.find("section" , attrs = {"data-testid":"TechSpecs"}).find("li" , attrs = {"data-testid":"title-techspec_runtime"}).find("div").text
        return procRawDuartion(raw_dura)
    except AttributeError as e:
        saveLog(e.args)
        return -1

def procRawDuartion(string) -> int:
    '''

    :param string:
    :return: -1 表示有错误
    '''
    try:
        li = string.replace("minutes" , "").split("hour")
        return eval(li[0]) * 60 + eval(li[1])
    except IndexError as e:
        saveLog(e.args)
        return -1

def findGenres(soup) -> list:
    try:
        result = []
        for i in soup.find("div", attrs={"data-testid": "genres"}).find_all("a"):
            result.append(i.text)
        return result
    except AttributeError as e:
        saveLog(e.args)
        return []

def findBoxoffice(soup) -> float:
    try:
        raw_box = soup.find("section" , attrs = {"data-testid":"BoxOffice"}).find("li" , attrs = {"data-testid":"title-boxoffice-cumulativeworldwidegross"}).find("ul").text
        return procBox(raw_box)
    except AttributeError as e:
        saveLog(e.args)
        return 0.0

def procBox(string) -> float:
    # moneyType = 1 if string[0] == '$' else -1
    return float(string[1:].replace("," , ""))

def getFullCredits(IMDBID) -> dict:
    url = "https://www.imdb.com/title/"+IMDBID+"/fullcredits"
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
    }
    resp = requests.get(url = url , headers = header)
    resp.raise_for_status()
    # resp.encoding = resp.apparent_encoding

    soup = BeautifulSoup(resp.text)

    fullList = {
        'actor':[],
        'director':[],
        'writer':[]
        # 'producer':[]
    }
    title_l = soup.find("div", attrs={'id': 'fullcredits_content'}).find_all("h4")
    table_l = soup.find("div", attrs={'id': 'fullcredits_content'}).find_all("table")
    if len(title_l) != len(table_l):
        saveLog("IMDBID: " + IMDBID + ", 在获取fullcredit时发生两个list长度不相等的问题\n")
        return fullList

    actor_list = []
    directer_list = []
    writer_list = []
    # producer_list = []
    for i , u in enumerate(title_l):
        text = re.sub("\(.*\)" , "" , u.text).strip()
        if text == "Cast":
            c_odd_list = table_l[i].find_all("tr" , attrs={"class" : "odd"})
            c_even_list = table_l[i].find_all("tr" , attrs={"class" : "even"})
            for j,v in enumerate(c_odd_list):
                name = v.find_all("td")[1].text.strip()
                ID = re.findall('nm\d*' , v.find_all("a")[1].attrs.get("href"))[0]
                actor_list.append(Person.Person(name , ID))
            for j,v in enumerate(c_even_list):
                name = v.find_all("td")[1].text.strip()
                ID = re.findall('nm\d*' , v.find_all("a")[1].attrs.get("href"))[0]
                actor_list.append(Person.Person(name , ID))

        elif text == "Directed by":
            d_tr_list = table_l[i].find_all("tr")
            for j, v in enumerate(d_tr_list):
                name = v.find("a").text.strip()
                ID = re.findall('nm\d*', v.find("a").attrs.get("href"))[0]
                person = Person.Person(name, ID)
                directer_list.append(person)

        elif text == "Writing Credits":
            w_tr_list = table_l[i].find_all("tr")
            for j, v in enumerate(w_tr_list):
                name = v.find("a").text.strip()
                ID = re.findall('nm\d*', v.find("a").attrs.get("href"))[0]
                person = Person.Person(name, ID)
                writer_list.append(person)

            pass
        # elif text == "Produced by":
        #     # p_tr_list = table_l[i].find_all("tr")
        #     # for j, v in enumerate(p_tr_list):
        #     #     name = v.find("a").text.strip()
        #     #     ID = re.findall('nm\d*', v.find("a").attrs.get("href"))[0]
        #     #     person = Person.Person(name, ID)
        #     #     writer_list.append(person)
        #
        #     pass

    fullList['actor'] = actor_list
    fullList['director'] = directer_list
    fullList['writer'] = writer_list

    return fullList

def getFullComp(IMDBID) -> dict:
    with open("./ing_data/firm.json") as f:
        current_firm = json.load(f)

    url = "https://www.imdb.com/title/"+IMDBID+"/companycredits"
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
    }
    resp = requests.get(url=url, headers=header)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text)

    soup_content = soup.find("div" , attrs = {"id":"company_credits_content"})
    soup_h4 = soup_content.find_all("h4" , recursive= False)
    soup_ul = soup_content.find_all("ul" , recursive= False)

    prod_comp = []
    distr_comp = []

    for i , v in enumerate(soup_h4):
        if v.attrs.get("id") == "production":
            a_s = soup_ul[i].find_all("a")
            for j in a_s:
                firm_name = j.text
                firm_id = re.findall('/company/co[0-9]*' , j.attrs.get("href"))[0]
                firm_id = firm_id.replace("/company/" , "")
                if firm_id in current_firm.keys():
                    firm_temp = Firm.Firm(firm_name , firm_id , False)
                    firm_temp.totalFilmBox = current_firm[firm_id]
                else:
                    firm_temp = Firm.Firm(firm_name, firm_id)
                    current_firm[firm_id] = firm_temp.totalFilmBox
                    with open('./ing_data/firm.json', 'w') as file:
                        json.dump(current_firm, file)
                prod_comp.append(firm_temp)

        elif v.attrs.get("id") == "distributors":
            a_s = soup_ul[i].find_all("a")
            for j in a_s:
                firm_name = j.text
                firm_id = re.findall('/company/co[0-9]*', j.attrs.get("href"))[0]
                firm_id = firm_id.replace("/company/", "")
                if firm_id in current_firm.keys():
                    firm_temp = Firm.Firm(firm_name , firm_id , False)
                    firm_temp.totalFilmBox = current_firm[firm_id]
                else:
                    firm_temp = Firm.Firm(firm_name, firm_id)
                    current_firm[firm_id] = firm_temp.totalFilmBox
                    with open('./ing_data/firm.json', 'w') as file:
                        json.dump(current_firm, file)
                distr_comp.append(firm_temp)

    fullComp = {
        'production': prod_comp,
        'distributors': distr_comp
    }
    return fullComp



# info =  getFullComp("tt7362036")
#
# i = 1