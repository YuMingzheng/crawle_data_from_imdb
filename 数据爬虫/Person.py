class Person:
    personName = ""           # 人名
    personID = ""             # 人的ID

    totalActorFilmBox = 0     # 这个人所主演的电影的票房
    totalDirectFilmBox = 0    # 这个人所指导的电影的票房
    totalWriteFilmBox = 0     # 这个人所编剧的电影的票房
    totalProduceFilmBox = 0   #这个人所发行的电影的票房

    actorFilm = []            # 参演的电影
    directFilm = []           # 导演的电影
    writeFilm = []            # 编剧的电影
    produceFilm = []          # 发行的电影

    def __init__(self , name , ID):
        self.personName = name
        self.personID = ID

    def addActorFilm(self , actorFilm):
        self.actorFilm.append(actorFilm)

    def addDirectFilm(self , directFilm):
        self.directFilm.append(directFilm)

    def addWriteFilm(self , writeFilm):
        self.writeFilm.append(writeFilm)

    def addProduceFilm(self , produceFilm):
        self.produceFilm.append(produceFilm)

    def calcTotalActorFilmBox(self):
        temp = 0
        for i in self.actorFilm:
            temp += i.grossBoxoffice
        self.totalActorFilmBox = temp

    def calcTotalDirectFilmBox(self):
        temp = 0
        for i in self.directFilm:
            temp += i.grossBoxoffice
        self.totalDirectFilmBox = temp

    def calcTotalWriteFilmBox(self):
        temp = 0
        for i in self.writeFilm:
            temp += i.grossBoxoffice
        self.totalWriteFilmBox = temp

    def calcTotalProduceFilmBox(self):
        temp = 0
        for i in self.produceFilm:
            temp += i.grossBoxoffice
        self.totalProduceFilmBox = temp

    def calcAll(self):
        self.calcTotalActorFilmBox()
        self.calcTotalDirectFilmBox()
        self.calcTotalWriteFilmBox()
        self.calcTotalProduceFilmBox()