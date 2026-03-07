import os
import re
import time

from merge import merge_zb_txt

currdir = os.path.dirname(__file__)
tvzh = [
    'CCTV-2 财经',
    'CCTV-3 综艺',
    'CCTV-4 中文国际',
    'CCTV-5 体育',
    'CCTV-6 电影',
    'CCTV-7 国防军事',
    'CCTV-8 电视剧',
    'CCTV-9 纪录',
    'CCTV-10 科教',
    'CCTV-11 戏曲',
    'CCTV-12 社会与法',
    'CCTV-13 新闻',
    'CCTV-14 少儿',
    'CCTV-15 音乐',
    'CCTV-16 奥林匹克',
    'CCTV-17 农业农村',
    'CCTV-5+ 体育赛事',
    'CCTV-4K 超高清',
    'CCTV-8K 超高清',
    'CCTV-1 综合'
]

# 创建正则表达式模式字典
pattern_dict = {
    'CCTV-2 财经': r'CCTV-?2',
    'CCTV-3 综艺': r'CCTV-?3',
    'CCTV-4 中文国际': r'CCTV-?4',
    'CCTV-5 体育': r'CCTV-?5',
    'CCTV-6 电影': r'CCTV-?6',
    'CCTV-7 国防军事': r'CCTV-?7',
    'CCTV-8 电视剧': r'CCTV-?8',
    'CCTV-9 纪录': r'CCTV-?9',
    'CCTV-10 科教': r'CCTV-?10',
    'CCTV-11 戏曲': r'CCTV-?11',
    'CCTV-12 社会与法': r'CCTV-?12',
    'CCTV-13 新闻': r'CCTV-?13',
    'CCTV-14 少儿': r'CCTV-?14',
    'CCTV-15 音乐': r'CCTV-?15',
    'CCTV-16 奥林匹克': r'CCTV-?16',
    'CCTV-17 农业农村': r'CCTV-?17',
    'CCTV-5+ 体育赛事': r'CCTV-?5\+',
    'CCTV-4K 超高清': r'CCTV-?4K',
    'CCTV-8K 超高清': r'CCTV-?8K',
    'CCTV-1 综合': r'CCTV-?1[^\d]*'
}

# 修改处理顺序，确保先尝试匹配CCTV-5+
def get_ordered_patterns():
    # 确保CCTV-5+在CCTV-5之前匹配
    ordered_patterns = []
    for name in tvzh:
        if name == 'CCTV-5+ 体育赛事':
            ordered_patterns.append((name, pattern_dict[name]))
    for name in tvzh:
        if name != 'CCTV-5+ 体育赛事':
            ordered_patterns.append((name, pattern_dict[name]))
    return ordered_patterns


def format_iptv(zb_urls_list:list):
    date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    new_zb_urls = [f"# IPTV直播源，更新于{date_str}"]
    
    for line in zb_urls_list:
        matched = False
        if not line.strip():
            new_zb_urls.append(line)
            continue
        if '#' in line:
            new_zb_urls.append(line)
            continue
        if re.findall(r'CCTV', line, re.IGNORECASE) == []:
            new_zb_urls.append(line)
            continue
        if ',' not in line:
            new_zb_urls.append(line)
            continue
            
        tvn_a = line.split(',', 1)
        tvname = tvn_a[0].strip()
        addr = tvn_a[1]
        
        # 使用有序的模式列表进行匹配
        for std_name, pattern in get_ordered_patterns():
            if re.search(pattern, tvname, re.IGNORECASE):
                new_zb_urls.append(std_name + ',' + addr)
                matched = True
                break
        if not matched:
            new_zb_urls.append(line)     
        
    # new_zb_urls.sort(key = lambda x:x.split(',')[0] if 'CCTV' in x else x)
    with open('tv.txt', 'w', encoding='utf8') as fw:
        fw.write('\n'.join(new_zb_urls))
    print('格式化完成，已保存为tv.txt')
            
if __name__ == '__main__':
    zb_txt_list = ["zb_list.txt", "other.txt"]
    merge_dict = merge_zb_txt(zb_txt_list)
    merge_list = []
    for k, v in merge_dict.items():
        merge_list.append(k)
        merge_list.extend(v)
        merge_list.append('')

        
    format_iptv(merge_list)
    # print("done")