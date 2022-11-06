import gym
import pygame
from gym import spaces
from pygame.event import pump
from car import Car
from pygame import display, time
from pygame.surfarray import array3d
import math
import numpy as np
import cv2
import random

class ParkingENV(gym.Env):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.fps = 1000
        self.spec = None
        self.metadata = {
            'render.modes': ['human','rgb_array'],
            'video.frames_per_second': self.fps
        } 
        self.clock = time.Clock()
        self.width = 500
        self.height = 500
        self.history = []
        self.poshistory = [(-999,-999)]
        for i in range(0, 6):
            self.history.append(np.zeros((84, 84)))
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.screen.fill((90,123,0))
        self.action_space = spaces.Discrete(7)
        self.observation_space = spaces.Box(low=0, high=255, shape=(252,84,1))
        self.totalframes = 0
        

    def step(self, action):
        pump()
        reward = -0.1
        parked = False

        if action == 1:
            self.agent.update(True, False, False, False)
        if action == 2:
            self.agent.update(True, False, True, False)
        if action == 3:
            self.agent.update(True, False, False, True)
        if action == 4:
            self.agent.update(False, True, False, False)
        if action == 5:
            self.agent.update(False, True, True, False)
        if action == 6:
            self.agent.update(False, True, False, True)
        
        self.screen.fill((90,123,0))
        pygame.draw.rect(self.screen, (255,255,255), self.spot)
        self.agent.rect = self.blitRotateCenter(self.screen, self.agent.image, *self.agent.rect.center, self.agent.driving_angle)
        image = array3d(display.get_surface())
        self.clock.tick(self.fps)
        pygame.display.update()
        angle = self.agent.driving_angle % 360
        info = {'position': (self.agent.rect.x,self.agent.rect.y), 'goal': (self.goalx,self.goaly)}
        reward = self.distance(self.poshistory[-1][0],self.poshistory[-1][1],self.goalx,self.goaly) - self.distance(self.agent.rect.x,self.agent.rect.y,self.goalx,self.goaly)
        if self.agent.rect.x == self.goalx and self.agent.rect.y == self.goaly:
            reward = 100
            parked = True
        self.poshistory.append((self.agent.rect.x,self.agent.rect.y))
        if self.totalframes > 600:
            reward = -10
            self.reset()
        self.totalframes += 1
        return self.pre_processing(image), reward, parked, info

    
    def reset(self):
        self.totalframes = 0
        self.history = []
        self.goalx = random.randrange(100,400)
        self.goaly = random.randrange(100,300)
        self.screen.fill((90,123,0))
        self.agent = Car()
        self.spot = pygame.Rect(self.goalx,self.goaly,32,64)
        self.history = []
        self.poshistory = [(-999,-999)]
        for i in range(0, 6):
            self.history.append(np.zeros((84, 84)))
        image = self.pre_processing(array3d(display.get_surface()))
        return image

    def render(self):
        display.update()
        
    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

    def pre_processing(self, image):
        image = cv2.cvtColor(cv2.resize(image, (84, 84)), cv2.COLOR_BGR2GRAY)
        _, image = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)
        image = image / 255
        del self.history[0]
        self.history.append(image)
        image = np.concatenate((self.history[-5], self.history[-3], image), axis=0)
        image = np.expand_dims(image, axis=-1)
        return image
    
    def blitRotateCenter(self, surf, image, left, top, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(center = (left, top)).center)
        surf.blit(rotated_image, new_rect)
        return new_rect

    def distance(self, x1,y1,x2,y2):
        return ((x1 - x2)**2 + (y1-y2)**2)**0.5