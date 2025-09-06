import streamlit as st
import requests
import geocoder
from datetime import datetime
import base64
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="Weather Dashboard", layout="wide", initial_sidebar_state="collapsed")

# --- API Keys ---
OWM_API_KEY = "fcb0eb65373687bdbf91fa208471c685"
UNSPLASH_ACCESS_KEY = "2pw-B8Cm6vGgNQopxyqiVS_uN0YiPTxFa3rdCT60T1M"

# --- Weather Icons ---
WEATHER_ICONS = {
    "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️", "Drizzle": "💧",
    "Thunderstorm": "⚡", "Snow": "❄️", "Mist": "🌫️", "Haze": "🌫️",
    "Fog": "🌫️", "Tornado": "🌪️"
}
AQI_LEVELS = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}

# --- Helper Functions ---
@st.cache_data(ttl=600)
def get_bg_image(query):
    """Fetches a background image from Unsplash based on a query."""
    if not UNSPLASH_ACCESS_KEY or "YOUR_UNSPLASH" in UNSPLASH_ACCESS_KEY:
        return "https://images.pexels.com/photos/209831/pexels-photo-209831.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    
    url = f"https://api.unsplash.com/photos/random?query={query}&orientation=landscape&client_id={UNSPLASH_ACCESS_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['urls']['regular']
    except Exception:
        pass # Fallback to default
    return "https://images.pexels.com/photos/209831/pexels-photo-209831.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"

