import pygame 
from support import import_folder
class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = (x,y))

    def update(self,shift):
        self.rect.x += shift

class StaticTile(Tile):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y)
        self.image = surface 

class Crate(StaticTile):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,pygame.image.load('C:\\Users\\shaok\\source\\repos\\2-7-2023 cmp hw\\2DMariostyleplatformer\\graphics\\terrain\\crate.png').convert_alpha())
        offset_y = y+size

        self.rect=self.image.get_rect(bottomleft = (x,offset_y))

class AnimatedTIle(Tile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
    def animate(self):
        self.frame_index +=0.2
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]


    def update(self,shift):
        self.animate()
        self.rect.x += shift
class Coin(AnimatedTIle):
     def __init__(self,size,x,y,path):
         super().__init__(size,x,y,path)
         center_x = x + int(size/2)
         center_y = y + int(size/2)
         self.rect = self.image.get_rect(center = (center_x,center_y))

class Palm (AnimatedTIle):
    def __init__(self,size,x,y,path,offset):
        super().__init__(size,x,y,path)
        offset_y = y - offset
        self.rect.topleft = (x,offset_y)


