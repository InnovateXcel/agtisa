import pygame
from pygame.locals import *
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Game")

# Load car image (Mustang)
car_image = pygame.image.load("car.png")
car_image = pygame.transform.scale(car_image, (100, 200))

# Car class
class Car:
    def __init__(self, x, y):
        self.image = car_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 0
        self.angle = 0

    def update(self):
        # Update car position based on speed and angle
        rad = math.radians(self.angle)
        self.rect.x += self.speed * math.sin(rad)
        self.rect.y -= self.speed * math.cos(rad)

        # Wrap around the screen
        if self.rect.right < 0:
            self.rect.left = screen_width
        elif self.rect.left > screen_width:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = screen_height
        elif self.rect.top > screen_height:
            self.rect.bottom = 0

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)

# Create car instance
car = Car(screen_width // 2, screen_height // 2)

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Accelerator pedal
    if keys[K_UP]:
        car.speed += 0.1
    elif keys[K_DOWN]:
        car.speed -= 0.1
    else:
        car.speed *= 0.95  # Apply deceleration

    # Steering
    if keys[K_LEFT]:
        car.angle += 5
    elif keys[K_RIGHT]:
        car.angle -= 5

    # Update car position and angle
    car.update()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw game elements
    car.draw()

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()