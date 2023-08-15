from flask import Flask, request, render_template, url_for, redirect
from flask_request_arg import request_arg
from urllib.parse import urlparse
from urllib import parse
import requests
from modules.constants import API_URL, API_HEADER, API_JSON_FORECAST, WEATHER_CODES, BACKGROUND_IMGS

app = Flask(__name__)


def get_bg(root, days=0):
    if root is None:
        return url_for('static', filename=BACKGROUND_IMGS['SUNNY'])
    if days == 0:
        data = root['forecast']['forecastday'][-1]['day']['condition']['code']
    else:
        data = root['forecast']['forecastday'][len(root['forecast']['forecastday'])-1]['day']['condition']['code']
    hit = 0
    for k, v in WEATHER_CODES.items():
        if int(k) == data:
            hit = WEATHER_CODES[k]
            break
    if hit == 5:
        return url_for('static', filename=BACKGROUND_IMGS['SNOWY'])
    elif hit == 4:
        return url_for('static', filename=BACKGROUND_IMGS['DARK'])
    elif hit == 3:
        return url_for('static', filename=BACKGROUND_IMGS['RAINY'])
    elif hit == 2:
        return url_for('static', filename=BACKGROUND_IMGS['CLOUDY'])
    else:
        return url_for('static', filename=BACKGROUND_IMGS['SUNNY'])


def get_data_days(city, num=0):
    querystring = {'q': city, 'days': num}
    response = requests.get(API_URL + API_JSON_FORECAST, headers=API_HEADER, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        return None


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


def redirect_url(f_name, location, days=0):
    return redirect(url_for(f_name, location=location, days=days))


@app.route('/', methods=['GET', 'POST'])
def index():
    location = request.args.get('location') if request.args.get('location') is not None else 'Ottawa'
    if request.method == 'POST':
        location = request.form['location']
    if location is request.args.get('location'):
        result = get_data_days(location)
        bgImg = get_bg(result)
        return render_template('index.html', result=result, days=0, bgImg=bgImg, txt_search=location)
    return redirect_url('index', location)


@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    location = request.args.get('location') if request.args.get('location') is not None else 'Ottawa'
    days = request.args.get('days') if request.args.get('days') is not None else 3
    if request.method == 'POST':
        days = request.form['days']
        location = request.form['location']
    if location is request.args.get('location') and days is request.args.get('days'):
        result = get_data_days(location, days)
        bgImg = get_bg(result, days)
        return render_template('index.html', result=result, days=int(days), bgImg=bgImg, txt_search=location)
    return redirect_url('forecast', location, days)


if __name__ == '__main__':
    app.run(debug=True)
