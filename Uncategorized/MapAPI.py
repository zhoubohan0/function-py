# 高德地图API:https://lbs.amap.com/api/webservice/guide/api/direction
import requests
import json


def get_location_x_y(place):
    # place = input("请输入您要查询的地址")
    url = 'https://restapi.amap.com/v3/geocode/geo?parameters'
    parameters = {
        'key': '8676ad3dd023a417ee45e1ea571b529b',
        'address': '%s' % place
    }
    page_resource = requests.get(url, params=parameters)
    text = page_resource.text  # 获得数据是json格式
    data = json.loads(text)  # 把数据变成字典格式
    location = data["geocodes"][0]['location']
    return location

def get_location(x,y):
    url = 'https://restapi.amap.com/v3/geocode/regeo?parameters'
    parameters = {
        'key': '8676ad3dd023a417ee45e1ea571b529b',
        'location': f'{x},{y}'
    }
    page_resource = requests.get(url, params=parameters)
    text = page_resource.text  # 获得数据是json格式
    data = json.loads(text)  # 把数据变成字典格式
    location = data["regeocode"]['formatted_address']
    return location

def get_route(from_place, to_place, type):
    # type：str,出行方式（1.公交、2.步行、3.驾车、4.骑行）
    from_location = get_location_x_y(from_place)
    to_location = get_location_x_y(to_place)

    url = "https://restapi.amap.com"
    if type == "1":
        url = url + "/v3/direction/transit/integrated"
        way = '公交'
    elif type == "2":
        url = url + "/v3/direction/walking"
        way = '步行'
    elif type == "3":
        url = url + "/v3/direction/driving"
        way = '驾车'
    elif type == "4":
        url = url + "/v4/direction/bicycling"
        way = '骑行'
    parameters = {
        'key': '8676ad3dd023a417ee45e1ea571b529b',
        'origin': str(from_location),
        'destination': str(to_location),
        'extensions': 'all',
        'output': 'json',
        'city': '天津',
    }
    print(f'从{from_place}到{to_place}{way}路线如下：')
    page_resource = requests.get(url, params=parameters)
    text = page_resource.text  # 获得数据是json格式
    data = json.loads(text)  # 把数据变成字典格式

    if type == "1":
        route = data['route']['transits']
        for i in route:
            i = i['segments'][0]['bus']['buslines'][0]['name']
            print(i)
    elif type == "2":
        route = data['route']['paths'][0]['steps']
        for i in route:
            i = i['instruction']
            print(i)
    elif type == "3":
        route = data['route']['paths'][0]['steps']
        for i in route:
            i = i['instruction']
            print(i)
    elif type == "4":
        route = data['data']['paths'][0]['steps']
        for i in route:
            i = i['instruction']
            print(i)


def get_distance(origins, destination):
    url = 'https://restapi.amap.com/v3/distance?parameters'
    parameters = {
        'key': '8676ad3dd023a417ee45e1ea571b529b',
        'origins': origins,  # 支持100个坐标对，坐标对见用“| ”分隔；经度和纬度用","分隔
        'destination': destination,
        'type': '1',  # 0：直线距离 1：驾车导航距离（仅支持国内坐标） 3：步行规划距离（仅支持5km之间的距离）
        'output': 'json',
    }
    page_resource = requests.get(url, params=parameters)
    text = page_resource.text  # 获得数据是json格式
    data = json.loads(text)  # 把数据变成字典格式
    distance = data["results"][0]['distance']
    print(distance)
    return distance


if __name__ == '__main__':
    get_distance('116.481028,39.98964', '114.465302,40.004717')
    get_route('南开大学', '周邓纪念馆', '3')
