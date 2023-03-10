import pygame
import helper.color as color
from menus.Inventory import Inventory
from items.ItemsManager import ItemsManager
from menus.MenuManager import MenuManager
from Recipes.RecipeManager import RecipeManager

pygame.init()

# ---- Variables --------------------------------------------------------
screen_width = 1200
screen_height = 800
screen_title = "Crafting Empire"
running = True

inventory_rows = 5
inventory_cols = 8
inventory_tile = "Inventory"
inventory_slot_size = 32
menu_spacing = 10
menu_title_spacing = 24
menu_font_size = 18

# ---- various --------------------------------------------------------
clock = pygame.time.Clock()

# ---- Pygame Screen --------------------------------------------------------
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(screen_title)
window_position = screen.get_rect().center
pygame.display.window_pos = window_position

# ---- create menus and menu manager --------------------------------------------------------
menu_manager = MenuManager()
inventory = Inventory(menu_spacing, screen_height//2-menu_spacing, screen_width//2, screen_height//2, inventory_slot_size, menu_spacing, inventory_rows,
                      inventory_cols, menu_spacing, menu_font_size, menu_title_spacing, inventory_tile, True)

menu_manager.add_menu(inventory)

# ---- create inventory and items --------------------------------------------------------
items_manager = ItemsManager()
items_manager.load_items("./items/items.json")

item1 = items_manager.get_item_by_id(0)
item2 = items_manager.get_item_by_id(1)
item3 = items_manager.get_item_by_id(2)
item4 = items_manager.get_item_by_id(3)
item5 = items_manager.get_item_by_id(4)

inventory.add_item(item1, 250)
inventory.add_item(item2, 300)
inventory.add_item(item3, 150)
inventory.add_item(item4, 1)
inventory.add_item(item5, 1)

print(inventory.get_items())

# ---- Rezepte --------------------------------------------------------
recipe_manager = RecipeManager(inventory, items_manager)
recipe_manager.load_recipes("./Recipes/recipes.json")
# print(recipe_manager.get_recipes_by_ingredient("Holz"))
# print(recipe_manager.can_craft(recipe_manager.get_recipe_by_name("Steinaxt")))
recipe_manager.craft(recipe_manager.get_recipe_by_name("Steinaxt"))
print(inventory.get_items())

# ---- Haupt-Schleife --------------------------------------------------------
while running:
    # Event-Handling
    for event in pygame.event.get():
        # the close button on the window was pressed
        if event.type == pygame.QUIT:
            running = False
        menu_manager.update(event)

    # clear the screen with black
    screen.fill(color.black)
    # draw inventory
    menu_manager.draw(screen)

    pygame.display.update()
    # limit the frame rate to 60 FPS
    clock.tick(60)

# Stop the Game and close the window
pygame.quit()
quit()
