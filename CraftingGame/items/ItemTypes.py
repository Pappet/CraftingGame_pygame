from enum import auto, Enum


class ItemType(Enum):
    RESOURCE = auto()
    COMPONENT = auto()
    TOOL = auto()
    MACHINE = auto()
    FOOD = auto()
    POTION = auto()
    WEAPON = auto()
