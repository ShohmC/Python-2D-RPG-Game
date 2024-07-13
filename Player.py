import pygame
from config import *


# Player.py
class Player(pygame.sprite.Sprite):
    def __init__(self, screen, initialXLocation, initialYLocation):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("Player/up1.png").convert_alpha(),
                                            (TILESIZE - 4, TILESIZE - 4))  # -4 so player can go through one block gaps
        self.rect = self.image.get_rect(topleft=(initialXLocation, initialYLocation))
        self.screen = screen
        self._layer = 3

        self.cooldown = 0
        self.cooldownTime = 200

        self.upCounter = 0
        self.leftCounter = 0
        self.downCounter = 0
        self.rightCounter = 0

        self.upCounterBool = False
        self.leftCounterBool = False
        self.downCounterBool = False
        self.rightCounterBool = False

        self.counterBooleans = [self.upCounterBool, self.leftCounterBool, self.downCounterBool, self.rightCounterBool]

        self.health = 100
        self.damage = 0

        self.exp = 0
        self.level = 1
        self.expStartingThreshold = 25
        self.upgradePoints = 0

    def expRequired(self, level):
        A = 10
        B = 25
        C = 35
        exp = A * (level * level) + B * level + C
        return exp

    def counterBooleanTorF(self, element):
        for i in range(len(self.counterBooleans)):
            self.counterBooleans[i] = False
            self.counterBooleans[element] = True

    def drawPlayerHealthBar(self, screen):
        screen.blit(pygame.font.Font(None, 48).render(f"Health", True, (0, 0, 0)), (50, 50))
        pygame.draw.rect(screen, (255, 0, 0), (175, 55, 150, 25))
        pygame.draw.rect(screen, (0, 255, 0), (175, 55, 150 * (self.health / 100), 25))
        screen.blit(pygame.font.Font(None, 36).render(f"{self.health}", True, (0, 0, 0)), (230, 56))

    def drawPlayerExpBar(self, screen):
        if self.exp > self.expStartingThreshold:
            self.level += 1
            self.upgradePoints += 1
            self.expStartingThreshold = self.expStartingThreshold * 1.125 + 100
        screen.blit(pygame.font.Font(None, 36).render(f"{self.level}", True, (0, 0, 0)), (632, 800))
        pygame.draw.rect(screen, (0, 0, 0), (354, 830, 576, 15))
        pygame.draw.rect(screen, (0, 0, 255), (354, 830, 576 * (self.exp / self.expRequired(self.level)), 15))

    def checkCollision(self, tileCollisionGroup, enemyCollisionGroup):
        currentTime = pygame.time.get_ticks()
        self.tileCollisionGroup = tileCollisionGroup
        self.enemyCollisionGroup = enemyCollisionGroup

        self.rect.move_ip(self.velocity)

        collisions = pygame.sprite.spritecollide(self, self.tileCollisionGroup, False)
        enemyCollisions = pygame.sprite.spritecollide(self, self.enemyCollisionGroup, False)

        if collisions or enemyCollisions:
            self.rect.move_ip(-self.velocity.x, -self.velocity.y)

