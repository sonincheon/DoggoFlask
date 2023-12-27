from flask import Flask, render_template
from flask_cors import CORS


# 라우트 파일 가져오기
from routes.weather import get_weather
from routes.hourly_weather import get_hourly_weather
from routes.strays import parsing_strays
from dao.stray_dao import insert_strays

app = Flask(__name__)
CORS(app, origins=['*'])


# 로깅 설정
# logging.basicConfig(level=logging.DEBUG)

# 홈페이지 라우트
@app.route('/')
def home():
    return render_template("index.html")  # index.html 파일을 렌더링


# 날씨 API 라우트
app.add_url_rule('/api/weather', 'get_weather', get_weather, methods=['GET'])
app.add_url_rule('/api/hourly_weather', 'get_hourly_weather', get_hourly_weather, methods=['GET'])
app.add_url_rule('/api/strays', 'parsing_strays', parsing_strays, methods=['GET'])


# 스케줄러 작업 정의
# def strays_task():
#     print('스케줄러 작동 시작...')
#     result = parsing_strays()
#     insert_strays(result)


if __name__ == '__main__':
    app.run(debug=True)
