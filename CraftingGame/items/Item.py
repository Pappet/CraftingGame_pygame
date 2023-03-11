import pygame

from CraftingGame.items.ItemTypes import ItemType


class Item:
    def __init__(self, id, name, image_path, category: ItemType, description, stackable):
        self.id = id
        self.name = name
        self.image = pygame.image.load(image_path)
        self.scaled_image = pygame.transform.scale(self.image, (self.image.get_width()*2, self.image.get_height()*2))
        self.category = category
        self.description = description
        self.stackable = stackable

    def get_image(self):
        return self.scaled_image

    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

    def get_description(self):
        return self.description
