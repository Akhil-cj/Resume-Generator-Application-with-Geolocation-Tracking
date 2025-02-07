import requests
from flask import request, current_app

def get_geolocation():
    try:
        # Get the IPStack API key from the config
        api_key = current_app.config['IPSTACK_API_KEY']
        
        # Get the user's IP address
        user_ip = request.remote_addr  # Use request.remote_addr for user's IP
        
        # Fallback for localhost development
        if user_ip == "127.0.0.1":
            user_ip = "8.8.8.8"  # Example: Use Google public DNS IP for testing
        
        # Build the API URL
        url = f"http://api.ipstack.com/{user_ip}?access_key={api_key}"
        
        # Make the API request
        response = requests.get(url)
        data = response.json()
        
        # Extract relevant geolocation details
        location = {
            "ip": data.get("ip"),
            "city": data.get("city"),
            "region": data.get("region_name"),
            "country": data.get("country_name"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude")
        }
        return location
    except Exception as e:
        return {"error": str(e)}
