import random

# Color Codes for simpler use

# Use it with:
# color.black
# etc.

# define colors
black = (0, 0, 0),
white = (255, 255, 255),
red = (255, 0, 0),
green = (0, 255, 0),
blue = (0, 0, 255),
yellow = (255, 255, 0),
magenta = (255, 0, 255),
cyan = (0, 255, 255),
gray = (128, 128, 128),
purple = (128, 0, 128),
brown = (165, 42, 42),
olivegreen = (128, 128, 0),
navyblue = (0, 0, 128),
teal = (0, 128, 128),
coralred = (255, 127, 80),
gold = (255, 215, 0),
pink = (255, 192, 203),
silver = (192, 192, 192),
khaki = (240, 230, 140),
orange = (255, 165, 0),
violet = (238, 130, 238),
skyblue = (135, 206, 235)


def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
