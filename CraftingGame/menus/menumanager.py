class MenuManager:
    def __init__(self) -> None:
        self.menus = []

    def add_menu(self, menu):
        self.menus.append(menu)

    def remove_menu(self, menu):
        self.menus.remove(menu)

    def draw(self, screen):
        for menu in self.menus:
            menu.draw(screen)

    def update(self, event):
        for menu in self.menus:
            menu.update(event)
