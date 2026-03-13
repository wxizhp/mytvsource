import asyncio
import json
import os
import re
import aiohttp
from collections import deque
from module_all import get_response
from urlsm import urls_dict



currdir = os.path.dirname(__file__)
save_dir = os.path.join(currdir, 'data')


with open(os.path.join(save_dir, 'proxy_list.json'), 'r', encoding='utf-8') as f:
    proxy_list = deque(json.load(f))

async def get_zb_from_txt(urls):
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



def get_zb_list4(urls,txt_name):
    lines = []
    proxy_used = ''
    for url in urls:
        if not url.strip():
            continue
        if proxy_used:
            proxy_url = proxy_used + '/' + url
            response = get_response(proxy_url)
            if response is not None:
                m3u8_text = response.text
                if '<html' in m3u8_text or len(m3u8_text) < 20:
                    print(f'响应内容异常，尝试下一个代理: {proxy_used}')
                    proxy_used = ''
                else:
                    lines.extend(m3u8_text.splitlines())
                    continue
            else:
                print(f'请求失败，尝试下一个代理: {proxy_used}')
                proxy_used = ''
        
        for proxy in proxy_urls:
            proxy_url = proxy + '/' + url
            response = get_response(proxy_url)
            if response is None:
                print(f'请求失败，尝试下一个代理: {proxy}')
                proxy_used = ''
                continue
            m3u8_text = response.text
            if '<html' in m3u8_text or len(m3u8_text) < 20:
                print(f'响应内容异常，尝试下一个代理: {proxy}')
                proxy_used = ''
                continue

            lines_ = m3u8_text.splitlines()
            lines.extend(lines_)
            proxy_used = proxy
            break
    if lines:
        m3u8_to_txt(lines, txt_name)
        print(f'直播源获取完成，已保存为{txt_name}')
    

async def get_proxy_url

async def get_zb(url, session: aiohttp.ClientSession, sem: asyncio.Semaphore):
    async with sem:
        if url.endwith()
        
        
async def get_zb_list(urls_dict,proxy_urls):
    async with aiohttp.ClientSession() as session:
        tasks =[]
        sem = asyncio.Semaphore(5)
        for k,urls in urls_dict.items():
            if 'txt' in k:
                for url in urls:
                    task = asyncio.create_task(get_zb_from_txt(url))
                    tasks.append(task)
            if 'm3u' in k:
                task = asyncio.create_task(get_zb_from_m3u(urls, sem))
                tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(get_zb_list(urls_dict))
    
        
