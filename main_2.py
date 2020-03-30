import json
import wikipedia
from tqdm import tqdm
import os
from datetime import datetime


class GetWikiUrl:
    def __init__(self, path):
        self.path = path
        self.file = open(self.path, encoding='utf-8')

    def __iter__(self):
        return self

    def __next__(self):
        country = self.file.readline().strip()
        if not country:
            raise StopIteration
        try:
            wiki_url = {country: wikipedia.page(country).url}
        except wikipedia.exceptions.PageError:
            wiki_url = {country: 'page not found'}
        except wikipedia.exceptions.DisambiguationError:
            country = country + '(country)'
            wiki_url = {country: wikipedia.page(country).url}
        return wiki_url


if __name__ == '__main__':

    print('Program started at:', datetime.now())

    with open('countries.json') as file:
        countries = json.load(file)

    # не знаю, как итерироваться по json'у, поэтому получил из него список стран и записал их во временный файл
    list_of_countries = []
    for country_info in countries:
        country_name = country_info.get('name').get('official')
        list_of_countries.append(country_name)
    with open('temp.txt', 'w', encoding='utf-8') as file:
        for country in list_of_countries:
            file.write(country + '\n')

    dict_of_countries = dict()
    for wiki_url in tqdm(GetWikiUrl('temp.txt')):
        dict_of_countries.update(wiki_url)

    os.remove('temp.txt')

    with open('wiki_url_2.json', 'w', encoding='utf-8') as file:
        json.dump(dict_of_countries, file, ensure_ascii=False, indent=4)

    print('Program finished at:', datetime.now())