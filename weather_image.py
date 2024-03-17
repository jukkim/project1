from flask import Flask, jsonify, request, render_template_string
import requests
from urllib.parse import quote

app = Flask(__name__)

# OpenWeatherMap API 키 설정
API_KEY = 'f25e19521f93d376eb4498430ae8c4df'
PEXELS_API_KEY = 'dpfXTdMUmB0LkAmcDKUKr83JGQeRElczwS9UtRktlbKU4u4WLfWx8bzo'


# 날씨 정보를 조회하는 라우트
@app.route('/weather', methods=['GET'])
def get_weather():
    # 쿼리 파라미터에서 도시 이름 가져오기
    city_name = request.args.get('city', '')
    if not city_name:
        return jsonify({'error': 'Missing city parameter'}), 400

    # 도시 이름을 URL 인코딩
    city_name_encoded = quote(city_name)

    # OpenWeatherMap API URL 구성
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name_encoded}&appid={API_KEY}&units=metric"

    # API 요청
    response = requests.get(url)
    if response.status_code != 200:
        # API 요청 실패 또는 도시를 찾을 수 없음
        return jsonify({'error': 'Failed to get weather information or city not found'}), response.status_code

    # API로부터 받은 날씨 정보
    weather_data = response.json()

    # 필요한 날씨 정보만 추출하여 응답
    result = {
        'city': city_name,
        'temperature': weather_data['main']['temp'],
        'description': weather_data['weather'][0]['description'],
        'humidity': weather_data['main']['humidity']
    }

    return jsonify(result)


@app.route('/show', methods=['GET'])
def show_animal_image():
    animal_name = request.args.get('animal', '')
    if not animal_name:
        return 'Missing animal parameter', 400

    headers = {'Authorization': PEXELS_API_KEY}
    url = f"https://api.pexels.com/v1/search?query={animal_name}&per_page=1"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return 'Failed to get image', response.status_code

    data = response.json()
    images = data['photos']

    if not images:
        return 'No images found', 404

    image_url = images[0]['src']['original']

    # HTML 페이지에서 이미지를 보여주기
    html_page = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{animal_name.capitalize()} Image</title>
    </head>
    <body>
        <h1>{animal_name.capitalize()} Image</h1>
        <img src="{image_url}" alt="{animal_name}" style="max-width:100%;height:auto;">
    </body>
    </html>
    """
    return render_template_string(html_page)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
