import pygame
import helper.color as color
from Inventory.inventory import Inventory
from Inventory.item import Item
from Inventory.item_types import ItemType


pygame.init()

# ---- Variables --------------------------------------------------------
screen_width = 1200
screen_height = 800
screen_title = "Crafting Empire"
running = True

inventory_rows = 4
inventory_cols = 5
inventory_tile = "Inventory"
menu_edge_spacing = 12
menu_title_spacing = 24

# ---- Pygame Screen --------------------------------------------------------
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(screen_title)
window_position = screen.get_rect().center
pygame.display.window_pos = window_position

# ---- create inventory and items --------------------------------------------------------
inventory = Inventory(0, 0, 32, 10, inventory_rows,
                      inventory_cols, menu_edge_spacing, menu_title_spacing, inventory_tile)
items = [Item("Item {}".format(i), ItemType.RESSOURCE) for i in range(6)]

# add items to inventory
for item in items:
    inventory.add_item(item)

# ---- Haupt-Schleife --------------------------------------------------------
while running:
    # Event-Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw inventory
    screen.fill(color.black)
    inventory.draw(screen)
    pygame.display.update()

pygame.quit()
quit()
