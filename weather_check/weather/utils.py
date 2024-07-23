import openmeteo_requests
import pandas as pd
import requests_cache
from geopy.geocoders import Nominatim
from retry_requests import retry

weather_codes = {
    0: 'Чистое небо',
    1: 'Преимущественно ясно',
    2: 'Преимущественно ясно',
    3: 'Преимущественно ясно',
    45: 'Туман и оседающий изморозь',
    48: 'Туман и оседающий изморозь',
    51: 'Морось: слабая',
    53: 'Морось: умеренная',
    55: 'Морось: интенсивная',
    56: 'Замерзающая морось: слабая',
    57: 'Замерзающая морось: плотная интенсивность',
    61: 'Дождь: слабый',
    63: 'Дождь: умеренный',
    65: 'Дождь: сильный',
    66: 'Замерзающий дождь: слабой интенсивности',
    67: 'Замерзающий дождь: сильной интенсивности',
    71: 'Снегопад: слабый',
    73: 'Снегопад: умеренный',
    75: 'Снегопад: сильный',
    77: 'Снежные зерна',
    80: 'Ливневые дожди: слабые',
    81: 'Ливневые дожди: умеренные',
    82: 'Ливневые дожди: сильные',
    85: 'Снежные ливни: слабые',
    86: 'Снежные ливни: сильные',
    95: 'Гроза: слабая или умеренная',
    96: 'Гроза с небольшим градом',
    99: 'Гроза с сильным градом'
}


def map_code_to_text(code):
    return weather_codes.get(code, 'Unknown')


def make_pretty_table(data):
    df = pd.DataFrame(data=data)
    df['Время'] = df['Время'].dt.tz_convert('Europe/Moscow').dt.strftime('%H:%M')
    df['Температура'] = df['Температура'].astype(int).apply(
        lambda temp: f'{temp} °C')
    df['Погода'] = df['Погода'].map(map_code_to_text)
    table = df.to_html(
        classes='table table-bordered',
        index=False,
        header=True,
        justify='left')
    return table


def numpy_data(hourly):
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(1).ValuesAsNumpy()
    hourly_data = {"Время": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}
    hourly_data["Температура"] = hourly_temperature_2m
    hourly_data["Погода"] = hourly_weather_code
    return hourly_data


def get_weather(сity):
    geolocator = Nominatim(user_agent="weather_check")
    location = geolocator.geocode(сity)
    if not location:
        return None
    latitude = location.latitude
    longitude = location.longitude

    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "weather_code"],
        "forecast_hours": 6
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    hourly = response.Hourly()
    hourly_data = numpy_data(hourly)
    table = make_pretty_table(hourly_data)
    return table
