from random import randint
import pygame
from tittle import AnimatedTIle

class enemy(AnimatedTIle):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,'C:\\Users\\shaok\\source\\repos\\2-7-2023 cmp hw\\2DMariostyleplatformer\\graphics\\enemy\\run')
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(3,5)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image,True,False)
    def reverse(self):
        self.speed *= -1



    def update(self,shift):
        self.rect.x += shift 
        self.animate()
        self.move()
        self.reverse_image()
