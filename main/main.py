import json
import os
from format_cctv import format_iptv


currdir = os.path.dirname(__file__)

def main():
    with open(os.path.join(currdir, 'zb_list_merge.json'), 'r', encoding='utf-8') as f:
        merge_dict = json.load(f)
    merge_list = []
    for k, v in merge_dict.items():
        merge_list.append(k)
        merge_list.extend(v)
        merge_list.append('')       
    format_iptv(merge_list)
    print("格式化完成")
    
    


if __name__ == "__main__":
    main()
    