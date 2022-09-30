import warnings
warnings.filterwarnings('ignore')

class Film:
    def __init__(self , name:str, ID:str):
        self.filmName = name  # 电影名字
        self.filmID = ID  # 电影的IMDB的ID

        self.releaseDate = ""  # 上映时间
        self.duration = 0  # 市场，单位：分钟
        self.filmType = []  # 电影类型，先用列表存起来，之后再处理
        self.grossBoxoffice = 0  # 总票房

        self.totalActorBox = 0  # 所有主演的票房总收入
        self.totalDirectBox = 0  # 所有导演的票房总收入

        self.totalProducFirmBox = 0  # 所有制作公司的票房总收入

        self.actorList = []  # 主演列表
        self.directList = []  # 导演列表

        self.productionFirm = []  # 制作公司


    def addActor(self , actor):
        self.actorList.append(actor)

    def addDirect(self , direct):
        self.directList.append(direct)

    # def calcTotalActorBox(self):
    #     temp = 0
    #     for i in self.actorList:
    #         temp += i.totalActorFilmBox
    #     self.totalActorBox = temp
    #
    # def calcTotalDirectBox(self):
    #     temp = 0
    #     for i in self.directList:
    #         temp += i.totalDirectFilmBox
    #     self.totalDirectBox = temp
    #
    # def calcTotalWriteBox(self):
    #     temp = 0
    #     for i in self.writerList:
    #         temp += i.totalWriteFilmBox
    #     self.totalWriteBox = temp
    #
    #
    # def clacTotalProducFirmBox(self):
    #     temp = 0
    #     for i in self.productionFirm:
    #         temp += i.totalProdFilmBox
    #     self.totalProducFirmBox = temp
    #
    # def calcTotalDistributeFirmBox(self):
    #     temp = 0
    #     for i in self.distributeFirm:
    #         temp += i.totalDistribBox
    #     self.totalDistributeFirmBox = temp
    #
    # def calcAll(self):
    #     self.calcTotalActorBox()
    #     self.calcTotalDirectBox()
    #     self.calcTotalWriteBox()
    #     self.clacTotalProducFirmBox()
    #     self.calcTotalDistributeFirmBox()

    def setReleaseDate(self , date:str):
        self.releaseDate = date

    def setDuration(self , duration:int):
        self.duration = duration

    def setFilmType(self , filmType:list):
        self.filmType = filmType

    def setGrossBoxoffice(self , money:float):
        self.grossBoxoffice = money

    def __str__(self):
        return "Name:" + self.filmName + ",ID:" + self.filmID




