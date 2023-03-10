import requests
from PyQt5.QtGui import QPixmap


def request_image(params, url="http://static-maps.yandex.ru/1.x/"):
    response = requests.get(url=url, params=params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return 'ERROR'
    pixmap = QPixmap()
    pixmap.loadFromData(response.content)
    return pixmap


def request_adress(params, url="http://geocode-maps.yandex.ru/1.x/"):
    response = requests.get(url=url, params=params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return 'ERROR'
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    # for i in json_response["response"]["GeoObjectCollection"]["featureMember"]:
    #     print(i["GeoObject"]["metaDataProperty"]["GeocoderMetaData"])
    adress = toponym["metaDataProperty"]["GeocoderMetaData"]['Address']
    return adress['formatted'], adress['postal_code']


def requests_nearby(params, url="http://geocode-maps.yandex.ru/1.x/"):
    coords = list(map(float, params['geocode'].split(',')))
    response = requests.get(url=url, params=params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return 'ERROR'
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"]
    results = []
    for i in toponym:
        point_coords = list(map(float, i["GeoObject"]['Point']['pos'].split()))
        d = ((coords[0] - point_coords[0]) ** 2 + (coords[1] - point_coords[1]) ** 2) ** 0.5
        # print(i)
        results.append((d, point_coords, i["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]['Address']['formatted']))
    results.sort(key=lambda x: x[0])
    return results[0][1], results[0][2]


if __name__ == '__main__':
    params = {
        'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
        'geocode': '37.677751,55.757718',
        'format': 'json'
    }
    print(requests_nearby(params, "http://geocode-maps.yandex.ru/1.x/"))