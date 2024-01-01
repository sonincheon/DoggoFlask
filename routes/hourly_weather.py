import json
import datetime
import pytz
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


def calculate_forecast_time():
    now = datetime.datetime.now(pytz.timezone("Asia/Seoul"))
    forecast_times = [2, 5, 8, 11, 14, 17, 20, 23]  # 예보 업데이트 시간

    # 현재 시간보다 이전인 가장 가까운 업데이트 시간 찾기
    latest_forecast_time = max(hour for hour in forecast_times if hour <= now.hour)
    forecast_datetime = now.replace(hour=latest_forecast_time, minute=0, second=0, microsecond=0)

    return forecast_datetime.strftime('%Y%m%d'), forecast_datetime.strftime('%H00')


def process_forecast_data(forecast_items):
    forecast_weather_data = {}
    now = datetime.datetime.now(pytz.timezone("Asia/Seoul"))
    current_hour_key = now.strftime('%Y%m%d%H00')
    print(current_hour_key)
    for item in forecast_items:
        forecast_date_time = item['fcstDate'] + item['fcstTime']
        category = item['category']
        value = item['fcstValue']

        # 현재 시간대와 같거나 이후의 데이터만 포함
        if forecast_date_time >= current_hour_key:
            if category in ['TMP', 'REH', 'PCP', 'PTY', 'WSD', 'POP', 'SKY']:
                if category == 'TMP':
                    forecast_weather_data.setdefault(forecast_date_time, {})['temperature'] = f"{value}°"
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
                    sky_condition = skies.get(value, "Unknown")
                    forecast_weather_data.setdefault(forecast_date_time, {})['sky'] = sky_condition
                elif category == 'POP':
                    forecast_weather_data.setdefault(forecast_date_time, {})['rain_chance'] = f"{value}%"
                elif category == 'PTY':
                    forecast_weather_data.setdefault(forecast_date_time, {})['rain'] = f"{value}mm"
                elif category == 'WSD':
                    forecast_weather_data.setdefault(forecast_date_time, {})['wind'] = f"{value}m/s"

    return forecast_weather_data


@app.route('/api/hourly_weather', methods=['GET'])
def get_hourly_weather():
    x = request.args.get('x')
    y = request.args.get('y')

    date, time = calculate_forecast_time()  # 업데이트 주기에 맞는 날짜와 시간 계산

    forecast_url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    API_KEY = 'Olxg1mLV/06zroxq+lNMTBH/PN1lq6uMU4NXhdDoeRAOXvszXzU8lChRY2zuMSqh5BN0vXrilLTQ+/FXdwDRHg=='

    num_of_rows = 300
    page_no = 1
    data_type = 'JSON'

    forecast_parameter = {
        'ServiceKey': API_KEY,
        'nx': x, 'ny': y,
        'base_date': date, 'base_time': time,
        'pageNo': page_no, 'numOfRows': num_of_rows,
        'dataType': data_type
    }

    try:
        forecast_response = requests.get(forecast_url, params=forecast_parameter)
        forecast_data = forecast_response.json()

        if 'response' in forecast_data and 'body' in forecast_data['response']:
            forecast_items = forecast_data['response']['body']['items']['item']
        else:
            return jsonify({"error": "Invalid API response"})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)})

    forecast_weather_data = process_forecast_data(forecast_items)
    print(forecast_weather_data)
    return jsonify(forecast_weather_data)


if __name__ == '__main__':
    app.run(debug=True)
