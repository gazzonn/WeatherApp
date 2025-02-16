from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY_FILE = 'api_key.txt'

def load_api_key():
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'r') as f:
            return f.read().strip()
    return ''

def save_api_key(api_key):
    with open(API_KEY_FILE, 'w') as f:
        f.write(api_key)

API_KEY = load_api_key()

@app.route('/', methods=['GET', 'POST'])
def index():
    global API_KEY
    weather_data = {}
    error = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            if not API_KEY:
                error = "API-ключ не установлен. Пожалуйста, введите ключ."
            else:
                weather_data = get_weather_data(city)
                if not weather_data:
                    error = "Город не найден. Проверьте название."
        else:
            error = "Пожалуйста, введите название города."
    return render_template('index.html', weather_data=weather_data, error=error)

@app.route('/set_api_key', methods=['POST'])
def set_api_key():
    global API_KEY
    data = request.json
    api_key = data.get('api_key', '')
    if api_key:
        API_KEY = api_key
        save_api_key(api_key)
        return jsonify({"status": "success", "api_key": API_KEY})
    return jsonify({"status": "error", "message": "API-ключ не может быть пустым"}), 400

def get_weather_data(city):
    global API_KEY
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    try:
        response = requests.get('http://api.openweathermap.org/data/2.5/weather', params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка API: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)