# FIX THIS PART

            if enemyCollisions:
                if currentTime - self.cooldown > self.cooldownTime:
                    for enemy in enemyCollisionGroup:
                        self.health -= enemy.damage
                    self.cooldown = currentTime
                if self.health <= 0:
                    print("Bye bye")

    def swordMovement(self):
        dt = pygame.time.Clock().tick(FPS) / 100
        keys = pygame.key.get_pressed()

        # Update the player's velocity based on the direction
        self.velocity = pygame.math.Vector2(0, 0)

        if keys[pygame.K_w]:
            self.counterBooleanTorF(0)
            self.upCounter = (self.upCounter + 1) % 20
            if self.upCounter in range(0, 10):
                self.image = pygame.transform.scale(pygame.image.load("Player/up1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            elif self.upCounter in range(10, 20):
                self.image = pygame.transform.scale(pygame.image.load("Player/up1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            self.velocity.y = -playerYVelocity * dt
        if keys[pygame.K_a]:
            self.counterBooleanTorF(1)
            self.leftCounter = (self.leftCounter + 1) % 20
            if self.leftCounter in range(0, 10):
                self.image = pygame.transform.scale(pygame.image.load("Player/up1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            elif self.leftCounter in range(10, 20):
                self.image = pygame.transform.scale(pygame.image.load("Player/up1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            self.velocity.x = -playerXVelocity * dt
        if keys[pygame.K_s]:
            self.counterBooleanTorF(2)
            self.downCounter = (self.downCounter + 1) % 20
            if self.downCounter in range(0, 10):
                self.image = pygame.transform.scale(pygame.image.load("Player/up1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            elif self.downCounter in range(10, 20):
                self.image = pygame.transform.scale(pygame.image.load("Player/up1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            self.velocity.y = playerYVelocity * dt
        if keys[pygame.K_d]:
            self.counterBooleanTorF(3)
            self.rightCounter = (self.rightCounter + 1) % 20
            if self.rightCounter in range(0, 10):
                self.image = pygame.transform.scale(pygame.image.load("Player/up1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            elif self.rightCounter in range(10, 20):
                self.image = pygame.transform.scale(pygame.image.load("Player/up1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            self.velocity.x = playerXVelocity * dt

    def bowMovement(self):
        dt = pygame.time.Clock().tick(FPS) / 100
        keys = pygame.key.get_pressed()

        # Update the player's velocity based on the direction
        self.velocity = pygame.math.Vector2(0, 0)

        if keys[pygame.K_w]:
            self.counterBooleanTorF(0)
            self.upCounter = (self.upCounter + 1) % 20
            if self.upCounter in range(0, 10):
                self.image = pygame.transform.scale(pygame.image.load("Player/right1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            elif self.upCounter in range(10, 20):
                self.image = pygame.transform.scale(pygame.image.load("Player/right1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            self.velocity.y = -playerYVelocity * dt
        if keys[pygame.K_a]:
            self.counterBooleanTorF(1)
            self.leftCounter = (self.leftCounter + 1) % 20
            if self.leftCounter in range(0, 10):
                self.image = pygame.transform.scale(pygame.image.load("Player/right1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            elif self.leftCounter in range(10, 20):
                self.image = pygame.transform.scale(pygame.image.load("Player/right1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            self.velocity.x = -playerXVelocity * dt
        if keys[pygame.K_s]:
            self.counterBooleanTorF(2)
            self.downCounter = (self.downCounter + 1) % 20
            if self.downCounter in range(0, 10):
                self.image = pygame.transform.scale(pygame.image.load("Player/right1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            elif self.downCounter in range(10, 20):
                self.image = pygame.transform.scale(pygame.image.load("Player/right1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            self.velocity.y = playerYVelocity * dt
        if keys[pygame.K_d]:
            self.counterBooleanTorF(3)
            self.rightCounter = (self.rightCounter + 1) % 20
            if self.rightCounter in range(0, 10):
                self.image = pygame.transform.scale(pygame.image.load("Player/right1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            elif self.rightCounter in range(10, 20):
                self.image = pygame.transform.scale(pygame.image.load("Player/right1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            self.velocity.x = playerXVelocity * dt
    def movement(self):
        dt = pygame.time.Clock().tick(FPS) / 100
        keys = pygame.key.get_pressed()

        # Update the player's velocity based on the direction
        self.velocity = pygame.math.Vector2(0, 0)

        if keys[pygame.K_w]:
            self.counterBooleanTorF(0)
            self.upCounter = (self.upCounter + 1) % 20
            if self.upCounter in range(0, 10):
                self.image = pygame.transform.scale(pygame.image.load("Player/up1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            elif self.upCounter in range(10, 20):
                self.image = pygame.transform.scale(pygame.image.load("Player/up2.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            self.velocity.y = -playerYVelocity * dt
        if keys[pygame.K_a]:
            self.counterBooleanTorF(1)
            self.leftCounter = (self.leftCounter + 1) % 20
            if self.leftCounter in range(0, 10):
                self.image = pygame.transform.scale(pygame.image.load("Player/left1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            elif self.leftCounter in range(10, 20):
                self.image = pygame.transform.scale(pygame.image.load("Player/left2.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            self.velocity.x = -playerXVelocity * dt
        if keys[pygame.K_s]:
            self.counterBooleanTorF(2)
            self.downCounter = (self.downCounter + 1) % 20
            if self.downCounter in range(0, 10):
                self.image = pygame.transform.scale(pygame.image.load("Player/down1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            elif self.downCounter in range(10, 20):
                self.image = pygame.transform.scale(pygame.image.load("Player/down2.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            self.velocity.y = playerYVelocity * dt
        if keys[pygame.K_d]:
            self.counterBooleanTorF(3)
            self.rightCounter = (self.rightCounter + 1) % 20
            if self.rightCounter in range(0, 10):
                self.image = pygame.transform.scale(pygame.image.load("Player/right1.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            elif self.rightCounter in range(10, 20):
                self.image = pygame.transform.scale(pygame.image.load("Player/right2.png").convert_alpha(),
                                                    (TILESIZE - 4, TILESIZE - 4))
            self.velocity.x = playerXVelocity * dt

    def update(self, tileCollisionGroup, enemyCollisionGroup, hotbar):
        if hotbar.currentSlotIndex == 0:
            self.swordMovement()

        if hotbar.currentSlotIndex == 1:
            self.bowMovement()
        if hotbar.currentSlotIndex != 0 and hotbar.currentSlotIndex != 1:
            self.movement()
        self.checkCollision(tileCollisionGroup, enemyCollisionGroup)
