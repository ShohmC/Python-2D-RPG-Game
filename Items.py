import pygame
import Player
from sprites import *
from config import *


class Sword(pygame.sprite.Sprite):
    def __init__(self, damage):
        super().__init__()
        self.image = pygame.image.load("Items/Sword.png")
        self.damage = damage


class Bow(pygame.sprite.Sprite):
    def __init__(self, damage):
        super().__init__()
        self.image = pygame.image.load("Items/Bow.png")
        self.damage = damage

class swordAttack(pygame.sprite.Sprite):
    def __init__(self, initialX, initialY):
        super().__init__()
        self.image = pygame.image.load("Player/Sword_Animations/sword_swipe_right.png")
        self.rect = self.image.get_rect(center=(initialX, initialY))
        self.cooldown = 0
        self.cooldownTime = 500
        self.despawnCounter = 0
        self.swordAttackGroup = pygame.sprite.LayeredUpdates()
        self.velocity = pygame.math.Vector2(0, 0)

    def attack(self, playerUp, playerLeft, playerDown, playerRight, playerX, playerY):
        time = pygame.time.get_ticks()

        if time - self.cooldown >= self.cooldownTime:
            if playerUp:
                self.image = pygame.image.load("Player/Sword_Animations/sword_swipe_up.png")
                self.swordAttackSprite = swordAttack(playerX + 10, playerY - 10)
            if playerLeft:
                self.image = pygame.image.load("Player/Sword_Animations/sword_swipe_left.png")
                self.swordAttackSprite = swordAttack(playerX - 10, playerY + 10)
            if playerDown:
                self.image = pygame.image.load("Player/Sword_Animations/sword_swipe_down.png")
                self.swordAttackSprite = swordAttack(playerX + 10, playerY + 30)
            if playerRight:
                self.image = pygame.image.load("Player/Sword_Animations/sword_swipe_right.png")
                self.swordAttackSprite = swordAttack(playerX + 30, playerY + 10)

        self.swordAttackGroup.add(self.swordAttackSprite)
        self.cooldown = time

    def checkCollision(self, tileCollisionGroup, enemyCollisionGroup, swordObject):
        swordItem = swordObject
        currentTime = pygame.time.get_ticks()

        collisions = pygame.sprite.spritecollide(self, tileCollisionGroup, False)
        enemyCollisions = pygame.sprite.spritecollide(self, enemyCollisionGroup, False)

        if enemyCollisions or collisions:
            if currentTime - self.cooldown > self.cooldownTime and self.despawnCounter >= 10:
                for enemies in enemyCollisionGroup:
                    enemies.health -= swordItem.damage
                    self.kill()

    def draw(self, screen, camera):
        for sword in self.swordAttackGroup:
            screen.blit(self.image, camera.apply(sword))

    def update(self, tileCollisionGroup, enemyCollisionGroup, swordObject):
        self.despawnSlash()
        self.checkCollision(tileCollisionGroup, enemyCollisionGroup, swordObject)
        self.swordAttackGroup.update(tileCollisionGroup, enemyCollisionGroup, swordObject)

    def despawnSlash(self):
        self.despawnCounter += 1
        if self.despawnCounter >= 10:
            self.kill()

class bowAttack(pygame.sprite.Sprite):
    def __init__(self, initialX, initialY, velocityX, velocityY):
        super().__init__()
        self.image = pygame.image.load("Player/Bow_Animations/arrow_up.png")
        self.rect = self.image.get_rect(center=(initialX, initialY))
        self.cooldown = 0
        self.cooldownTime = 1000
        self.velocity = pygame.math.Vector2(velocityX, velocityY)
        self.distanceTravelled = 0
        self.bowAttackGroup = pygame.sprite.LayeredUpdates()

    def attack(self, playerUp, playerLeft, playerDown, playerRight, initialX, initialY):
        time = pygame.time.get_ticks()

        if time - self.cooldown >= self.cooldownTime:
            if playerUp:
                self.image = pygame.image.load("Player/Bow_Animations/arrow_up.png")
                self.bowAttackSprite = bowAttack(initialX, initialY, 0, -3)
            if playerLeft:
                self.image = pygame.image.load("Player/Bow_Animations/arrow_left.png")
                self.bowAttackSprite = bowAttack(initialX, initialY, -3, 0)
            if playerDown:
                self.image = pygame.image.load("Player/Bow_Animations/arrow_down.png")
                self.bowAttackSprite = bowAttack(initialX, initialY, 0, 3)
            if playerRight:
                self.image = pygame.image.load("Player/Bow_Animations/arrow_right.png")
                self.bowAttackSprite = bowAttack(initialX, initialY, 3, 0)

            self.bowAttackGroup.add(self.bowAttackSprite)
            self.cooldown = time

    def checkCollision(self, tileCollisionGroup, enemyCollisionGroup, bowObject):
        bowItem = bowObject
        currentTime = pygame.time.get_ticks()

        collisions = pygame.sprite.spritecollide(self, tileCollisionGroup, False)
        enemyCollisions = pygame.sprite.spritecollide(self, enemyCollisionGroup, False)

        if enemyCollisions or collisions:
            if currentTime - self.cooldown > self.cooldownTime:
                for enemies in enemyCollisionGroup:
                    enemies.health -= bowItem.damage
                    self.kill()

    def draw(self, screen, camera):
        for arrow in self.bowAttackGroup:
            arrow.rect.move_ip(arrow.velocity)
            screen.blit(self.image, camera.apply(arrow))

    def update(self, playerUp, playerLeft, playerDown, playerRight, tileCollisionGroup, enemyCollisionGroup,
               initialX, initialY, bowObject):
        self.checkCollision(tileCollisionGroup, enemyCollisionGroup, bowObject)
        self.bowAttackGroup.update(playerUp, playerLeft, playerDown, playerRight, tileCollisionGroup,
                                   enemyCollisionGroup,
                                   initialX, initialY, bowObject)
        self.despawnArrow()

    def despawnArrow(self):
        self.distanceTravelled += self.velocity.length()
        if self.distanceTravelled >= TILESIZE * 4:
            self.kill()