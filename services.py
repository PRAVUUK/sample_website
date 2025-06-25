import requests
import logging
from datetime import datetime, timezone
from django.conf import settings
from django.utils import timezone as django_timezone
from .models import City, WeatherData, WeatherAlert

logger = logging.getLogger(__name__)


class OpenWeatherMapService:
    """Service class to handle OpenWeatherMap API calls"""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    GEOCODING_URL = "https://api.openweathermap.org/geo/1.0"
    
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        if not self.api_key:
            logger.warning("OpenWeatherMap API key not configured")
    
    def get_current_weather(self, lat, lon):
        """
        Get current weather data for given coordinates
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            
        Returns:
            dict: Weather data or None if error
        """
        if not self.api_key:
            logger.error("OpenWeatherMap API key not configured")
            return None
        
        url = f"{self.BASE_URL}/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'  # Use metric units (Celsius)
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data: {e}")
            return None
    
    def get_weather_by_city_name(self, city_name, country_code=None):
        """
        Get current weather data by city name
        
        Args:
            city_name (str): Name of the city
            country_code (str): Optional country code (e.g., 'US', 'GB')
            
        Returns:
            dict: Weather data or None if error
        """
        if not self.api_key:
            logger.error("OpenWeatherMap API key not configured")
            return None
        
        url = f"{self.BASE_URL}/weather"
        params = {
            'q': f"{city_name},{country_code}" if country_code else city_name,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data for {city_name}: {e}")
            return None
    
    def geocode_city(self, city_name, country_code=None, limit=5):
        """
        Get coordinates for a city name using OpenWeatherMap Geocoding API
        
        Args:
            city_name (str): Name of the city
            country_code (str): Optional country code
            limit (int): Number of results to return
            
        Returns:
            list: List of location data or empty list if error
        """
        if not self.api_key:
            logger.error("OpenWeatherMap API key not configured")
            return []
        
        url = f"{self.GEOCODING_URL}/direct"
        params = {
            'q': f"{city_name},{country_code}" if country_code else city_name,
            'limit': limit,
            'appid': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error geocoding {city_name}: {e}")
            return []
    
    def reverse_geocode(self, lat, lon, limit=5):
        """
        Get city name from coordinates
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            limit (int): Number of results to return
            
        Returns:
            list: List of location data or empty list if error
        """
        if not self.api_key:
            logger.error("OpenWeatherMap API key not configured")
            return []
        
        url = f"{self.GEOCODING_URL}/reverse"
        params = {
            'lat': lat,
            'lon': lon,
            'limit': limit,
            'appid': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error reverse geocoding {lat}, {lon}: {e}")
            return []


class WeatherDataService:
    """Service class to handle weather data operations"""
    
    def __init__(self):
        self.api_service = OpenWeatherMapService()
    
    def create_or_update_city(self, name, country, country_code, lat, lon, openweather_id=None):
        """
        Create or update a city record
        
        Args:
            name (str): City name
            country (str): Country name
            country_code (str): Country code
            lat (float): Latitude
            lon (float): Longitude
            openweather_id (int): OpenWeatherMap city ID
            
        Returns:
            City: City instance
        """
        city, created = City.objects.get_or_create(
            latitude=lat,
            longitude=lon,
            defaults={
                'name': name,
                'country': country,
                'country_code': country_code,
                'openweather_id': openweather_id
            }
        )
        
        if not created:
            # Update existing city if needed
            city.name = name
            city.country = country
            city.country_code = country_code
            if openweather_id:
                city.openweather_id = openweather_id
            city.save()
        
        return city
    
    def save_weather_data(self, city, weather_data):
        """
        Save weather data to database
        
        Args:
            city (City): City instance
            weather_data (dict): Weather data from API
            
        Returns:
            WeatherData: Created weather data instance
        """
        # Convert timestamp
        data_timestamp = datetime.fromtimestamp(
            weather_data['dt'], 
            tz=timezone.utc
        )
        
        # Convert sunrise/sunset if available
        sunrise = None
        sunset = None
        if 'sys' in weather_data:
            if 'sunrise' in weather_data['sys']:
                sunrise = datetime.fromtimestamp(
                    weather_data['sys']['sunrise'], 
                    tz=timezone.utc
                )
            if 'sunset' in weather_data['sys']:
                sunset = datetime.fromtimestamp(
                    weather_data['sys']['sunset'], 
                    tz=timezone.utc
                )
        
        # Extract weather condition
        weather_info = weather_data['weather'][0]
        
        # Extract main weather data
        main_data = weather_data['main']
        
        # Extract wind data
        wind_data = weather_data.get('wind', {})
        
        # Extract cloud data
        clouds_data = weather_data.get('clouds', {})
        
        # Extract precipitation data
        rain_data = weather_data.get('rain', {})
        snow_data = weather_data.get('snow', {})
        
        # Create or update weather data
        weather_obj, created = WeatherData.objects.update_or_create(
            city=city,
            data_timestamp=data_timestamp,
            defaults={
                'temperature': main_data['temp'] + 273.15,  # Convert to Kelvin for storage
                'feels_like': main_data['feels_like'] + 273.15,
                'temp_min': main_data['temp_min'] + 273.15,
                'temp_max': main_data['temp_max'] + 273.15,
                'pressure': main_data['pressure'],
                'humidity': main_data['humidity'],
                'sea_level': main_data.get('sea_level'),
                'ground_level': main_data.get('grnd_level'),
                'weather_main': weather_info['main'],
                'weather_description': weather_info['description'],
                'weather_icon': weather_info['icon'],
                'weather_id': weather_info['id'],
                'wind_speed': wind_data.get('speed'),
                'wind_deg': wind_data.get('deg'),
                'wind_gust': wind_data.get('gust'),
                'cloudiness': clouds_data.get('all'),
                'visibility': weather_data.get('visibility'),
                'rain_1h': rain_data.get('1h'),
                'snow_1h': snow_data.get('1h'),
                'sunrise': sunrise,
                'sunset': sunset,
            }
        )
        
        return weather_obj
    
    def fetch_and_save_weather(self, city):
        """
        Fetch weather data from API and save to database
        
        Args:
            city (City): City instance
            
        Returns:
            WeatherData: Weather data instance or None if error
        """
        weather_data = self.api_service.get_current_weather(
            city.latitude, 
            city.longitude
        )
        
        if weather_data:
            return self.save_weather_data(city, weather_data)
        
        return None
    
    def search_and_add_city(self, city_name, country_code=None):
        """
        Search for a city and add it to the database
        
        Args:
            city_name (str): City name to search
            country_code (str): Optional country code
            
        Returns:
            tuple: (City instance or None, error message or None)
        """
        # First try to geocode the city
        locations = self.api_service.geocode_city(city_name, country_code)
        
        if not locations:
            return None, f"City '{city_name}' not found"
        
        # Use the first result
        location = locations[0]
        
        # Create city
        city = self.create_or_update_city(
            name=location['name'],
            country=location['country'],
            country_code=location.get('country', ''),
            lat=location['lat'],
            lon=location['lon']
        )
        
        # Fetch and save initial weather data
        weather_data = self.fetch_and_save_weather(city)
        
        if weather_data:
            return city, None
        else:
            return city, "City added but weather data could not be fetched"
    
    def get_latest_weather(self, city):
        """
        Get the latest weather data for a city
        
        Args:
            city (City): City instance
            
        Returns:
            WeatherData: Latest weather data or None
        """
        return city.weather_data.first()
    
    def update_weather_for_city(self, city):
        """
        Update weather data for a specific city
        
        Args:
            city (City): City instance
            
        Returns:
            WeatherData: Updated weather data or None
        """
        return self.fetch_and_save_weather(city)

