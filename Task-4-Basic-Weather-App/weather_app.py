import os
import requests
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherApp:
    def __init__(self, root):
        self.root = root

        # Window settings
        self.root.title("Weather App | Oasis Infobyte")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)
        self.root.configure(bg="#F4F7FB")

        self.create_header()
        self.create_search_section()
        self.create_weather_card()

    def create_header(self):
        """Create application header."""

        header = tk.Frame(
            self.root,
            bg="#1F4E79",
            height=150
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="🌦️ Weather App",
            font=("Segoe UI", 30, "bold"),
            bg="#1F4E79",
            fg="white"
        )
        title.pack(pady=(28, 5))

        subtitle = tk.Label(
            header,
            text="Real-Time Weather Information",
            font=("Segoe UI", 13),
            bg="#1F4E79",
            fg="#DCEBFA"
        )
        subtitle.pack()

    def create_search_section(self):
        """Create location search section."""

        search_frame = tk.Frame(
            self.root,
            bg="#F4F7FB"
        )
        search_frame.pack(pady=35)

        label = tk.Label(
            search_frame,
            text="Enter City or ZIP Code",
            font=("Segoe UI", 13, "bold"),
            bg="#F4F7FB",
            fg="#263238"
        )
        label.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(0, 10)
        )

        self.location_entry = tk.Entry(
            search_frame,
            width=40,
            font=("Segoe UI", 14),
            relief="solid",
            bd=1
        )
        self.location_entry.grid(
            row=1,
            column=0,
            padx=(0, 12),
            ipady=11
        )

        self.location_entry.bind(
            "<Return>",
            lambda event: self.get_weather()
        )

        search_button = tk.Button(
            search_frame,
            text="Search",
            command=self.get_weather,
            font=("Segoe UI", 12, "bold"),
            bg="#1F4E79",
            fg="white",
            activebackground="#163A5C",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=11
        )
        search_button.grid(
            row=1,
            column=1
        )

    def create_weather_card(self):
        """Create weather information card."""

        self.weather_card = tk.Frame(
            self.root,
            bg="white",
            width=850,
            height=350,
            relief="solid",
            bd=1
        )
        self.weather_card.pack(
            padx=70,
            pady=5
        )
        self.weather_card.pack_propagate(False)

        self.location_label = tk.Label(
            self.weather_card,
            text="Search for a location",
            font=("Segoe UI", 24, "bold"),
            bg="white",
            fg="#1F4E79"
        )
        self.location_label.pack(
            pady=(30, 8)
        )

        self.condition_label = tk.Label(
            self.weather_card,
            text="Current weather will appear here",
            font=("Segoe UI", 13),
            bg="white",
            fg="#607D8B"
        )
        self.condition_label.pack(
            pady=(0, 18)
        )

        self.temperature_label = tk.Label(
            self.weather_card,
            text="-- °C",
            font=("Segoe UI", 36, "bold"),
            bg="white",
            fg="#263238"
        )
        self.temperature_label.pack()

        self.details_frame = tk.Frame(
            self.weather_card,
            bg="white"
        )
        self.details_frame.pack(
            pady=25
        )

        self.feels_label = tk.Label(
            self.details_frame,
            text="Feels Like\n-- °C",
            font=("Segoe UI", 11),
            bg="white",
            fg="#455A64",
            width=20
        )
        self.feels_label.grid(
            row=0,
            column=0,
            padx=15
        )

        self.humidity_label = tk.Label(
            self.details_frame,
            text="Humidity\n-- %",
            font=("Segoe UI", 11),
            bg="white",
            fg="#455A64",
            width=20
        )
        self.humidity_label.grid(
            row=0,
            column=1,
            padx=15
        )

        self.wind_label = tk.Label(
            self.details_frame,
            text="Wind Speed\n-- m/s",
            font=("Segoe UI", 11),
            bg="white",
            fg="#455A64",
            width=20
        )
        self.wind_label.grid(
            row=0,
            column=2,
            padx=15
        )

    def get_weather(self):
        """Fetch weather information."""

        location = self.location_entry.get().strip()

        # Empty input validation
        if not location:
            messagebox.showwarning(
                "Missing Location",
                "Please enter a city name or ZIP code."
            )
            return

        # API key validation
        if not API_KEY:
            messagebox.showerror(
                "API Key Error",
                "OpenWeatherMap API key is missing.\n\n"
                "Please check your .env file."
            )
            return

        # Detect ZIP code
        if location.replace("-", "").isdigit():
            params = {
                "zip": f"{location},IN",
                "appid": API_KEY,
                "units": "metric"
            }
        else:
            params = {
                "q": location,
                "appid": API_KEY,
                "units": "metric"
            }

        try:
            response = requests.get(
                BASE_URL,
                params=params,
                timeout=10
            )

            # Invalid API key
            if response.status_code == 401:
                messagebox.showerror(
                    "Invalid API Key",
                    "The OpenWeatherMap API key is invalid.\n\n"
                    "Please check your API key."
                )
                return

            # Location not found
            if response.status_code == 404:
                messagebox.showerror(
                    "Location Not Found",
                    f"Weather information was not found for:\n\n"
                    f"{location}\n\n"
                    "Please check the city name or ZIP code."
                )
                return

            # Other API errors
            if response.status_code != 200:
                messagebox.showerror(
                    "Weather Service Error",
                    f"Unable to fetch weather data.\n\n"
                    f"Status Code: {response.status_code}"
                )
                return

            data = response.json()
            self.display_weather(data)

        except requests.exceptions.Timeout:
            messagebox.showerror(
                "Connection Timeout",
                "The weather service took too long to respond.\n\n"
                "Please check your internet connection and try again."
            )

        except requests.exceptions.ConnectionError:
            messagebox.showerror(
                "Connection Error",
                "Unable to connect to the weather service.\n\n"
                "Please check your internet connection."
            )

        except requests.exceptions.RequestException:
            messagebox.showerror(
                "Network Error",
                "A network error occurred while fetching weather data."
            )

        except ValueError:
            messagebox.showerror(
                "Data Error",
                "Unable to process the weather data."
            )

        except KeyError:
            messagebox.showerror(
                "Data Error",
                "Unexpected weather data was received."
            )

    def display_weather(self, data):
        """Display weather information."""

        city = data["name"]
        country = data["sys"]["country"]

        temperature_c = data["main"]["temp"]
        temperature_f = (temperature_c * 9 / 5) + 32

        feels_like_c = data["main"]["feels_like"]

        humidity = data["main"]["humidity"]

        condition = data["weather"][0]["description"].title()

        wind_speed = data["wind"]["speed"]

        # Update location
        self.location_label.config(
            text=f"📍 {city}, {country}"
        )

        # Update condition
        self.condition_label.config(
            text=condition
        )

        # Update temperature
        self.temperature_label.config(
            text=f"{temperature_c:.1f} °C  |  {temperature_f:.1f} °F"
        )

        # Update details
        self.feels_label.config(
            text=f"Feels Like\n{feels_like_c:.1f} °C"
        )

        self.humidity_label.config(
            text=f"Humidity\n{humidity}%"
        )

        self.wind_label.config(
            text=f"Wind Speed\n{wind_speed} m/s"
        )


def main():
    root = tk.Tk()
    WeatherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()