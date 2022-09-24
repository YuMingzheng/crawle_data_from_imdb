from ProcessOneFilm import crawleOneFilm
from saveData import save_film_data
import warnings
warnings.filterwarnings("ignore")


ids = ['tt7362036']

for i in ids:
    film = crawleOneFilm(i)
    if film is not None:
        save_film_data(film , './out/' , 'film.txt')
    else :
        continue


def from_douban_get_imdbid(douban_id : str):
    url = "https://movie.douban.com/subject/" + douban_id
