import requests
from bs4 import BeautifulSoup
from typing import Dict
from html import unescape
from termcolor import colored

MENU_URL = "http://menu.dining.ucla.edu/Menus"

def _get_html(url: str) -> str:
    request = requests.get(url)
    if request.status_code == 200:
        return request.content
    else:
        raise Exception("Network Error! Check your connection.")

def _format_output() -> Dict[str, list]:
    html = _get_html(MENU_URL)
    soup = BeautifulSoup(html, "lxml")
    restaurants = soup.find_all('h3')
    menu = soup.find_all("ul", {"class": "sect-list"})
    menu_dict = dict(zip(restaurants, menu))

    res_dict = {}
    for key, value in menu_dict.items():
        name = key.text
        res_dict[name] = []
        dishes = value.find_all('a', {"class": "recipelink"})
        for link in dishes:
            res_dict[name].append(unescape(link.text))
    
    return res_dict

def print_menu_all() -> str:
    menu_dict = _format_output()
    for key, value in menu_dict.items():
        print(colored(key+": ", "white", attrs=['bold']))
        for item in value:
            print("\t"+item)
        print("")


    

