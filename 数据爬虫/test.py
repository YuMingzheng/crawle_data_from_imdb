import Film
import Person

film1 = Film.Film("film1" ,  "film1.id")
film1.setGrossBoxoffice(111111)

film2 = Film.Film("film2" , "film2.id")
film2.setGrossBoxoffice(222222)

actor1 = Person.Person("actor1" , "actor1.id")
actor2 = Person.Person("actor2" , "actor2.id")

direc1 = Person.Person("dirct1" , "direc1.id")

# film1.addActor(actor1)
# film2.addActor(actor2)

film1.addDirect(direc1)
film2.addDirect(direc1)


direc1.addDirectFilm(film1)
direc1.addDirectFilm(film2)
direc1.calcAll()

direc1.calcAll()
film1.calcAll()
film2.calcAll()

print(film1.totalDirectBox)
i=1




