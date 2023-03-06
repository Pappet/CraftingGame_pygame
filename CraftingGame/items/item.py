import pygame

from CraftingGame.items.item_types import ItemType


class Item:
    def __init__(self, id, name, image_path, category: ItemType, description, stackable):
        self.id = id
        self.name = name
        self.image = pygame.image.load(image_path)
        self.category = category
        self.description = description
        self.stackable = stackable

    def get_image(self):
        return self.image

    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

    def get_description(self):
        return self.description
