import json

from CraftingGame.items.item import Item


class ItemsManager:
    def __init__(self):
        self.items = []

    def load_items(self, items_file_path):
        with open(items_file_path, 'r') as f:
            items_data = json.load(f)

        for item_data in items_data:
            item = Item(item_data['id'], item_data['name'], item_data['image_path'],
                        item_data['category'], item_data['description'], item_data['stackable'])
            self.items.append(item)

    def get_item_by_id(self, item_id):
        for item in self.items:
            if item.id == item_id:
                return item

        return None
