import re
from urlsm import urls,proxy_get_url
# from format_cctv import format_iptv
import requests


def get_response(url, timeout=10):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0'
    }
    try:
        res = requests.get(url, headers=headers, timeout=timeout)
        if res.status_code == 200:
            return res
    except Exception as e:
        print(e)
        return None

def get_proxy_list(proxyurl)->list:
    proxy_list = []
    res = get_response(proxyurl)
    if not res:
        return proxy_list
    res_json = res.json()
    data = res_json.get('data', [])
    for item in data:
        url = item.get('url')
        if url:
            proxy_list.append(url)
    return proxy_list



def get_zb_urls(urls,proxyurl,get_proxy_list):
    first_line = ['CCTV, #genre#']
    zb_urls_list = []
    has_add_url = []
    proxy_list = get_proxy_list(proxyurl)
    proxy_used = ''
    for url in urls:
        res_text = ''
        proxy_url = ''
        for proxy in proxy_list:
            if proxy_used:
                proxy_url = proxy_used + '/' + url
                res = get_response(proxy_url)
                if not res:
                    proxy_used = ''
                    continue
                res_text = res.text
                if '<html' in res_text:
                    proxy_used = ''
                    res_text = ''
                    continue
                break
            else:
  
                
                proxy_url = proxy + '/' + url
                res = get_response(proxy_url)
                if not res:
                    continue
                res_text = res.text
                if '<html' in res_text:
                    res_text = ''
                    continue
                proxy_used = proxy        
                break
                
                
        if not res_text:
            continue
        print(f'开始获取:{proxy_url}')
        
        for line in res_text.splitlines():
            if not line.strip() or '#genre#' in line:
                continue
            if '#' in line:
                continue
            if ',' not in line:
                continue
            tv_name, tv_url = line.split(',', 1)
            if tv_url in has_add_url:
                continue
            has_add_url.append(tv_url)
            if re.findall(r'CCTV', tv_name, re.IGNORECASE):
                zb_urls_list.append(line)
            
    if not zb_urls_list:
        raise Exception('没有获取到直播源')
    first_line.extend(zb_urls_list)
    full_list = first_line
    return full_list
    
    
    # zb_urls_list.sort(key = lambda x:x.split(',')[0])
    # format_iptv(zb_urls_list)





def get_zb_urls_list():
    for i in range(5):
        try:
            full_list = get_zb_urls(urls,proxy_get_url,get_proxy_list)
            with open('zb_list.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(full_list))

            return full_list
            
            
        except Exception as e:
            print(e)


if __name__ == '__main__':
    get_zb_urls_list()
    
        
