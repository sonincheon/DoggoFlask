import json
import datetime
import pytz
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


@app.route('/api/hourly_weather', methods=['GET'])
def get_hourly_weather():
    print('응답받음')
    x = request.args.get('x')
    y = request.args.get('y')

    # 날짜 및 시간 설정
    # 날짜 및 시간 설정
    now = datetime.datetime.now()
    date = now.strftime('%Y%m%d')
    korea_timezone = pytz.timezone("Asia/Seoul")
    now = now - datetime.timedelta(hours=3)
    time = now.strftime('%H00')

    # 예보 요청 주소 및 요청 변수 지정
    forecast_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    API_KEY = 'Olxg1mLV/06zroxq+lNMTBH/PN1lq6uMU4NXhdDoeRAOXvszXzU8lChRY2zuMSqh5BN0vXrilLTQ+/FXdwDRHg=='

    # 한 페이지에 포함된 결과 수
    num_of_rows = 1000
    # 페이지 번호
    page_no = 1
    # 응답 데이터 형식 지정
    data_type = 'JSON'

    forecast_parameter = {
        'ServiceKey': API_KEY,
        'nx': x, 'ny': y,
        'base_date': date, 'base_time': time,
        'pageNo': page_no, 'numOfRows': num_of_rows,  # 24시간 데이터를 위해 더 많은 행 수가 필요
        'dataType': data_type
    }

    # 요청 및 응답
    try:
        forecast_response = requests.get(forecast_url, params=forecast_parameter)
        forecast_data = forecast_response.json()
        # print("API Response:", json.dumps(forecast_data, indent=4))

        if 'response' in forecast_data and 'body' in forecast_data['response']:
            forecast_items = forecast_data['response']['body']['items']['item']
        else:
            return jsonify({"error": "Invalid API response"})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)})

    # 현재 날짜와 시간을 YYYYMMDDHHMM 형식으로 설정
    now = datetime.datetime.now(korea_timezone)
    current_datetime = now.strftime("%Y%m%d%H00")

    print(current_datetime)
    forecast_weather_data = {}

    for item in forecast_items:
        # 예보 날짜와 시간을 YYYYMMDDHHMM 형식으로 설정
        forecast_date_time = item['fcstDate'] + item['fcstTime']

        if int(forecast_date_time) < int(current_datetime):
            print()
            continue

        category = item['category']
        value = item['fcstValue']

        if category in ['TMP', 'REH', 'PCP', 'PTY', 'WSD', 'POP', 'SKY']:
            if category == 'TMP':
                forecast_weather_data.setdefault(forecast_date_time, {})['tmperature'] = f"{value}°"
            elif category == 'REH':
                forecast_weather_data.setdefault(forecast_date_time, {})['humidity'] = f"{value}%"
            elif category == 'PCP':
                forecast_weather_data.setdefault(forecast_date_time, {})['condition'] = value
            elif category == 'SKY':
                skies = {
                    '1': '맑음',
                    '3': '구름많음',
                    '4': '흐림'
                }
                sky_condition = skies.get(value, "Unknown")  # Get the corresponding text or "Unknown" if not found
                forecast_weather_data.setdefault(forecast_date_time, {})['sky'] = sky_condition
            elif category == 'POP':
                forecast_weather_data.setdefault(forecast_date_time, {})['rain_chance'] = f"{value}%"
            elif category == 'PTY':
                forecast_weather_data.setdefault(forecast_date_time, {})['rain'] = f"{value}mm"
            elif category == 'WSD':
                forecast_weather_data.setdefault(forecast_date_time, {})['wind'] = f"{value}m/s"

    forecast_weather_data = json.dumps(forecast_weather_data, ensure_ascii=False, indent=4)
    print("API Response:", json.dumps(forecast_weather_data, indent=4))

    return forecast_weather_data


if __name__ == '__main__':
    app.run(debug=True)
