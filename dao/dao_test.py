import pymysql

try:
    # 데이터베이스 연결
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='Nuri110534!',
        db='my_pet',
        charset='utf8'
    )

    with conn.cursor() as cursor:
        print('DB 작업 실행...')

        # 기존 데이터 삭제
        cursor.execute("DELETE FROM stray_tb")

        # SQL 쿼리
        sql = "INSERT INTO stray_tb (stray_id, animal_number, breed, city, image_link, region) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (1, 1, '길냥이', '판교', '이미지 링크', '경기도'))

        # 변경사항 커밋
        conn.commit()

except pymysql.MySQLError as e:
    print(f"Database error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    conn.close()
    print('DB 작업 종료.')
