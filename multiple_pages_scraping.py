import os
import re
import requests

def scrape_multiple_pages(begin_page, end_page):
    def get_page_data(page_number):
        link = 'https://flk.npc.gov.cn/api/'
        get_data = {
            'type': 'flfg',
            'searchType': 'title;vague',
            'sortTr': 'f_bbrq_s;desc',
            'gbrqStart': '',
            'gbrqEnd': '',
            'sxrqStart': '',
            'sxrqEnd': '',
            'sort': 'true',
            'page': str(page_number),
            'size': '10',
            '_': '1697203841360'
        }
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        }

        folder_path = 'npc_law_files'
        os.makedirs(folder_path, exist_ok=True)

        json_data = requests.get(url=link, params=get_data, headers=headers).json()
        for content_id in json_data['result']['data']:
            url = 'https://flk.npc.gov.cn/api/detail'
            data = {'id': content_id['id']}
            response = requests.post(url=url, data=data, headers=headers)
            result = response.json()['result']

            title = result['title']

            safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)

            path = result['body'][0]['path'] if result['body'][0]['path'] else ''
            if not path:
                print(f"Path not found for title: {title}")
                continue

            download_url = 'https://wb.flk.npc.gov.cn' + path
            print(title, download_url)

            file_extension = download_url.split('.')[-1]
            content = requests.get(url=download_url, headers=headers).content
            filepath = os.path.join(folder_path, f"{safe_title}.{file_extension}")
            with open(filepath, mode='wb') as f:
                f.write(content)

        return len(json_data['result']['data'])

    for page_number in range(begin_page, end_page + 1):
        print(f"Scraping page {page_number}...")
        get_page_data(page_number)

scrape_multiple_pages(7, 10)
