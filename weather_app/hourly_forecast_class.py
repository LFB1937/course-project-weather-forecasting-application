from datetime import datetime

# Helper function to convert temperature from Fahrenheit to Celsius
def fahrenheit_to_celsius(f):
    """
    Convert a temperature from Fahrenheit to Celsius.

    Args:
        f (float): Temperature in Fahrenheit.

    Returns:
        float: Temperature in Celsius, rounded to preserve precision.
    """
    return (f - 32) * 5 / 9

# Helper function to convert temperature from Celsius to Fahrenheit
def celsius_to_fahrenheit(c):
    """
    Convert a temperature from Celsius to Fahrenheit.

    Args:
        c (float): Temperature in Celsius.

    Returns:
        float: Temperature in Fahrenheit, rounded to preserve precision.
    """
    return c * 9 / 5 + 32

# Dictionary mapping weather icon codes to emojis for visual representation
icon_to_emoji = {
    "skc": "☀️",          # Fair/clear
    "few": "🌤️",         # Few clouds
    "sct": "⛅",          # Scattered clouds
    "bkn": "🌥️",         # Broken clouds
    "ovc": "☁️",          # Overcast
    "wind": "🌬️",        # Windy
    "rain": "🌧️",        # Rain
    "rain_showers": "🌦️", # Rain showers
    "tsra": "⛈️",        # Thunderstorms
    "tsra_hi": "⛈️",     # Thunderstorms (high probability variant)
    "tsra_sct": "⛈️",    # Scattered thunderstorms
    "snow": "❄️",         # Snow
    "fog": "🌫️",         # Fog
}

# Class representing an hourly weather forecast
class HourlyForecast:
    def __init__(self, timestamp, temperature_f, temperature_c, dewpoint_f, dewpoint_c, 
                 probability_of_precipitation, relative_humidity, wind_speed, wind_direction, 
                 icon_url, short_forecast, weather_icon):
        """
        Initialize an HourlyForecast object with weather data.

        Args:
            timestamp (str): ISO format timestamp of the forecast (e.g., '2025-04-28T16:00:00-05:00').
            temperature_f (float): Temperature in Fahrenheit.
            temperature_c (float): Temperature in Celsius.
            dewpoint_f (float): Dewpoint temperature in Fahrenheit.
            dewpoint_c (float): Dewpoint temperature in Celsius.
            probability_of_precipitation (float): Chance of precipitation as a percentage.
            relative_humidity (float): Relative humidity as a percentage.
            wind_speed (str): Wind speed (e.g., '10 mph').
            wind_direction (str): Wind direction (e.g., 'S' for South).
            icon_url (str): URL to the weather icon from the API.
            short_forecast (str): Brief description of the weather (e.g., 'Sunny').
            weather_icon (str): Emoji representing the weather condition.
        """
        self.timestamp = timestamp
        self.temperature_f = temperature_f
        self.temperature_c = temperature_c
        self.dewpoint_f = dewpoint_f
        self.dewpoint_c = dewpoint_c
        self.probability_of_precipitation = probability_of_precipitation
        self.relative_humidity = relative_humidity
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.icon_url = icon_url
        self.short_forecast = short_forecast
        self.weather_icon = weather_icon

        # Format timestamp for display
        dt = datetime.fromisoformat(timestamp)
        self.forecast_hour = dt.strftime("%H:%M")  # e.g., '16:00'
        self.formatted_date = dt.strftime("%Y-%m-%d")  # e.g., '2025-04-28'

        # Format weather data for UI display
        self.chance_of_rain = f"{probability_of_precipitation}%"
        self.temperature_fahrenheit = f"{temperature_f:.0f} F"
        self.dewpoint_fahrenheit = f"{dewpoint_f:.0f} F"
        self.relative_humidity = f"{relative_humidity}%"
        self.wind = f"{wind_speed} {wind_direction}".strip()

    @classmethod
    def from_dict(cls, data, timestamp_key='timestamp'):
        """
        Create an HourlyForecast object from a dictionary of weather data.

        Args:
            data (dict): Dictionary containing weather data from CSV.
            timestamp_key (str): Key for the timestamp field in the dictionary (default 'timestamp', 
                                 can be 'start_time' if 'timestamp' is absent).

        Returns:
            HourlyForecast: An instance of HourlyForecast with parsed and converted data.

        Raises:
            KeyError: If required fields are missing.
            ValueError: If data cannot be converted or units are unrecognized.
        """
        # Extract timestamp using the provided key
        timestamp = data[timestamp_key]

        # Extract and convert temperature
        temperature_value = float(data['temperature'])
        temperature_unit = data['temperature_unit'].strip()
        if temperature_unit == 'F':
            temperature_f = temperature_value
            temperature_c = fahrenheit_to_celsius(temperature_value)
        elif temperature_unit == 'C':
            temperature_c = temperature_value
            temperature_f = celsius_to_fahrenheit(temperature_value)
        else:
            raise ValueError(f"Unknown temperature unit: {temperature_unit}")

        # Extract and convert dewpoint
        dewpoint_value = float(data['dewpoint_value'])
        dewpoint_unit = data['dewpoint_unit'].strip()
        if dewpoint_unit == 'wmoUnit:degC':
            dewpoint_c = dewpoint_value
            dewpoint_f = celsius_to_fahrenheit(dewpoint_value)
        elif dewpoint_unit == 'wmoUnit:degF':
            dewpoint_f = dewpoint_value
            dewpoint_c = fahrenheit_to_celsius(dewpoint_value)
        else:
            raise ValueError(f"Unknown dewpoint unit: {dewpoint_unit}")

        # Extract other weather metrics
        probability_of_precipitation = float(data['precipitation_probability_value'])
        relative_humidity = float(data['relative_humidity_value'])
        wind_speed = data['wind_speed']
        wind_direction = data['wind_direction']
        icon_url = data['weather_icon_url']
        short_forecast = data['short_forecast']

        # Map weather icon code to emoji
        code = icon_url.split('/')[-1].split('?')[0].split(',')[0]
        weather_icon = icon_to_emoji.get(code, '❓')  # Default to '?' if code is unknown

        return cls(timestamp, temperature_f, temperature_c, dewpoint_f, dewpoint_c,
                   probability_of_precipitation, relative_humidity, wind_speed, wind_direction,
                   icon_url, short_forecast, weather_icon)