from collections import deque
import json
import os
import requests
from threading import Thread
import aiohttp
import asyncio



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
async def test_url(line, session:aiohttp.ClientSession,sem:asyncio.Semaphore,tv: list):
    async with sem:
        url = line.split(',')[1]
        try: 
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    tv.append(line)
                    print(f"URL {url} 测试成功")
        except Exception as e:
            print(f"请求URL {url} 时发生错误: {e}")


async def test_network_fun():
    async with aiohttp.ClientSession() as session:
        merge_dict = get_url_list('zb_list_merge.json')
        tv: list = []
        for k, lines in merge_dict.items():
            tv.append(k)
            tasks = []
            sem = asyncio.Semaphore(100)  # 限制并发数量为100
            for line in lines:
                if not line.strip():
                    continue
                if ',' not in line:
                    continue
                if any(filer in line for filer in filer_url):
                    continue
                task = asyncio.create_task(test_url(line.strip(), session,sem,tv))
                tasks.append(task)
            await asyncio.gather(*tasks)
        print("测试完成，成功的URL数量：", len(tv))
        with open(os.path.join(save_dir, 'tv_test.txt'), 'w', encoding='utf-8') as f:
            for line in tv:
                f.write(line + '\n')

        
    
        
if __name__ == "__main__":
    asyncio.run(test_network_fun())
