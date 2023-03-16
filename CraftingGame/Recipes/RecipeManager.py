import json
import math


class RecipeManager:
    def __init__(self, inventory, item_manager, message_menu):
        self.recipes = []
        self.inventory = inventory
        self.item_manager = item_manager
        self.message_menu = message_menu

    def load_recipes(self, recipes_file_path):
        with open(recipes_file_path, 'r') as f:
            self.recipes = json.load(f)

    def get_recipe_by_name(self, name):
        recipe_dict = {recipe["name"]: recipe for recipe in self.recipes}
        return recipe_dict.get(name)

    def get_recipes_by_ingredient(self, ingredient):
        return [recipe for recipe in self.recipes if ingredient in recipe["ingredients"]]

    def can_craft(self, recipe) -> bool:
        if recipe in self.recipes:
            ingredients = recipe["ingredients"]
            inventory_items = self.inventory.get_items()
            free_space = self.inventory.get_free_inventory_space()
            for item, amount in ingredients.items():
                if inventory_items.get(item, 0) < amount:
                    self.message_menu.add_message(f"Not enough Ingredients for {recipe['name']} in Inventory!")
                    return False
                elif free_space < math.ceil(amount / self.inventory.max_stack_size):
                    self.message_menu.add_message(f"Not enough Inventory Space for {recipe['name']}!")
                    return False
            return True
        else:
            self.message_menu.add_message(f"This is an invalid Recipe!")
            return False

    def craft(self, recipe) -> bool:
        if self.can_craft(recipe):
            self.message_menu.add_message(f"You are crafting a {recipe['name']}")
            ingredients = recipe["ingredients"]
            results = recipe["results"]
            inventory_items = self.inventory.get_items()
            for item, amount in ingredients.items():
                if inventory_items.get(item, 0) < amount:
                    self.message_menu.add_message(f"Not enough Ingredients for {recipe['name']} in Inventory!")
                    return False
            for item, amount in ingredients.items():
                item_object = self.item_manager.get_item_by_name(item)
                self.inventory.remove_item(item_object, amount)
            for item, amount in results.items():
                item_object = self.item_manager.get_item_by_name(item)
                self.inventory.add_item(item_object, amount)
            self.message_menu.add_message(f"Crafted {recipe['name']} successfully!")
            return True
        else:
            self.message_menu.add_message(f"Can't craft this recipe!")
            return False
