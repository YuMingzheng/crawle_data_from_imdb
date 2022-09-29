import re

from ProcessOneFilm import crawleOneFilm
from saveData import save_film_data
import warnings
warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup


def from_douban_get_imdbid(douban_id : str):
    import requests
    from bs4 import BeautifulSoup
    import time
    url = "https://movie.douban.com/subject/" + douban_id
    douban_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    }
    cookie = {
        'cookie': 'll="118254"; bid=JjNjUx_X__A; __utmz=30149280.1663765422.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _vwo_uuid_v2=D75064BA3572224A69942C478F080A99F|b5336ef789adc779a8ab04bd6fb58743; viewed="35681856"; gr_user_id=d107d974-a76c-4062-bf2c-12014ea12e86; dbcl2="191413562:6X2MeYrmrR4"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.19141; ck=cscU; __utmc=30149280; __utmc=223695111; __utma=30149280.68016018.1663765422.1664020362.1664028125.10; __utmt=1; __utmb=30149280.2.10.1664028125; __utma=223695111.658081827.1663765422.1664020362.1664028241.9; __utmb=223695111.0.10.1664028241; __utmz=223695111.1664028241.9.4.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ses.100001.4cf6=*; _pk_ref.100001.4cf6=["","",1664028241,"https://www.douban.com/"]; _pk_id.100001.4cf6=2e9ec54f24bd52d3.1663765421.9.1664028244.1664023821.; ap_v=0,6.0'
    }
    try:
        resp = requests.get(url=url, headers=douban_header , cookies = cookie)
    except requests.exceptions.ConnectionError as e:
        time.sleep(5)
        resp = requests.get(url=url, headers=douban_header)
    if resp.status_code != 200:
        resp = requests.get(url=url, headers=douban_header, cookie=cookie)
    douban_soup = BeautifulSoup(resp.text)
    try:
        text = douban_soup.find("div" , attrs = {"id" : "info"}).text.replace("\n" , "")
    except AttributeError as e:
        return ""
    if "IMDb" in text:
        return re.findall("IMDb: tt[0-9]*" , text)[0].replace("IMDb: " , "")
    else:
        return ""


ids = set()

with open("./douban/html.html" , "r", encoding="utf-8") as f:
    lis_text = f.read()

lis_soup = BeautifulSoup(lis_text)
lis = lis_soup.find("ul" , attrs = {"class" : "explore-list"}).find_all("li" , recursive=False)
for li in lis:
    ids.add(re.findall("[0-9]+" ,li.find("a" , recursive=False).attrs['href'])[0])
# print(ids)
for index , i in enumerate(ids):
    print("---------"+str(index)+"-------------")
    imdbid = from_douban_get_imdbid(i)
    if imdbid != "":
        film = crawleOneFilm(imdbid)
        if film is not None:
            save_film_data(film , './out/' , 'film.txt')
        else :
            continue


# print(from_douban_get_imdbid("2643010"))