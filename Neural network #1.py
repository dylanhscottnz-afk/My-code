import math
import random

cards = [
    {"Name": "Archer Queen", "Cost": 5, "Attack": 7, "Defense": 9},
    {"Name": "Archers", "Cost": 3, "Attack": 5, "Defense": 8},
    {"Name": "Arrows", "Cost": 3, "Attack": 6, "Defense": 7},
    {"Name": "Baby Dragon", "Cost": 4, "Attack": 5, "Defense": 8},
    {"Name": "Balloon", "Cost": 5, "Attack": 10, "Defense": 1},
    {"Name": "Bandit", "Cost": 3, "Attack": 8, "Defense": 6},
    {"Name": "Barbarian Barrel", "Cost": 2, "Attack": 4, "Defense": 8},
    {"Name": "Barbarian Hut", "Cost": 6, "Attack": 5, "Defense": 7},
    {"Name": "Barbarians", "Cost": 5, "Attack": 6, "Defense": 9},
    {"Name": "Bats", "Cost": 2, "Attack": 5, "Defense": 7},
    {"Name": "Battle Healer", "Cost": 4, "Attack": 6, "Defense": 5},
    {"Name": "Battle Ram", "Cost": 4, "Attack": 9, "Defense": 3},
    {"Name": "Berserker", "Cost": 2, "Attack": 5, "Defense": 6},
    {"Name": "Bomb Tower", "Cost": 4, "Attack": 1, "Defense": 9},
    {"Name": "Bomber", "Cost": 2, "Attack": 5, "Defense": 7},
    {"Name": "Boss Bandit", "Cost": 6, "Attack": 9, "Defense": 8},
    {"Name": "Bowler", "Cost": 5, "Attack": 5, "Defense": 9},
    {"Name": "Cannon", "Cost": 3, "Attack": 1, "Defense": 8},
    {"Name": "Cannon Cart", "Cost": 5, "Attack": 7, "Defense": 9},
    {"Name": "Clone", "Cost": 3, "Attack": 7, "Defense": 2},
    {"Name": "Dark Prince", "Cost": 4, "Attack": 7, "Defense": 8},
    {"Name": "Dart Goblin", "Cost": 3, "Attack": 7, "Defense": 7},
    {"Name": "Earthquake", "Cost": 3, "Attack": 8, "Defense": 3},
    {"Name": "Electro Dragon", "Cost": 5, "Attack": 5, "Defense": 8},
    {"Name": "Electro Giant", "Cost": 7, "Attack": 9, "Defense": 5},
    {"Name": "Electro Spirit", "Cost": 1, "Attack": 4, "Defense": 7},
    {"Name": "Electro Wizard", "Cost": 4, "Attack": 5, "Defense": 9},
    {"Name": "Elite Barbarians", "Cost": 6, "Attack": 8, "Defense": 8},
    {"Name": "Elixir Collector", "Cost": 6, "Attack": 6, "Defense": 2},
    {"Name": "Elixir Golem", "Cost": 3, "Attack": 9, "Defense": 2},
    {"Name": "Executioner", "Cost": 5, "Attack": 5, "Defense": 9},
    {"Name": "Fire Spirit", "Cost": 1, "Attack": 5, "Defense": 7},
    {"Name": "Fireball", "Cost": 4, "Attack": 7, "Defense": 8},
    {"Name": "Firecracker", "Cost": 3, "Attack": 6, "Defense": 8},
    {"Name": "Fisherman", "Cost": 3, "Attack": 3, "Defense": 9},
    {"Name": "Flying Machine", "Cost": 4, "Attack": 7, "Defense": 7},
    {"Name": "Freeze", "Cost": 4, "Attack": 8, "Defense": 5},
    {"Name": "Furnace", "Cost": 4, "Attack": 7, "Defense": 7},
    {"Name": "Giant", "Cost": 5, "Attack": 9, "Defense": 2},
    {"Name": "Giant Skeleton", "Cost": 6, "Attack": 6, "Defense": 9},
    {"Name": "Giant Snowball", "Cost": 2, "Attack": 4, "Defense": 8},
    {"Name": "Goblin Barrel", "Cost": 3, "Attack": 10, "Defense": 1},
    {"Name": "Goblin Cage", "Cost": 4, "Attack": 3, "Defense": 9},
    {"Name": "Goblin Curse", "Cost": 2, "Attack": 5, "Defense": 7},
    {"Name": "Goblin Demolisher", "Cost": 4, "Attack": 7, "Defense": 8},
    {"Name": "Goblin Drill", "Cost": 4, "Attack": 9, "Defense": 4},
    {"Name": "Goblin Gang", "Cost": 3, "Attack": 6, "Defense": 8},
    {"Name": "Goblin Giant", "Cost": 6, "Attack": 9, "Defense": 3},
    {"Name": "Goblin Hut", "Cost": 4, "Attack": 5, "Defense": 7},
    {"Name": "Goblin Machine", "Cost": 5, "Attack": 7, "Defense": 7},
    {"Name": "Goblins", "Cost": 2, "Attack": 5, "Defense": 8},
    {"Name": "Goblinstein", "Cost": 5, "Attack": 8, "Defense": 8},
    {"Name": "Golden Knight", "Cost": 4, "Attack": 7, "Defense": 7},
    {"Name": "Golem", "Cost": 8, "Attack": 10, "Defense": 2},
    {"Name": "Graveyard", "Cost": 5, "Attack": 10, "Defense": 1},
    {"Name": "Guards", "Cost": 3, "Attack": 4, "Defense": 9},
    {"Name": "Heal Spirit", "Cost": 1, "Attack": 6, "Defense": 3},
    {"Name": "Hog Rider", "Cost": 4, "Attack": 10, "Defense": 1},
    {"Name": "Hunter", "Cost": 4, "Attack": 4, "Defense": 9},
    {"Name": "Ice Golem", "Cost": 2, "Attack": 4, "Defense": 8},
    {"Name": "Ice Spirit", "Cost": 1, "Attack": 4, "Defense": 8},
    {"Name": "Ice Wizard", "Cost": 3, "Attack": 3, "Defense": 9},
    {"Name": "Inferno Dragon", "Cost": 4, "Attack": 6, "Defense": 9},
    {"Name": "Inferno Tower", "Cost": 5, "Attack": 1, "Defense": 10},
    {"Name": "Knight", "Cost": 3, "Attack": 4, "Defense": 9},
    {"Name": "Lava Hound", "Cost": 7, "Attack": 10, "Defense": 2},
    {"Name": "Lightning", "Cost": 6, "Attack": 8, "Defense": 6},
    {"Name": "Little Prince", "Cost": 3, "Attack": 6, "Defense": 9},
    {"Name": "Lumberjack", "Cost": 4, "Attack": 8, "Defense": 7},
    {"Name": "Magic Archer", "Cost": 4, "Attack": 8, "Defense": 7},
    {"Name": "Mega Knight", "Cost": 7, "Attack": 7, "Defense": 9},
    {"Name": "Mega Minion", "Cost": 3, "Attack": 4, "Defense": 8},
    {"Name": "Mighty Miner", "Cost": 4, "Attack": 6, "Defense": 9},
    {"Name": "Miner", "Cost": 3, "Attack": 9, "Defense": 5},
    {"Name": "Mini P.E.K.K.A", "Cost": 4, "Attack": 6, "Defense": 9},
    {"Name": "Minion Giant", "Cost": 4, "Attack": 9, "Defense": 2},
    {"Name": "Minion Horde", "Cost": 5, "Attack": 7, "Defense": 8},
    {"Name": "Minions", "Cost": 3, "Attack": 5, "Defense": 8},
    {"Name": "Mirror", "Cost": 1, "Attack": 5, "Defense": 5},
    {"Name": "Monk", "Cost": 5, "Attack": 7, "Defense": 8},
    {"Name": "Mortar", "Cost": 4, "Attack": 8, "Defense": 8},
    {"Name": "Mother Witch", "Cost": 4, "Attack": 7, "Defense": 7},
    {"Name": "Musketeer", "Cost": 4, "Attack": 5, "Defense": 9},
    {"Name": "Night Witch", "Cost": 4, "Attack": 8, "Defense": 6},
    {"Name": "P.E.K.K.A", "Cost": 7, "Attack": 7, "Defense": 10},
    {"Name": "Phoenix", "Cost": 4, "Attack": 7, "Defense": 8},
    {"Name": "Poison", "Cost": 4, "Attack": 8, "Defense": 8},
    {"Name": "Prince", "Cost": 5, "Attack": 8, "Defense": 8},
    {"Name": "Princess", "Cost": 3, "Attack": 7, "Defense": 7},
    {"Name": "Rage", "Cost": 2, "Attack": 7, "Defense": 4},
    {"Name": "Ram Rider", "Cost": 5, "Attack": 9, "Defense": 7},
    {"Name": "Rascals", "Cost": 5, "Attack": 5, "Defense": 9},
    {"Name": "Rocket", "Cost": 6, "Attack": 8, "Defense": 8},
    {"Name": "Ronin", "Cost": 5, "Attack": 7, "Defense": 9},
    {"Name": "Royal Delivery", "Cost": 3, "Attack": 2, "Defense": 9},
    {"Name": "Royal Ghost", "Cost": 3, "Attack": 7, "Defense": 7},
    {"Name": "Royal Giant", "Cost": 6, "Attack": 10, "Defense": 2},
    {"Name": "Royal Hogs", "Cost": 5, "Attack": 10, "Defense": 2},
    {"Name": "Royal Recruits", "Cost": 7, "Attack": 7, "Defense": 9},
    {"Name": "Rune Giant", "Cost": 4, "Attack": 7, "Defense": 5},
    {"Name": "Skeleton Army", "Cost": 3, "Attack": 5, "Defense": 9},
    {"Name": "Skeleton Barrel", "Cost": 3, "Attack": 9, "Defense": 3},
    {"Name": "Skeleton Dragons", "Cost": 4, "Attack": 6, "Defense": 7},
    {"Name": "Skeleton King", "Cost": 4, "Attack": 8, "Defense": 8},
    {"Name": "Skeletons", "Cost": 1, "Attack": 3, "Defense": 8},
    {"Name": "Sparky", "Cost": 6, "Attack": 8, "Defense": 8},
    {"Name": "Spear Goblins", "Cost": 2, "Attack": 5, "Defense": 6},
    {"Name": "Spirit Empress", "Cost": 6, "Attack": 8, "Defense": 8},
    {"Name": "Suspicious Bush", "Cost": 2, "Attack": 8, "Defense": 3},
    {"Name": "Tesla", "Cost": 4, "Attack": 1, "Defense": 9},
    {"Name": "The Log", "Cost": 2, "Attack": 4, "Defense": 9},
    {"Name": "Three Musketeers", "Cost": 9, "Attack": 8, "Defense": 8},
    {"Name": "Tombstone", "Cost": 3, "Attack": 2, "Defense": 9},
    {"Name": "Tornado", "Cost": 3, "Attack": 3, "Defense": 10},
    {"Name": "Valkyrie", "Cost": 4, "Attack": 5, "Defense": 9},
    {"Name": "Vines", "Cost": 3, "Attack": 5, "Defense": 8},
    {"Name": "Void", "Cost": 5, "Attack": 5, "Defense": 8},
    {"Name": "Wall Breakers", "Cost": 2, "Attack": 10, "Defense": 1},
    {"Name": "Witch", "Cost": 5, "Attack": 6, "Defense": 7},
    {"Name": "Wizard", "Cost": 5, "Attack": 5, "Defense": 8},
    {"Name": "X-Bow", "Cost": 6, "Attack": 9, "Defense": 8},
    {"Name": "Zap", "Cost": 2, "Attack": 4, "Defense": 7},
    {"Name": "Zappies", "Cost": 4, "Attack": 4, "Defense": 9},
    {"Name": "Archers Evolution", "Cost": 3, "Attack": 6, "Defense": 9},
    {"Name": "Baby Dragon Evolution", "Cost": 4, "Attack": 6, "Defense": 9},
    {"Name": "Barbarians Evolution", "Cost": 5, "Attack": 7, "Defense": 10},
    {"Name": "Bats Evolution", "Cost": 2, "Attack": 6, "Defense": 8},
    {"Name": "Battle Ram Evolution", "Cost": 4, "Attack": 10, "Defense": 4},
    {"Name": "Bomber Evolution", "Cost": 2, "Attack": 8, "Defense": 8},
    {"Name": "Cannon Evolution", "Cost": 3, "Attack": 1, "Defense": 9},
    {"Name": "Dart Goblin Evolution", "Cost": 3, "Attack": 8, "Defense": 8},
    {"Name": "Electro Dragon Evolution", "Cost": 5, "Attack": 6, "Defense": 10},
    {"Name": "Electro Giant Evolution", "Cost": 7, "Attack": 10, "Defense": 6},
    {"Name": "Elite Barbarians Evolution", "Cost": 6, "Attack": 9, "Defense": 9},
    {"Name": "Executioner Evolution", "Cost": 5, "Attack": 6, "Defense": 10},
    {"Name": "Firecracker Evolution", "Cost": 3, "Attack": 8, "Defense": 9},
    {"Name": "Furnace Evolution", "Cost": 4, "Attack": 8, "Defense": 8},
    {"Name": "Giant Evolution", "Cost": 5, "Attack": 10, "Defense": 3},
    {"Name": "Giant Snowball Evolution", "Cost": 2, "Attack": 5, "Defense": 9},
    {"Name": "Goblin Barrel Evolution", "Cost": 3, "Attack": 10, "Defense": 2},
    {"Name": "Goblin Cage Evolution", "Cost": 4, "Attack": 4, "Defense": 10},
    {"Name": "Goblin Drill Evolution", "Cost": 4, "Attack": 10, "Defense": 4},
    {"Name": "Goblin Giant Evolution", "Cost": 6, "Attack": 10, "Defense": 4},
    {"Name": "Hunter Evolution", "Cost": 4, "Attack": 5, "Defense": 10},
    {"Name": "Ice Spirit Evolution", "Cost": 1, "Attack": 5, "Defense": 9},
    {"Name": "Inferno Dragon Evolution", "Cost": 4, "Attack": 7, "Defense": 10},
    {"Name": "Knight Evolution", "Cost": 3, "Attack": 5, "Defense": 10},
    {"Name": "Lumberjack Evolution", "Cost": 4, "Attack": 9, "Defense": 8},
    {"Name": "Mega Knight Evolution", "Cost": 7, "Attack": 8, "Defense": 10},
    {"Name": "Minion Horde Evolution", "Cost": 5, "Attack": 8, "Defense": 9},
    {"Name": "Mirror Evolution", "Cost": 1, "Attack": 6, "Defense": 6},
    {"Name": "Mortar Evolution", "Cost": 4, "Attack": 9, "Defense": 8},
    {"Name": "Musketeer Evolution", "Cost": 4, "Attack": 6, "Defense": 10},
    {"Name": "P.E.K.K.A Evolution", "Cost": 7, "Attack": 8, "Defense": 10},
    {"Name": "Princess Evolution", "Cost": 3, "Attack": 8, "Defense": 8},
    {"Name": "Royal Ghost Evolution", "Cost": 3, "Attack": 8, "Defense": 8},
    {"Name": "Royal Giant Evolution", "Cost": 6, "Attack": 10, "Defense": 3},
    {"Name": "Royal Hogs Evolution", "Cost": 5, "Attack": 10, "Defense": 3},
    {"Name": "Royal Recruits Evolution", "Cost": 7, "Attack": 8, "Defense": 10},
    {"Name": "Skeleton Army Evolution", "Cost": 3, "Attack": 6, "Defense": 10},
    {"Name": "Skeleton Barrel Evolution", "Cost": 3, "Attack": 10, "Defense": 4},
    {"Name": "Skeletons Evolution", "Cost": 1, "Attack": 5, "Defense": 10},
    {"Name": "Tesla Evolution", "Cost": 4, "Attack": 1, "Defense": 10},
    {"Name": "Valkyrie Evolution", "Cost": 4, "Attack": 6, "Defense": 10},
    {"Name": "Wall Breakers Evolution", "Cost": 2, "Attack": 10, "Defense": 2},
    {"Name": "Witch Evolution", "Cost": 5, "Attack": 7, "Defense": 8},
    {"Name": "Wizard Evolution", "Cost": 5, "Attack": 6, "Defense": 9},
    {"Name": "Zap Evolution", "Cost": 2, "Attack": 5, "Defense": 9},
    {"Name": "Hero Balloon", "Cost": 5, "Attack": 10, "Defense": 2},
    {"Name": "Hero Barbarian Barrel", "Cost": 2, "Attack": 5, "Defense": 9},
    {"Name": "Hero Berserker", "Cost": 2, "Attack": 7, "Defense": 7},
    {"Name": "Hero Bowler", "Cost": 5, "Attack": 6, "Defense": 10},
    {"Name": "Hero Dark Prince", "Cost": 4, "Attack": 8, "Defense": 9},
    {"Name": "Hero Electro Wizard", "Cost": 4, "Attack": 6, "Defense": 10},
    {"Name": "Hero Giant", "Cost": 5, "Attack": 10, "Defense": 3},
    {"Name": "Hero Goblins", "Cost": 2, "Attack": 6, "Defense": 9},
    {"Name": "Hero Ice Golem", "Cost": 2, "Attack": 5, "Defense": 9},
    {"Name": "Hero Ice Wizard", "Cost": 3, "Attack": 4, "Defense": 10},
    {"Name": "Hero Knight", "Cost": 3, "Attack": 5, "Defense": 10},
    {"Name": "Hero Magic Archer", "Cost": 4, "Attack": 9, "Defense": 8},
    {"Name": "Hero Mega Minion", "Cost": 3, "Attack": 6, "Defense": 9},
    {"Name": "Hero Mini P.E.K.K.A", "Cost": 4, "Attack": 8, "Defense": 10},
    {"Name": "Hero Musketeer", "Cost": 4, "Attack": 7, "Defense": 10},
    {"Name": "Hero Tombstone", "Cost": 3, "Attack": 3, "Defense": 10},
    {"Name": "Hero Valkyrie", "Cost": 4, "Attack": 6, "Defense": 10},
    {"Name": "Hero Wizard", "Cost": 5, "Attack": 7, "Defense": 9},
    {"Name": "Cannoneer", "Cost": 0, "Attack": 1, "Defense": 8},
    {"Name": "Dagger Duchess", "Cost": 0, "Attack": 1, "Defense": 8},
    {"Name": "Royal Chef", "Cost": 0, "Attack": 3, "Defense": 7},
    {"Name": "Tower Princess", "Cost": 0, "Attack": 1, "Defense": 8},
]

