import requests

# Replace <YOUR_API_KEY> with your actual TomTom API key
api_key = "93v0A4i8R298ggGHjsAx488ZkH0sZc07"

# Define the latitude and longitude coordinates of the desired position
latitude = 13.041671
longitude = 80.167140

# Construct the API request URL
base_url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
request_url = f"{base_url}?point={latitude},{longitude}&unit=KMPH&key={api_key}"

# Send the API request
response = requests.get(request_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the API response
    data = response.json()

    # Extract the maximum speed limit information from the response
    max_speed = data['flowSegmentData']['currentSpeed']

    # Display the maximum speed limit
    print(f"The maximum speed limit in the Porur area is {max_speed} km/h.")
else:
    # Handle API request errors
    print("Error: Failed to retrieve the maximum speed limit.")
