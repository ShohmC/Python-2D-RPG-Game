# main.py
import time
import pygame
from pygame.locals import *
from config import *
from Inventory import *
from sprites import *
from Player import *
from Enemies import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

tilesDictionary = {
    "Grass Tile": "Tiles/GrassTile.png",
    "Grass Ledge Up": "Tiles/GrassLedgeUp.png",
    "Grass Ledge Down": "Tiles/GrassLedgeDown.png",
    "Grass Ledge Left": "Tiles/GrassLedgeLeft.png",
    "Grass Ledge Right": "Tiles/GrassLedgeRight.png",

    "Dirt Tile": "Tiles/DirtTile.png",
    "Dirt Ledge Up": "Tiles/DirtLedgeUp.png",
    "Dirt Ledge Down": "Tiles/DirtLedgeDown.png",
    "Dirt Ledge Left": "Tiles/DirtLedgeLeft.png",
    "Dirt Ledge Right": "Tiles/DirtLedgeRight.png",

    "Hotbar": "Inventory/Hotbar.png",
    "Selected Hotbar": "Inventory/SelectedHotbar.png",

    "Wall Tile": "Tiles/WallTile.png",
    "Water Tile": "Tiles/WaterTile.png",
    "Tree Tile": "Tiles/TreeTile.png",
    "Chests": "Items/Chest.png"
}

hotbarTransformScale = pygame.transform.scale(pygame.image.load(tilesDictionary["Hotbar"]).convert_alpha(),
                                              (TILESIZE * 2, TILESIZE * 2))
selectedHotbarTransformScale = pygame.transform.scale(
    pygame.image.load(tilesDictionary["Selected Hotbar"]).convert_alpha(),
    (TILESIZE * 2, TILESIZE * 2))

swordItem = Sword(5)
bowItem = Bow(3)


