from CraftingGame.menus.menu import Menu


class Item_info(Menu):
    def __init__(self, x, y, width=100, height=100, edge_spacing=10, title_spacing=30, title="Default"):
        super().__init__(x, y, width, height, edge_spacing, title_spacing, title)
