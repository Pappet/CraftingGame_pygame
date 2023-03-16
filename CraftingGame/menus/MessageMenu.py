import pygame
import datetime
import CraftingGame.helper.color as color
from CraftingGame.menus.Menu import Menu
from CraftingGame.menus.Button import Button


class MessageMenu(Menu):
    def __init__(self, x, y, width, height, edge_spacing, menu_font_size, title_spacing, title, active, surface,
                 button_manager):
        super().__init__(x=x, y=y, message_menu=self, button_manager=button_manager, width=width, height=height,
                         edge_spacing=edge_spacing, menu_font_size=menu_font_size, title_spacing=title_spacing,
                         title=title, active=active)
        self.surface = surface
        self.text_surface = None
        self.font = pygame.font.SysFont("arial", menu_font_size)
        self.text = ""
        self.bg_color = color.gainsboro

        self.info = {
            'width': self.width - self.edge_spacing * 2,
            'height': self.height - self.title_spacing - self.edge_spacing * 2,
            'x': self.x + self.edge_spacing,
            'y': self.y + self.edge_spacing + self.title_spacing,
            'left_x': self.x + self.edge_spacing * 2,
            'middle_x': self.x + self.edge_spacing * 2 + 80,
            'right_x': self.x + self.edge_spacing * 2 + 80 + 130,
            'rect': (self.x + self.edge_spacing, self.y + self.edge_spacing + self.title_spacing,
                     self.width - self.edge_spacing * 2, self.height - self.title_spacing - self.edge_spacing * 2)
        }

        self.close_button = Button(self.x, self.y, self.title_spacing, self.title_spacing, "X", 18, color.black,
                                   color.red, color.coralred, self.toggle_menu)
        self.button_manager.add_button(self.close_button)

    def add_message(self, message):
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')

        # Füge die neue Nachricht mit Zeitstempel am Anfang des Texts hinzu
        self.text = f"{timestamp} - {message}\n{self.text}"

        # Wenn das Log-Textfeld voll ist, die älteste Zeile löschen
        if self.text.count('\n') >= self.info["height"] // self.menu_font_size:
            self.text = '\n'.join(self.text.split('\n')[:-1])

    def draw(self, surface):
        super().draw(surface)
        max_length = 79
        max_lines = 18

        if self.active:
            pygame.draw.rect(self.surface, color.gray, self.info["rect"])

            # Zeilenumbrüche im Text suchen
            lines = self.text.split("\n")

            # Textblöcke erstellen und zeichnen
            y = self.info["y"] + self.menu_font_size
            line_count = 0
            for line in lines:
                if line_count < max_lines:
                    words = line.split()
                    current_line = ""
                    for word in words:
                        if len(current_line) + len(word) + 1 <= max_length:
                            current_line += word + " "
                        else:
                            text_surface = self.font.render(current_line, True, color.black)
                            text_rect = text_surface.get_rect()
                            text_rect.midleft = (self.info["x"] + self.menu_font_size, y)
                            self.surface.blit(text_surface, text_rect)
                            y += self.menu_font_size
                            line_count += 1
                            if line_count >= max_lines:
                                break
                            current_line = word + " "
                    if current_line:
                        text_surface = self.font.render(current_line, True, color.black)
                        text_rect = text_surface.get_rect()
                        text_rect.midleft = (self.info["x"] + self.menu_font_size, y)
                        self.surface.blit(text_surface, text_rect)
                        y += self.menu_font_size
                        line_count += 1
                        if line_count >= max_lines:
                            break

    def update(self, event):
        super().update(event)

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_m:
                    self.add_message("TEST EINTRAG!!! BESONDERS LANG UND UNLESERLICH!!! OB DER WOHL REIN PASSST???? ")
