import json
from dataclasses import dataclass, asdict

from bs4 import BeautifulSoup
import requests
from typing import List

url = "https://www.iog.org.tr/files/sonuclar/20150104_ValideBendi/genel.html"


def get_all_tags(tag_name: str, has_id: bool = False):
    """
    param tag_name: tag_name
    param has_id: True if you need tag has id else False
    """
    return soup.body.find_all(tag_name, id=has_id)


def get_tag_id(tag_name: str, id_name: str):
    return soup.find(tag_name, id_name)


def get_tags_id(id_name: str, tags: list) -> List:
    return [tag[id_name] for tag in tags]


def between_tags(tags: list):
    tables_between_links = []
    second_a = ""
    for i in range(len(tags) - 1):
        first_a = soup.find('a', id=tags[i])
        second_a = soup.find('a', id=tags[i + 1])
        current_element = first_a.find_next_sibling()
        while current_element and current_element != second_a and current_element.name == 'table':
            distance = current_element.find("td", id="c01")
            if distance and "km" in distance.text:
                tables_between_links.append(distance)
            tables_between_links.append(current_element)
            current_element = current_element.find_next_sibling()

    current_element = second_a.find_next_sibling()
    while current_element and current_element.name == 'table':
        tables_between_links.append(current_element)
        current_element = current_element.find_next_sibling()

    return tables_between_links

def get_only_one_between_tag(tags, count):
    first_a = soup.find('a', id=tags[count])
    second_a = soup.find('a', id=tags[count+1])
    current_element = first_a.find_next_sibling()
    while current_element and current_element != second_a and current_element.name == 'table':
        current_element = current_element.find_next_sibling()
        try:
            if current_element.find("tr"):
                print(current_element.find("tr"))
        except AttributeError as e:
            print(e)


def first_irregular_tag(last_tag):
    lst = []
    current_element = last_tag.find_next_sibling()
    while current_element and current_element.name == 'table':
        lst.append(current_element)
        current_element = current_element.find_next_sibling()
    return lst


def convert_turkish(content: str):
    return content.replace('Ð', 'Ğ').replace('Ý', 'İ').replace('Þ', 'Ş').replace('ý', 'ı').replace('þ', 'ş').replace(
        'ð', "ğ").replace("\xa0 ", "")


r = requests.get(url)

content = r.text

html_content = convert_turkish(content)

soup = BeautifulSoup(html_content, 'html.parser')

a_tags = get_all_tags("a", has_id=True)

track_names = get_tags_id('id', a_tags)

# print(track_names)

tables_between_links = between_tags(track_names)

for table in tables_between_links:
    pass
    #print(table.get_text(" ").strip().split("\n"))

db_table = ["ADI SOYADI", "KULUBU", "SURE"]

test_data = {"ADI_SOYADI": "Mustafa Bayrak", "KULUBU": "FB", "SURE": "10", "PARKUR": "SAMPIYONLAR LIGI"}



print(get_only_one_between_tag(track_names, 1))

# son yapılan: iki tane a tagi arasında ki table'ların th etiketleri bulduk

# TODO: bulduğumuz tagleri \n split edicez, sonra tablo uzunluğu kadar dönüp her bir elemanı key:value olarak kaydedicez.
# TODO: Bunu en son toplu olarak db ye yollicaz.
# TODO: boş gelen elemana dikkat et YB.
# TODO: gelen isimleri mapping ile db table'yi değiştireceksin.
