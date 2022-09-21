# -*- coding; utf-8 -*-
import requests
from bs4 import BeautifulSoup
import struct
import zlib
import re
from fontTools.ttLib import TTFont


class get_maoyan:
    def __init__(self):
        self.header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Cache-Control": "max-age=0",
                        "Connection": "keep-alive",
                        "Cookie": "__mta=250379193.1530718965618.1552724185734.1552724186874.62; _"
                                  "lxsdk_cuid=16465f5cf2dc8-0994698fdc2ac7-16386950-fa000-16465f5cf2dc8; "
                                  "uuid_n_v=v1; uuid=7C57E28047C311E991B9E9D2BD010A06F94D2F7FE0214E68BD819AD9CE2300A3; _"
                                  "csrf=c2cda66b44c7a9967419cf9f1380acb41f32261f8158b5d047a141f9beefb3a3; _"
                                  "lxsdk=7C57E28047C311E991B9E9D2BD010A06F94D2F7FE0214E68BD819AD9CE2300A3; __"
                                  "mta=250379193.1530718965618.1552724158451.1552724183308.61; _"
                                  "lxsdk_s=1698590d4c2-02c-2b-16a%7C%7C45",
                        "Host": "maoyan.com",
                        "Referer": "https://maoyan.com/board/6",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 "
                                      "(KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}

        self.url = 'https://maoyan.com/board/1'
        self.maoyan_dict = dict()

    def get_page_info(self):
        repon = requests.get(self.url, headers=self.header)
        if repon.status_code == 200:
            soup = BeautifulSoup(repon.text, 'lxml')
        else:
            return -1
        # 获得当前页面的字体文件路径
        woff_style = soup.select('style')[0]
        # print(woff_style)
        for line in woff_style.text.split('\n'):
            if 'woff' in line:
                is_line = line
        font_url = 'http:' + re.search('//vfile.*?(woff)', is_line).group(0)
        self.maoyan_dict = self.get_maoyan_dict(font_url)
        # print(self.maoyan_dict)

        movies = soup.select('.board-wrapper')
        movie_list = movies[0].select('dd')
        for i in range(len(movie_list)):
            movie_name = movie_list[i].select('.movie-item-info')[0].select('.name')[0].text
            movie_star = movie_list[i].select('.star')[0].text[3:]
            movie_date = movie_list[i].select('.releasetime')[0].text
            real_money = movie_list[i].select('.realtime')[0].select('.stonefont')[0].text
            real_unit = movie_list[i].select('.realtime')[0].text[-2]
            total_money = movie_list[i].select('.total-boxoffice')[0].select('.stonefont')[0].text
            total_unit = movie_list[i].select('.total-boxoffice')[0].text[-2]

            print('电影: ', movie_name)
            print('主演: ', movie_star)
            print('上映时间: ', movie_date)
            print('实时票房: ', self.convert_boxoffice(real_money), real_unit)
            print('总票房: ', self.convert_boxoffice(total_money), total_unit)

    def get_maoyan_dict(self, url):
        font_woff = requests.get(url, stream=True)
        with open('maoyan.woff', 'wb') as w:
            for bunk in font_woff:
                w.write(bunk)

        base_font = TTFont('basefont.woff')
        base_num = ['8', '7', '9', '0', '1', '5', '4', '6', '3', '2']
        base_code = ['uniF860', 'uniF408', 'uniEF2B', 'uniF875', 'uniE03A', 'uniEA55', 'uniEE0E', 'uniF7A4', 'uniE3B1', 'uniF813']
        onlineFonts = TTFont('maoyan.woff')
        uni_list = onlineFonts.getGlyphNames()[1:-1]
        temp = {}
        for i in range(10):
            onlineGlyph = onlineFonts['glyf'][uni_list[i]]
            for j in range(10):
                baseGlyph = base_font['glyf'][base_code[j]]
                if onlineGlyph == baseGlyph:
                    temp[uni_list[i][3:].lower()] = base_num[j]
        return temp

    def convert_boxoffice(self, money):
        byte_money = money.__repr__()
        # print(byte_money)
        money_num_list = byte_money.split('\\u')
        # print(money_num_list)
        rea_money = ''
        for byte_num in money_num_list:
            num = self.maoyan_dict.get(byte_num[:4], byte_num[:4])
            # print(byte_num, num)
            rea_money = f'{rea_money}{num}{byte_num[4:]}'
        return rea_money[1:-1]


if __name__ == '__main__':
    a = get_maoyan()
    a.get_page_info()

