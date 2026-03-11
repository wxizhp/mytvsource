import requests


res = requests.get("https://[2a00:1450:4009:80d::200e]")
if res.status_code == 200:
    print(res.text)
else:
    print('请求失败')