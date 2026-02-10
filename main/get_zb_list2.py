import os
import requests
from lxml import etree
from m3u8_to_txt import m3u8_to_txt


def get_zb_list2(url,txt_name):
    
    response = requests.get(url)
    html_json = response.json()
    m3u8_url = html_json.get('playlist')
    if m3u8_url:
        response_m3u8 = requests.get(m3u8_url)
        m3u8_text = response_m3u8.text
        with open('zb_list2.html', 'w', encoding='utf-8') as f:
            f.write(m3u8_text)
        # print(m3u8_text)
        lines = m3u8_text.splitlines()
        m3u8_to_txt(lines, txt_name)
        print(f'直播源获取完成，已保存为{txt_name}')
        

if __name__ == '__main__':
    url = 'https://www.iptv-free.com/api/seo/language/chinese'
    get_zb_list2(url, 'zb_list2.txt')