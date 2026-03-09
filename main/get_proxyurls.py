import json
import os
from module_all import get_response
from urlsm import proxy_get_url

currdir = os.path.dirname(__file__)

def get_proxy_list(proxyurl)->None:
    proxy_list = []
    res = get_response(proxyurl)
    if not res:
        return
    res_json = res.json()
    data = res_json.get('data', [])
    for item in data:
        url = item.get('url')
        if url:
            proxy_list.append(url)
    if proxy_list:
        with open(os.path.join(currdir,'data', 'proxy_list.json'), 'w', encoding='utf-8') as f:
            json.dump(list(proxy_list), f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    get_proxy_list(proxy_get_url)