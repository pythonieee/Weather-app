import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time

st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

# API key for OpenWeatherMap API
API_KEY = "f854de0828c391d399e8b26de4a3fa4f"  # Replace with your actual API key

def get_weather_data(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            st.error(f"Error: {data.get('message', 'Unknown error')}")
            return None, None
            
        # Forecast data (5 days)
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()
        
        if forecast_response.status_code != 200:
            st.error(f"Error: {forecast_data.get('message', 'Unknown error')}")
            return data, None
            
        return data, forecast_data
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None

# Function to display weather icon
def get_weather_icon(icon_code):
    return f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

def process_forecast_data(forecast_data):
    forecast_list = forecast_data['list']
    forecast_items = []
    
    for item in forecast_list:
        dt = datetime.fromtimestamp(item['dt'])
        forecast_items.append({
            'datetime': dt,
            'date': dt.date(),
            'time': dt.strftime('%H:%M'),
            'temp': item['main']['temp'],
            'feels_like': item['main']['feels_like'],
            'weather_main': item['weather'][0]['main'],
            'weather_description': item['weather'][0]['description'],
            'icon': item['weather'][0]['icon'],
            'humidity': item['main']['humidity'],
            'wind_speed': item['wind']['speed']
        })
    
    return forecast_items


def create_temp_chart(forecast_items):

    df = pd.DataFrame(forecast_items)
    

    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Plot temperature
    ax.plot(df['datetime'], df['temp'], 'r-', label='Temperature (°C)')
    ax.plot(df['datetime'], df['feels_like'], 'b--', label='Feels Like (°C)')
    
    
    ax.set_xlabel('Date/Time')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title('Temperature Forecast')
    
    
    plt.xticks(rotation=45)
    
    ax.legend()

    plt.tight_layout()
    
    return fig


def main():
    
    st.title("🌤️ Weather Dashboard")
    
    st.sidebar.header("Settings")
    
    city = st.sidebar.text_input("Enter city name", "London")
    
    temp_unit = st.sidebar.selectbox("Temperature unit", ["Celsius", "Fahrenheit"])
    
    search = st.sidebar.button("Search") 

    if search or 'weather_data' in st.session_state:
        with st.spinner("Fetching weather data..."):
            weather_data, forecast_data = get_weather_data(city)
            if weather_data:
                st.session_state.weather_data = weather_data
                st.session_state.forecast_data = forecast_data
            else:
                st.error("Failed to fetch weather data. Please try again.")
                return
        
        
        weather_data = st.session_state.weather_data
        forecast_data = st.session_state.forecast_data
        
        
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        if temp_unit == "Fahrenheit":
            temp = (temp * 9/5) + 32
            feels_like = (feels_like * 9/5) + 32
        
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            st.subheader("Current Weather")
            st.image(get_weather_icon(weather_data['weather'][0]['icon']), width=100)
            st.write(f"**{weather_data['weather'][0]['main']}**: {weather_data['weather'][0]['description']}")
        
        with col2:
            st.metric("Temperature", f"{temp:.1f} {'°F' if temp_unit == 'Fahrenheit' else '°C'}")
            st.metric("Feels Like", f"{feels_like:.1f} {'°F' if temp_unit == 'Fahrenheit' else '°C'}")
            st.metric("Humidity", f"{weather_data['main']['humidity']}%")
            st.metric("Wind Speed", f"{weather_data['wind']['speed']} m/s")
        
       

        if forecast_data:
            st.subheader("5-Day Forecast")
            
            
            forecast_items = process_forecast_data(forecast_data)
            
            
            st.subheader("Temperature Forecast")
            temp_chart = create_temp_chart(forecast_items)
            st.pyplot(temp_chart)
            
            
            st.subheader("Daily Forecast")
            
            
            days = {}
            for item in forecast_items:
                day_str = item['date'].strftime('%Y-%m-%d')
                if day_str not in days:
                    days[day_str] = item
            
            
            cols = st.columns(min(5, len(days)))
            for i, (day, data) in enumerate(list(days.items())[:5]):
                with cols[i]:
                    date_obj = datetime.strptime(day, '%Y-%m-%d')
                    st.write(f"**{date_obj.strftime('%a, %b %d')}**")
                    st.image(get_weather_icon(data['icon']), width=50)
                    temp = data['temp']
                    if temp_unit == "Fahrenheit":
                        temp = (temp * 9/5) + 32
                    st.write(f"{temp:.1f} {'°F' if temp_unit == 'Fahrenheit' else '°C'}")
                    st.write(f"{data['weather_main']}")
            
            
            st.subheader("Hourly Forecast")
            
            
            df = pd.DataFrame(forecast_items[:8])  
            
            
            if temp_unit == "Fahrenheit":
                df['temp'] = (df['temp'] * 9/5) + 32
                df['feels_like'] = (df['feels_like'] * 9/5) + 32
            
            
            display_df = pd.DataFrame({
                'Time': df['time'],
                'Temperature': df['temp'].map(lambda x: f"{x:.1f} {'°F' if temp_unit == 'Fahrenheit' else '°C'}"),
                'Weather': df['weather_description'],
                'Humidity': df['humidity'].map(lambda x: f"{x}%"),
                'Wind': df['wind_speed'].map(lambda x: f"{x} m/s")
            })
            
            st.dataframe(display_df)

if __name__ == "__main__":
    main()