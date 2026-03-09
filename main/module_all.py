import os
import re

import requests


currdir = os.path.dirname(__file__)
save_dir = os.path.join(currdir, 'data')
def get_response(url, timeout=15):
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
    
def m3u8_to_txt(lines:list,txt_name):
    txtstr = []
    tvname = ''
    last_tvname = ''
    temp = {}

    for line in lines:
        if 'EXTINF' in line:
            tvname = line.split(',')[-1].strip()
            
            if not tvname or re.findall(r'^CCTV', tvname, re.IGNORECASE) == []: 
                tvname = ''
                continue
            if temp.get(tvname) is None and len(temp.keys()) > 0:
                for k, v in temp.items():
                    for i in v:
                        txtstr.append(k + ',' + i)
                # temp[tvname] = []
                # last_tvname = tvname
                # continue
            temp[tvname] = []
            last_tvname = tvname
            
        if '#' not in line and 'http' in line:
            if tvname:
                temp[tvname].append(line.strip())

    with open(os.path.join(save_dir, txt_name), 'w', encoding='utf8') as fw:
        strs = 'CCTV,#genre#\n'
        fw.write(strs + '\n'.join(txtstr))