import pygame


class Button:
    def __init__(self, x, y, width, height, text, font_size, text_color, bg_color, hover_color, callback=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.callback = callback

    def draw(self, win):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        x_condition = self.x <= mouse_x <= self.x + self.width
        y_condition = self.y <= mouse_y <= self.y + self.height

        color = self.hover_color if x_condition and y_condition else self.bg_color

        pygame.draw.rect(win, color, (self.x, self.y, self.width, self.height))

        font = pygame.font.Font(None, self.font_size)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        win.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            x_condition = self.x <= mouse_x <= self.x + self.width
            y_condition = self.y <= mouse_y <= self.y + self.height

            if x_condition and y_condition:
                if self.callback:
                    self.callback()
                return True

        return False
