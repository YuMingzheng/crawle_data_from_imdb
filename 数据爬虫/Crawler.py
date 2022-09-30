import pandas as pd

from ProcessOneFilm import crawleOneFilm
from saveData import save_film_data
import warnings
warnings.filterwarnings("ignore")


movie_df = pd.read_csv("./ing_data/all_movie_list.csv")
movie_list = movie_df['imdb id'].to_list()

for index , i in enumerate(movie_list):
    print("---------"+str(index)+"-------------")
    film = crawleOneFilm(i)
    if film is not None:
        save_film_data(film , './out/' , 'film.txt')
    else :
        continue

# print(from_douban_get_imdbid("2643010"))