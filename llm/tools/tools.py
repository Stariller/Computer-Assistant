import requests
from datetime import datetime
import json
from typing import Optional, List
import subprocess
import os

if os.getenv("WEATHER_API_KEY") is None:
    print("""
        WARNING: 
        WEATHER_API_KEY environment variable is not set.
        Set WEATHER_API_KEY in your environment variables.
        Some tools will fail without setting the environment variable.
        Go to https://www.weatherapi.com/ to get a free API key.
    """)
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY") # www.weatherapi.com

def get_ip():
    """
    Returns the public IP address of the device.
    
    Returns:
        str: The public IP address of the device.
    """
    return requests.get("https://api.ipify.org").text

def get_current_weather(city: str):
    """
    Returns the current weather for the specified city.
    
    Args:
        city (str): The city to get the weather for.
    
    Returns:
        dict: The weather data.
    """
    data = requests.get(f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}").json()
    print(json.dumps(data, indent=4))
    return data

def get_forecast(city: str):
    """
    Returns the forecast for the specified city.
    
    Args:
        city (str): The city to get the forecast for.
    
    Returns:
        dict: The forecast data.
    """
    data = requests.get(f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}").json()
    print(json.dumps(data, indent=4))
    return data

def get_city():
    """
    Returns the city of the device.
        
    Returns:
        str: The city of the device.
    """
    data = requests.get(f"http://ip-api.com/json/{get_ip()}").json()
    print(data)
    return data["city"]

def get_date():
    """
    Returns the current date in ISO 8601 format.

    Returns:
        str: A string representing the current date. YYYY-MM-DD
    """
    print(datetime.now().strftime("%Y-%m-%d"))
    return datetime.now().strftime("%Y-%m-%d")

def get_time(formatting: str = "") -> str:
    """
    Returns the current time of day.
    
    The raw return value is a string in 24-hour HH:MM:SS format (e.g. 14:17:16).
    Assistant must re-format this for the user by dropping seconds *or* converting
    to 12-hour with AM/PM depending on the user's locale / wording, never exposing
    the seconds directly.
    
    Returns:
        str: Current time as HH:MM:SS
    """
    now = datetime.now()
    # Supported values (case-insensitive): "24h", "12h", "no_seconds" / "drop_seconds"
    if not formatting:
        out = now.strftime("%H:%M:%S")
    else:
        fmt = formatting.lower()
        if fmt in ("12h", "12-hour", "12"):
            out = now.strftime("%I:%M %p").lstrip("0")
        elif fmt in ("24h", "24-hour", "24"):
            out = now.strftime("%H:%M:%S")
        elif fmt in ("no_seconds", "drop_seconds"):
            out = now.strftime("%H:%M")
        else:
            out = now.strftime("%H:%M:%S")
    print(out)
    return out

def enter_cli_command(commands: List[str]) -> str:
    """Run shell commands and return their combined output.

    Args:
        commands (List[str]): Each string is executed verbatim in the host shell.

    Returns:
        str: The concatenated stdout (or stderr if no stdout) from all commands, separated
        by newlines. Any execution error is captured and returned in place of output.
    """
    outputs: List[str] = []
    for cmd in commands:
        print(f"Executing command: {cmd}")
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                text=True,
                capture_output=True,
                check=False,
            )
            out = result.stdout.strip() or result.stderr.strip()
            outputs.append(out)
        except Exception as exc:
            outputs.append(f"Error executing '{cmd}': {exc}")
    return "\n".join(outputs)
