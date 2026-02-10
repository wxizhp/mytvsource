

import re


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

    with open(txt_name,'w',encoding='utf8') as fw:
        strs = 'CCTV,#genre#\n'
        fw.write(strs + '\n'.join(txtstr))