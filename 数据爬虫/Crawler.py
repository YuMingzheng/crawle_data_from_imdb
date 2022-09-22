import requests
import re
import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


base_url = "https://www.imdb.com/title/tt7362036/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}
