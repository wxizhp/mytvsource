from collections import deque
import requests
from threading import Thread



def get_url_list(file_name):
    url_list: deque = deque()
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            url_list.append(line.strip())
    return url_list

            
def  request_url(url):
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True
    except Exception as e:
        # print(e)
        return False



def request_urls(url_list, tv:list):
    while url_list:
        line = url_list.popleft()
        

        if not line:
            continue
        if "#genre" in line:
            continue
        tv_name, url = line.split(',', 1)
        if request_url(url):
            tv.append(line)


def test_network_fun():
    url_list = get_url_list('tv_format.txt')
    tv = []
    ths = []
    for i in range(10):
        ths.append(Thread(target=request_urls, args=(url_list, tv)))
        ths[i].start()
    
    for th in ths:
        th.join()
    print(f'总直播源数量：{len(tv)}')
    with open('tv.txt', 'w', encoding='utf-8') as f:
        for url in tv:
            f.write(url + '\n')
        
if __name__ == "__main__":
    test_network_fun()
