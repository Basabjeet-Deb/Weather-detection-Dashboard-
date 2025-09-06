# Weather-detection-Dashboard-
# 🌦️ Python Weather Dashboard

A sleek, modern, and feature-rich weather dashboard built with Python and Streamlit. This application provides real-time weather information, a 5-day forecast, an interactive map, and air quality data, all presented in a beautiful, dynamically-updating interface.

## ✨ Features

- **Real-Time Weather:** Get the current temperature, "feels like" temperature, weather condition (with icons), and humidity.
- **Dynamic Backgrounds:** The app background changes to a high-quality image from Unsplash that reflects the current weather conditions (e.g., a sunny picture for a "Clear" sky).
- **5-Day Forecast:** See a detailed forecast for the next 5 days, including temperature, conditions, and icons.
- **Interactive Map:** A map displays the exact location of the city you're viewing.
- **Air Quality Index (AQI):** Provides the current AQI and detailed information about pollutants.
- **Wind Details:** Shows wind speed and direction.
- **Glassmorphism UI:** A beautiful "frosted glass" effect is applied to all UI elements, ensuring text is readable and stylish against any background image.
- **Customizable Units:** Switch between Metric (°C, m/s) and Imperial (°F, mph) units.
- **Geolocation:** Use the "My Location" button to automatically fetch weather for your current location.

## 🛠️ Technologies Used

- **Python:** The core programming language for all logic.
- **Streamlit:** The web application framework that turns the Python script into an interactive UI.
- **OpenWeatherMap API:** Used to fetch all weather, forecast, and air quality data.
- **Unsplash API:** Used to fetch high-quality, dynamic background images.
- **geopy:** A Python library used for the "My Location" feature.
- **HTML/CSS:** Custom HTML and CSS are injected to create the custom "glassmorphism" UI and responsive metric cards.

## 🚀 Setup and Installation

Follow these steps to get the Weather Dashboard running on your local machine.

### 1. Prerequisites

Make sure you have Python 3.7+ installed.

### 2. Get the Code

Download the `WeatherDashboard.py` file to a directory on your computer.

### 3. Install Dependencies

You'll need to install a few Python libraries. You can do this using `pip`. Open your terminal or command prompt and run:

```bash
pip install streamlit requests geopy
```

### 4. Get API Keys

This dashboard requires two API keys to function:

- **OpenWeatherMap API Key:**
  1. Go to [OpenWeatherMap](https://openweathermap.org/) and create a free account.
  2. Navigate to the "API keys" tab in your account.
  3. Generate a new key. It may take a couple of hours for the key to become active.

- **Unsplash API Key:**
  1. Go to [Unsplash Developers](https://unsplash.com/developers) and create an account.
  2. Create a "New Application."
  3. Your API "Access Key" will be available on your application's dashboard.

### 5. Add API Keys to the Script

Open the `WeatherDashboard.py` file and replace the placeholder API keys near the top of the file with the keys you just generated.

```python
# WeatherDashboard.py
OPENWEATHER_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"
UNSPLASH_ACCESS_KEY = "YOUR_UNSPLASH_API_KEY"
```

### 6. Run the Application

Once the dependencies are installed and the API keys are set, you can run the app. Navigate to the directory containing the script in your terminal and run:

```bash
streamlit run WeatherDashboard.py
```

Your web browser should open with the Weather Dashboard running and ready to use!
