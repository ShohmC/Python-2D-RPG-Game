# Inventory.py
import pygame
from sprites import *
from config import *
from Player import *
from Items import *


class ItemUpgradeMenu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.isItemUpdateMenuEnable = False
        self.cooldown = 0
        self.cooldownTime = 200
        self.rectangleUpgradeButton = []
    def drawMenu(self, screen, player, sword, bow):
        mouseX, mouseY = pygame.mouse.get_pos()
        initialRectX = 400
        initialRectY = 280
        mainSurface = pygame.Surface((960, 750), pygame.SRCALPHA)
        mainSurface.fill((0, 0, 0, 128))

        for i in range(3):
            self.rectangleUpgradeButton.append(
                pygame.draw.rect(screen, (0, 129, 255), (initialRectX, initialRectY, 75, 35)))
            initialRectY += 100

        screen.blit(pygame.font.Font(None, 64).render("Upgrade Menu", True, (0, 0, 0)), (200, 135))
        screen.blit(pygame.font.Font(None, 64).render(f"Skill Points: {player.upgradePoints}", True, (0, 0, 0)),
                    (750, 135))
        screen.blit(pygame.font.Font(None, 64).render("Sword", True, (0, 0, 0)), (200, 275))
        screen.blit(pygame.font.Font(None, 64).render("Bow", True, (0, 0, 0)), (200, 375))
        screen.blit(pygame.font.Font(None, 64).render("Health", True, (0, 0, 0)), (200, 475))
        screen.blit(pygame.font.Font(None, 24).render(f"{sword.damage}", True, (0, 0, 0)), (432, 290))
        screen.blit(pygame.font.Font(None, 24).render(f"{bow.damage}", True, (0, 0, 0)), (428, 390))
        screen.blit(pygame.font.Font(None, 24).render(f"{player.health}", True, (0, 0, 0)), (422, 490))
        screen.blit(mainSurface, (160, 105))

        for events in pygame.event.get():
            if events.type == pygame.MOUSEBUTTONDOWN:
                if self.rectangleUpgradeButton[0].collidepoint(mouseX, mouseY) and player.upgradePoints > 0:
                    sword.damage += 1
                    player.upgradePoints -= 1
                    print(sword.damage)
                if self.rectangleUpgradeButton[1].collidepoint(mouseX, mouseY) and player.upgradePoints > 0:
                    bow.damage += 0.5
                    player.upgradePoints -= 1
                if self.rectangleUpgradeButton[2].collidepoint(mouseX, mouseY) and player.upgradePoints > 0:
                    player.health += 5
                    player.upgradePoints -= 1

    def onMenuOpen(self):
        keys = pygame.key.get_pressed()
        currentTime = pygame.time.get_ticks()
        if currentTime - self.cooldown > self.cooldownTime:
            if keys[pygame.K_m]:
                self.isItemUpdateMenuEnable = not self.isItemUpdateMenuEnable
                self.cooldown = currentTime


class Hotbar(pygame.sprite.Sprite):
    def __init__(self, unselectedHotbar, selectedHotbar):
        pygame.sprite.Sprite.__init__(self)
        self.unselectedHotbar = unselectedHotbar
        self.selectedHotbar = selectedHotbar
        self.currentSlotIndex = 0
        self.hotbarSlots = [None] * 9
        self.hotbarXPositions = []
        self.swordItem = Sword(5)
        self.bowItem = Bow(2)

    def drawHotbar(self, screen):
        initialX = 354
        initialY = 850
        for i in range(len(self.hotbarSlots)):
            hotbarSlot = pygame.Rect(initialX, initialY, TILESIZE * 2, TILESIZE * 2)
            self.hotbarSlots[i] = hotbarSlot
            pygame.draw.rect(screen, (0, 0, 0), hotbarSlot)
            if i == self.currentSlotIndex:
                screen.blit(self.selectedHotbar, self.hotbarSlots[i])
            else:
                screen.blit(self.unselectedHotbar, (initialX, initialY))
            initialX += TILESIZE * 2
        self.hotbarSlots[0] = self.swordItem.image.get_rect(center=self.hotbarSlots[0].center)
        self.hotbarSlots[1] = self.bowItem.image.get_rect(center=self.hotbarSlots[1].center)
        screen.blit(self.swordItem.image, self.hotbarSlots[0])
        screen.blit(self.bowItem.image, self.hotbarSlots[1])

    def selectNextSlot(self, increment):
        self.currentSlotIndex = (self.currentSlotIndex - increment) % len(self.hotbarSlots)


class Inventory(pygame.sprite.Sprite):
    def __init__(self, inventorySlotImage, inventorySelectedSlotImage):
        pygame.sprite.Sprite.__init__(self)
        self.inventorySlotImage = inventorySlotImage
        self.inventorySelectedSlotImage = inventorySelectedSlotImage
        self.isInventoryEnabledOrDisabled = False
        self.cooldown = 0
        self.cooldownTime = 200
        self.counter = 0
        self.temporarySlot = False

        self.rows = 9
        self.columns = 3
        self.inventory = [[None for _ in range(self.rows)] for _ in range(self.columns)]
        self.selectedSlot = [[False for _ in range(self.rows)] for _ in range(self.columns)]

    def enableInventory(self):
        keys = pygame.key.get_pressed()
        currentTime = pygame.time.get_ticks()
        if currentTime - self.cooldown > self.cooldownTime:
            if keys[pygame.K_i]:
                self.isInventoryEnabledOrDisabled = not self.isInventoryEnabledOrDisabled
                self.cooldown = currentTime

    def drawInventory(self, screen):
        xPos = 354
        yPos = 754
        for row in range(self.columns):
            for col in range(self.rows):
                slot = pygame.Rect(xPos, yPos, TILESIZE * 2, TILESIZE * 2)
                self.inventory[row][col] = slot
                pygame.draw.rect(screen, (0, 0, 0), slot)
                xPos = xPos + TILESIZE * 2

                if self.selectedSlot[row][col]:
                    screen.blit(self.inventorySelectedSlotImage, self.inventory[row][col])
                else:
                    screen.blit(self.inventorySlotImage, self.inventory[row][col])
            xPos = 354
            yPos = yPos - TILESIZE * 2

    def selectInventorySlot(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        for row in range(self.columns):
            for col in range(self.rows):
                if self.inventory[row][col].collidepoint(mouseX, mouseY):
                    for r in range(self.columns):
                        for c in range(self.rows):
                            self.selectedSlot[r][c] = False
                    self.selectedSlot[row][col] = not self.selectedSlot[row][col]
