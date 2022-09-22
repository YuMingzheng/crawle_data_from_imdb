import requests
import re
import os
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup

import warnings

warnings.filterwarnings("ignore")


def CrawlerOneFilm(filmId):
    # 函数功能：传入一个IMDB电影的ID，返回电影的全部特征
    # In: filmId
    # return : 全部特征

    url = "https://www.imdb.com/title/" + filmId

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
        }
        resp = requests.get(url = url , headers = headers)
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
    except ConnectionError as e:
        print("Error:" , e.args)
        return ""
    



base_url = "https://www.imdb.com/title/tt7362036/"
