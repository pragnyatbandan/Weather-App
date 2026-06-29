from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'indore'


    WEATHER_API_KEY = '6d26a00060a3b4c1ba92e7273b7ccd54'    

    # Image search
    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    
    image_url = ''  # default fallback
    try:
        image_data = requests.get(city_url).json()
        search_items = image_data.get("items")
        if search_items and len(search_items) > 1:
            image_url = search_items[1]['link']
        elif search_items:
            image_url = search_items[0]['link']
    except Exception:
        image_url = ''

    # Weather search
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}'
    PARAMS = {'units': 'metric'}

    try:
        data = requests.get(url, params=PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        day = datetime.date.today()
        return render(request, 'weather/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'humidity': humidity,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })
    except KeyError:
        messages.error(request, 'Entered city is not available')
        day = datetime.date.today()
        return render(request, 'weather/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'indore',
            'exception_occurred': True
        })