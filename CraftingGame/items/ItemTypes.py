from enum import auto, Enum


class ItemType(Enum):
    RESOURCE = auto()      # Rohstoffe werden zum Herstellen von Gegenständen, Bau von Strukturen oder als Kraftstoff verwendet
    COMPONENT = auto()     # Komponenten sind Teile oder Materialien, die zum Herstellen von Gegenständen oder Strukturen verwendet werden
    TOOL = auto()          # Werkzeuge werden zum Sammeln von Ressourcen, Handwerk oder Interaktion mit der Spielwelt verwendet
    MACHINE = auto()       # Maschinen führen automatisierte Aktionen aus, wie das Verarbeiten von Ressourcen oder das Erzeugen von Energie
    FOOD = auto()          # Nahrung stellt die Gesundheit oder Ausdauer des Charakters wieder her und kann temporäre Effekte bieten
    POTION = auto()        # Tränke bieten temporäre oder permanente Effekte, wie Heilung, Buffs oder Debuffs
    WEAPON = auto()        # Waffen werden im Kampf verwendet, um Schaden zuzufügen oder Feinde zu besiegen
    AMMO = auto()          # Munition wird für Fernkampfwaffen benötigt, z. B. Pfeile für Bögen oder Kugeln für Schusswaffen
    STRUCTURE = auto()     # Strukturen sind Gebäude oder Konstruktionen, die im Spiel platziert werden können, z. B. Häuser, Brücken oder Verteidigungsanlagen
    ARMOR = auto()         # Rüstungen schützen den Charakter vor Schaden (z.B. Helme, Brustplatten, Beinschienen)
    CLOTHING = auto()      # Kleidung dient zur Charakteranpassung und kann leichte Schutz- oder Statuseffekte bieten
    ACCESSORY = auto()     # Accessoires wie Ringe oder Amulette können passive Boni oder spezielle Fähigkeiten verleihen
    CONSUMABLE = auto()    # Verbrauchsgegenstände werden einmal verwendet und können Heilung oder temporäre Buffs/Debuffs bewirken
    KEY_ITEM = auto()      # Schlüsselgegenstände sind wichtig für die Handlung oder Quests und können nicht verkauft oder weggeworfen werden
    RECIPE = auto()        # Rezepte oder Baupläne ermöglichen das Erlernen neuer Handwerksrezepte oder das Bauen neuer Strukturen
    MISC = auto()          # Verschiedene Gegenstände, die keine spezifische Kategorie haben, können Sammelobjekte, Trophäen oder dekorative Objekte sein
