from get_zb_list import get_zb_urls_list
from merge import merge_zb_txt
from format_cctv import format_iptv
from get_zb_list2_to_wuqiong import get_zb_list2, get_zb_list3, get_zb_list4


zb_txt_list = ["zb_list.txt", "other.txt", "zb_list2.txt", "zb_list3.txt", "zb_list4.txt"]


def main():
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
        "",


    ]
    get_zb_list2(url2, 'zb_list2.txt')
    get_zb_list3(url3, 'zb_list3.txt')
    get_zb_list4(urls4, 'zb_list4.txt')
    

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