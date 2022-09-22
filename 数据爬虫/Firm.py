

class Firm:
    firmName = ""         # 公司名称
    firmID = ""           # 公司的IMDB的ID

    totalProdFilmBox = 0  # 该公司所prod的所有电影的票房
    totalDistribBox = 0   # 该公司所distrib的所有电影的票房

    productFilm = []      # 该公司prod的电影list
    distributeFilm = []   # 该公司distrib的电影的list

    def __init__(self , name,  ID):
        self.firmName = name
        self.firmID = ID

    def calcTotalProdFilmBox(self):
        temp = 0
        for i in self.productFilm:
            temp += i.grossBoxoffice

        self.totalProdFilmBox = temp

    def calcTotalDistribBox(self):
        temp = 0
        for i in self.distributeFilm:
            temp += i.grossBoxoffice

        self.totalDistribBox = temp
