import datetime
import json
import requests
from django.shortcuts import render

# Create your views here.
def index(request):
    # API_KEY = open('C:\\weatherAPI\\weather_project\\API_KEY','r').read()
    api_key = "adcd26143cfd99083d71ad4c25533f25"
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=hourly,minutely&appid={}"
    
    
    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')
    
    
def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat,lon,api_key)).json()
   
    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }
    
    
    daily_forecasts = []
# Check if 'daily' key exists in the forecast_response
    if "daily" in forecast_response:
        # Check how many days are returned by the API
        # daily_data_list = forecast_response['daily'][:5]  # Limit to 5 days
        
        for daily_data in forecast_response["daily"][:5]:
            # Use .get() method to safely access nested keys
            day = datetime.datetime.fromtimestamp(daily_data.get('dt', 0)).strftime('%A')
            min_temp = round(daily_data.get("temp", {}).get("min", 0) - 273.15, 2)
            max_temp = round(daily_data.get("temp", {}).get("max", 0) - 273.15, 2)
            description = daily_data.get('weather', [{}])[0].get('description', 'No description')
            icon = daily_data.get("weather", [{}])[0].get("icon", "No icon")

            daily_forecasts.append({
                "day": day,
                "min_temp": min_temp,
                "max_temp": max_temp,
                "description": description,
                "icon": icon,
            })
    else:
        print(f"Error: {forecast_response.get('message', 'Unknown error')}")

    return weather_data, daily_forecasts

