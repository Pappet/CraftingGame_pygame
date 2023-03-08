import json
from typing import List, Optional

from CraftingGame.items.Item import Item
from CraftingGame.items.ItemTypes import ItemType


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

    def get_item_by_id(self, item_id) -> Optional[Item]:
        for item in self.items:
            if item.id == item_id:
                return item

        return None

    def get_items_by_category(self, category: ItemType) -> List[Item]:
        result = []
        for item in self.items:
            if item.category == category:
                result.append(item)
        return result

    def get_items_by_name(self, name: str) -> List[Item]:
        result = []
        for item in self.items:
            if name.lower() in item.name.lower():
                result.append(item)
        return result

    def get_item_by_name(self, name):
        for item in self.items:
            if item.name == name:
                return item
        return None
