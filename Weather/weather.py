import requests

# Your fixed API key
api_key = '211dcd841c073e3ace9376e27e1652f6'

# Get the city name from the user
city_name = input("Enter the city name you want to check the weather for: ")

# OpenWeatherMap API endpoint
url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=en"

# Make the API request
response = requests.get(url)

# If the request is successful (200 OK)
if response.status_code == 200:
    # Get the data in JSON format
    weather_data = response.json()
    
    # Print the weather information to the screen
    print(f"Weather for {city_name}:")
    print(f"Temperature: {weather_data['main']['temp']}°C")
    print(f"Feels Like: {weather_data['main']['feels_like']}°C")
    print(f"Humidity: {weather_data['main']['humidity']}%")
    print(f"Description: {weather_data['weather'][0]['description'].capitalize()}")
else:
    print('The request failed, error code:', response.status_code)
