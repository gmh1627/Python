import json
import re
import requests
import os

# 定义车站信息的URL
URL_STATION_NAME = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'

class Station:
    def __init__(self):
        # 设置请求头
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/123.0.0.0 Safari/537.36"
        }

        # 获取车站版本号
        self.version = '1.9320'

    def synchronization(self):
        # 发送GET请求获取车站信息
        response = requests.get(URL_STATION_NAME, headers=self.headers, params={
            "station_version": self.version
        })
        return response.text

    def extract(self):
        # 提取响应中的车站信息
        response = self.synchronization()
        response = response.replace("var station_names =", '').strip()
        return response[:-2]  # 去掉末尾的多余字符

    def process(self):
        # 处理提取的数据
        response = self.extract()
        response = re.findall(r'@(.*?)\|\|\|', response)
        print(f'共有{len(response)}个车站')
        response = [i.split("|") for i in response]

        # 创建一个新的车站字典，只包含所需的字段
        station_dict = []
        for item in response:
            station_info = {
                "车站名": item[1],
                "车站代码": item[2],
                "车站编号": item[5],
                "所在城市": item[7],
                "城市编号": item[6]
            }
            station_dict.append(station_info)

        self.save_station(station_dict)
        
        return station_dict

    def save_station(self, station_dict):
        os.makedirs('resource', exist_ok=True)
        # 将车站信息保存到本地文件
        with open('resource/station_dict.json', 'w', encoding='utf-8') as f:
            json.dump(station_dict, f, ensure_ascii=False, indent=4)

    @staticmethod
    def find_keyword_station(keyword, _type='station'):
        # 查找含有keyword的站名
        with open('resource/station_dict.json', 'rt', encoding='utf-8') as f:
            station_dict = json.load(f)
        
        if _type == 'station':
            response = [item for item in station_dict if keyword.lower() in item["车站名"].lower()]
        elif _type == 'code':
            response = [item for item in station_dict if keyword.lower() in item["车站代码"].lower()]
        else:
            response = []

        return response
    
    def find_stations_with_last_char(self, char):
        # 查找所有字典的key里最后一个字是指定字符的站名，并保存结果到JSON文件
        with open('resource/station_dict.json', 'rt', encoding='utf-8') as f:
            station_dict = json.load(f)
        
        # 使用列表推导式来找到符合要求的站名
        matching_stations = [item for item in station_dict if item['车站名'].endswith(char)]
        
        # 保存结果到JSON文件
        self.save_matching_stations(matching_stations, char)
        
        return matching_stations

    def save_matching_stations(self, matching_stations, char):
        # 将车站信息保存到本地文件
        filename = f'resource/stations_with_last_char_{char}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(matching_stations, f, ensure_ascii=False, indent=4)

    def find_stations_in_city(self, city_name):
        # 查找所在城市为指定城市的车站
        with open('resource/station_dict.json', 'rt', encoding='utf-8') as f:
            station_dict = json.load(f)
        
        # 使用列表推导式来找到符合要求的站名，并排除不需要的字段
        matching_stations = [
            {k: v for k, v in item.items() if k not in ['所在城市', '城市编号']}
            for item in station_dict if city_name.lower() in item['所在城市'].lower()
        ]
        
        return matching_stations

# 主程序入口
if __name__ == "__main__":
    station = Station()
    station.process()
    
    result = station.find_stations_with_last_char('东')
    print(f"找到 {len(result)} 个以 '东' 结尾的站名")
    
    result = station.find_stations_with_last_char('西')
    print(f"找到 {len(result)} 个以 '西' 结尾的站名")
    
    result = station.find_stations_with_last_char('南')
    print(f"找到 {len(result)} 个以 '南' 结尾的站名")
    
    result = station.find_stations_with_last_char('北')
    print(f"找到 {len(result)} 个以 '北' 结尾的站名")
    
    # 查找含有'湛江'的站名
    keyword = '湛江'
    result = station.find_keyword_station(keyword, _type='station')
    print(result)
    
    # 查找所在城市为'湛江'的车站
    city_name = '湛江'
    result = station.find_stations_in_city(city_name)
    print(f"找到 {len(result)} 个位于 '{city_name}' 的车站:")
    print(result)