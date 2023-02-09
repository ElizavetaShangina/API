import requests
from PyQt5.QtGui import QPixmap


def request_image(url="http://static-maps.yandex.ru/1.x/", params={}):
    response = requests.get(url=url, params=params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return -1
    pixmap = QPixmap()
    pixmap.loadFromData(response.content)
    return pixmap


def request_adress(url="http://geocode-maps.yandex.ru/1.x/", params={}):
    response = requests.get(url=url, params=params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return -1
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    # for i in json_response["response"]["GeoObjectCollection"]["featureMember"]:
    #     print(i["GeoObject"]["metaDataProperty"]["GeocoderMetaData"])
    adress = toponym["metaDataProperty"]["GeocoderMetaData"]['Address']
    return adress['formatted'], adress['postal_code']


if __name__ == '__main__':
    print(request_adress("http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=Петровки, 38, 1&format=json"))