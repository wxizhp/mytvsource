from collections import deque
import requests
from threading import Thread
import aiohttp
import asyncio



def get_url_list(file_name):
    url_list: deque = deque()
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            url_list.append(line.strip())
    return url_list

            



async def test_url(line, session,sem,tv: list):
    async with sem:
        url = line.split(',')[1]    # 获取一个信号量
        async with session.get(url) as response:
            if response.status == 200:
                tv.append(line)



async def test_network_fun():
    async with aiohttp.ClientSession() as session:
        url_list = get_url_list('tv_format.txt')
        tv: list = []
        tasks = []
        sem = asyncio.Semaphore(20)  # 限制并发数量为100
        for line in url_list:
            if not line.strip():
                continue
            if '#' in line:
                tv.append(line.strip())
                continue
            if ',' not in line:
                continue
            task = asyncio.create_task(test_url(line.strip(), session,sem,tv))
            tasks.append(task)
        await asyncio.gather(*tasks)
        print("测试完成，成功的URL数量：", len(tv))
        with open('tv.txt', 'w', encoding='utf-8') as f:
            for line in tv:
                f.write(line + '\n')

        
    
        
if __name__ == "__main__":
    asyncio.run(test_network_fun())
