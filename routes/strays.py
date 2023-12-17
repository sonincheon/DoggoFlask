import json

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import time


def parsing_id(onclick_str):
    """ 'moveUrl' 함수 호출에서 숫자 값을 추출 """
    match = re.search(r"moveUrl\('(\d+)'\);", onclick_str)
    return match.group(1) if match else None


def parsing_info(text_div):
    """ 공고번호와 품종 정보를 추출 """
    dds = text_div.find_all('dd')
    notice_number = dds[0].text.strip() if len(dds) > 0 else None
    list = notice_number.split('-')
    region = list[0]
    city = list[1]
    breed = dds[2].text.strip() if len(dds) > 0 else None
    return region, city, breed


# 메인 함수 , 유기동물보호소를 크롤링해와 다중 딕셔너리를 리스트로 감아서 반환
def parsing_strays():
    start = time.time()
    base_url = "https://www.animal.go.kr"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0'
                      'Safari/537.36'
    }

    int_page = 1
    stray_list = []

    print("크롤링 시작 ! ! ! ! !")
    while True:
        res = requests.get(
            f"{base_url}/front/awtis/public/publicList.do?totalCount=2705&pageSize=10&boardId=&desertionNo=&menuNo"
            f"=1000000055&searchSDate=&searchEDate=&searchUprCd=&searchOrgCd=&searchCareRegNo"
            f"=&searchUpKindCd=&searchKindCd=&searchSexCd=&searchRfid=&&page={int_page}",
            headers=headers)

        if res.status_code == requests.codes.ok:
            soup = BeautifulSoup(res.text, 'html.parser')
            no_content = soup.find('li', string=lambda text: text and '등록된 게시물이 없습니다.' in text)

            if no_content:
                print("페이지 끝까지 순회완료.")
                print("문자열 가공 함수 실행중...")
                print("크롤링 종료.")
                break

            li_items = soup.select('li')
            print(f"{int_page}페이지 접근완료")
            for li in li_items:
                photo_div = li.find('div', class_='photo')
                txt_div = li.find('div', class_='txt')

                if photo_div and txt_div:
                    img = photo_div.find('img')
                    more_btn = photo_div.find('a', class_='moreBtn')

                    img_src = urljoin(base_url, img.get('src')) if img else None
                    img_src = re.sub(r'\[\d+\]', '', img_src) if img_src else None

                    animal_number = parsing_id(more_btn.get('onclick')) if more_btn else None

                    region, city, breed = parsing_info(txt_div)

                    stray_list.append(
                        {'region': region, 'city': city, 'breed': breed,
                         'animalNumber': animal_number, 'imageLink': img_src})


        else:
            print("네트워크 오류 : [에러코드 ", res.status_code, "]")
            print("크롤링 종료.")
            break

        int_page += 1
    end = time.time()
    print(end - start)

    for stray_data in stray_list:
        print(stray_data)

    json_strays = json.dumps(stray_list, ensure_ascii=False, indent=5)
    return json_strays

# result = parsing_strays()


# for data in result:
#     print(data)
