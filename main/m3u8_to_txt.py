

import os


currdir = os.path.dirname(__file__)
txtstr = ''
tag = 0
tvname = ''
with open(os.path.join(currdir,'iptv.m3u'),'r',encoding='utf8') as fr:
    for line in fr:
        if 'EXTINF' in line:
            tag = 0
            tvname = line.split(',')[-1].strip()
            txtstr = txtstr + tvname + ','
            tag = tag + 1
        if '#' not in line:
            if tag > 1:
                txtstr = txtstr + tvname + ',' + line
            else:
                txtstr = txtstr + line
            # txtstr = txtstr + line
            tag = tag + 1

with open(os.path.join(currdir,'iptv.txt'),'w',encoding='utf8') as fw:
    fw.write(txtstr)