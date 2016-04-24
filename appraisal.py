import bs4
import re
import requests
import statistics


def _get_page_soup(url):
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, "lxml")
    return soup

def get_effect_averages():
    soup = _get_page_soup("http://backpack.tf/effects")
    effects = soup.find_all("li", class_="item")
    effects.sort(key=lambda effect: effect["data-effect_name"])
    averages = {}
    for effect in effects:
        price_soup = effect.find("span", class_="bottom-right")
        if price_soup is not None:
            res = re.match(r"avg (\d+\.?[\d?]+) keys", price_soup.contents[0])
            averages[effect["data-effect_name"]] = float(res.groups()[0])
    return averages


def get_price_averages(hat):
    soup = _get_page_soup("http://backpack.tf/unusuals/" + hat)
    unusuals = soup.find_all("li", class_="item")
    unusuals.sort(key=lambda unusual: unusual["data-effect_name"])
    averages = {}
    for unusual in unusuals:
        price_soup = unusual.find("span", class_="bottom-right")
        if price_soup is not None:
            res = re.match(r"~(\d+\.?[\d?]+) keys", price_soup.contents[0])
            averages[unusual["data-effect_name"]] = float(res.groups()[0])
    return averages

EFFECT_AVERAGES = get_effect_averages()


def get_price(hat, effect):
    hat_averages = get_price_averages(hat)
    price_values = []
    for key in hat_averages.keys():
        price_values.append(hat_averages[key] / EFFECT_AVERAGES[key] * EFFECT_AVERAGES[effect])
    return statistics.mean(price_values)