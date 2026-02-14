from get_zb_list import get_zb_urls_list
from merge import merge_zb_txt
from format_cctv import format_iptv
from main.get_zb_list2_to_wuqiong import get_zb_list2, get_zb_list3


zb_txt_list = ["zb_list.txt", "other.txt", "zb_list2.txt", "zb_list3.txt", "zb_list4.txt", "zb_list4_1.txt"]


def main():
    get_zb_list2('https://www.iptv-free.com/api/seo/language/chinese', 'zb_list2.txt')
    get_zb_list3('https://ip-tv.app/China', 'zb_list3.txt')
    get_zb_urls_list()
    print("获取直播源完成，开始合并")
    merge_dict = merge_zb_txt(zb_txt_list)
    print("合并完成，开始格式化")
    merge_list = []
    for k, v in merge_dict.items():
        merge_list.append(k)
        merge_list.extend(v)
        merge_list.append('')       
    format_iptv(merge_list)
    print("格式化完成")


if __name__ == "__main__":
    main()