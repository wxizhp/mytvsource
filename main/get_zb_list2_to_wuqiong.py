import json
import os
from lxml import etree
from collections import deque
from module_all import get_response, m3u8_to_txt


currdir = os.path.dirname(__file__)
save_dir = os.path.join(currdir, 'data')

with open(os.path.join(save_dir, 'proxy_list.json'), 'r', encoding='utf-8') as f:
    proxy_urls = deque(json.load(f))

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
    urls4 = [
        "https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/cn_cctv.m3u",
        "https://raw.githubusercontent.com/jia070310/lemonTV/refs/heads/main/iptv-fe.m3u",
        "https://raw.githubusercontent.com/YanG-1989/m3u/refs/heads/main/Gather.m3u",
        "https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u",
        "https://raw.githubusercontent.com/vbskycn/iptv/refs/heads/master/tv/iptv6.m3u",
        "https://raw.githubusercontent.com/vbskycn/iptv/refs/heads/master/tv/iptv4.m3u",
        "https://raw.githubusercontent.com/jisoypub/iptv/refs/heads/main/ipv4.m3u",
        "https://raw.githubusercontent.com/sammy0101/hk-iptv-auto/refs/heads/main/hk_live.m3u",
        "https://raw.githubusercontent.com/sumingyd/Telecom-Shandong-IPTV-List/refs/heads/main/Telecom-Shandong.m3u",
        "https://raw.githubusercontent.com/lptv800/lptv800.github.io/refs/heads/master/IPTV.m3u",
        "https://raw.githubusercontent.com/peterHchina/iptv/refs/heads/main/CNTV-V4.m3u",
        "https://raw.githubusercontent.com/zhi35/iptv/refs/heads/master/iptv.m3u"
       

    ]
    get_zb_list2(url2, 'zb_list2.txt')
    get_zb_list3(url3, 'zb_list3.txt')
    get_zb_list4(urls4, 'zb_list4.txt')
    
   