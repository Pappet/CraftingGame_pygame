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
menu_edge_spacing = 10
menu_title_spacing = 24

# ---- Pygame Screen --------------------------------------------------------
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(screen_title)
window_position = screen.get_rect().center
pygame.display.window_pos = window_position

# ---- create inventory and items --------------------------------------------------------
inventory = Inventory(0, 0, 32, 10, inventory_rows,
                      inventory_cols, menu_edge_spacing, menu_title_spacing, inventory_tile)

item1 = Item("Sword", ItemType.WEAPON, "A sharp sword for combat.")
item2 = Item("Potion", ItemType.POTION,
             "A magical potion that heals you.")

inventory.add_item(item1)
inventory.add_item(item2)

clock = pygame.time.Clock()
selected_item = None

# ---- Haupt-Schleife --------------------------------------------------------
while running:
    # Event-Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
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
                # get the grid coordinates of the click
                print(event.pos)
                grid_x = (
                    event.pos[0] - inventory.x) // (inventory.slot_size + inventory.slot_spacing)
                grid_y = (event.pos[1] - inventory.y -
                          inventory.title_spacing - inventory.edge_spacing) // (inventory.slot_size + inventory.slot_spacing - (inventory.edge_spacing//2))
                print((grid_x, grid_y))
                # check if the click was inside the inventory
                if 0 <= grid_x < inventory.cols and 0 <= grid_y < inventory.rows:
                    # get the selected slot
                    slot = inventory.slots[grid_y * inventory.cols + grid_x]
                    # get the item in the slot, if any
                    selected_item = inventory.get_selected_item(event.pos)
                    # print the item information
                    if selected_item is not None:
                        print("Selected item:", selected_item.name)
                        print("Description:", selected_item.description)

    # draw inventory
    screen.fill(color.black)
    inventory.draw(screen)

    # draw the selected item's info
    if selected_item is not None:
        font = pygame.font.Font(None, 18)
        name_text = font.render(selected_item.name, True, (255, 255, 255))
        desc_text = font.render(
            selected_item.description, True, (255, 255, 255))
        image_item = selected_item.get_image()
        screen.blit(image_item, (inventory.x +
                    inventory.width + 20, inventory.y))
        screen.blit(name_text, (inventory.x +
                    inventory.width + 20, inventory.y + 40))
        screen.blit(desc_text, (inventory.x +
                    inventory.width + 20, inventory.y + 60))

    pygame.display.update()
    clock.tick(60)  # limit the frame rate to 60 FPS

pygame.quit()
quit()
