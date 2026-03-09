import json
import os
import re
from urlsm import urls
from collections import deque
from module_all import get_response



currdir = os.path.dirname(__file__)
save_dir = os.path.join(currdir, 'data')

with open(os.path.join(save_dir, 'proxy_list.json'), 'r', encoding='utf-8') as f:
    proxy_list = deque(json.load(f))

def get_zb_urls(urls):
    first_line = ['CCTV, #genre#']
    zb_urls_list = []
    has_add_url = []
    if '' not in proxy_list:
        proxy_list.append('')  # 添加一个空字符串，表示直接访问
    proxy_used = ''
    for url in urls:
        if not url.strip():
            continue
        res_text = ''
        proxy_url = ''
        if 'git' not in url:
            res = get_response(url)
            if not res:
                continue
            res_text = res.text
            if '<html' in res_text or len(res_text) < 20:
                res_text = ''
                continue
        else:   
            if proxy_used not in proxy_list:
                proxy_list.appendleft(proxy_used)  # 将之前成功的代理添加回列表
            for proxy in proxy_list:
                if len(proxy) > 0:  
                    proxy_url = proxy + '/' + url
                else:
                    proxy_url = url                  
                res = get_response(proxy_url)
                if not res:
                    continue
                res_text = res.text
                if '<html' in res_text or len(res_text) < 20:
                    res_text = ''
                    continue
                proxy_used = proxy        
                break
                
                
        if not res_text or len(res_text) < 20:
            continue
        
        
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
        print(f'获取成功:{proxy_url}')
            
    if not zb_urls_list:
        print('未获取到直播源')
        
    first_line.extend(zb_urls_list)
    with open(os.path.join(save_dir, 'zb_list.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(first_line))
    print('zb_list.txt保存成功')
    


if __name__ == '__main__':
    get_zb_urls(urls)
    
        
