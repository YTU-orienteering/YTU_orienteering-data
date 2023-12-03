import json
from dataclasses import dataclass, asdict

from bs4 import BeautifulSoup
import requests
from typing import List

url = "https://www.iog.org.tr/files/sonuclar/20150104_ValideBendi/genel.html"
url_1 = "https://www.iog.org.tr/files/sonuclar/20220130_kulupmerkezi/genel.html"
url_2 = "https://www.iog.org.tr/files/sonuclar/20230924_fatihormani/genel.html"


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


def get_column_names(tags, count) -> List:
    first_a = soup.find('a', id=tags[count])
    second_a = soup.find('a', id=tags[count + 1])
    current_element = first_a.find_next_sibling()
    while current_element and current_element != second_a and current_element.name == 'table':
        current_element = current_element.find_next_sibling()
        th_elements = current_element.find_all("th")
        try:
            if th_elements:
                return [th.get_text().split("\n")[0] for th in th_elements if th.get_text().split("\n") != ['']]
        except AttributeError as e:
            print(e)


def get_racers_data(tags, count):
    first_a = soup.find('a', id=tags[count])
    second_a = soup.find('a', id=tags[count + 1])
    current_element = first_a.find_next_sibling()
    bir_defa_calis = True
    while current_element and current_element != second_a and current_element.name == 'table' and bir_defa_calis:
        current_element = current_element.find_next_sibling()
        current_element = current_element.find_next_sibling()
        td_elements = current_element.find_all("td")
        try:
            if td_elements:
                bir_defa_calis = False
                return [th.get_text().split("\n")[0] for th in td_elements if th.get_text().split("\n")[0] != '\xa0' and th.get_text().split("\n")[0] != '&np']
        except AttributeError as e:
            print(e)


r = requests.get(url_2)

content = r.text

html_content = convert_turkish(content)

soup = BeautifulSoup(html_content, 'html.parser')

a_tags = get_all_tags("a", has_id=True)

track_names = get_tags_id('id', a_tags)  # uzun, orta

print(track_names)

tables_between_links = between_tags(track_names)

for table in tables_between_links:
    pass
    # print(table.get_text(" ").strip().split("\n"))

db_table = ["ADI SOYADI", "KULUBU", "SURE"]

column_data = get_column_names(track_names, 1)
racers_data = get_racers_data(track_names, 1)

column_len = len(column_data)
racers_len = len(racers_data)

zip_lst = []
for i in range(0, racers_len, column_len):
    zip_lst.append(tuple(zip(column_data, get_racers_data(track_names, 0)[i:i + column_len])))

final_lst = []
for data in zip_lst:
    data_dict = {}
    if data:
        for i in range(column_len):
            column_name = data[i][0]
            column_value = data[i][1]
            if column_name == 'Name' or column_name == "Adı Soyadı":
                data_dict["ADI_SOYADI"] = column_value
            if column_name == 'Club' or column_name == "Kulübü":
                data_dict["KULUBU"] = column_value
            if column_name.lower() == "time" or column_name == "Süre":
                data_dict["SURE"] = column_value


        data_dict["PARKUR"] = "Kısa Parkur"
        final_lst.append(data_dict)

print(final_lst)
test_data = {"ADI_SOYADI": "Mustafa Bayrak", "KULUBU": "FB", "SURE": "10", "PARKUR": "SAMPIYONLAR LIGI"}

column_data.append("PARKUR")

# son yapılan: iki tane a tagi arasında ki table'ların th etiketleri bulduk

# TODO: bulduğumuz tagleri \n split edicez, sonra tablo uzunluğu kadar dönüp her bir elemanı key:value olarak kaydedicez.
# TODO: Bunu en son toplu olarak db ye yollicaz.
# TODO: boş gelen elemana dikkat et YB.
# TODO: gelen isimleri mapping ile db table'yi değiştireceksin.
