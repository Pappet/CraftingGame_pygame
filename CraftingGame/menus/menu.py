import pygame
import helper.color as color


class Menu:
    def __init__(self, x, y, width=100, height=100, edge_spacing=10, title_spacing=30, title="Default"):
        self.x = x
        self.y = y
        self.edge_spacing = edge_spacing
        self.title_spacing = title_spacing
        self.title = title
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.bg_color = color.gray
        # change the font to a system font that is available on your system
        self.font = pygame.font.SysFont("arial", self.title_spacing)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, new_value):
        self._width = new_value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, new_value):
        self._height = new_value

    def get_image(self):
        return self.image

    def draw(self, surface):
        self.image.fill(self.bg_color)
        bg_rect = self.image.get_rect(topleft=(self.x, self.y))
        # topleft=(self.x - self.edge_spacing, self.y - self.edge_spacing - self.title_spacing))
        pygame.draw.rect(surface, self.bg_color, bg_rect)

        title_surface = self.font.render(self.title, True, color.white)
        surface.blit(title_surface, (self.x - (title_surface.get_width()/2) +
                     (self.width/2) - (self.edge_spacing/2), self.y + (self.edge_spacing/2)))
