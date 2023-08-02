import random
import pygame
import requests
from playsound import playsound

#get the speed limit for porur area
api_key = "93v0A4i8R298ggGHjsAx488ZkH0sZc07"
latitude = 13.041671
longitude = 80.167140
base_url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
request_url = f"{base_url}?point={latitude},{longitude}&unit=KMPH&key={api_key}"
response = requests.get(request_url)
if response.status_code == 200:
    data = response.json()
    max_speed = data['flowSegmentData']['currentSpeed']
    print(f"The maximum speed limit in the Porur area is {max_speed} km/h.")
else:
    print("Error: Failed to retrieve the maximum speed limit.")

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AGTISA car simulation window")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)

class CarGame:
    def __init__(self):
        self.speed = 0.0
        self.acceleration = 0.0
        self.x = screen_width // 2  # X-coordinate on the map
        self.y = screen_height // 2  # Y-coordinate on the map

    def update_speed(self, acceleration):
        # Increase or decrease the speed based on the acceleration value
        self.speed += acceleration

        # Limit the speed within a specific range (optional)
        max_speed = 70.0
        min_speed = 0.0
        self.speed = max(min(self.speed, max_speed), min_speed)

    def update_position(self):
        # Simulating the movement of the car based on speed
        self.x += self.speed

        # Wrap around the screen edges
        if self.x < 0:
            self.x = screen_width
        elif self.x > screen_width:
            self.x = 0

    def draw_car(self):
        # Draw a car at the current position
        car_image = pygame.image.load("car.png")
        screen.blit(car_image, (self.x - car_image.get_width() // 2, self.y - car_image.get_height() // 2))

    def draw_controls(self):
        # Display the acceleration and speed values
        acceleration_text = f"Acceleration: {self.acceleration:.2f}"
        speed_text = f"Speed: {self.speed:.2f}"
        font = pygame.font.Font(None, 24)
        acceleration_surface = font.render(acceleration_text, True, white)
        speed_surface = font.render(speed_text, True, white)

        screen.blit(acceleration_surface, (20, 20))
        screen.blit(speed_surface, (20, 50))
        
        if self.speed>max_speed:
            alert_text = f"You are crossing the limit"
            font = pygame.font.Font(None, 24)
            alert_surface = font.render(alert_text, True, white)

            screen.blit(alert_surface, (20, 80))
        
        #if self.speed>max_speed:
            #print('Alert! You are crossing the maximum speed limit in Porur area')
            #audio_file = 'beep.mp3'  # Replace with the actual path to the audio file
            #playsound(audio_file)

    def get_speed(self):
        return self.speed

# Create an instance of the CarGame
car_game = CarGame()

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                car_game.acceleration = 0.1  # Set positive acceleration when up arrow key is pressed
            elif event.key == pygame.K_DOWN:
                car_game.acceleration = -0.1  # Set negative acceleration when down arrow key is pressed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                car_game.acceleration = 0.0  # Set acceleration to 0 when arrow keys are released

    # Clear the screen
    screen.fill(black)

    # Update the game state
    car_game.update_speed(car_game.acceleration)
    car_game.update_position()

    # Draw the car
    car_game.draw_car()

    # Draw the controls
    car_game.draw_controls()

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
