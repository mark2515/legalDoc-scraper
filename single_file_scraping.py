import os
import re
import requests

url = 'https://flk.npc.gov.cn/api/detail/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}
data = {
    'id': 'ZmY4MDgxODE4YTIxZGMxMzAxOGE1MTMyOGUwYzBjM2M%3D'
}
response = requests.post(url=url, data=data, headers=headers)
result = response.json()['result']

title = result['title']
path = result['body'][0]['path'] if result['body'][0]['path'] else ''
download_url = 'https://wb.flk.npc.gov.cn' + path

if not path:
    print(f"Path not found for title: {title}")
else:
    print(title, download_url)

    file_extension = download_url.split('.')[-1]
    content = requests.get(url=download_url, headers=headers).content

    folder_path = 'npc_law_file'
    os.makedirs(folder_path, exist_ok=True)

    safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)
    with open(os.path.join(folder_path, safe_title + '.' + file_extension), mode='wb') as f:
        f.write(content)
