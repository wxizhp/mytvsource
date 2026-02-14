import os
import requests
from lxml import etree
from m3u8_to_txt import m3u8_to_txt
from collections import deque
from urlsm import proxy_get_url




def get_proxy_list(proxyurl)->deque:
    proxy_list = deque()
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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0'
}

def get_response(url, timeout=10):
    try:
        res = requests.get(url, headers=headers, timeout=timeout)
        if res.status_code == 200:
            return res
    except Exception as e:
        print(e)
        return None

def get_zb_list2(url,txt_name):
    
    response = get_response(url)
    if response is None:
        return
    html_json = response.json()
    m3u8_url = html_json.get('playlist')
    if m3u8_url:
        response_m3u8 = get_response(m3u8_url)
        if response_m3u8 is None:
            print(f'请求m3u8失败,{m3u8_url}')
            return
        m3u8_text = response_m3u8.text
        # with open('zb_list2.html', 'w', encoding='utf-8') as f:
        #     f.write(m3u8_text)
        # print(m3u8_text)
        lines = m3u8_text.splitlines()
        m3u8_to_txt(lines, txt_name)
        print(f'直播源获取完成，已保存为{txt_name}')

    
def get_zb_list3(url,txt_name):
    response = get_response(url)
    if response is None:
        return
    m3u8_text = response.text
    lines = m3u8_text.splitlines()
    m3u8_to_txt(lines, txt_name)
    print(f'直播源获取完成，已保存为{txt_name}')


def get_zb_list4(urls,txt_name):
    proxy_urls = get_proxy_list(proxyurl=proxy_get_url)
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



        

if __name__ == '__main__':
    url2 = 'https://www.iptv-free.com/api/seo/language/chinese'

    url3 = 'https://ip-tv.app/China'


    url4 = "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/cn_cctv.m3u"

    url4_1 = "https://raw.githubusercontent.com/jia070310/lemonTV/refs/heads/main/iptv-fe.m3u"

   

    

    # get_zb_list2(url2, 'zb_list2.txt')
    # get_zb_list3(url3, 'zb_list3.txt')

    # get_zb_list4(url4, 'zb_list4.txt')
    get_zb_list4(url4_1, 'zb_list4_1.txt')
    
   