import json

class RecipeManager:
    def __init__(self):
        self.recipes = []

    def load_recipes(self, recipes_file_path):
        with open(recipes_file_path, 'r')as f:
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

    def can_craft(self, recipe, inventory) -> bool:
        if recipe in self.recipes:
            for item, amount in recipe["ingredients"].items():
                if inventory.get(item, 0) < amount:
                    return False
                return True
        return False
