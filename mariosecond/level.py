import pygame
from support import import_csv_layout, import_cut_graphic
from settings import tile_size,screen_height, screen_width
from tittle import Tile, StaticTile, Crate, Coin, Palm
from Enemy import enemy
from decoration import Sky,water, Clouds
from player import Player
from particles import ParticleEffect
from game_data import levels 
class Level:
    def __init__(self,current_level,surface,create_overworld):
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None
        
        # overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        #player 
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal=pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        #dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # terrain setup
        terrain_layout= import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')

        #grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout,'grass')

        #crates
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout,'crates')

        #coins
        coins_layout = import_csv_layout(level_data['coins'])
        self.conin_sprites = self.create_tile_group(coins_layout,'coins')

        # foreground palms
        fg_palm_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg palms')

        # background palms
        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg palms')

        # Enemy
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout,'enemies')

        # Constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout,'constraints')

        #decoration
        self.sky = Sky(8)
        level_width = len(terrain_layout[0])* tile_size
        self.water = water(screen_height - 25,level_width)
        self.clouds= Clouds(400,level_width,15)

    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y= row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphic('C:\\Users\\shaok\\source\\repos\\2-7-2023 cmp hw\\2DMariostyleplatformer\\graphics\\terrain\\terrain_tiles.png')
                        tile_surface=terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                        sprite_group.add(sprite)

                    if type == 'grass':
                        grass_tile_list= import_cut_graphic('C:\\Users\\shaok\\source\\repos\\2-7-2023 cmp hw\\2DMariostyleplatformer\\graphics\\decoration\\grass\\grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)

                    if type =='crates':
                        sprite = Crate(tile_size,x,y)

                    if type == 'coins':
                        if val == '0':sprite = Coin(tile_size,x,y,'C:\\Users\\shaok\\source\\repos\\2-7-2023 cmp hw\\2DMariostyleplatformer\\graphics\\coins\\gold')
                        if val == '1': sprite = Coin(tile_size,x,y,'C:\\Users\\shaok\\source\\repos\\2-7-2023 cmp hw\\2DMariostyleplatformer\\graphics\\coins\\silver')
                    if type =='fg palms':
                        if val =='1': sprite= Palm(tile_size,x,y,'C:\\Users\\shaok\\source\\repos\\2-7-2023 cmp hw\\2DMariostyleplatformer\\graphics\\terrain\\palm_small',38)
                        if val =='2': sprite= Palm(tile_size,x,y,'C:\\Users\\shaok\\source\\repos\\2-7-2023 cmp hw\\2DMariostyleplatformer\\graphics\\terrain\\palm_large',64)
                    if type == 'bg palms':
                        sprite = Palm(tile_size,x,y,'C:\\Users\\shaok\\source\\repos\\2-7-2023 cmp hw\\2DMariostyleplatformer\\graphics\\terrain\\palm_bg',64)

                    if type == 'enemies':
                        sprite = enemy(tile_size,x,y)

                    if type == 'constraints':
                        sprite = Tile(tile_size,x,y)
                    
                    
                    sprite_group.add(sprite)
        return sprite_group
    def player_setup(self,layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y= row_index * tile_size
                if val == '0':
                   sprite = Player((x,y),self.display_surface,self.create_jump_particles)
                   self.player.add(sprite)
                if val =='1':
                    hat_surface = pygame.image.load('C:\\Users\\shaok\\source\\repos\\2-7-2023 cmp hw\\2DMariostyleplatformer\\graphics\\character\\hat.png').convert_alpha()
                    sprite = StaticTile(tile_size,x,y,hat_surface)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False):
                enemy.reverse()

    def create_jump_particles(self,pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10,5)
        else:
             pos += pygame.math.Vector2(10,-5)
        jump_particle_sprite = ParticleEffect(pos,'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        colliable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()

        for sprite in colliable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0: 
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        
        if player.on_left and (player.rect.left< self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right> self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collission(self):
        player = self.player.sprite
        player.apply_gravity()
        colliable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
        for sprite in colliable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    
                elif player.direction.y < 0: 
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                    

        if player.on_ground and player.direction.y<0 or player.direction.y>1:
            player.on_ground = False
        if  player.on_ground and player.direction.y>0:
            player.on_ceiling = False
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width/4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width/4) and direction_x >0:
            self.world_shift = -8
            player.speed =0
        else:
            self.world_shift = 0
            player.speed =8 
    
    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom-offset,'land')
            self.dust_sprite.add(fall_dust_particle)

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level,0)
            
    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal,False):
            self.create_overworld(self.current_level,self.new_max_level)

    def run(self):
        # runs the level 
        
        # decoration
        #sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        # backgournd palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)
        
        # terrain
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)
        
        #enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)
        
        # crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        #grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        #coins
        self.conin_sprites.update(self.world_shift)
        self.conin_sprites.draw(self.display_surface)

        #foreground palms 
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        #dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        #player sprite
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collission()
        self.create_landing_dust()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        self.check_death()
        self.check_win()
        
        #Water 
        self.water.draw(self.display_surface,self.world_shift)
        

      

      

       


    

        
