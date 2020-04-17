# coding: utf-8


import requests
import re
import numpy as np
import json

r = requests.get('http://map.amap.com/service/subway?_1469083453978&srhdata=1100_drw_beijing.json')

'''
可以将JSON文件存在本地，请求一次之后从本地读取
fo = open('subway.json', 'r+')
stext = fo.read()
'''

def get_lines_stations_info(text):
	# 线路名称
    lines_pat = re.compile("(?:\"ln\":\")([^\"]+)")
    lines_list = re.findall(lines_pat, text)
    # 各线路站点信息
    stations_pat = re.compile("(\"st\":\[[^\]]+)")
    stations_list = re.findall(stations_pat, text)

    lines_info = {}
    stations_info = {}

    for i in range(len(lines_list)):
        line = lines_list[i]
        stations = stations_list[i]
        # 线路站点名称
        name_pat = re.compile("(?:\"n\":\")([^\"]+)")
        names = re.findall(name_pat, stations)
        # 线路站点位置
        location_pat = re.compile("(?:\"sl\":\")([^\"]+)")
        locations = re.findall(location_pat, stations)
        lines_info[line] = names
        for i in range(len(names)):
            if not stations_info.__contains__(names[i]):
                stations_info[names[i]] = tuple(map(float, locations[i].split(',')))
            else:
                pass
    return lines_info, stations_info

lines_info, stations_info = get_lines_stations_info(r.text)


# 根据线路信息，建立站点邻接表dict
def get_neighbor_info(lines_info):
    neighbor_info = {}
    def add_neighbor_dict(info, str1, str2):
        if info.__contains__(str1):
            info[str1].add(str2)
        else:
            info[str1] = set([str2])
    
    for line in lines_info:
        stations = lines_info[line]
        for i in range(len(stations)-1):
            add_neighbor_dict(neighbor_info, stations[i], stations[i+1])
            add_neighbor_dict(neighbor_info, stations[i+1], stations[i])
    return neighbor_info
        
neighbor_info = get_neighbor_info(lines_info)


import networkx as nx
import matplotlib
import matplotlib.pyplot as plt

# 如果汉字无法显示，请参照
matplotlib.rcParams['font.sans-serif'] = ['SimHei'] 
matplotlib.rcParams['font.family']='sans-serif'
matplotlib.rcParams['figure.figsize'] = '17,10'

subway_graph = nx.Graph(neighbor_info)
nx.draw(subway_graph, stations_info, with_labels=True, node_size=8)
plt.show()

#  简单BFS算法
def get_path_BFS(lines_info, neighbor_info, from_station, to_station):
    pathes = [[from_station]]
    visited = set()
    while pathes:
        path = pathes.pop(0)    #每次第一个path出队列
        prev = path[-1]
        if prev in visited: continue
        next_s = neighbor_info[prev]
        
        for station in next_s:
            if station in path: continue 
            
            new_path = path+[station]
            pathes.append(new_path)
            if station == to_station:
                return new_path
        visited.add(prev)

def search_path(start_station, end_station):
    path = get_path_BFS(lines_info, neighbor_info, start_station, end_station)
    return 'recomended route: ' + '->'.join(path)

path = search_path('香山','国家图书馆')
print(path)



