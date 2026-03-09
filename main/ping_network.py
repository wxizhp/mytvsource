import json
import os

import requests


currdir = os.path.dirname(__file__)
save_dir = os.path.join(currdir, 'data')
with open(os.path.join(save_dir, 'zb_list_merge.json'), 'r', encoding='utf-8') as f:
    zb_merge_dict = json.load(f)


ping_api = {
    "url": "https://uapis.cn/api/v1/network/ping",
    "param": {
        "host": "",
    },
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0"
    },
}

def ping_network(zb_merge_dict):
    
    for k, v in zb_merge_dict.items():
        for i in v:
            ping_api["param"]["host"] = i
            res = requests.get(ping_api["url"], params=ping_api["param"], headers=ping_api["headers"])
            print(res.json())
            print(i)


