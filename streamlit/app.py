import streamlit as st
import requests

API_KEY = "5ee5780d9c11f09843a4d8d8261b6bf9"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather_icon(description):
    icons = {
        "clear sky": "☀️",
        "few clouds": "🌤️",
        "scattered clouds": "☁️",
        "broken clouds": "🌥️",
        "shower rain": "🌦️",
        "rain": "🌧️",
        "thunderstorm": "⛈️",
        "snow": "❄️",
        "mist": "🌫️"
    }
    return icons.get(description.lower(), "🌍")  # Default icon

st.title("Weather Information Application")
st.write("Enter a city name to get the current weather information.")

city_name = st.text_input("City Name (e.g., Pune):")

if city_name:
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()

        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        city_display_name = data['name']

        weather_icon = get_weather_icon(weather_description)

        st.subheader(f"Weather in {city_display_name}:")
        st.markdown(f"### {weather_icon} {weather_description.capitalize()}")
        st.write(f"**Temperature:** {temperature} °C")
        st.write(f"**Feels Like:** {feels_like} °C")
        st.write(f"**Humidity:** {humidity}%")
        st.write(f"**Wind Speed:** {wind_speed} m/s")
    else:
        error_message = response.json().get("message", "Unknown error occurred")
        st.error(f"Error: {error_message}. Please try again!")
        st.write("Debug Info:", response.json())  # For troubleshooting
