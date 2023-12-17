import pymysql

# 해당 함수는 실제로 실행 x , 단지 코드로서 보관
def insert_strays(data_list):
    print('db 작업 함수 호출 ! ! ! !')
    # 데이터베이스 연결 설정
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Nuri110534!',
        db='my_pet',
        charset='utf8'
    )

    try:
        with conn.cursor() as cursor:
            print('db 작업 실행 ! ! ! !')
            # 기존 데이터 삭제
            cursor.execute("DELETE FROM stray_tb")

            # SQL 쿼리
            sql = ("INSERT INTO stray_tb (stray_id, animal_number, breed, city, image_link, region) VALUES (%s, %s, %s, %s, %s, %s)")

            # `stray_id` 초기화
            stray_id = 1

            # 데이터 리스트를 순회하며 데이터베이스에 삽입
            for data in data_list:
                # animalNumber 문자열을 정수로 변환
                animal_number = int(data['animalNumber']) if data['animalNumber'] else None

                # 데이터 로깅 (검증을 위함)
                print(f"Inserting: {stray_id}, {animal_number}, {data['breed']}, {data['city']}, {data['imageLink']}, {data['region']}")

                # 데이터 삽입
                cursor.execute(sql, (stray_id, animal_number, data['breed'], data['city'], data['imageLink'], data['region']))

                # `stray_id` 증가
                stray_id += 1

            # 변경사항 커밋
            conn.commit()

    except pymysql.MySQLError as e:
        print(f"db 작업 실패 ! ! ! ! !: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

    print('db 작업 종료 ! ! ! !')