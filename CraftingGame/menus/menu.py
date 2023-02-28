import pygame
import helper.color as color


class Menu:
    def __init__(self, x, y, width=100, height=100, edge_spacing=10, menu_font_size=18, title_spacing=30, title="Default", active=False):
        self.x = x
        self.y = y
        self.edge_spacing = edge_spacing
        self.title_spacing = title_spacing
        self.title = title
        self.width = width
        self.height = height
        self.menu_font_size = menu_font_size
        self.image = pygame.Surface((self.width, self.height))
        self.bg_color = color.gray
        # change the font to a system font that is available on your system
        self.font = pygame.font.SysFont("arial", self.title_spacing)
        self.active = active

    def toogle_menu(self):
        self.active = not self.active

    def get_image(self):
        return self.image

    def draw(self, surface):
        if self.active:
            self.image.fill(self.bg_color)
            bg_rect = self.image.get_rect(topleft=(self.x, self.y))
            # topleft=(self.x - self.edge_spacing, self.y - self.edge_spacing - self.title_spacing))
            pygame.draw.rect(surface, self.bg_color, bg_rect)

            title_surface = self.font.render(self.title, True, color.white)
            surface.blit(title_surface, (self.x - (title_surface.get_width()/2) +
                                         (self.width/2) - (self.edge_spacing/2), self.y + (self.edge_spacing/2)))

    def update(self, event):
        return