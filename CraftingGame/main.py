import pygame
import helper.color as color
from menus.inventory import Inventory
from menus.item import Item
from menus.item_types import ItemType
from menus.menu import Menu
from menus.menus_manager import menus_manager

pygame.init()

# ---- Variables --------------------------------------------------------
screen_width = 1200
screen_height = 800
screen_title = "Crafting Empire"
running = True

inventory_rows = 4
inventory_cols = 5
inventory_tile = "Inventory"
inventory_slot_size = 32
menu_spacing = 10
menu_title_spacing = 24
menu_font_size = 18

# ---- Pygame Screen --------------------------------------------------------
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(screen_title)
window_position = screen.get_rect().center
pygame.display.window_pos = window_position
# ---- create inventory and items --------------------------------------------------------
menu_manager = menus_manager()


# ---- create inventory and items --------------------------------------------------------
inventory = Inventory(0, 0, 100, 100, inventory_slot_size, menu_spacing, inventory_rows,
                      inventory_cols, menu_spacing, menu_title_spacing, inventory_tile)

test_menu = Menu(300, 300, 200, 200, menu_spacing, menu_title_spacing, "TEST")

menu_manager.add_menu(inventory)
menu_manager.add_menu(test_menu)

item1 = Item("Sword", ItemType.WEAPON, "A sharp sword for combat.")
item2 = Item("Potion", ItemType.POTION, "A magical potion that heals you.")

inventory.add_item(item1)
inventory.add_item(item2)

clock = pygame.time.Clock()
selected_item = None

# ---- Haupt-Schleife --------------------------------------------------------
while running:
    # Event-Handling
    for event in pygame.event.get():
        # the close button on the window was pressed
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # testing the inventory - add and remove an test item
            if event.key == pygame.K_a:
                if inventory.get_free_inventory_space() > 0:
                    inventory.add_item(
                        Item("TEST", ItemType.RESSOURCE, "THIS IS A TEST ITEM!"))
            elif event.key == pygame.K_r:
                if inventory.get_free_inventory_space() < inventory.get_inventory_space():
                    inventory.remove_item(
                        inventory.get_last_filled_slot().item)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # check if left mouse button was pressed
            if event.button == 1:
                selected_item_index = False
                # Go through all slots and check if the position of the click is within in one slot
                for slot in inventory.slots:
                    if slot.is_clicked(event.pos):
                        # slot was clicked. Set the helper index to true
                        selected_item_index = True
                        # set the item in slot
                        selected_item = slot.item_in_slot()
                    # if no slot was clicked set it to None
                    if selected_item_index is False:
                        selected_item = None

    # clear the screen with black
    screen.fill(color.black)
    # draw inventory
    menu_manager.draw(screen)

    # draw the selected item's info
    if selected_item is not None:
        font = pygame.font.Font(None, menu_font_size)
        name_text = font.render(selected_item.name, True, color.white)
        desc_text = font.render(
            selected_item.description, True, color.white)
        image_item = selected_item.get_image()
        screen.blit(image_item, (inventory.x +
                    inventory.width + menu_spacing, inventory.y))
        screen.blit(name_text, (inventory.x +
                    inventory.width + menu_spacing, inventory.y + 40))
        screen.blit(desc_text, (inventory.x +
                    inventory.width + menu_spacing, inventory.y + 60))

    pygame.display.update()
    # limit the frame rate to 60 FPS
    clock.tick(60)

# Stop the Game and close the window
pygame.quit()
quit()