def set_bg_from_url(url):
    """Sets the background of the app from a URL."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            bin_str = base64.b64encode(response.content).decode()
            page_bg_img = f'''
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{bin_str}");
                background-size: cover;
                background-attachment: fixed;
            }}
            [data-testid="stHeader"], [data-testid="stToolbar"] {{
                background-color: rgba(0,0,0,0);
            }}
            .main-container {{
                margin-top: -80px;
                padding: 2rem;
                padding-top: 4rem;
            }}
            
            /* Card style for data display */
            .card {{
                background-color: rgba(0, 0, 0, 0.65);
                backdrop-filter: blur(8px);
                padding: 1.5rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.18);
                margin-bottom: 1rem;
                color: white !important;
            }}

            /* --- NEW Custom Metric Card Styling --- */
            .metric-card {{
                background-color: rgba(0, 0, 0, 0.65);
                backdrop-filter: blur(8px);
                padding: 1rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.18);
                text-align: center;
                height: 100%; /* Ensures equal height in columns */
            }}
            .metric-card .label {{
                font-size: 1.1rem;
                color: rgba(255, 255, 255, 0.7);
                margin-bottom: 0.5rem;
            }}
            .metric-card .value {{
                font-size: 2.2rem;
                font-weight: 600;
                line-height: 1.2;
            }}
            .metric-card .delta {{
                font-size: 1rem;
                color: rgba(255, 255, 255, 0.9);
            }}
            .metric-card .icon {{
                font-size: 2.5rem;
            }}

            /* --- The REFINED Input Container --- */
            .input-container {{
                background-color: rgba(0, 0, 0, 0.65);
                backdrop-filter: blur(8px);
                padding: 1.5rem;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.18);
                margin-bottom: 1rem;
            }}
            /* This is the key to perfect alignment */
            .input-container [data-testid="stHorizontalBlock"] {{
                align-items: flex-end;
            }}
            .input-container label {{
                color: rgba(255, 255, 255, 0.8) !important;
                font-weight: bold;
            }}
            .input-container .stTextInput input {{
                background-color: rgba(0,0,0,0.3);
                color: white;
            }}
            .input-container .stButton button {{
                background-color: rgba(0,0,0,0.4);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                width: 100%;
            }}
            </style>
            '''
            st.markdown(page_bg_img, unsafe_allow_html=True)
    except Exception:
        st.error("Failed to load background image.")

def deg_to_cardinal(deg):
    """Converts wind direction from degrees to cardinal points."""
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    ix = int((deg + 11.25)/22.5)
    return dirs[ix % 16]

@st.cache_data(ttl=600)
def get_weather_data(city, units):
    """Fetches weather data using standard 'weather' and 'forecast' APIs."""
    if not OWM_API_KEY or "YOUR_KEY" in OWM_API_KEY:
        return None, "OpenWeatherMap API key is missing from the script."
    try:
        # --- Get Current Weather & Coordinates ---
        current_weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OWM_API_KEY}&units={units}"
        current_res = requests.get(current_weather_url).json()
        if current_res.get('cod') != 200:
            return None, current_res.get('message', 'City not found')
        
        lat, lon = current_res['coord']['lat'], current_res['coord']['lon']

        # --- Get 5-Day Forecast ---
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OWM_API_KEY}&units={units}"
        forecast_res = requests.get(forecast_url).json()
        if forecast_res.get('cod') != "200":
            return None, forecast_res.get('message', 'Could not retrieve forecast')

        # --- Get Air Quality ---
        aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OWM_API_KEY}"
        aqi_res = requests.get(aqi_url).json()
        aqi = aqi_res['list'][0]['main']['aqi'] if aqi_res.get('list') else "N/A"

        # --- Combine Data ---
        weather_data = {
            'name': current_res['name'],
            'lat': lat, 'lon': lon,
            'current': {
                'temp': current_res['main']['temp'],
                'feels_like': current_res['main']['feels_like'],
                'humidity': current_res['main']['humidity'],
                'weather': current_res['weather'],
                'wind_speed': current_res['wind']['speed'],
                'wind_deg': current_res['wind']['deg'],
                'sunrise': current_res['sys']['sunrise'],
                'sunset': current_res['sys']['sunset'],
                'pressure': current_res['main']['pressure'],
                'visibility': current_res.get('visibility', 10000),
                'aqi': aqi
            },
            'forecast': forecast_res['list']
        }
        return weather_data, None
    except Exception as e:
        return None, f"An error occurred: {e}"

# --- Main App UI ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="card" style="text-align: center;"><h1>Weather Dashboard</h1></div>', unsafe_allow_html=True)

# --- Initialize Session State ---
if 'units' not in st.session_state:
    st.session_state.units = 'metric'
if 'city' not in st.session_state:
    try:
        g = geocoder.ip('me')
        st.session_state.city = g.city if g.city else "London"
    except Exception:
        st.session_state.city = "London"

# --- User Inputs ---
st.markdown('<div class="input-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([4, 2, 2])
with col1:
    new_city = st.text_input("Enter a city:", st.session_state.city, key="city_input")
    if new_city: st.session_state.city = new_city
with col2:
    unit_choice = st.radio("Units", ('Celsius', 'Fahrenheit'), index=0 if st.session_state.units == 'metric' else 1)
    st.session_state.units = 'metric' if unit_choice == 'Celsius' else 'imperial'
with col3:
    if st.button("My Location", key="my_location_btn"):
        try:
            g = geocoder.ip('me')
            if g.city: st.session_state.city = g.city
        except Exception: st.error("Could not detect location.")
st.markdown('</div>', unsafe_allow_html=True)


# --- Data Fetching and Display ---
if not OWM_API_KEY or "YOUR_KEY" in OWM_API_KEY:
    st.warning("Please add your OpenWeatherMap API key to the script to fetch weather data.")
elif st.session_state.city:
    with st.spinner('Fetching weather data...'):
        weather_data, error = get_weather_data(st.session_state.city, st.session_state.units)

    if error:
        st.error(f"Could not retrieve weather for {st.session_state.city}. Error: {error}")
    else:
        # Set dynamic background
        condition_query = weather_data['current']['weather'][0]['main']
        city_query = weather_data['name']
        bg_url = get_bg_image(f"{condition_query} {city_query}")
        set_bg_from_url(bg_url)

        unit_symbol = "°C" if st.session_state.units == 'metric' else '°F'
        speed_unit = "m/s" if st.session_state.units == 'metric' else "mph"
        
        # --- Current Weather ---
        st.markdown(f'<div class="card"><h2>Current Weather in {weather_data["name"]}</h2></div>', unsafe_allow_html=True)
        current = weather_data['current']
        icon = WEATHER_ICONS.get(current['weather'][0]['main'], "❓")
        
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Temperature</div>
                <div class="value">{current['temp']:.1f}{unit_symbol}</div>
                <div class="delta">Feels like {current['feels_like']:.1f}{unit_symbol}</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Condition</div>
                <div class="value">{current['weather'][0]['description'].capitalize()}</div>
                <div class="icon">{icon}</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Humidity</div>
                <div class="value">{current['humidity']}%</div>
                <div class="delta">&nbsp;</div>
            </div>
            """, unsafe_allow_html=True)

        # --- 5-Day Forecast & Map/Details ---
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown('<div class="card"><h3>5-Day Forecast</h3></div>', unsafe_allow_html=True)
            daily_forecasts = {}
            for entry in weather_data['forecast']:
                day = datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d')
                if day not in daily_forecasts:
                    daily_forecasts[day] = {'temps': [], 'icons': []}
                daily_forecasts[day]['temps'].append(entry['main']['temp'])
                daily_forecasts[day]['icons'].append(entry['weather'][0]['main'])

            for i, (day, data) in enumerate(daily_forecasts.items()):
                if i > 4: break
                day_date = datetime.strptime(day, '%Y-%m-%d').strftime('%A, %b %d')
                day_icon = WEATHER_ICONS.get(max(set(data['icons']), key=data['icons'].count), "❓")
                max_temp, min_temp = max(data['temps']), min(data['temps'])
                forecast_html = f"""
                <div class="card" style="font-family: monospace; text-align: left;">
                   {day_date:<20} {day_icon} H: {max_temp:.1f}{unit_symbol} / L: {min_temp:.1f}{unit_symbol}
                </div>
                """
                st.markdown(forecast_html, unsafe_allow_html=True)
        
        with col2:
            # --- Map ---
            st.markdown('<div class="card"><h3>Location</h3>', unsafe_allow_html=True)
            map_data = pd.DataFrame({'lat': [weather_data['lat']], 'lon': [weather_data['lon']]})
            st.map(map_data, zoom=10)
            st.markdown('</div>', unsafe_allow_html=True)

            # --- Additional Details ---
            st.markdown('<div class="card"><h3>Additional Details</h3></div>', unsafe_allow_html=True)
            wind_direction = deg_to_cardinal(current['wind_deg'])
            aqi_text = AQI_LEVELS.get(current['aqi'], "N/A")
            details = {
                "Wind": f"{current['wind_speed']:.1f} {speed_unit} ({wind_direction})",
                "Air Quality": f"{aqi_text}",
                "Sunrise": f"{datetime.fromtimestamp(current['sunrise']).strftime('%H:%M')}",
                "Sunset": f"{datetime.fromtimestamp(current['sunset']).strftime('%H:%M')}",
                "Pressure": f"{current['pressure']} hPa",
                "Visibility": f"{current.get('visibility', 10000) / 1000:.1f} km"
            }
            for label, value in details.items():
                detail_html = f'<div class="card" style="font-family: monospace;"><b>{label}:</b> {value}</div>'
                st.markdown(detail_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)