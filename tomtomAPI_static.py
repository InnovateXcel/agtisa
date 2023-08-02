import requests

# Replace <YOUR_API_KEY> with your actual TomTom API key
api_key = "93v0A4i8R298ggGHjsAx488ZkH0sZc07"

# Define the bounding box coordinates of the desired area
bbox = "12.9569,80.1276,13.0910,80.2086"

# Construct the API request URL
base_url = "https://api.tomtom.com/traffic/flowSegmentData/1/flow/absolute"
request_url = f"{base_url}/{bbox}.json?unit=KMPH&key={api_key}"

# Send the API request
response = requests.get(request_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the API response
    data = response.json()

    # Extract the static speed limit information from the response
    speed_limit = data['flowSegmentData']['currentSpeed']

    # Display the static speed limit
    print(f"The static speed limit in the given area is {speed_limit} km/h.")
else:
    # Handle API request errors
    print("Error: Failed to retrieve the static speed limit.")
