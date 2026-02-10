import os




def merge_zb_txt(zb_txt_list):
    merged_list = {}
    has_add_url = []

    for zb_txt in zb_txt_list:
        tv_type = ''
        if os.path.exists(zb_txt):
            with open(zb_txt, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip():
                        continue
                    # if line_num == 0 and '#genre#' not in line and ',' not in line:
                    #     tv_type = '其他,#genre#'
                    #     if merged_list.get(tv_type):
                    #         merged_list[tv_type].append(line.strip())
                    #         continue
                    #     merged_list[tv_type] = [line.strip()]                        # 添加一个默认的
                    #     continue
                    if '#genre#' in line and ',' in line:
                        type_name = line.split(',')[0].strip()
                        if not type_name:
                            tv_type = '其他,#genre#'
                            if merged_list.get(tv_type):
                                continue
                            merged_list[tv_type] = []
                        tv_type = type_name + ',#genre#'
                        if merged_list.get(tv_type):
                            continue
                        merged_list[tv_type] = [] 
                        continue
                    if '#' in line:
                        continue
                    if ',' not in line:
                        continue
                    if len(merged_list.keys()) == 0:
                        merged_list['其他,#genre#'] = []
                    if tv_type == '':
                        tv_type = '其他,#genre#'
                        if merged_list.get(tv_type) is None:
                            merged_list[tv_type] = []
                    tv_name, tv_url = line.split(',', 1)
                    if tv_url in has_add_url:
                        continue
                    has_add_url.append(tv_url)
                    merged_list[tv_type].append(line.strip())
    print(f'合并完成，类型数量：{len(merged_list.keys())}，总直播源数量：{len(has_add_url)}')
    return merged_list
                

if __name__ == "__main__":
    zb_txt_list = ["zb_list.txt", "other.txt"]
    merged_list = merge_zb_txt(zb_txt_list)
    print(merged_list)