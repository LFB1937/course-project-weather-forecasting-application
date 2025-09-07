import csv
from hourly_forecast_class import HourlyForecast

# Class to manage hourly forecast data, including loading from CSV and storing forecasts
class HourlyForecastManager:
    def __init__(self, csv_filename, forecast_generated_time):
        """
        Initialize the HourlyForecastManager with a CSV filename and forecast generation time.

        Args:
            csv_filename (str): Path to the CSV file containing hourly forecast data.
            forecast_generated_time (str): Timestamp when the forecast was generated.
        """
        self.csv_filename = csv_filename
        self.forecast_generated_time = forecast_generated_time
        self.forecasts = []  # List to store HourlyForecast objects

    def load_forecasts(self):
        """
        Load hourly forecast data from the CSV file into HourlyForecast objects.

        This method reads the CSV file, validates its structure, and creates HourlyForecast objects
        for each row. It adapts to different timestamp field names ('timestamp' or 'start_time'),
        handles missing files, and skips invalid rows, logging errors to the console.

        Returns:
            bool: True if forecasts were loaded successfully, False otherwise.
        """
        try:
            with open(self.csv_filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                # Determine the timestamp field name ('timestamp' or 'start_time')
                timestamp_key = 'timestamp' if 'timestamp' in reader.fieldnames else 'start_time'
                if timestamp_key not in reader.fieldnames:
                    print(f"Error: No valid timestamp field ('timestamp' or 'start_time') in {self.csv_filename}")
                    return False

                # Process each row in the CSV
                for row in reader:
                    try:
                        # Create an HourlyForecast object using the dynamic timestamp key
                        forecast = HourlyForecast.from_dict(row, timestamp_key)
                        self.forecasts.append(forecast)
                    except KeyError as e:
                        print(f"Skipping invalid row due to missing key {e} in {row}")
                    except ValueError as e:
                        print(f"Skipping invalid row due to value error {e} in {row}")
            return True  # Successfully loaded forecasts
        except FileNotFoundError:
            print(f"Error: CSV file {self.csv_filename} not found.")
            return False  # Failed due to missing file
        except Exception as e:
            print(f"Error loading hourly forecasts: {e}")
            return False  # Failed due to unexpected error

    def get_forecasts(self):
        """
        Retrieve the list of loaded hourly forecasts.

        Returns:
            list: List of HourlyForecast objects.
        """
        return self.forecasts