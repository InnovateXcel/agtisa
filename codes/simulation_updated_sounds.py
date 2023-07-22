import pygame
import sys
import requests

# Define your main menu class
class MainMenu:
    def __init__(self):
        # Initialize any necessary variables for the main menu
        self.font = None
        self.background_image = None
        self.start_image = None
    def initialize(self):
        # Initialize the font module
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)  # Define the font for the text
        self.start_image = pygame.image.load("start.png")

    def handle_events(self, events):
        # Handle events for the main menu
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Start the game when Enter key is pressed
                    return "start_game"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    start_image_rect = self.start_image.get_rect()
                    start_image_rect.center = (screen_width // 2, screen_height // 2 + 130)
                    if start_image_rect.collidepoint(event.pos):
                        # Start the game when the start button is clicked
                        return "start_game"


    
    def draw_background(self):
        background_image = pygame.image.load("menu.png")  # Load the background image
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
        screen.blit(background_image, (0,0))
    
    def draw_start(self):
        scaled_icon_image = pygame.transform.scale(self.start_image, (350, 350))
        start_icon_x = screen_width // 2 - scaled_icon_image.get_width() // 2
        start_icon_y = screen_height // 2 + 130 - scaled_icon_image.get_height() // 2
        screen.blit(scaled_icon_image, (start_icon_x, start_icon_y))
    
    def draw_exit(self):
        exit_image = pygame.image.load("exit.png")
        scaled_icon_image = pygame.transform.scale(exit_image, (230, 230))
        exit_icon_x = screen_width - scaled_icon_image.get_width() + 65
        exit_icon_y = -80    
        screen.blit(scaled_icon_image, (exit_icon_x, exit_icon_y))
        
# Create an instance of the MainMenu class
main_menu = MainMenu()

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Main Menu")

# Initialize the main menu
main_menu.initialize()

# Game loop
running = True
while running:
    # Handle events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Update the main menu and check if it returns a command to start the game
    command = main_menu.handle_events(events)
    if command == "start_game":
        break

    # Draw the main menu on the screen
    main_menu.draw_background()
    main_menu.draw_start()
    main_menu.draw_exit()

    # Update the display
    pygame.display.flip()

# Game screen

api_key = "93v0A4i8R298ggGHjsAx488ZkH0sZc07"
latitude = 13.041671
longitude = 80.167140
location_name = 'Porur'
base_url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
request_url = "{base_url}?point={latitude},{longitude}&unit=KMPH&key={}".format(latitude=latitude, longitude=longitude, base_url=base_url, api_key=api_key)
try:
    response = requests.get(request_url)
    if response.status_code == 200:
        data = response.json()
        max_speed = data['flowSegmentData']['currentSpeed']
        print("The maximum speed limit in the Porur area is {} km/h.".format(max_speed))
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
        self.engine_sound_playing = False
        self.brake_sound_playing = False
        self.beep_sound_playing = False
        self.beep_time=0
        self.speed = 0.0
        self.acceleration = 0.0
        self.drag = 0.99  # Deceleration factor (1 means no deceleration)
        self.acceleration_factor = 0.48  # Acceleration factor
        self.deceleration_factor = 0.18  # Deceleration factor
        self.gear_levels = {
            1: {'acceleration': 0.4, 'max_speed': 10},
            2: {'acceleration': 0.6, 'max_speed': 25},
            3: {'acceleration': 0.7, 'max_speed': 40},
            4: {'acceleration': 0.9, 'max_speed': 65},
            5: {'acceleration': 1.2, 'max_speed': 100}
        }
        self.min_speed = 0.0
        self.current_gear = 1
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.background_x = 0

    def update_speed(self, acceleration):
        self.acceleration = acceleration

        if self.acceleration > 0:
            self.speed += self.acceleration * self.gear_levels[self.current_gear]['acceleration']
        else:
            self.speed += self.acceleration * self.deceleration_factor

        if self.acceleration == 0.0:
            self.speed *= self.drag

        self.speed = max(self.min_speed, min(self.speed, self.gear_levels[self.current_gear]['max_speed']))

    def update_position(self):
        # Update position based on current speed
        self.x += self.speed

        if self.x < 0:
            self.x = screen_width
        elif self.x > screen_width:
            self.x = 0
    
    def increase_gear(self):
        if self.current_gear < len(self.gear_levels):
            self.current_gear += 1
            print("Gear increased to {}".format(self.current_gear))
        else:
            print("Already in the highest gear level")

    def decrease_gear(self):
        if self.current_gear > 1:
            self.current_gear -= 1
            print("Gear decreased to {}".format(self.current_gear))
        else:
            print("Already in the lowest gear level")
            
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
        
    def play_engine_sound(self):
        if not self.engine_sound_playing:
            pygame.mixer.music.load("engine_sound.mp3")  # Load the engine sound file
            pygame.mixer.music.play(-1)  # Play the sound in a loop (-1 means looping)
            self.engine_sound_playing = True

    def stop_engine_sound(self):
        if self.engine_sound_playing:
            pygame.mixer.music.stop()
            self.engine_sound_playing = False

    def play_brake_sound(self):
        if not self.brake_sound_playing:
            pygame.mixer.music.load("brake_sound.mp3")  # Load the brake sound file
            pygame.mixer.music.play(-1)  # Play the sound in a loop (-1 means looping)
            self.brake_sound_playing = True

    def stop_brake_sound(self):
        if self.brake_sound_playing:
            pygame.mixer.music.stop()
            self.brake_sound_playing = False
            
    def play_beep_sound(self):
        if not self.beep_sound_playing:
            pygame.mixer.music.load("beep.mp3")  # Load the beep sound file
            pygame.mixer.music.play()  # Play the sound
            self.beep_sound_playing = True

    def stop_beep_sound(self):
        if self.beep_sound_playing:
            pygame.mixer.music.stop()
            self.beep_sound_playing = False
            
    def check_speed_limit(self):
        if self.speed > max_speed:
            current_time = pygame.time.get_ticks()
            if current_time - self.beep_time >= 5000:  # Check if 5 seconds have passed
                self.beep_time = current_time
                self.play_beep_sound()        
    
    
    def draw_controls(self):
        if self.speed<max_speed:
            speed_clr=(0,128,0)
        else:
            speed_clr=(255,0,0)
            
        acceleration_text = "Acceleration: {:.2f}".format(self.acceleration)
        speedtxt_text = "Speed: "
        speedval_text = "{:.2f} km/hr".format(self.speed)
        font = pygame.font.Font(None, 24)
        acceleration_surface = font.render(acceleration_text, True, black)
        speedtxt_surface = font.render(speedtxt_text, True, black)
        speedval_surface = font.render(speedval_text, True, speed_clr)

        screen.blit(acceleration_surface, (20, 20))
        screen.blit(speedtxt_surface, (20, 50))
        screen.blit(speedval_surface, (78, 50))
        
        # Location name
        alert_text = "{}".format(location_name)
        alert_surface = font.render(alert_text, True, (0, 0, 255))
        screen.blit(alert_surface, (745, 38))

        # Max speed
        alert_text = "{} km/hr".format(max_speed)
        alert_surface = font.render(alert_text, True, (200, 106, 0))
        screen.blit(alert_surface, (728, 63))
        
        alert_text = "*Demonstration"
        alert_surface = font.render(alert_text, True, white)
        screen.blit(alert_surface, (14, 570))
        
        gear_text = "(H/G) Gear : {}".format(self.current_gear)
        gear_surface = font.render(gear_text, True, black)
        screen.blit(gear_surface, (20, 75))
        
        if self.speed > max_speed:
            alert_text = "You are crossing the speed limit"
            alert_surface = font.render(alert_text, True, (255, 0, 0))
            screen.blit(alert_surface, (20, 100))

    def get_speed(self):
        return self.speed
    
car_game = CarGame()
clock = pygame.time.Clock()

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                car_game.acceleration = 0.1  # UP arrow, i.e., apply acceleration
                car_game.play_engine_sound()  # Start playing the engine sound
            elif event.key == pygame.K_DOWN:
                car_game.acceleration = 0.0  # DOWN arrow, i.e., apply brake
                car_game.play_brake_sound()  # Start playing the brake sound
            elif event.key == pygame.K_h:
                car_game.increase_gear()  # Increase gear level (press 'h' key)
            elif event.key == pygame.K_g:
                car_game.decrease_gear()  # Decrease gear level (press 'g' key)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                car_game.acceleration = -0.1  # Release accelerator or brake
                car_game.stop_engine_sound()  # Stop playing the engine sound
                car_game.stop_brake_sound()  # Stop playing the brake sound



    screen.fill(black)

    car_game.update_speed(car_game.acceleration)
    car_game.update_position()
    car_game.check_speed_limit()

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

# Quit the game
pygame.quit()
sys.exit()
