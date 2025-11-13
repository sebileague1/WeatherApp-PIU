# în core/weather_service.py
import requests
from datetime import datetime

def get_weather_forecast():
    """
    Preia prognoza meteo de la Open-Meteo pentru Iași.
    Returnează o listă de dicționare cu datele procesate sau None dacă e o eroare.
    """
    # Coordonatele pentru Iași
    lat = "47.16"
    lon = "27.60"
    
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,precipitation_probability,windspeed_10m"
        f"&windspeed_unit=kmh&timezone=Europe/Bucharest"
    )
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        
        hourly_data = data['hourly']
        processed_forecasts = []
        
        for i in range(len(hourly_data['time'])):
            processed_forecasts.append({
                'time': datetime.fromisoformat(hourly_data['time'][i]),
                'temp': hourly_data['temperature_2m'][i],
                'precip_prob': hourly_data['precipitation_probability'][i],
                'wind': hourly_data['windspeed_10m'][i]
            })
            
        print(f"Am preluat {len(processed_forecasts)} prognoze orare.")
        return processed_forecasts
        
    except requests.RequestException as e:
        print(f"Eroare la apelul API: {e}")
        return None