class Game:
    def __init__(self):
        self.lastClickTime = 0
        self.doubleClickThreshold = .2

        self.clock = pygame.time.Clock()
        self.running = True
        self.activeItem = None

        self.tileSpriteGroup = pygame.sprite.LayeredUpdates()
        self.collisionTileSpriteGroup = pygame.sprite.LayeredUpdates()
        self.enemySpriteGroup = pygame.sprite.LayeredUpdates()
        self.collisionEnemySpriteGroup = pygame.sprite.LayeredUpdates()
        self.playerSpriteGroup = pygame.sprite.LayeredUpdates()
        self.chestSpriteGroup = pygame.sprite.LayeredUpdates()
        self.itemSpriteGroup = pygame.sprite.LayeredUpdates()
        self.camera = Camera()
        self.hotbar = Hotbar(hotbarTransformScale, selectedHotbarTransformScale)
        self.inventory = Inventory(hotbarTransformScale, selectedHotbarTransformScale)
        self.itemUpgradeMenu = ItemUpgradeMenu()
        self.bowAttack = bowAttack(0, 0, 0, 0)
        self.swordAttack = swordAttack(0, 0)

    def drawTile(self, column, tileLetter, j, i, image, layer, isACollisionTile, tileSizeMultiplier):
        if column == tileLetter:
            self.tileName = Tiles(screen, j * TILESIZE, i * TILESIZE, image, layer, tileSizeMultiplier)
            self.tileSpriteGroup.add(self.tileName)
            if isACollisionTile == True:
                self.collisionTileSpriteGroup.add(self.tileName)
        if column == "C":
            self.chestTile = Chest(screen, j * TILESIZE, i * TILESIZE, image, layer, tileSizeMultiplier,
                                   [Sword(5), Bow(3)])
            self.chestSpriteGroup.add(self.chestTile)
            for items in self.chestTile.itemsInsideChest:
                self.itemSpriteGroup.add(items)

    def spawnEnemy(self, enemyName, j, i, health):
        self.enemies = enemyName(screen, j * TILESIZE, i * TILESIZE, health)
        self.enemySpriteGroup.add(self.enemies)
        self.collisionEnemySpriteGroup.add(self.enemies)

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                grassTiles = Tiles(screen, j * TILESIZE, i * TILESIZE, tilesDictionary["Grass Tile"], GRASS_LAYER,
                                   TILESIZE_MULTIPLIER)
                self.tileSpriteGroup.add(grassTiles)
                # Fun fact since technically everything is drawn as grass then the tiles are drawn over due to layering
                # if grass were a collision box, then all tiles would be collided bc grass is technically under all tiles
                if column == "P":
                    self.playerCharacter = Player(screen, j * TILESIZE, i * TILESIZE)
                    self.playerSpriteGroup.add(self.playerCharacter)
                if column == "E":
                        self.spawnEnemy(Bat, j, i, 20)
                if column == "L":
                    self.spawnEnemy(testEnemy, j, i, 10023)
                self.drawTile(column, "1", j, i, tilesDictionary["Grass Ledge Up"], 1, False, TILESIZE_MULTIPLIER)
                self.drawTile(column, "2", j, i, tilesDictionary["Grass Ledge Down"], 1, False, TILESIZE_MULTIPLIER)
                self.drawTile(column, "3", j, i, tilesDictionary["Grass Ledge Left"], 1, False, TILESIZE_MULTIPLIER)
                self.drawTile(column, "4", j, i, tilesDictionary["Grass Ledge Right"], 1, False, TILESIZE_MULTIPLIER)
                self.drawTile(column, "D", j, i, tilesDictionary["Dirt Tile"], 2, False, TILESIZE_MULTIPLIER)
                self.drawTile(column, "5", j, i, tilesDictionary["Dirt Ledge Up"], 1, False, TILESIZE_MULTIPLIER)
                self.drawTile(column, "6", j, i, tilesDictionary["Dirt Ledge Down"], 1, False, TILESIZE_MULTIPLIER)
                self.drawTile(column, "7", j, i, tilesDictionary["Dirt Ledge Left"], 1, False, TILESIZE_MULTIPLIER)
                self.drawTile(column, "8", j, i, tilesDictionary["Dirt Ledge Right"], 1, False, TILESIZE_MULTIPLIER)
                self.drawTile(column, "w", j, i, tilesDictionary["Wall Tile"], 2, True, TILESIZE_MULTIPLIER)
                self.drawTile(column, "W", j, i, tilesDictionary["Water Tile"], 2, True, TILESIZE_MULTIPLIER)
                self.drawTile(column, "T", j, i, tilesDictionary["Tree Tile"], 2, True, TILESIZE_MULTIPLIER * 2)
                self.drawTile(column, "C", j, i, tilesDictionary["Chests"], 2, True, TILESIZE_MULTIPLIER)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == MOUSEWHEEL:
                if event.y > 0:
                    self.hotbar.selectNextSlot(1)
                elif event.y < 0:
                    self.hotbar.selectNextSlot(-1)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                currentTime = time.time()
                timeSinceLastClick = currentTime - self.lastClickTime

                if (not self.inventory.isInventoryEnabledOrDisabled and not self.chestTile.openChestBoolean and
                        self.hotbar.currentSlotIndex == 1):
                    self.bowAttack.attack(self.playerCharacter.counterBooleans[0],
                                          self.playerCharacter.counterBooleans[1],
                                          self.playerCharacter.counterBooleans[2],
                                          self.playerCharacter.counterBooleans[3],
                                          self.playerCharacter.rect.x, self.playerCharacter.rect.y)

                if (not self.inventory.isInventoryEnabledOrDisabled and not self.chestTile.openChestBoolean and
                        self.hotbar.currentSlotIndex == 0):
                    self.swordAttack.attack(self.playerCharacter.counterBooleans[0],
                                            self.playerCharacter.counterBooleans[1],
                                            self.playerCharacter.counterBooleans[2],
                                            self.playerCharacter.counterBooleans[3],
                                            self.playerCharacter.rect.x, self.playerCharacter.rect.y)

                if self.inventory.isInventoryEnabledOrDisabled:
                    self.inventory.selectInventorySlot()

                    for row in range(self.inventory.columns):
                        for col in range(self.inventory.rows):
                            if (self.inventory.selectedSlot[row][col] == any(
                                    self.inventory.selectedSlot[col][row] for
                                    col in range(self.inventory.columns) for
                                    row in range(self.inventory.rows))
                                    and timeSinceLastClick <= self.doubleClickThreshold):
                                self.inventory.selectedSlot[row][col] = False

                if self.chestTile.openChestBoolean:
                    self.chestTile.selectChestSlot()

                    for row in range(self.chestTile.rows):
                        for col in range(self.chestTile.columns):
                            if (self.chestTile.selectedChestSlot[col][row] == any(
                                    self.chestTile.selectedChestSlot[col][row] for
                                    col in range(self.chestTile.columns) for
                                    row in range(self.chestTile.rows))
                                    and timeSinceLastClick <= self.doubleClickThreshold):
                                self.chestTile.selectedChestSlot[col][row] = False

                self.lastClickTime = currentTime

    def update(self):
        self.playerSpriteGroup.update(self.collisionTileSpriteGroup, self.collisionEnemySpriteGroup, self.hotbar)
        self.camera.update(self.playerSpriteGroup)
        for chests in self.chestSpriteGroup.sprites():
            chests.onChestOpen(self.playerCharacter)
        for enemies in self.enemySpriteGroup.sprites():
            enemies.updateMovement(self.playerCharacter.rect, self.collisionTileSpriteGroup, self.playerSpriteGroup)

        self.bowAttack.update(self.playerCharacter.counterBooleans[0], self.playerCharacter.counterBooleans[1],
                              self.playerCharacter.counterBooleans[2], self.playerCharacter.counterBooleans[3],
                              self.collisionTileSpriteGroup, self.collisionEnemySpriteGroup,
                              self.playerCharacter.rect.x, self.playerCharacter.rect.y, bowItem)

        self.swordAttack.update(self.collisionTileSpriteGroup, self.collisionEnemySpriteGroup, swordItem)

        self.inventory.enableInventory()
        self.itemUpgradeMenu.onMenuOpen()
        self.tileSpriteGroup.update()

    def draw(self):
        for tiles in self.tileSpriteGroup.sprites():
            screen.blit(tiles.image, self.camera.apply(tiles))

        for players in self.playerSpriteGroup.sprites():
            screen.blit(players.image, self.camera.apply(players))
            players.drawPlayerHealthBar(screen)
            players.drawPlayerExpBar(screen)

        for enemy in self.enemySpriteGroup.sprites():
            screen.blit(enemy.image, self.camera.apply(enemy))
            enemy.drawHealthBar(screen, self.camera)

        if self.inventory.isInventoryEnabledOrDisabled:
            self.inventory.drawInventory(screen)

        if self.itemUpgradeMenu.isItemUpdateMenuEnable:
            self.itemUpgradeMenu.drawMenu(screen, self.playerCharacter, swordItem, bowItem)

        if self.chestTile.openChestBoolean:
            self.chestTile.drawChestSlots(screen, pygame.transform.scale(
                pygame.image.load(tilesDictionary["Selected Hotbar"]).convert_alpha(),
                (TILESIZE * 2, TILESIZE * 2)),
                                          pygame.transform.scale(
                                              pygame.image.load(tilesDictionary["Hotbar"]).convert_alpha(),
                                              (TILESIZE * 2, TILESIZE * 2)))
        self.hotbar.drawHotbar(screen)
        self.bowAttack.draw(screen, self.camera)
        self.swordAttack.draw(screen, self.camera)

        self.clock.tick(FPS)
        pygame.display.flip()

    def main(self):
        while self.running:
            screen.fill(RED)
            self.events()
            self.update()
            self.draw()


g = Game()
g.createTilemap()
while g.running:
    g.main()
pygame.quit()
