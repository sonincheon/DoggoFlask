import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 '
                  'Safari/537.36'
}

res = requests.get("https://www.animal.go.kr/front/awtis/public/publicList.do?totalCount=2705&pageSize=10&boardId"
                   "=&desertionNo=&menuNo=1000000055&searchSDate=2023-10-30&searchEDate=2023-11-30&searchUprCd"
                   "=&searchOrgCd=&searchCareRegNo=&searchUpKindCd=&searchKindCd=&searchSexCd=&searchRfid=&&page=1",
                   headers=headers)

if res.status_code == requests.codes.ok:
    soup = BeautifulSoup(res.text, 'html.parser')
    li_items = soup.select('li')  # 'li div' 요소들을 찾습니다.

    for li in li_items:
        thumbnail_div = li.find('div', class_='photo')
        txt_div = li.find('div', class_='txt')

        if thumbnail_div and txt_div:
            img = thumbnail_div.find('a href')
            if img:
                img_src = img.get('onclick')  # 이미지 src 추출
                print("유기동물 id :", img_src)

            # 'txt' div의 내용 추출
            print("Text div 내용:", txt_div.get_text(strip=True))
