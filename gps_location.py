import geocoder
from geopy.geocoders import Nominatim
import pygame
import requests
from playsound import playsound

def get_location():
    g = geocoder.ip('me')
    return g.latlng

latitude, longitude = get_location()
latitude=latitude
longitude=longitude
print(f"Latitude: {latitude}")
print(f"Longitude: {longitude}")

def get_location_name(latitude, longitude):
    geolocator = Nominatim(user_agent="location_app")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    return location.address

latitude_x = latitude
longitude_y = longitude

location_name = get_location_name(latitude, longitude)
print(location_name)

api_key = "93v0A4i8R298ggGHjsAx488ZkH0sZc07"
base_url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
request_url = f"{base_url}?point={latitude},{longitude}&unit=KMPH&key={api_key}"
try:
    response = requests.get(request_url)
    if response.status_code == 200:
        data = response.json()
        max_speed = data['flowSegmentData']['currentSpeed']
        print(f"The maximum speed limit in the {location_name} area is {max_speed} km/h.")
    else:
        print("Error: Failed to retrieve the maximum speed limit.")
except:
    print("Network error")

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AGTISA car simulation window")

black = (0, 0, 0)
white = (255, 255, 255)

class CarGame:
    def __init__(self):
        self.speed = 0.0
        self.acceleration = 0.0
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

        if self.acceleration == 0.0:
            self.speed *= self.drag

        self.speed = max(self.min_speed, min(self.speed, self.max_speed))

    def update_position(self):
        self.x += self.speed

        if self.x < 0:
            self.x = screen_width
        elif self.x > screen_width:
            self.x = 0
    def draw_car(self):
        car_image = pygame.image.load("car.png")
        car_x = screen_width // 2 - car_image.get_width() // 2
        car_y = screen_height // 2 + 130 - car_image.get_height() // 2
        screen.blit(car_image, (car_x, car_y))
        
    def draw_location_icon(self):
    #Location icon image
        location_icon_image = pygame.image.load("location.png")
        scaled_icon_image = pygame.transform.scale(location_icon_image, (30, 30))
        location_icon_x = screen_width - scaled_icon_image.get_width() - 20
        location_icon_y = 5    
        screen.blit(scaled_icon_image, (location_icon_x, location_icon_y))
    
    def draw_warning_icon(self):
    #Warning icon image
        warning_icon_image = pygame.image.load("warning.png")
        scaled_icon_image = pygame.transform.scale(warning_icon_image, (30, 30))
        warning_icon_x = screen_width - scaled_icon_image.get_width() - 70
        warning_icon_y = 55    
        screen.blit(scaled_icon_image, (warning_icon_x, warning_icon_y))
        
    def draw_pedals_icon(self):
    #Pedals icon image
        pedals_icon_image = pygame.image.load("pedals.png")
        scaled_icon_image = pygame.transform.scale(pedals_icon_image, (100, 100))
        pedals_icon_x = screen_width - scaled_icon_image.get_width() - 20
        pedals_icon_y = 490    
        screen.blit(scaled_icon_image, (pedals_icon_x, pedals_icon_y))


    def draw_background(self):
        #Background image
        background_image = pygame.image.load("background.jpg")
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
        screen.blit(background_image, (self.background_x % screen_width - screen_width, 0))
        screen.blit(background_image, (self.background_x % screen_width, 0))

    def draw_controls(self):
        if self.speed<max_speed:
            speed_clr=(0,128,0)
        else:
            speed_clr=(255,0,0)
        acceleration_text = f"Acceleration: {self.acceleration:.2f}"
        speedtxt_text = f"Speed: "
        speedval_text = f"{self.speed:.2f} km/hr"
        font = pygame.font.Font(None, 24)
        acceleration_surface = font.render(acceleration_text, True, black)
        speedtxt_surface = font.render(speedtxt_text, True, black)
        speedval_surface = font.render(speedval_text, True, speed_clr)

        screen.blit(acceleration_surface, (20, 20))
        screen.blit(speedtxt_surface, (20, 60))
        screen.blit(speedval_surface, (78, 60))
        
        #Location name
        alert_text = f"{location_name}"
        alert_surface = font.render(alert_text, True, (0, 0, 255))
        screen.blit(alert_surface, (20, 38))
        
        alert_text = f"{max_speed} km/hr"
        alert_surface = font.render(alert_text, True, (200, 106, 0))
        screen.blit(alert_surface, (728, 63))
        
        alert_text = f"*Demonstration"
        alert_surface = font.render(alert_text, True, white)
        screen.blit(alert_surface, (14, 570))
        
        if self.speed > max_speed:
            alert_text = f"You are crossing the speed limit"
            alert_surface = font.render(alert_text, True, (255, 0, 0))
            screen.blit(alert_surface, (20, 80))

    def get_speed(self):
        return self.speed

car_game = CarGame()
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                car_game.acceleration = 0.1  # UP arrow, ie apply acceleration
            elif event.key == pygame.K_DOWN:
                car_game.acceleration = 0.0  # DOWN arrow,ie apply brake
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                car_game.acceleration = -0.1 # decelerate if accelerator is not applied
    screen.fill(black)

    car_game.update_speed(car_game.acceleration)
    car_game.update_position()

    car_game.background_x += car_game.speed

    if car_game.background_x <= -screen_width:
        car_game.background_x = 0

    car_game.draw_background()

    car_game.draw_car()

    car_game.draw_controls()

    car_game.draw_location_icon()
    
    car_game.draw_warning_icon()
    
    car_game.draw_pedals_icon()
    
    pygame.display.flip()

    clock.tick(60)

pygame.quit()