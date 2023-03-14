import pygame 

class ui:
    def __init__(self,surface):
        # set up
        self.display_surface = surface

        # health
        self.health_bar = pygame.image.load('C:\\Users\\CMP_ShJiang\\source\\repos\\platformerinpygame\\graphics\\ui\\health_bar.png')
        
        #coins
        self.coin = pygame.image.load('C:\\Users\\CMP_ShJiang\\source\\repos\\platformerinpygame\\graphics\\ui\\coin.png')
        self.coin_rect = self.coin.get_rect(topleft = (50,61))
        self.font = pygame.font.Font('C:\\Users\\CMP_ShJiang\\source\\repos\\platformerinpygame\\graphics\\ui\\ARCADEPI.TTF',30)

    def show_health(self,current,full):
        self.display_surface.blit(self.health_bar,(20,10))


    def show_coins(self,amount):
        self.display_surface.blit(self.coin,self.coin_rect)  
        coin_amount_surf = self.font.render(str(amount),False,'#33323d')
        coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 4,self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf,coin_amount_rect)
