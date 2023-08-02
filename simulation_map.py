import pygame
import requests
import folium
from geopy.geocoders import Nominatim
import math

# API and location information
api_key = "93v0A4i8R298ggGHjsAx488ZkH0sZc07"
latitude = 13.041671
longitude = 80.167140
location_name = 'Porur'

# TomTom API URL
base_url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
request_url = f"{base_url}?point={latitude},{longitude}&unit=KMPH&key={api_key}"

# Make the API request to get the maximum speed limit
try:
    response = requests.get(request_url)
    if response.status_code == 200:
        data = response.json()
        max_speed = data['flowSegmentData']['currentSpeed']
        print(f"The maximum speed limit in the Porur area is {max_speed} km/h.")
    else:
        print("Error: Failed to retrieve the maximum speed limit.")
except:
    print("Network error")

# Pygame initialization
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AGTISA car simulation window")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Geolocator and Map
geolocator = Nominatim(user_agent="car_simulation")
map_osm = folium.Map(location=[latitude, longitude], zoom_start=15)

# Load images
car_image = pygame.image.load("car.png")
location_icon_image = pygame.image.load("location.png")
warning_icon_image = pygame.image.load("warning.png")
pedals_icon_image = pygame.image.load("pedals.png")
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Scale images
scaled_location_icon_image = pygame.transform.scale(location_icon_image, (30, 30))
scaled_warning_icon_image = pygame.transform.scale(warning_icon_image, (30, 30))
scaled_pedals_icon_image = pygame.transform.scale(pedals_icon_image, (100, 100))

# Font
font = pygame.font.Font(None, 24)

# CarGame class
class CarGame:
    def __init__(self):
        self.speed = 0.0
        self.acceleration = 0.0
        self.steering_angle = 0.0
        self.drag = 0.99  # Deceleration factor (1 means no deceleration)
        self.acceleration_factor = 0.48  # Acceleration factor
        self.deceleration_factor = 0.18  # Deceleration factor
        self.max_speed = 70.0
        self.min_speed = 0.0
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.background_x = 0

    def update_speed(self, acceleration):
        self.acceleration = acceleration

        if self.acceleration > 0:
            self.speed += self.acceleration * self.acceleration_factor
        else:
            self.speed += self.acceleration * self.deceleration_factor

        if self.speed <= 20:
            self.max_speed = 30
        elif self.speed <= 40:
            self.max_speed = 60
        elif self.speed <= 60:
            self.max_speed = 80
        else:
            self.max_speed = 120

        if self.acceleration == 0.0:
            self.speed *= self.drag

        self.speed = max(self.min_speed, min(self.speed, self.max_speed))

    def update_position(self):
        self.x += self.speed * math.cos(math.radians(self.steering_angle))
        self.y += self.speed * math.sin(math.radians(self.steering_angle))

        if self.x < 0:
            self.x = screen_width
        elif self.x > screen_width:
            self.x = 0
        if self.y < 0:
            self.y = screen_height
        elif self.y > screen_height:
            self.y = 0

    def update_steering_angle(self, angle):
        self.steering_angle = angle

    def draw_car(self):
        car_x = screen_width // 2 - car_image.get_width() // 2
        car_y = screen_height // 2 + 130 - car_image.get_height() // 2
        screen.blit(car_image, (car_x, car_y))

    def draw_location_icon(self):
        location_icon_x = screen_width - scaled_location_icon_image.get_width() - 20
        location_icon_y = 5
        screen.blit(scaled_location_icon_image, (location_icon_x, location_icon_y))

    def draw_warning_icon(self):
        warning_icon_x = screen_width - scaled_warning_icon_image.get_width() - 70
        warning_icon_y = 55
        screen.blit(scaled_warning_icon_image, (warning_icon_x, warning_icon_y))

    def draw_pedals_icon(self):
        pedals_icon_x = screen_width - scaled_pedals_icon_image.get_width() - 20
        pedals_icon_y = 490
        screen.blit(scaled_pedals_icon_image, (pedals_icon_x, pedals_icon_y))

    def draw_background(self):
        screen.blit(background_image, (self.background_x % screen_width - screen_width, 0))
        screen.blit(background_image, (self.background_x % screen_width, 0))

    def draw_controls(self):
        if self.speed < self.max_speed:
            speed_clr = (0, 128, 0)
        else:
            speed_clr = (255, 0, 0)
        acceleration_text = f"Acceleration: {self.acceleration:.2f}"
        speedtxt_text = "Speed: "
        speedval_text = f"{self.speed:.2f} km/hr"
        acceleration_surface = font.render(acceleration_text, True, black)
        speedtxt_surface = font.render(speedtxt_text, True, black)
        speedval_surface = font.render(speedval_text, True, speed_clr)

        screen.blit(acceleration_surface, (20, 20))
        screen.blit(speedtxt_surface, (20, 50))
        screen.blit(speedval_surface, (78, 50))

        # Location name
        alert_text = f"{self.get_address()}"
        alert_surface = font.render(alert_text, True, (0, 0, 255))
        screen.blit(alert_surface, (745, 38))

        alert_text = f"{self.max_speed} km/hr"
        alert_surface = font.render(alert_text, True, (200, 106, 0))
        screen.blit(alert_surface, (728, 63))

        alert_text = "*Demonstration"
        alert_surface = font.render(alert_text, True, white)
        screen.blit(alert_surface, (14, 570))

        if self.speed > self.max_speed:
            alert_text = "You are crossing the speed limit"
            alert_surface = font.render(alert_text, True, (255, 0, 0))
            screen.blit(alert_surface, (20, 80))

    def get_speed(self):
        return self.speed

    def get_address(self):
        location = geolocator.reverse(f"{latitude}, {longitude}")
        if location is not None:
            address = location.address
            return address
        else:
            return "Address not found"

# Create an instance of CarGame
car_game = CarGame()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle keyboard events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                car_game.update_speed(1.0)
            elif event.key == pygame.K_DOWN:
                car_game.update_speed(-1.0)
            elif event.key == pygame.K_LEFT:
                car_game.update_steering_angle(-30.0)
            elif event.key == pygame.K_RIGHT:
                car_game.update_steering_angle(30.0)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                car_game.update_speed(0.0)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                car_game.update_steering_angle(0.0)

    # Update car position and speed
    car_game.update_position()

    # Clear the screen
    screen.fill(white)

    # Draw game elements
    car_game.draw_background()
    car_game.draw_car()
    car_game.draw_location_icon()
    car_game.draw_warning_icon()
    car_game.draw_pedals_icon()
    car_game.draw_controls()

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()