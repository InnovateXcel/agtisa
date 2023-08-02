import requests
api_key = "93v0A4i8R298ggGHjsAx488ZkH0sZc07"

coordinates = [
    (13.0418, 80.2341,'T.Nagar'),
    (13.041671, 80.167140,'Porur'),
    (12.9516, 80.1462,'Chromepet'),
    (11.4070,79.6912,'Chidambaram',)
]

latitude = 13.0418
longitude = 80.2341

base_url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
print("The real time speed limits (with traffic flow) are as follows")

for latitude,longitude,area in coordinates:
    request_url = f"{base_url}?point={latitude},{longitude}&unit=KMPH&key={api_key}"
    response = requests.get(request_url)

    if response.status_code == 200:
        data = response.json()
        max_speed = data['flowSegmentData']['currentSpeed']
        print(f"The maximum speed limit in the {area} area is {max_speed} km/h.")
    else:
        print("Error: Failed to retrieve the maximum speed limit.")
