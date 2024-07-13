# sprites.py
import math
import pygame
from Items import *
from config import *


class Tiles(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, image, layer, tileSizeMultiplier):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(),
                                            (TILESIZE * tileSizeMultiplier, TILESIZE * tileSizeMultiplier))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.layer = layer


class Chest(Tiles):
    def __init__(self, screen, x, y, image, layer, tileSizeMultiplier, itemsInsideChest):
        super().__init__(screen, x, y, image, layer, tileSizeMultiplier)
        self.itemsInsideChest = itemsInsideChest
        self.numberOfItemsInsideChest = len(itemsInsideChest)
        self.openChestBoolean = False
        self.cooldown = 0
        self.cooldownTime = 200

        self.columns = 4
        self.rows = 6
        self.chestArrayRepresentation = [[None for _ in range(self.rows)] for _ in range(self.columns)]
        self.selectedChestSlot = [[False for _ in range(self.rows)] for _ in range(self.columns)]
        self.itemRectArray = [[None for _ in range(self.rows)] for _ in range(self.columns)]

    def onChestOpen(self, player):  # As long as the cooldown time method is within update it will work
        keys = pygame.key.get_pressed()
        currentTime = pygame.time.get_ticks()
        if currentTime - self.cooldown > self.cooldownTime:
            if player.rect.y in range(self.rect.bottom - 2, self.rect.bottom + 2):
                if keys[pygame.K_SPACE]:
                    self.openChestBoolean = not self.openChestBoolean
                    self.cooldown = currentTime
            if player.rect.x not in range(self.rect.x - 30, self.rect.x + 30):
                self.openChestBoolean = False
            if player.rect.y not in range(self.rect.bottom - 30, self.rect.bottom + 30):
                self.openChestBoolean = False

    def drawChestSlots(self, screen, selectedChestSlotImage, unselectedChestSlotImage):
        xPos = 1000
        yPos = 50
        itemIndex = 0
        for row in range(self.rows):
            for col in range(self.columns):

                chestSlot = pygame.Rect(xPos, yPos, TILESIZE * 2, TILESIZE * 2)
                self.chestArrayRepresentation[col][row] = chestSlot
                pygame.draw.rect(screen, (0, 0, 0), chestSlot)
                xPos = xPos + TILESIZE * 2

                if self.selectedChestSlot[col][row]:
                    screen.blit(selectedChestSlotImage, self.chestArrayRepresentation[col][row])
                else:
                    screen.blit(unselectedChestSlotImage, self.chestArrayRepresentation[col][row])

                if itemIndex < self.numberOfItemsInsideChest:
                    itemImage = self.itemsInsideChest[itemIndex].image
                    itemRect = itemImage.get_rect(center=chestSlot.center)
                    self.chestArrayRepresentation[col][row] = itemRect  # Rectangle data is changed
                    self.itemRectArray[col][row] = itemRect
                    screen.blit(itemImage, itemRect)
                    itemIndex += 1

            xPos = 1000
            yPos = yPos + TILESIZE * 2

    def selectChestSlot(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        for row in range(self.rows):
            for col in range(self.columns):
                if self.chestArrayRepresentation[col][row].collidepoint(mouseX, mouseY):
                    if self.chestArrayRepresentation[col][row] == self.itemRectArray[col][row]:
                        pass
                    for c in range(self.columns):
                        for r in range(self.rows):
                            self.selectedChestSlot[c][r] = False
                    self.selectedChestSlot[col][row] = not self.selectedChestSlot[col][row]

    def moveItemsAroundChest(self):
        pass


class Camera(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(0, 0)

    def apply(self, sprite):
        return sprite.rect.move(self.offset)

    def update(self, targetGroup):
        if targetGroup.sprites():
            targetSprite = targetGroup.sprites()[0]
            targetCenter = pygame.math.Vector2(targetSprite.rect.x + targetSprite.rect.width / 2,
                                               targetSprite.rect.y + targetSprite.rect.height / 2)
            self.offset = pygame.math.Vector2(self.displaySurface.get_width() / 2,
                                              self.displaySurface.get_height() / 2) - targetCenter
