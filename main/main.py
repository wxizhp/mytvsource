from get_zb_list import get_zb_urls_list
from merge import merge_zb_txt
from format_cctv import format_iptv


zb_txt_list = ["zb_list.txt", "other.txt"]


def main():
    get_zb_urls_list()
    merge_dict = merge_zb_txt(zb_txt_list)
    merge_list = []
    for k, v in merge_dict.items():
        merge_list.append(k)
        merge_list.extend(v)
        merge_list.append('')

        
    format_iptv(merge_list)
    print("done")


if __name__ == "__main__":
    main()