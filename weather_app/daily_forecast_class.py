# Conversion function for Fahrenheit to Celsius
def fahrenheit_to_celsius(f: float) -> float:
    return (f - 32) / 1.8

# Conversion function for Celsius to Fahrenheit
def celsius_to_fahrenheit(c: float) -> float:
    return c * 1.8 + 32

# DailyForecast class to represent a single period of daily weather data
class DailyForecast:
    def __init__(self, period_name, temperature_fahrenheit, temperature_celsius, chance_of_rain, icon_url, detailed_forecast):
        """
        Initialize a DailyForecast object with the specified attributes.
        
        Args:
            period_name (str): Name of the forecast period (e.g., "Monday Night").
            temperature_fahrenheit (str): Temperature in Fahrenheit (e.g., "60 F").
            temperature_celsius (str): Temperature in Celsius (e.g., "16 C").
            chance_of_rain (str): Probability of precipitation (e.g., "90%").
            icon_url (str): URL to the weather icon.
            detailed_forecast (str): Detailed weather description.
        """
        self.period_name = period_name
        self.temperature_fahrenheit = temperature_fahrenheit
        self.temperature_celsius = temperature_celsius
        self.chance_of_rain = chance_of_rain
        self.icon_url = icon_url
        self.detailed_forecast = detailed_forecast

    @classmethod
    def from_dict(cls, data_dict):
        """
        Create a DailyForecast object from a dictionary, handling data cleaning and conversion.
        
        Args:
            data_dict (dict): Dictionary containing CSV row data with keys:
                'period_name', 'temperature', 'temperature_unit', 'probability_of_precipitation',
                'icon', 'detailed_forecast'.
        
        Returns:
            DailyForecast: A new instance with cleaned and converted data.
        """
        # Extract and clean data from the dictionary
        period_name = data_dict.get('period_name', '').strip()
        temperature_str = data_dict.get('temperature', '').strip()
        temperature_unit = data_dict.get('temperature_unit', '').strip().upper()
        probability_of_precipitation = data_dict.get('probability_of_precipitation', '').strip()
        icon_url = data_dict.get('icon', '').strip()
        detailed_forecast = data_dict.get('detailed_forecast', '').strip()

        # Handle missing or invalid temperature data
        if not temperature_str or not temperature_unit:
            temperature_fahrenheit = "N/A"
            temperature_celsius = "N/A"
        else:
            try:
                temperature = float(temperature_str)
                if temperature_unit == 'F':
                    temperature_fahrenheit = f"{int(temperature)} F"
                    celsius = (temperature - 32) * 5 / 9
                    temperature_celsius = f"{round(celsius)} C"
                elif temperature_unit == 'C':
                    temperature_celsius = f"{int(temperature)} C"
                    fahrenheit = (temperature * 9 / 5) + 32
                    temperature_fahrenheit = f"{round(fahrenheit)} F"
                else:
                    temperature_fahrenheit = "N/A"
                    temperature_celsius = "N/A"
            except ValueError:
                temperature_fahrenheit = "N/A"
                temperature_celsius = "N/A"

        # Format chance of rain
        chance_of_rain = f"{probability_of_precipitation}%" if probability_of_precipitation else "N/A"

        # Return a new DailyForecast instance
        return cls(period_name, temperature_fahrenheit, temperature_celsius, chance_of_rain, icon_url, detailed_forecast)