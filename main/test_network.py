from collections import deque
import json
import os
import requests
from threading import Thread
import aiohttp
import asyncio
from collections import deque



filer_url = [
    "kkk.jjjj.jiduo.me"
]

currdir = os.path.dirname(__file__)
save_dir = os.path.join(currdir, 'data')

def get_url_list(file_name)-> dict:
    with open(os.path.join(save_dir, file_name), 'r', encoding='utf-8') as f:
        merge_dict = json.load(f)
        return merge_dict

            


timeout = aiohttp.ClientTimeout(total=10)  # 设置总超时时间为10秒
async def test_url(line, session:aiohttp.ClientSession,sem:asyncio.Semaphore,tv: deque):
    async with sem:
        url = line.split(',')[1]
        try: 
            content1 = None
            content2 = None
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    content1 = await response.read()
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    content2 = await response.read()
                    if content1 != content2:
                        tv.appendleft(line)
                        print(f"{url} 测试成功")
        except Exception as e:
            print(f"请求URL {url} 时发生错误: {e}")


async def test_network_fun():
    async with aiohttp.ClientSession() as session:
        merge_dict = get_url_list('zb_list_merge.json')
        tv: dict = {}
        for k, lines in merge_dict.items():
            tv[k] = deque()  # 使用deque来存储成功的URL
            tasks = []
            sem = asyncio.Semaphore(100)  # 限制并发数量为100
            for line in lines:
                if not line.strip():
                    continue
                if ',' not in line:
                    continue
                if '[' in line and ']' in line:
                    tv[k].append(line)
                    continue
                if any(filer in line for filer in filer_url):
                    continue
                task = asyncio.create_task(test_url(line.strip(), session,sem,tv[k]))
                tasks.append(task)
            await asyncio.gather(*tasks)
        print("测试完成，成功的URL数量：", len(tv))
        
        with open(os.path.join(save_dir, 'tv_test.txt'), 'w', encoding='utf-8') as f:
            ttv_list = []
            for k, lines in tv.items():
                ttv_list.append(k)
                for line in lines:
                    ttv_list.append(line)
            f.write('\n'.join(ttv_list))
                

        
    
        
if __name__ == "__main__":
    asyncio.run(test_network_fun())
