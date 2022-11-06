import pygame
import math

class Car(pygame.sprite.Sprite):       
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load('car.png').convert_alpha()   
        self.image = pygame.transform.rotate(self.image, 90) 
        self.rect = self.image.get_rect(center = (250, 400)) 
        self.speed = 5                     
        self.driving_angle = 0  
        self.steering_angle = 0   
        self.mask = pygame.mask.from_surface(self.image)   
       
    def update(self, updir,downdir,leftdir,rightdir):  
        move = updir - downdir
        stear = rightdir - leftdir
        self.steering_angle = max(-2.5, min(2.5, self.steering_angle - stear * 0.2))  
        self.rect.y -= round(math.cos(math.radians(self.driving_angle)) * move * self.speed)
        self.rect.x -= round(math.sin(math.radians(self.driving_angle)) * move * self.speed)
        self.driving_angle += (self.steering_angle * move) % 360 
        self.rect.x = self.rect.x
        self.rect.y = self.rect.y
        self.mask = pygame.mask.from_surface(self.image)