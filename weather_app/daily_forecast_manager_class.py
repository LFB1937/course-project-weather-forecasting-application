import csv
from datetime import datetime
from daily_forecast_class import DailyForecast

# DailyForecastManager class to load and manage daily forecast data from a CSV file
class DailyForecastManager:
    def __init__(self, csv_filename, generated_time):
        """
        Initialize the DailyForecastManager with a CSV filename and generation time.
        
        Args:
            csv_filename (str): Path to the CSV file containing forecast data.
            generated_time (str): Timestamp when the forecast was generated.
        """
        self.csv_filename = csv_filename
        self.generated_time = generated_time
        self.forecasts = []

    def load_forecasts(self):
        """
        Load forecast data from the CSV file into a list of DailyForecast objects.
        
        Returns:
            bool: True if loading succeeds, False otherwise.
        """
        try:
            with open(self.csv_filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    forecast = DailyForecast.from_dict(row)
                    self.forecasts.append(forecast)
            return True
        except FileNotFoundError:
            print(f"File {self.csv_filename} not found.")
            return False
        except Exception as e:
            print(f"Error loading forecasts: {e}")
            return False

    def get_forecasts(self):
        """
        Retrieve the list of loaded DailyForecast objects.
        
        Returns:
            list: List of DailyForecast objects.
        """
        return self.forecasts

    def __str__(self):
        """
        Provide a string summary of the manager's state.
        
        Returns:
            str: Summary including generation time and forecast count.
        """
        return f"Daily Forecast Manager\nGenerated at: {self.generated_time}\nNumber of forecasts: {len(self.forecasts)}"