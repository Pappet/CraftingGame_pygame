import json


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
        for recipe in self.recipes:
            if recipe["name"] == name:
                return recipe
        return None

    def get_recipes_by_ingredient(self, ingredient):
        results = []
        for recipe in self.recipes:
            for item, amount in recipe["ingredients"].items():
                if item == ingredient:
                    results.append(recipe)
        return results

    def can_craft(self, recipe) -> bool:
        if recipe in self.recipes:
            for item, amount in recipe["ingredients"].items():
                if self.inventory.get_items().get(item, 0) < amount:
                    print(f"Not enough Ingredients for {recipe['name']} in Inventory!")
                    return False
                return True
        self.message_menu.add_message(f"This is an invalid Recipe!")
        return False

    def craft(self, recipe) -> bool:
        if self.can_craft(recipe):
            self.message_menu.add_message(f"You are crafting a {recipe['name']}")
            for ingredients_item, ingredients_amount in recipe["ingredients"].items():
                item_object = self.item_manager.get_item_by_name(ingredients_item)
                self.inventory.remove_item(item_object, ingredients_amount)
                self.message_menu.add_message(f"Removed {ingredients_amount} of {ingredients_item}!")

            for result_item, result_amount in recipe["results"].items():
                result_object = self.item_manager.get_item_by_name(result_item)
                self.inventory.add_item(result_object, result_amount)
                self.message_menu.add_message(f"Added {result_amount} of {result_item}!")
            return True
        self.message_menu.add_message(f"Can't craft this recipe!")
        return False
