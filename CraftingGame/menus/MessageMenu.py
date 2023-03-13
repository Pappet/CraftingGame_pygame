import pygame
import datetime
import CraftingGame.helper.color as color
import CraftingGame.helper.pygame_text as text
from CraftingGame.menus.Menu import Menu


class MessageMenu(Menu):
    def __init__(self, x, y, width, height, edge_spacing, menu_font_size, title_spacing, title, active, surface):
        super().__init__(x=x, y=y, message_menu=self, width=width, height=height,
                         edge_spacing=edge_spacing, menu_font_size=menu_font_size, title_spacing=title_spacing,
                         title=title, active=active)
        self.surface = surface
        self.text_surface = None
        self.font = pygame.font.SysFont("arial", menu_font_size)
        self.text = ""

        self.info_width = self.width - self.edge_spacing * 2
        self.info_height = self.height - self.title_spacing - self.edge_spacing * 2
        self.info_x = self.x + self.edge_spacing
        self.info_y = self.y + self.edge_spacing + self.title_spacing
        self.info_left_x = self.info_x + self.edge_spacing
        self.info_middle_x = self.info_left_x + 80
        self.info_right_x = self.info_middle_x + 130
        self.text_rect = (self.info_x, self.info_y, self.info_width, self.info_height)

    def add_message(self, message):
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')

        # Füge die neue Nachricht mit Zeitstempel am Anfang des Texts hinzu
        self.text = f"{timestamp} - {message}\n{self.text}"

        # Wenn das Log-Textfeld voll ist, die älteste Zeile löschen
        if self.text.count('\n') > self.info_height // self.menu_font_size:
            self.text = '\n'.join(self.text.split('\n')[:-1])
            print("TOO BIG")

        # Log-Textfeld neu rendern
        self.text_surface = self.font.render(self.text, True, color.white)

    def draw(self, surface):
        super().draw(surface)

        if self.active:
            pygame.draw.rect(self.surface, color.gray, self.text_rect)

            # Zeilenumbrüche im Text suchen
            lines = self.text.split("\n")

            # Wenn der Text höher als das Textfeld ist, nur die unteren Zeilen anzeigen
            if len(lines) > self.info_height // self.menu_font_size:
                lines = lines[-self.info_height // self.menu_font_size:]

            # Textblöcke erstellen und zeichnen
            y = self.info_y + self.menu_font_size
            for line in lines:
                text_surface = self.font.render(line, True, color.black)
                text_rect = text_surface.get_rect()
                text_rect.midleft = (self.info_x + self.menu_font_size, y)
                self.surface.blit(text_surface, text_rect)
                y += self.menu_font_size

    def update(self, event):
        super().update(event)

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_m:
                    self.add_message("TEST EINTRAG!!!")