data = [
    {"Name": "Mortar Cannon Cart Bait", "Cards": ["Barbarian Barrel", "Cannon Cart", "Fireball", "Goblin Gang", "Ice Wizard", "Mortar", "Rascals", "Skeleton Barrel"], "target": 9.46},
    {"Name": "Golem Night Witch Phoenix", "Cards": ["Arrows", "Bomber", "Elite Barbarians", "Golem", "Mini P.E.K.K.A", "Night Witch", "Phoenix", "Zap"], "target": 8.74},
    {"Name": "Mortar Cannon Cart Log Bait", "Cards": ["Cannon Cart", "Fireball", "Goblin Gang", "Ice Wizard", "Mortar", "Rascals", "Skeleton Barrel", "The Log"], "target": 7.21},
    {"Name": "Royal Hogs Archer Queen Cycle", "Cards": ["Archer Queen", "Cannon", "Earthquake", "Ice Spirit", "Royal Delivery", "Royal Hogs", "Skeletons", "The Log"], "target": 6.49},
    {"Name": "Hog Musketeer Cycle", "Cards": ["Cannon", "Fireball", "Hog Rider", "Ice Golem", "Ice Spirit", "Musketeer", "Skeletons", "The Log"], "target": 6.45},
    {"Name": "Knight Inferno Tower Bait", "Cards": ["Goblin Barrel", "Goblin Gang", "Ice Spirit", "Inferno Tower", "Knight", "Princess", "Rocket", "The Log"], "target": 5.37},
    {"Name": "Hog Ice Golem Cycle", "Cards": ["Cannon", "Fireball", "Hog Rider", "Ice Golem", "Ice Spirit", "Musketeer", "Skeletons", "The Log"], "target": 3.02},

    {"Name": "Three Musketeers Mirror Pump", "Cards": ["Elite Barbarians", "Elixir Collector", "Golden Knight", "Lumberjack", "Mirror", "Royal Ghost", "Three Musketeers", "Zap"], "target": 10},
    {"Name": "Furnace Mirror Barrel Bait", "Cards": ["Arrows", "Bowler", "Furnace", "Goblin Barrel", "Mini P.E.K.K.A", "Minion Horde", "Mirror", "Rascals"], "target": 8.83},
    {"Name": "Furnace Hunter Mirror Bait", "Cards": ["Arrows", "Bowler", "Furnace", "Goblin Barrel", "Hunter", "Mirror", "Rascals", "Rocket"], "target": 6.72},
    {"Name": "Furnace Mini Pekka Mirror Bait", "Cards": ["Arrows", "Bowler", "Furnace", "Goblin Barrel", "Mini P.E.K.K.A", "Mirror", "Rascals", "Rocket"], "target": 6.22},
    {"Name": "Pekka Lumberjack Mirror Control", "Cards": ["Electro Wizard", "Executioner", "Lumberjack", "Mega Knight", "Mirror", "P.E.K.K.A", "Rage", "Tornado"], "target": 3.25},
    {"Name": "Lava Night Witch Mirror Clone", "Cards": ["Clone", "Freeze", "Lava Hound", "Minions", "Mirror", "Night Witch", "Skeleton Army", "Zap"], "target": 1},

    {"Name": "Giant Sparky Wizard Tornado", "Cards": ["Giant", "Heal Spirit", "Mini P.E.K.K.A", "Sparky", "Tornado", "Vines", "Wizard", "Zap"], "target": 7.53},
    {"Name": "Pekka Mega Knight Double Wizard", "Cards": ["Electro Wizard", "Lumberjack", "Mega Knight", "Mini P.E.K.K.A", "P.E.K.K.A", "Tornado", "Wizard", "Zap"], "target": 7.17},
    {"Name": "Goblin Giant Mighty Miner Wizard", "Cards": ["Giant Skeleton", "Goblin Curse", "Goblin Giant", "Inferno Dragon", "Mighty Miner", "Mini P.E.K.K.A", "Wizard", "Zap"], "target": 1},
    {"Name": "Goblinstein Elite Barbarians Wizard", "Cards": ["Elite Barbarians", "Firecracker", "Goblinstein", "Mega Knight", "Minion Horde", "P.E.K.K.A", "Rocket", "Wizard"], "target": 1},
    {"Name": "Miner Mighty Miner Minion Horde", "Cards": ["Electro Dragon", "Goblin Curse", "Lumberjack", "Mighty Miner", "Miner", "Minion Horde", "Suspicious Bush", "Wizard"], "target": 1},

    {"Name": "Pekka Double Prince Witch", "Cards": ["Arrows", "Dark Prince", "Mini P.E.K.K.A", "Minion Horde", "P.E.K.K.A", "Prince", "Valkyrie", "Witch"], "target": 7.21},
    {"Name": "Giant Graveyard Witch", "Cards": ["Arrows", "Bowler", "Giant", "Giant Snowball", "Graveyard", "Mini P.E.K.K.A", "Minions", "Witch"], "target": 4.69},
    {"Name": "Giant Graveyard Witch Zappies", "Cards": ["Arrows", "Bowler", "Giant", "Giant Snowball", "Graveyard", "Guards", "Witch", "Zappies"], "target": 3.97},
    {"Name": "Giant Graveyard Bowler Witch", "Cards": ["Arrows", "Bowler", "Giant", "Giant Snowball", "Graveyard", "Guards", "Minions", "Witch"], "target": 1},
    {"Name": "Mortar Goblinstein Sparky Witch", "Cards": ["Bats", "Giant Skeleton", "Goblinstein", "Mini P.E.K.K.A", "Mortar", "Sparky", "Valkyrie", "Witch"], "target": 1},
    {"Name": "Royal Giant Balloon Witch", "Cards": ["Balloon", "Barbarians", "Goblin Demolisher", "Golden Knight", "Inferno Dragon", "Mega Knight", "Royal Giant", "Witch"], "target": 1},

    {"Name": "Goblin Giant Elite Barbarians Rage", "Cards": ["Dark Prince", "Electro Wizard", "Elite Barbarians", "Goblin Giant", "Heal Spirit", "Rage", "Sparky", "Zap"], "target": 9.78},
    {"Name": "Elixir Golem Elite Barbarians Dragons", "Cards": ["Arrows", "Battle Healer", "Electro Dragon", "Elite Barbarians", "Elixir Golem", "Inferno Dragon", "Rage", "Zap"], "target": 6.04},
    {"Name": "Giant Elite Barbarians Witch Pump", "Cards": ["Arrows", "Elite Barbarians", "Elixir Collector", "Giant", "Heal Spirit", "Mini P.E.K.K.A", "Rage", "Witch"], "target": 6.04},
    {"Name": "Electro Giant Ronin Wizard", "Cards": ["Electro Giant", "Elite Barbarians", "Inferno Dragon", "Rascals", "Ronin", "Valkyrie", "Witch", "Wizard"], "target": 4.83},
    {"Name": "Goblin Giant Sparky Elite Barbarians", "Cards": ["Dark Prince", "Electro Wizard", "Elite Barbarians", "Goblin Giant", "Heal Spirit", "Rage", "Sparky", "Zap"], "target": 2.08},
    {"Name": "Golem Giant Skeleton Clone Rocket", "Cards": ["Clone", "Elite Barbarians", "Executioner", "Freeze", "Giant Skeleton", "Golem", "Minion Horde", "Rocket"], "target": 1},

    {"Name": "Elixir Golem Skeleton King Wizard", "Cards": ["Arrows", "Elixir Golem", "Lightning", "Night Witch", "Rage", "Skeleton Army", "Skeleton King", "Wizard"], "target": 10},
    {"Name": "Elixir Golem Skeleton King Witch", "Cards": ["Arrows", "Elixir Golem", "Lightning", "Night Witch", "Rage", "Skeleton Army", "Skeleton King", "Witch"], "target": 8.02},
    {"Name": "Elixir Golem Electro Dragon Curse", "Cards": ["Arrows", "Electro Dragon", "Elixir Golem", "Goblin Curse", "Lightning", "Night Witch", "Skeleton Army", "Skeleton King"], "target": 6.49},
    {"Name": "Double Golem Skeleton King", "Cards": ["Arrows", "Elixir Golem", "Golem", "Inferno Dragon", "Night Witch", "Rage", "Skeleton King", "Witch"], "target": 5.32},
    {"Name": "Elixir Golem Monk Healer", "Cards": ["Arrows", "Barbarians", "Battle Healer", "Electro Dragon", "Elixir Golem", "Monk", "Night Witch", "Rage"], "target": 4.92},
    {"Name": "Elixir Golem Executioner Void", "Cards": ["Elixir Golem", "Executioner", "Goblin Curse", "Night Witch", "Rage", "Skeleton Army", "Skeleton King", "Void"], "target": 1},

    {"Name": "Elixir Golem Goblin Machine Zappies", "Cards": ["Arrows", "Baby Dragon", "Barbarians", "Bowler", "Elixir Golem", "Goblin Machine", "Lightning", "Zappies"], "target": 8.92},
    {"Name": "Goblin Giant Pekka Machine Rage", "Cards": ["Bomber", "Goblin Curse", "Goblin Giant", "Goblin Machine", "Minions", "P.E.K.K.A", "Rage", "Vines"], "target": 7.35},
    {"Name": "Elixir Golem Machine Freeze", "Cards": ["Elixir Golem", "Executioner", "Freeze", "Goblin Machine", "Mini P.E.K.K.A", "Night Witch", "Skeleton Army", "Vines"], "target": 6.4},
    {"Name": "Mega Knight Machine Mother Witch", "Cards": ["Arrows", "Bandit", "Battle Ram", "Electro Wizard", "Goblin Machine", "Lumberjack", "Mega Knight", "Mother Witch"], "target": 6.35},
    {"Name": "Goblin Giant Pekka Machine Wizard", "Cards": ["Arrows", "Bomber", "Electro Wizard", "Goblin Curse", "Goblin Giant", "Goblin Machine", "P.E.K.K.A", "Rage"], "target": 1},
    {"Name": "Boss Bandit Machine Mother Witch", "Cards": ["Archers", "Arrows", "Bomber", "Boss Bandit", "Goblin Machine", "Lightning", "Mega Knight", "Mother Witch"], "target": 1},

    {"Name": "Three Musketeers Little Prince Pump", "Cards": ["Barbarian Barrel", "Elite Barbarians", "Elixir Collector", "Heal Spirit", "Ice Golem", "Little Prince", "Royal Ghost", "Three Musketeers"], "target": 10},
    {"Name": "Three Musketeers Bandit Hunter", "Cards": ["Bandit", "Barbarian Barrel", "Battle Ram", "Elixir Collector", "Hunter", "Ice Golem", "Royal Ghost", "Three Musketeers"], "target": 8.29},
    {"Name": "Three Musketeers Golden Knight Hunter", "Cards": ["Barbarian Barrel", "Battle Ram", "Elixir Collector", "Golden Knight", "Hunter", "Ice Golem", "Royal Ghost", "Three Musketeers"], "target": 5.95},
    {"Name": "Three Musketeers Royal Hogs Hunter", "Cards": ["Barbarian Barrel", "Fireball", "Heal Spirit", "Hunter", "Ice Golem", "Royal Ghost", "Royal Hogs", "Three Musketeers"], "target": 4.42},
    {"Name": "Three Musketeers Ronin Zappies", "Cards": ["Battle Ram", "Dark Prince", "Golden Knight", "Heal Spirit", "Ronin", "Three Musketeers", "Zap", "Zappies"], "target": 3.16},
    {"Name": "Three Musketeers Royal Giant Sparky", "Cards": ["Balloon", "Magic Archer", "Mega Knight", "P.E.K.K.A", "Rage", "Royal Giant", "Sparky", "Three Musketeers"], "target": 1},

    {"Name": "Golem Cannon Cart Dragons", "Cards": ["Barbarian Barrel", "Cannon Cart", "Dark Prince", "Electro Dragon", "Goblin Cage", "Golem", "Skeleton Dragons", "Tornado"], "target": 10},
    {"Name": "Golem Lumberjack Night Witch", "Cards": ["Arrows", "Bomber", "Elite Barbarians", "Golem", "Lumberjack", "Mega Minion", "Night Witch", "Zap"], "target": 8.15},
    {"Name": "Golem Skeleton King Miner", "Cards": ["Goblin Curse", "Golem", "Inferno Dragon", "Miner", "Night Witch", "Skeleton Army", "Skeleton King", "Zap"], "target": 6.76},
    {"Name": "Golem Baby Dragon Lightning", "Cards": ["Baby Dragon", "Golem", "Lightning", "Lumberjack", "Mega Minion", "Night Witch", "Tornado", "Zap"], "target": 3.7},
    {"Name": "Golem Healer Double Dragon Pump", "Cards": ["Barbarian Barrel", "Battle Healer", "Electro Dragon", "Elixir Collector", "Golem", "Lumberjack", "Skeleton Dragons", "Tornado"], "target": 2.12},
    {"Name": "Golem Healer Valkyrie Pump", "Cards": ["Baby Dragon", "Battle Healer", "Elixir Collector", "Golem", "Mini P.E.K.K.A", "Valkyrie", "Vines", "Zappies"], "target": 1},

    {"Name": "Hog Giant Skeleton Lightning", "Cards": ["Barbarians", "Firecracker", "Giant Skeleton", "Guards", "Hog Rider", "Lightning", "Minion Horde", "The Log"], "target": 8.38},
    {"Name": "Hog Mighty Miner Furnace", "Cards": ["Cannon", "Electro Spirit", "Furnace", "Hog Rider", "Lightning", "Mighty Miner", "Skeletons", "The Log"], "target": 8.15},
    {"Name": "Hog Knight Earthquake", "Cards": ["Earthquake", "Firecracker", "Hog Rider", "Ice Spirit", "Knight", "Skeletons", "Tesla", "The Log"], "target": 6.35},
    {"Name": "Hog Electro Spirit Cycle", "Cards": ["Cannon", "Electro Spirit", "Fireball", "Hog Rider", "Ice Golem", "Musketeer", "Skeletons", "The Log"], "target": 4.55},
    {"Name": "Hog Musketeer Ice Spirit", "Cards": ["Cannon", "Fireball", "Hog Rider", "Ice Golem", "Ice Spirit", "Musketeer", "Skeletons", "The Log"], "target": 3.12},
    {"Name": "Hog 2.6", "Cards": ["Cannon", "Fireball", "Hog Rider", "Ice Golem", "Ice Spirit", "Musketeer", "Skeletons", "The Log"], "target": 1},

    {"Name": "Lava Baby Dragon Flying Machine", "Cards": ["Baby Dragon", "Barbarians", "Fireball", "Flying Machine", "Lava Hound", "Mega Minion", "Tombstone", "Zap"], "target": 10},
    {"Name": "Lava Miner Phoenix", "Cards": ["Barbarians", "Flying Machine", "Goblin Curse", "Lava Hound", "Miner", "Phoenix", "Tombstone", "Zap"], "target": 7.39},
    {"Name": "Lava Minion Giant Dragons", "Cards": ["Fireball", "Inferno Dragon", "Lava Hound", "Minion Giant", "Skeleton Dragons", "Tombstone", "Valkyrie", "Zap"], "target": 5.18},
    {"Name": "LavaLoon Mega Minion", "Cards": ["Balloon", "Barbarians", "Fireball", "Lava Hound", "Mega Minion", "Minions", "Tombstone", "Zap"], "target": 3.75},
    {"Name": "Lava Cannon Clone Void", "Cards": ["Arrows", "Baby Dragon", "Cannon", "Clone", "Electro Wizard", "Ice Golem", "Lava Hound", "Void"], "target": 1},

    {"Name": "Graveyard Inferno Dragon Freeze", "Cards": ["Bowler", "Executioner", "Freeze", "Graveyard", "Inferno Dragon", "Knight", "Tornado", "Zappies"], "target": 10},
    {"Name": "Graveyard Baby Dragon Ice Wizard", "Cards": ["Baby Dragon", "Barbarian Barrel", "Graveyard", "Ice Wizard", "Knight", "Poison", "Tombstone", "Tornado"], "target": 7.3},
    {"Name": "Graveyard Goblin Hut Tornado", "Cards": ["Baby Dragon", "Barbarian Barrel", "Goblin Hut", "Graveyard", "Ice Wizard", "Knight", "Poison", "Tornado"], "target": 5.68},
    {"Name": "Graveyard Bats Cycle", "Cards": ["Barbarian Barrel", "Bats", "Graveyard", "Ice Wizard", "Knight", "Poison", "Skeletons", "Tesla"], "target": 4.02},
    {"Name": "Graveyard Knight Witch", "Cards": ["Barbarian Barrel", "Goblin Cage", "Graveyard", "Ice Wizard", "Knight", "Poison", "Vines", "Witch"], "target": 1},

    {"Name": "X-Bow Musketeer Pump", "Cards": ["Electro Spirit", "Elixir Collector", "Fire Spirit", "Knight", "Musketeer", "Skeletons", "The Log", "X-Bow"], "target": 10},
    {"Name": "X-Bow Knight Ice Spirit", "Cards": ["Archers", "Fireball", "Ice Spirit", "Knight", "Skeletons", "Tesla", "The Log", "X-Bow"], "target": 7.35},
    {"Name": "X-Bow Valkyrie Cycle", "Cards": ["Archers", "Electro Spirit", "Fireball", "Skeletons", "Tesla", "The Log", "Valkyrie", "X-Bow"], "target": 5.5},
    {"Name": "X-Bow Knight Electro Spirit", "Cards": ["Archers", "Electro Spirit", "Fireball", "Knight", "Skeletons", "Tesla", "The Log", "X-Bow"], "target": 4.24},
    {"Name": "X-Bow Mega Knight Pump", "Cards": ["Electro Spirit", "Elixir Collector", "Fire Spirit", "Giant Snowball", "Little Prince", "Mega Knight", "Skeletons", "X-Bow"], "target": 1},

    {"Name": "Royal Giant Mega Knight Bait", "Cards": ["Bats", "Dart Goblin", "Goblin Barrel", "Mega Knight", "Prince", "Princess", "Royal Giant", "Skeleton Army"], "target": 9.78},
    {"Name": "Royal Giant Lumberjack Phoenix", "Cards": ["Barbarian Barrel", "Electro Wizard", "Goblin Cage", "Heal Spirit", "Lightning", "Lumberjack", "Phoenix", "Royal Giant"], "target": 6.67},
    {"Name": "Royal Giant Giant Skeleton Zappies", "Cards": ["Bomber", "Earthquake", "Firecracker", "Giant Skeleton", "Hunter", "Royal Giant", "Skeleton Army", "Zappies"], "target": 6.58},
    {"Name": "Royal Giant Fisherman Ghost", "Cards": ["Barbarian Barrel", "Electro Spirit", "Fireball", "Fisherman", "Hunter", "Royal Ghost", "Royal Giant", "Skeletons"], "target": 2.89},
    {"Name": "Royal Giant Hunter Cycle", "Cards": ["Barbarian Barrel", "Electro Spirit", "Fireball", "Fisherman", "Hunter", "Royal Ghost", "Royal Giant", "Skeletons"], "target": 1},

    {"Name": "Knight Dart Goblin Bait", "Cards": ["Cannon", "Dart Goblin", "Goblin Barrel", "Goblin Gang", "Ice Spirit", "Knight", "Princess", "The Log"], "target": 10},
    {"Name": "Knight Rocket Tesla Bait", "Cards": ["Goblin Barrel", "Ice Spirit", "Knight", "Princess", "Rocket", "Skeletons", "Tesla", "The Log"], "target": 7.17},
    {"Name": "Knight Goblin Gang Tesla Bait", "Cards": ["Goblin Barrel", "Goblin Gang", "Ice Spirit", "Knight", "Princess", "Rocket", "Tesla", "The Log"], "target": 5.46},
    {"Name": "Wall Breakers Barrel Bait", "Cards": ["Cannon", "Dart Goblin", "Goblin Barrel", "Ice Spirit", "Princess", "Skeleton Army", "Valkyrie", "Wall Breakers"], "target": 3.83},
    {"Name": "Knight Classic Log Bait", "Cards": ["Goblin Barrel", "Goblin Gang", "Ice Spirit", "Inferno Tower", "Knight", "Princess", "Rocket", "The Log"], "target": 1},

    {"Name": "Hog Mega Knight Electro Wizard", "Cards": ["Bandit", "Dark Prince", "Electro Wizard", "Firecracker", "Guards", "Hog Rider", "Mega Knight", "Zap"], "target": 10},
    {"Name": "Mega Knight Miner Inferno Dragon", "Cards": ["Bats", "Goblin Gang", "Inferno Dragon", "Mega Knight", "Miner", "Skeleton Barrel", "Spear Goblins", "Zap"], "target": 7.03},
    {"Name": "Hog Mega Knight Witch Freeze", "Cards": ["Arrows", "Freeze", "Hog Rider", "Lumberjack", "Mega Knight", "Mini P.E.K.K.A", "Valkyrie", "Witch"], "target": 5.23},
    {"Name": "Mega Knight Miner Snowball Bait", "Cards": ["Bats", "Giant Snowball", "Goblin Gang", "Inferno Dragon", "Mega Knight", "Miner", "Skeleton Barrel", "Spear Goblins"], "target": 4.83},
    {"Name": "Mega Knight Bandit Cannon Cart", "Cards": ["Bandit", "Bats", "Cannon Cart", "Furnace", "Inferno Tower", "Mega Knight", "Mega Minion", "Princess"], "target": 1},

    {"Name": "Goblin Drill Wall Breakers Bait", "Cards": ["Arrows", "Bats", "Goblin Drill", "Goblin Gang", "Inferno Dragon", "Mega Knight", "Skeleton Barrel", "Wall Breakers"], "target": 10},
    {"Name": "Goblin Drill Furnace Poison", "Cards": ["Berserker", "Furnace", "Giant Snowball", "Goblin Drill", "Poison", "Royal Delivery", "Skeletons", "Tesla"], "target": 7.35},
    {"Name": "Goblin Drill Knight Tesla", "Cards": ["Bomber", "Fire Spirit", "Giant Snowball", "Goblin Drill", "Knight", "Poison", "Skeletons", "Tesla"], "target": 5.72},
    {"Name": "Goblin Drill Knight Cannon", "Cards": ["Bomber", "Cannon", "Fire Spirit", "Giant Snowball", "Goblin Drill", "Knight", "Poison", "Skeletons"], "target": 4.1},
    {"Name": "Goblin Drill Berserker Rocket", "Cards": ["Berserker", "Bomber", "Cannon", "Fire Spirit", "Giant Snowball", "Goblin Drill", "Rocket", "Skeletons"], "target": 1},

    {"Name": "Giant Sparky Minion Horde", "Cards": ["Arrows", "Bats", "Giant", "Mini P.E.K.K.A", "Minion Horde", "Skeleton Army", "Sparky", "Zap"], "target": 10},
    {"Name": "Giant Sparky Wizard Cycle", "Cards": ["Giant", "Heal Spirit", "Mini P.E.K.K.A", "Skeletons", "Sparky", "Tornado", "Wizard", "Zap"], "target": 7.21},
    {"Name": "Giant Graveyard Inferno Dragon", "Cards": ["Fireball", "Giant", "Graveyard", "Inferno Dragon", "Mini P.E.K.K.A", "Skeleton Army", "Witch", "Zap"], "target": 5.68},
    {"Name": "Giant Starter Beatdown", "Cards": ["Archers", "Arrows", "Fireball", "Giant", "Knight", "Mini P.E.K.K.A", "Minions", "Musketeer"], "target": 4.06},
    {"Name": "Giant Prince Wizard Cycle", "Cards": ["Electro Spirit", "Fire Spirit", "Giant", "Goblins", "Prince", "Skeletons", "Spear Goblins", "Wizard"], "target": 1}
]

random.seed(49)
w_1 = random.uniform(-1, 1)
w_2 = random.uniform(-1, 1)
w_3 = random.uniform(-1, 1)
bias = random.uniform(-1, 1)

learning_rate = 0.01
epochs = 5000


for epoch in range(epochs):
    for deck in data:
        total_attack = 0
        total_defense = 0
        total_cost = 0

        for card_name in deck["Cards"]:
            for card in cards:
                if card["Name"] == card_name:
                    total_attack += card["Attack"]
                    total_defense += card["Defense"]
                    total_cost += card["Cost"]
                    break

        average_attack = total_attack / len(deck["Cards"])
        average_defense = total_defense / len(deck["Cards"])
        average_cost = total_cost / len(deck["Cards"])

        x1 = average_attack
        x2 = average_defense
        x3 = average_cost

        target = deck["target"]


        Ans = (w_1 * x1) + (w_2 * x2) + (w_3 * x3) + bias

        error = Ans - target

        w_1 -= learning_rate * error * x1
        w_2 -= learning_rate * error * x2
        w_3 -= learning_rate * error * x3
        bias -= learning_rate * error
        



