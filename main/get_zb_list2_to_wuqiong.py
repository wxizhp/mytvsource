import os
import requests
from lxml import etree
from m3u8_to_txt import m3u8_to_txt


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




        

if __name__ == '__main__':
    url2 = 'https://www.iptv-free.com/api/seo/language/chinese'

    url3 = 'https://ip-tv.app/China'

   

    

    get_zb_list2(url2, 'zb_list2.txt')
    get_zb_list3(url3, 'zb_list3.txt')
    
   