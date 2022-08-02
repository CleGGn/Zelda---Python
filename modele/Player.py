import pygame
from settings import *
from pygame.math import Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('assets/test/player.png').convert_alpha() # Le visuel
        self.rect = self.image.get_rect(topleft = pos) # la position
        self.hitbox = self.rect.inflate(0, -26) # la hitbox de notre player

        self.direction = pygame.math.Vector2() # la direction
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

    # Fonction qui check la direction du joueur en fonction des boutons qu'il presse
    # Notre WORLD_MAP est un array donc aller vers le haut équivaut à reduire x de 1
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            # Il faut remettre la direction à 0 si rien n'est pressé, sinon le joueur continuera d'aller dans cette direction
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        
    # Fonction qui déplace le personnage en fonction de sa vitesse
    def move(self,speed):
        if self.direction.magnitude() != 0: # magnitude correspond à la taille du vecteur. On vérifie donc qu'il soit supérieur à 0
            # Si le vecteur est supérieur à 0, on le "normalize". Grosso modo on enlève la virgule pour lui donner une valeur fixe  
            # On utilise cette méthode pour les déplacements en diagonale qui sont toujours légèrement supérieur à déplacement en ligne
            self.direction = self.direction.normalize() 
        # Une fois la normalisation faite, on donne la nouvelle position du personnage    
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    # Fonction qui gère les collisions (non pas avec la surface des sprites mais avec les hitboxes)
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox): # "colliderect()"" verifie s'il y a collision entre "sprite" et "hitbox"
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left # s'il y a collision entre les hitboxs alors on place la droite de la hitbox du personnage sur la gauche de la hitbox du sprite
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self):
        self.input()
        self.move(self.speed)
    