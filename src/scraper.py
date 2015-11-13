import db

import urllib2
from bs4 import BeautifulSoup

RECIPE_LIST_URL = 'http://www.chowhound.com/recipes?page='

def scrape_recipe(recipe_url):
    page = urllib2.urlopen(recipe_url).read()
    soup = BeautifulSoup(page, 'html.parser')
    recipe_name = soup.find('h1', {'itemprop': 'name'}).text
    ingredients = [tag.text.strip().lower() for tag in soup.find_all('span', {'itemprop': 'name'})]
    return recipe_name, ingredients

def urls_from_page(page):
    page = urllib2.urlopen(RECIPE_LIST_URL + str(page))
    soup = BeautifulSoup(page, 'html.parser')
    for div in soup.find_all('div', {'class': 'image_link_medium'}):
        yield div.findAll('a')[0].attrs['href']

def get_recipes():
    database = db.DatabaseAdapter()
    for page in range(22, 233):
        print page
        for url in urls_from_page(page):
            name, ingredients = scrape_recipe(url)
            database.add_recipe(name, ingredients)

if __name__ == '__main__':
    get_recipes()
