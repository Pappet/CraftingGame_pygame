from Inventory.item_types import ItemType
import pygame
import random
import helper.color as color


class Item():
    def __init__(self, name, category: ItemType):
        self.name = name
        # self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.Surface((32, 32))
        self.image.fill(color.random_color())
        self.category = category

    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

    def get_image(self):
        return self.image
