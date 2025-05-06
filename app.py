import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="centered"
)

# Add custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #0D47A1;
    }
    .weather-card {
        background-color: #f0f8ff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .forecast-card {
        background-color: #e1f5fe;
        border-radius: 10px;
        padding: 10px;
        margin: 5px;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>Weather Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# Weather API Configuration
# Replace 'YOUR_API_KEY_HERE' with your actual WeatherAPI.com API key
api_key = "6dd0c2965ca046f6ab5155057250505"

# Default location
default_location = "Pune, India"
location = st.sidebar.text_input("Enter City Name", default_location)

# Units selection
units = st.sidebar.selectbox("Temperature Units", ["Celsius", "Fahrenheit"])

# Define weather icons mapping
weather_icons = {
    "Sunny": "☀️",
    "Clear": "🌞",
    "Partly cloudy": "⛅",
    "Cloudy": "☁️",
    "Overcast": "☁️",
    "Mist": "🌫️",
    "Patchy rain possible": "🌦️",
    "Patchy snow possible": "🌨️",
    "Patchy sleet possible": "🌧️",
    "Patchy freezing drizzle possible": "🌧️",
    "Thundery outbreaks possible": "⛈️",
    "Blowing snow": "❄️",
    "Blizzard": "❄️",
    "Fog": "🌫️",
    "Freezing fog": "🌫️",
    "Patchy light drizzle": "🌧️",
    "Light drizzle": "🌧️",
    "Freezing drizzle": "🌧️",
    "Heavy freezing drizzle": "🌧️",
    "Patchy light rain": "🌧️",
    "Light rain": "🌧️",
    "Moderate rain at times": "🌧️",
    "Moderate rain": "🌧️",
    "Heavy rain at times": "🌧️",
    "Heavy rain": "🌧️",
    "Light freezing rain": "🌧️",
    "Moderate or heavy freezing rain": "🌧️",
    "Light sleet": "🌨️",
    "Moderate or heavy sleet": "🌨️",
    "Patchy light snow": "🌨️",
    "Light snow": "🌨️",
    "Patchy moderate snow": "🌨️",
    "Moderate snow": "❄️",
    "Patchy heavy snow": "❄️",
    "Heavy snow": "❄️",
    "Ice pellets": "🧊",
    "Light rain shower": "🌦️",
    "Moderate or heavy rain shower": "🌦️",
    "Torrential rain shower": "🌧️",
    "Light sleet showers": "🌨️",
    "Moderate or heavy sleet showers": "🌨️",
    "Light snow showers": "🌨️",
    "Moderate or heavy snow showers": "❄️",
    "Light showers of ice pellets": "🧊",
    "Moderate or heavy showers of ice pellets": "🧊",
    "Patchy light rain with thunder": "⛈️",
    "Moderate or heavy rain with thunder": "⛈️",
    "Patchy light snow with thunder": "⛈️",
    "Moderate or heavy snow with thunder": "⛈️",
}

# Function to get weather data
@st.cache_data(ttl=600)  # Cache data for 10 minutes
def get_weather_data(location, api_key):
    try:
        url = f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=3&aqi=yes&alerts=yes"
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None
 
# Get weather data
weather_data = get_weather_data(location, api_key)

# Display weather information if data is available
if weather_data:
    # Extract current weather information
    current = weather_data["current"]
    location_data = weather_data["location"]
    forecast = weather_data["forecast"]["forecastday"]
    
    # Location and time information
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### 📍 {location_data['name']}, {location_data['country']}")
        local_time = datetime.strptime(location_data['localtime'], "%Y-%m-%d %H:%M")
        st.write(f"Local time: {local_time.strftime('%A, %d %B %Y, %H:%M')}")
    
    with col2:
        condition_text = current['condition']['text']
        icon = weather_icons.get(condition_text, "🌡️")
        st.markdown(f"## {icon} {condition_text}")
    
    # Main weather card
    st.markdown("<div class='weather-card'>", unsafe_allow_html=True)
    
    # Temperature display
    temp_unit = "°C" if units == "Celsius" else "°F"
    temp_value = current["temp_c"] if units == "Celsius" else current["temp_f"]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"### {temp_value}{temp_unit}")
        st.write(f"Feels like: {current['feelslike_c'] if units == 'Celsius' else current['feelslike_f']}{temp_unit}")
    
    with col2:
        st.markdown("### Humidity")
        st.write(f"{current['humidity']}%")
        st.write(f"Pressure: {current['pressure_mb']} mb")
    
    with col3:
        st.markdown("### Wind")
        wind_unit = "km/h" if units == "Celsius" else "mph"
        wind_value = current["wind_kph"] if units == "Celsius" else current["wind_mph"]
        st.write(f"{wind_value} {wind_unit} ({current['wind_dir']})")
        st.write(f"Gusting to {current['gust_kph'] if units == 'Celsius' else current['gust_mph']} {wind_unit}")
    
    # Additional information
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"UV Index: {current['uv']}")
    with col2:
        st.write(f"Visibility: {current['vis_km'] if units == 'Celsius' else current['vis_miles']} {'km' if units == 'Celsius' else 'miles'}")
    with col3:
        st.write(f"Precipitation: {current['precip_mm'] if units == 'Celsius' else current['precip_in']} {'mm' if units == 'Celsius' else 'in'}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Air Quality Information
    if 'air_quality' in current:
        st.markdown("<h3 class='sub-header'>Air Quality</h3>", unsafe_allow_html=True)
        
        aqi = current['air_quality']
        
        # Create AQI color function
        def get_aqi_color(aqi_value):
            if aqi_value <= 50:
                return "green", "Good"
            elif aqi_value <= 100:
                return "yellow", "Moderate"
            elif aqi_value <= 150:
                return "orange", "Unhealthy for Sensitive Groups"
            elif aqi_value <= 200:
                return "red", "Unhealthy"
            elif aqi_value <= 300:
                return "purple", "Very Unhealthy"
            else:
                return "maroon", "Hazardous"
        
        us_epa_index = aqi.get('us-epa-index', 1)
        color, category = get_aqi_color(us_epa_index * 50)  # Convert 1-6 scale to approximate AQI
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div style='background-color: {color}; padding: 10px; border-radius: 5px; text-align: center;'>"
                       f"<h4 style='color: {'white' if color in ['red', 'purple', 'maroon'] else 'black'};'>{category}</h4>"
                       "</div>", unsafe_allow_html=True)
        
        with col2:
            air_quality_data = {
                "Pollutant": ["Carbon Monoxide (CO)", "Ozone (O₃)", "Nitrogen dioxide (NO₂)", "Sulfur dioxide (SO₂)"],
                "Value (μg/m³)": [
                    round(aqi.get('co', 0), 2),
                    round(aqi.get('o3', 0), 2),
                    round(aqi.get('no2', 0), 2),
                    round(aqi.get('so2', 0), 2)
                ]
            }
            st.dataframe(pd.DataFrame(air_quality_data), hide_index=True)
    
    # 3-Day Forecast
    st.markdown("<h3 class='sub-header'>3-Day Forecast</h3>", unsafe_allow_html=True)
    
    forecast_cols = st.columns(len(forecast))
    
    for i, day in enumerate(forecast):
        date = datetime.strptime(day['date'], "%Y-%m-%d")
        with forecast_cols[i]:
            st.markdown("<div class='forecast-card'>", unsafe_allow_html=True)
            st.write(f"**{date.strftime('%A')}**")
            
            # Weather icon
            day_condition = day['day']['condition']['text']
            day_icon = weather_icons.get(day_condition, "🌡️")
            st.markdown(f"### {day_icon}")
            st.write(day_condition)
            
            # Temperature
            temp_max = day['day']['maxtemp_c'] if units == "Celsius" else day['day']['maxtemp_f']
            temp_min = day['day']['mintemp_c'] if units == "Celsius" else day['day']['mintemp_f']
            st.write(f"**High:** {temp_max}{temp_unit}")
            st.write(f"**Low:** {temp_min}{temp_unit}")
            
            # Precipitation
            precip = day['day']['totalprecip_mm'] if units == "Celsius" else day['day']['totalprecip_in']
            precip_unit = "mm" if units == "Celsius" else "in"
            st.write(f"Precipitation: {precip} {precip_unit}")
            
            # Chance of rain
            st.write(f"Rain chance: {day['day']['daily_chance_of_rain']}%")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Weather Alerts section
    if "alerts" in weather_data and weather_data["alerts"]["alert"]:
        st.markdown("<h3 class='sub-header'>⚠️ Weather Alerts</h3>", unsafe_allow_html=True)
        
        for alert in weather_data["alerts"]["alert"]:
            st.warning(f"**{alert['headline']}**\n\n{alert['desc']}\n\nEvent: {alert['event']}\nEffective: {alert['effective']}\nExpires: {alert['expires']}")
    
    # Hourly forecast for today
    st.markdown("<h3 class='sub-header'>Hourly Forecast (Today)</h3>", unsafe_allow_html=True)
    
    # Get the hourly forecast data
    hourly_data = forecast[0]['hour']
    
    # Filter hourly data to show only future hours and limit to next 12 hours
    current_hour = datetime.now().hour
    filtered_hours = [h for h in hourly_data if datetime.strptime(h['time'], "%Y-%m-%d %H:%M").hour >= current_hour][:12]
    
    # Prepare data for the chart
    hour_labels = [datetime.strptime(h['time'], "%Y-%m-%d %H:%M").strftime("%H:%M") for h in filtered_hours]
    temperatures = [h['temp_c'] if units == "Celsius" else h['temp_f'] for h in filtered_hours]
    conditions = [h['condition']['text'] for h in filtered_hours]
    
    # Create hourly forecast chart
    hourly_data = {
        'Hour': hour_labels,
        'Temperature': temperatures,
        'Condition': conditions
    }
    
    hourly_df = pd.DataFrame(hourly_data)
    st.line_chart(hourly_df.set_index('Hour')['Temperature'])
    
    # Show detailed hourly data
    if st.checkbox("Show detailed hourly forecast"):
        detailed_hour_data = []
        
        for hour in filtered_hours:
            hour_time = datetime.strptime(hour['time'], "%Y-%m-%d %H:%M").strftime("%H:%M")
            hour_temp = hour['temp_c'] if units == "Celsius" else hour['temp_f']
            hour_condition = hour['condition']['text']
            hour_precip = hour['precip_mm'] if units == "Celsius" else hour['precip_in']
            hour_wind = hour['wind_kph'] if units == "Celsius" else hour['wind_mph']
            
            detailed_hour_data.append({
                'Time': hour_time,
                'Temperature': f"{hour_temp}{temp_unit}",
                'Condition': hour_condition,
                'Precipitation': f"{hour_precip} {'mm' if units == 'Celsius' else 'in'}",
                'Wind': f"{hour_wind} {'km/h' if units == 'Celsius' else 'mph'}"
            })
        
        st.dataframe(pd.DataFrame(detailed_hour_data), hide_index=True)
    
    # Footer
    st.markdown("---")
    st.markdown("Data provided by [WeatherAPI.com](https://www.weatherapi.com/)")
    st.markdown("Created with Streamlit")
    
else:
    # Display error message if location is not found
    if api_key:
        st.error(f"Could not find weather data for '{location}'. Please check the city name and try again.")