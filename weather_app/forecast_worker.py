import csv
import requests
from datetime import datetime
from geopy.location import Location
from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication

"""
A worker that fetches weather data in the background.
"""
class ForecastWorker(QThread):
    """
    Signal to communicate results back to the main thread.
    Emits: success (bool), message (str), daily_time (str), hourly_time (str)
    """
    worker_finished = pyqtSignal(bool, str, str, str)

    def __init__(self, location: Location) -> None:
        super().__init__()
        self.location = location

    def run(self) -> None:
        try:
            latitude = round(self.location.latitude, 4)
            longitude = round(self.location.longitude, 4)
            location_url = f"https://api.weather.gov/points/{latitude},{longitude}"
            location_data = self._get_api_data(location_url)

            daily_forecast_url = location_data["properties"]["forecast"]
            daily_forecast_data = self._get_api_data(daily_forecast_url)
            daily_forecast_generated_time = (
                daily_forecast_data["properties"].get("generatedAt", datetime.now().isoformat())
            )
            self._save_daily_forecast(daily_forecast_data)

            hourly_forecast_url = location_data["properties"]["forecastHourly"]
            hourly_forecast_data = self._get_api_data(hourly_forecast_url)
            hourly_forecast_generated_time = (
                hourly_forecast_data["properties"].get("generatedAt", datetime.now().isoformat())
            )
            self._save_hourly_forecast(hourly_forecast_data)

            self.worker_finished.emit(
                True, "Forecast CSV files written", daily_forecast_generated_time, hourly_forecast_generated_time
            )
        except requests.exceptions.RequestException as e:
            self.worker_finished.emit(False, f"Forecast fetch failed: {str(e)}", "", "")
        except (KeyError, TypeError) as e:
            self.worker_finished.emit(False, f"Invalid API response format: {str(e)}", "", "")
        except (IOError, OSError) as e:
            self.worker_finished.emit(False, f"File save failed: {str(e)}", "", "")

    def _get_api_data(self, url: str) -> dict:
        """
        Fetch JSON data from the API with no-cache headers.
        """
        response = requests.get(url, headers={"Cache-Control": "no-cache", "Pragma": "no-cache"}, timeout=10)
        response.raise_for_status()
        return response.json()

    def _save_daily_forecast(self, daily_forecast_data: dict) -> None:
        """Save daily forecast data to CSV"""
        daily_periods = daily_forecast_data["properties"]["periods"]

        # Open a CSV file named 'daily_forecast_data.csv' in write mode
        with open('daily_forecast_data.csv', 'w', newline='') as daily_file:
            # Create a list of headers in this exact order
            headers = [
                "forecast_period", "name", "start_time", "end_time", "isDaytime",
                "temperature", "temperature_unit", "temperature_trend",
                "precipitation_probability_unit", "precipitation_probability_value",
                "wind_speed", "wind_direction", "weather_icon_url",
                "short_forecast", "detailed_forecast"
            ]

            # Create a csv.DictWriter object using the file and fieldnames
            writer = csv.DictWriter(daily_file, fieldnames=headers)

            # Write the headers to the file
            writer.writeheader()

            # Loop through each item in daily_periods and write it to the CSV
            for period in daily_periods:
                writer.writerow({
                    "forecast_period": period.get("number", ""),
                    "name": period.get("name", ""),
                    "start_time": period.get("startTime", ""),
                    "end_time": period.get("endTime", ""),
                    "isDaytime": period.get("isDaytime", ""),
                    "temperature": period.get("temperature", ""),
                    "temperature_unit": period.get("temperatureUnit", ""),
                    "temperature_trend": period.get("temperatureTrend", ""),
                    "precipitation_probability_unit": period.get("probabilityOfPrecipitation", {}).get("unitCode", ""),
                    "precipitation_probability_value": period.get("probabilityOfPrecipitation", {}).get("value", ""),
                    "wind_speed": period.get("windSpeed", ""),
                    "wind_direction": period.get("windDirection", ""),
                    "weather_icon_url": period.get("icon", ""),
                    "short_forecast": period.get("shortForecast", ""),
                    "detailed_forecast": period.get("detailedForecast", "")
                })

    def _save_hourly_forecast(self, hourly_forecast_data: dict) -> None:
        """Save hourly forecast data to CSV"""
        hourly_periods = hourly_forecast_data["properties"]["periods"]

        # Open a CSV file named 'hourly_forecast_data.csv' in write mode
        with open('hourly_forecast_data.csv', 'w', newline='') as hourly_file:
            # Create a list of headers in this exact order
            headers = [
                "forecast_period", "start_time", "temperature", "temperature_unit",
                "precipitation_probability_unit", "precipitation_probability_value",
                "dewpoint_unit", "dewpoint_value", "relative_humidity_unit", "relative_humidity_value",
                "wind_speed", "wind_direction", "weather_icon_url", "short_forecast"
            ]

            # Create a csv.DictWriter object using the file and fieldnames
            writer = csv.DictWriter(hourly_file, fieldnames=headers)

            # Write the headers to the file
            writer.writeheader()

            # Loop through each item in hourly_periods and write it to the CSV
            for period in hourly_periods:
                writer.writerow({
                    "forecast_period": period.get("number", ""),
                    "start_time": period.get("startTime", ""),
                    "temperature": period.get("temperature", ""),
                    "temperature_unit": period.get("temperatureUnit", ""),
                    "precipitation_probability_unit": period.get("probabilityOfPrecipitation", {}).get("unitCode", ""),
                    "precipitation_probability_value": period.get("probabilityOfPrecipitation", {}).get("value", ""),
                    "dewpoint_unit": period.get("dewpoint", {}).get("unitCode", ""),
                    "dewpoint_value": period.get("dewpoint", {}).get("value", ""),
                    "relative_humidity_unit": period.get("relativeHumidity", {}).get("unitCode", ""),
                    "relative_humidity_value": period.get("relativeHumidity", {}).get("value", ""),
                    "wind_speed": period.get("windSpeed", ""),
                    "wind_direction": period.get("windDirection", ""),
                    "weather_icon_url": period.get("icon", ""),
                    "short_forecast": period.get("shortForecast", "")
                })

def main():
    app = QCoreApplication([])
    location = Location("New York", (40.71282, -74.00603), {})
    worker = ForecastWorker(location)
    worker.worker_finished.connect(
        lambda success, message, daily_time, hourly_time: (
            print("Success:", success),
            print("Message:", message),
            print("Daily time:", daily_time),
            print("Hourly time:", hourly_time),
            app.quit()
        )
    )
    worker.start()
    app.exec_()

if __name__ == "__main__":
    main()