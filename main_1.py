import json
import wikipedia
from tqdm import tqdm
from datetime import datetime
#import sys


if __name__ == '__main__':

    print('Program started at:', datetime.now())

    with open('countries.json') as file:
        countries = json.load(file)

    list_of_countries = []
    for country_info in countries:
        country_name = country_info.get('name').get('official')
        list_of_countries.append(country_name)

    #print(sys.getsizeof(list_of_countries))

    dict_of_countries = dict()
    for country_name in tqdm(list_of_countries):
        try:
            dict_of_countries.update({country_name: wikipedia.page(country_name).url})
        except wikipedia.exceptions.PageError:
            dict_of_countries.update({country_name: 'page not found'})
        except wikipedia.exceptions.DisambiguationError:
            country_name = country_name + '(country)'
            dict_of_countries.update({country_name: wikipedia.page(country_name).url})


    with open('wiki_url.json', 'w', encoding='utf-8') as file:
        json.dump(dict_of_countries, file, ensure_ascii=False, indent=4)

    print('Program finished at:', datetime.now())


