import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600

# Set colors
black = (0, 0, 0)
white = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)

# Set up OpenGL
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (screen_width / screen_height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glEnable(GL_DEPTH_TEST)

# Set up lighting
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_POSITION, (0, 1, 1, 0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))

# Car class
class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0.0

    def update(self, turn_direction):
        self.angle += turn_direction * 5.0  # Adjust the turn speed as needed

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, 0, self.y)
        glRotatef(self.angle, 0, 1, 0)
        
        # Draw the car model or geometry
        glColor3f(1.0, 0.0, 0.0)  # Set the car color
        glBegin(GL_QUADS)
        glVertex3f(-0.5, 0.0, -0.5)
        glVertex3f(0.5, 0.0, -0.5)
        glVertex3f(0.5, 0.0, 0.5)
        glVertex3f(-0.5, 0.0, 0.5)
        glEnd()

        glPopMatrix()

car = Car(0, 0)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                car.update(-1)  # Turn the car left
            elif event.key == pygame.K_RIGHT:
                car.update(1)  # Turn the car right
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                car.update(0)  # Stop turning

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Set the camera position and orientation
    glLoadIdentity()
    gluLookAt(0, 5, 10, 0, 0, 0, 0, 1, 0)

    # Draw the car
    car.draw()

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
