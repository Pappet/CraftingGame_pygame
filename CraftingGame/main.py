import pygame

import helper.color as color
from menus.Inventory import Inventory
from items.ItemsManager import ItemsManager
from menus.MenuManager import MenuManager
from menus.Menu import Menu
from menus.CraftingMenu import CraftingMenu
from menus.ButtonManager import ButtonManager
from menus.MessageMenu import MessageMenu
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
inventory_slot_size = 64
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
button_manager = ButtonManager()
top_left = (0, 0)
top_right = (screen_width//2, 0)
bottom_left = (0, screen_height//2)
bottom_right = (screen_width//2, screen_height//2)

message_menu = MessageMenu(bottom_right[0], bottom_right[1], screen_width//2, screen_height//2, menu_spacing, menu_font_size, menu_title_spacing, "Nachrichten", True, screen, button_manager)

# ---- create inventory and items --------------------------------------------------------
items_manager = ItemsManager()
items_manager.load_items("./items/items.json")

inventory = Inventory(bottom_left[0], bottom_left[1], screen_width//2, screen_height//2, inventory_slot_size, menu_spacing, inventory_rows,
                      inventory_cols, menu_spacing, menu_font_size, menu_title_spacing, inventory_tile, True, message_menu, button_manager)

# ---- Rezepte --------------------------------------------------------
recipe_manager = RecipeManager(inventory, items_manager, message_menu)
recipe_manager.load_recipes("./Recipes/recipes.json")

# ---- create menus and menu manager --------------------------------------------------------
crafting_menu = CraftingMenu(top_left[0], top_left[1], screen_width//2, screen_height//2, menu_spacing, menu_font_size, menu_title_spacing, "Herstellung", True, inventory, items_manager, message_menu, button_manager)
map_menu = Menu(top_right[0], top_right[1], message_menu, button_manager, screen_width//2, screen_height//2, menu_spacing, menu_font_size, menu_title_spacing, "Karte", True)

menu_manager.add_menu(inventory)
menu_manager.add_menu(crafting_menu)
menu_manager.add_menu(map_menu)
menu_manager.add_menu(message_menu)

# ---- Manipulate the Inventory --------------------------------------------------------
for item in items_manager.items:
    if item.stackable:
        inventory.add_item(item, 99)
    else:
        inventory.add_item(item, 1)

# print(inventory.get_items())
print(recipe_manager.get_recipes_by_ingredient("Ton"))
# print(recipe_manager.can_craft(recipe_manager.get_recipe_by_name("Steinaxt")))
# print(recipe_manager.crafting())
recipe_manager.craft(recipe_manager.get_recipe_by_name("ungebrannte Tonschale"))
recipe_manager.craft(recipe_manager.get_recipe_by_name("gebrannte Tonschale"))
# print(inventory.get_items())

# ---- Haupt-Schleife --------------------------------------------------------
while running:
    # Event-Handling
    for event in pygame.event.get():
        # the close button on the window was pressed
        if event.type == pygame.QUIT:
            running = False
        menu_manager.update(event)
        button_manager.handle_clicks(event)

    # clear the screen with black
    screen.fill(color.black)
    # draw inventory
    menu_manager.draw(screen)
    button_manager.draw_buttons(screen)

    pygame.display.update()
    # limit the frame rate to 60 FPS
    clock.tick(60)

# Stop the Game and close the window
pygame.quit()
quit()
