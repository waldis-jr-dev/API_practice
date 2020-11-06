import requests
import pprint
import datetime
import static


KEY = static.weather_api()
city = 'Kiev'


def data_from_api_current(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={KEY}&units=metric'
    resp = requests.get(url)
    weather = resp.json()
    if 'message' in weather.keys() and weather['message'] == 'city not found':
        raise Exception('City not found')
    answer_weather = {'feels_like': 0, 'temp': 0, 'sunrise': 0, 'sunset': 0, 'description': 0}
    answer_weather['feels_like'] = weather['main']['feels_like']
    answer_weather['temp'] = weather['main']['temp']

    sunrise = weather['sys']['sunrise']
    sunrise = datetime.datetime.fromtimestamp(sunrise)
    answer_weather['sunrise'] = sunrise.strftime("%d-%m-%Y %H:%M:%S")

    sunset = weather['sys']['sunset']
    sunset = datetime.datetime.fromtimestamp(sunset)
    answer_weather['sunset'] = sunset.strftime("%d-%m-%Y %H:%M:%S")

    answer_weather['description'] = weather['weather'][0]['description']
    return answer_weather


def data_from_api_five_days(city):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={KEY}&units=metric'
    resp = requests.get(url)
    weather = resp.json()
    if 'message' in weather.keys() and weather['message'] == 'city not found':
        raise Exception('City not found')
    weather_one_iteration = {'min_temp': 100, 'max_temp': -100, 'description': 0, 'humidity': 0}
    weather_five = {}
    for i in weather['list']:
        dt = datetime.datetime.fromtimestamp(i['dt'])
        date = dt.strftime("%d-%m-%Y")
        time = dt.strftime("%H:%M:%S")

        if date not in weather_five.keys():
            woi = weather_one_iteration.copy()
            weather_five[date] = woi

        if time == '12:00:00':
            weather_five[date]['description'] = i['weather'][0]['description']
            weather_five[date]['humidity'] = i['main']['humidity']

        if weather_five[date]['min_temp'] >= i['main']['temp_min']:
            weather_five[date]['min_temp'] = i['main']['temp_min']

        if weather_five[date]['max_temp'] <= i['main']['temp_max']:
            weather_five[date]['max_temp'] = i['main']['temp_max']

    return weather_five


def main_loop():
    while True:
        city = input('What city do you want?(or EXIT) \n>>>')
        if city.lower() == 'exit':
            print('Bye-Bye, USER...')
            break
        try:
            print('******************************************\nWEATHER NOW: ')
            pprint.pprint(data_from_api_current(city))
            print('******************************************')
            print('******************************************\nWEATHER FOR 5 DAYS: ')
            pprint.pprint(data_from_api_five_days(city))
            print('******************************************')
        except Exception as error:
            print(f'\nSorry, but {error}\n')


if __name__ == '__main__':
    main_loop()
