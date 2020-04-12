import time
import pygame
from pygame.locals import *

class Input:
    def __init__(self, key, down):
        self.key = key
        self.down = down
        self.up = not down

class InputManager:
    def __init__(self):
        self.init_joystick()
        self.buttons = ['up', 'down', 'left', 'right', 'start', 'A', 'B', 'X', 'Y', 'L', 'R']
        self.key_map = {
            K_UP : 'up',
            K_DOWN : 'down',
            K_LEFT : 'left',
            K_RIGHT : 'right',
            K_RETURN : 'start',
            K_a : 'A',
            K_b : 'B',
            K_x : 'X',
            K_y : 'Y',
            K_l : 'L',
            K_r : 'R'
        }
        self.quit_attempt = False

    def get_events(self):
        events = []
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.quit_attempt = True

    def init_joystick(self, index):
        joystick = pygame.joystick.Joystick(index)
        joystick.init()
        self.joystick = joystick
        self.joystick_name = joystick.get_name()
