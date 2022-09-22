

class Film:
    filmName = ""               # 电影名字
    filmID = ""                 # 电影的IMDB的ID
    releaseDate = ""            # 上映时间
    duration = 0                # 市场，单位：分钟
    fimeType = []               # 电影类型，先用列表存起来，之后再处理

    grossBoxoffice = 0          # 总票房

    totalActorBox = 0           # 所有主演的票房总收入
    totalDirectBox = 0          # 所有导演的票房总收入
    totalWriteBox = 0           # 所有编剧的票房总收入
    totalProducBox = 0          # 所有发行人的票房总收入
    totalProducFirmBox = 0      # 所有制作公司的票房总收入
    totalDistributeFirmBox = 0  # 所有发行公司的票房总收入

    actorList = []              # 主演列表
    directList = []             # 导演列表
    writerList = []             # 编剧列表
    producerList = []           # 发行人列表

    productionFirm = []         # 制作公司
    distributeFirm = []         # 发行公司

    def __init__(self , name, ID):
        self.filmName = name
        self.filmID = ID

    def addActor(self , actor):
        self.actorList.append(actor)

    def addDirect(self , direct):
        self.directList.append(direct)

    def addWriter(self , writer):
        self.writerList.append(writer)

    def addProducer(self , producer):
        self.producerList.append(producer)




