from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_api_key():
    try:
        with open('api_key.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_api_key(api_key):
    with open('api_key.txt', 'w') as f:
        f.write(api_key)

def get_weather(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru'
    response = requests.get(url)
    return response.json()

@app.route('/', methods=['GET', 'POST'])
def index():
    api_key = get_api_key()

    if request.method == 'POST':
        if 'set_api_key' in request.form:
            new_api_key = request.form['api_key']
            save_api_key(new_api_key)
            api_key = new_api_key

        if 'city' in request.form and api_key:
            city = request.form['city']
            weather_data = get_weather(city, api_key)
            if weather_data.get('cod') == 200:
                return render_template('index.html', weather=weather_data, api_key_set=True)
            else:
                return render_template('index.html', error="Город не найден", api_key_set=True)

    return render_template('index.html', api_key_set=bool(api_key))

if __name__ == '__main__':
    app.run(debug=True)
