import pygame


def draw_multiline_text(window, text, size, color, x, y, max_width):
    """
    Zeichnet einen mehrzeiligen Text auf ein Pygame-Fenster.

    window: Pygame-Fenster
    font: Pygame-Schriftart
    text: Text, der dargestellt werden soll
    color: Farbe des Texts
    x: x-Koordinate des Textanfangs
    y: y-Koordinate des Textanfangs
    max_width: maximale Breite des Textabschnitts
    """
    font = pygame.font.SysFont("arial", size)
    text_sections = []
    for line in text.split('\n'):
        words = line.split(' ')
        section = ''
        for word in words:
            if font.size(section + word + ' ')[0] < max_width:
                section += word + ' '
            else:
                text_sections.append(section)
                section = word + ' '
        text_sections.append(section)

    for section in text_sections:
        text_surface = font.render(section, True, color)
        window.blit(text_surface, (x, y))
        y += font.size(section)[1]

    return y


# To Draw text on the screen
def draw_text(screen, text, size, color, x, y):
    font = pygame.font.SysFont("arial", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)