import requests
from discord.ext import tasks
import discord
import psutil
import platform
import time

class Utils:
    def __init__(self, bot, news_api_key, weather_api_key, channel_id):
        self.bot = bot
        self.news_api_key = news_api_key
        self.weather_api_key = weather_api_key
        self.channel_id = channel_id
        self.start_time = time.time()


    def get_coordinates(self, city, country=None):
        """Fetches latitude and longitude of a city (with optional country) using OpenWeatherMap Geocoding API"""
        if country:
            query = f"{city},{country}"
        else:
            query = city

        url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=1&appid={self.weather_api_key}"
        response = requests.get(url)

        if response.status_code == 401:
            return None, None, "Invalid API Key! Please check your OpenWeatherMap API key."

        response = response.json()
        if not response or not isinstance(response, list) or len(response) == 0:
            return None, None, "City not found! Please check the name and try again."

        lat = response[0].get("lat")
        lon = response[0].get("lon")
        return lat, lon, None

    def fetch_weather(self, city):
        """Fetches weather information using a city name"""
        lat, lon, error = self.get_coordinates(city)
        if error:
            return error

        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.weather_api_key}&lang=en&units=metric"
        response = requests.get(url).json()

        if response.get("cod") != 200:
            return "Location not found! Please check the coordinates and try again."

        name = response.get("name", "Unknown location")
        temp = response["main"].get("temp", "N/A")
        description = response["weather"][0].get("description", "No description")
        humidity = response["main"].get("humidity", "N/A")
        wind = response["wind"].get("speed", "N/A")

        # Definindo a frase especial para diferentes faixas de temperatura
        if temp <= 0:
            special_phrase = "🥶 It's freezing! Stay warm!"
        elif 0 < temp <= 10:
            special_phrase = "🧥 It's chilly outside. Better grab a jacket!"
        elif 10 < temp <= 20:
            special_phrase = "🌤 A bit cool today. A light sweater should be fine."
        elif 20 < temp <= 30:
            special_phrase = "🌞 It's quite warm! A perfect day for outdoor activities."
        else:
            special_phrase = "🔥 It's hot! Stay hydrated and cool."

        return (f"🌤 **Weather in {name}**\n"
                f"🌡 Temperature: {temp}°C\n"
                f"💧 Humidity: {humidity}%\n"
                f"💨 Wind: {wind} m/s\n"
                f"{special_phrase}")

    @tasks.loop(hours=3) # In Tests
    async def post_weather(self):
        """Automatically posts weather updates every 3 hours"""
        city = "Lisboa"
        weather = self.fetch_weather(city)

        channel = self.bot.get_channel(self.channel_id)
        if channel:
            await channel.send(weather)

    async def get_status(self, ctx):
        """Returns system status including CPU, RAM usage, and uptime"""

        # CPU and RAM usage
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent

        # Uptime
        uptime_seconds = int(time.time() - self.start_time)
        uptime = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))

        # OS Info
        system_info = f"{platform.system()} {platform.release()}"

        # Create Embed Message
        embed = discord.Embed(
            title="📊 System Status",
            color=discord.Color.blue()
        )
        embed.add_field(name="🖥️ OS", value=system_info, inline=True)
        embed.add_field(name="💾 CPU Usage", value=f"{cpu_usage}%", inline=True)
        embed.add_field(name="📈 RAM Usage", value=f"{ram_usage}%", inline=True)
        embed.add_field(name="⏳ Uptime", value=uptime, inline=False)

        await ctx.send(embed=embed)
