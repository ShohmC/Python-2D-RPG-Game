import pygame
from config import *


class Enemies(pygame.sprite.Sprite):
    def __init__(self, screen, initialXLocation, initialYLocation, initialImage, upImage1, upImage2, downImage1,
                 downImage2, leftImage1, leftImage2, rightImage1, rightImage2, health, damage, expOnKill):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.initialXLocation = initialXLocation
        self.initialYLocation = initialYLocation
        self.image = pygame.transform.scale(pygame.image.load(initialImage).convert_alpha(),
                                            (TILESIZE - 4, TILESIZE - 4))
        self.upImage1 = pygame.transform.scale(pygame.image.load(upImage1).convert_alpha(),
                                               (TILESIZE - 4, TILESIZE - 4))
        self.upImage2 = pygame.transform.scale(pygame.image.load(upImage2).convert_alpha(),
                                               (TILESIZE - 4, TILESIZE - 4))
        self.downImage1 = pygame.transform.scale(pygame.image.load(downImage1).convert_alpha(),
                                                 (TILESIZE - 4, TILESIZE - 4))
        self.downImage2 = pygame.transform.scale(pygame.image.load(downImage2).convert_alpha(),
                                                 (TILESIZE - 4, TILESIZE - 4))
        self.leftImage1 = pygame.transform.scale(pygame.image.load(leftImage1).convert_alpha(),
                                                 (TILESIZE - 4, TILESIZE - 4))
        self.leftImage2 = pygame.transform.scale(pygame.image.load(leftImage2).convert_alpha(),
                                                 (TILESIZE - 4, TILESIZE - 4))
        self.rightImage1 = pygame.transform.scale(pygame.image.load(rightImage1).convert_alpha(),
                                                  (TILESIZE - 4, TILESIZE - 4))
        self.rightImage2 = pygame.transform.scale(pygame.image.load(rightImage2).convert_alpha(),
                                                  (TILESIZE - 4, TILESIZE - 4))
        self.rect = self.image.get_rect(topleft=(initialXLocation, initialYLocation))
        self._layer = 3
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 2
        self.health = health
        self.maxHealth = health
        self.prevX = self.rect.x
        self.prevY = self.rect.y
        self.upCounter = 0
        self.downCounter = 0
        self.leftCounter = 0
        self.rightCounter = 0

        self.damage = damage

        self.expOnKill = expOnKill

    def drawHealthBar(self, screen, camera):
        healthBarRectangle = pygame.Rect(0, 0, TILESIZE, 5)
        healthBarRectangle.topleft = camera.apply(self).topleft
        healthBarRectangle.y += 30
        pygame.draw.rect(screen, (255, 0, 0), healthBarRectangle)  # Red background
        healthBarRectangle.width = TILESIZE * (self.health / self.maxHealth)
        pygame.draw.rect(screen, (0, 255, 0), healthBarRectangle)

    def animation(self):
        if self.rect.y < self.prevY:
            self.upCounter = (self.upCounter + 1) % 20
            if self.upCounter in range(0, 10):
                self.image = self.upImage1
            elif self.upCounter in range(10, 20):
                self.image = self.upImage2
        elif self.rect.y > self.prevY:
            self.downCounter = (self.downCounter + 1) % 20
            if self.downCounter in range(0, 10):
                self.image = self.downImage1
            elif self.downCounter in range(10, 20):
                self.image = self.downImage2
        elif self.rect.x < self.prevX:
            self.leftCounter = (self.leftCounter + 1) % 20
            if self.leftCounter in range(0, 10):
                self.image = self.leftImage1
            elif self.leftCounter in range(10, 20):
                self.image = self.leftImage2
        elif self.rect.x > self.prevX:
            self.rightCounter = (self.rightCounter + 1) % 20
            if self.rightCounter in range(0, 10):
                self.image = self.rightImage1
            elif self.rightCounter in range(10, 20):
                self.image = self.rightImage2

        self.prevY = self.rect.y
        self.prevX = self.rect.x

    def collision(self, tileCollisionGroup, playerCollisionGroup):
        self.tileCollisionGroup = tileCollisionGroup
        self.playerCollisionGroup = playerCollisionGroup
        collisions = pygame.sprite.spritecollide(self, self.tileCollisionGroup, False)
        playerCollisions = pygame.sprite.spritecollide(self, self.playerCollisionGroup, False)
        if self.health <= 0:
            for player in playerCollisionGroup:
                player.exp += self.expOnKill
            self.kill()
        if collisions or playerCollisions:
            self.rect.move_ip(-self.velocity.x, -self.velocity.y)
            self.velocity = pygame.math.Vector2(-1, -1)
            if playerCollisions:
                for player in playerCollisionGroup:
                    pass
                if self.health <= 0:
                    self.kill()

    def updateMovement(self, player_rect, tileCollisionGroup, playerCollisionGroup):
        distance = pygame.math.Vector2(player_rect.x - self.rect.x, player_rect.y - self.rect.y).length()
        if distance <= TILESIZE * 8:
            direction = pygame.math.Vector2(player_rect.x - self.rect.x, player_rect.y - self.rect.y)
            if distance > 0:
                direction.normalize_ip()
                self.velocity = direction * self.speed
                # Collision checker
                self.collision(tileCollisionGroup, playerCollisionGroup)
        else:
            self.velocity = pygame.math.Vector2(0, 0)
        # Have movement and animation at the end so player can get damaged
        self.rect.move_ip(self.velocity)
        self.animation()


class Bat(Enemies):
    def __init__(self, screen, initialXLocation, initialYLocation, health):
        super().__init__(screen, initialXLocation, initialYLocation, "Enemy/Bat/left1.png",
                         "Enemy/Bat/left1.png", "Enemy/Bat/left2.png",
                         "Enemy/Bat/right1.png", "Enemy/Bat/right2.png", "Enemy/Bat/left1.png",
                         "Enemy/Bat/left2.png", "Enemy/Bat/right1.png", "Enemy/Bat/right2.png", health, 5,
                         25000000000000000)


class testEnemy(Enemies):
    def __init__(self, screen, initialXLocation, initialYLocation, health):
        super().__init__(screen, initialXLocation, initialYLocation, "Enemy/Bat/left1.png",
                         "Enemy/Bat/left1.png", "Enemy/Bat/left2.png",
                         "Enemy/Bat/right1.png", "Enemy/Bat/right2.png", "Enemy/Bat/left1.png",
                         "Enemy/Bat/left2.png", "Enemy/Bat/right1.png", "Enemy/Bat/right2.png", health, 1232,
                         10)
