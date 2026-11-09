import math
import random
import json
from pathlib import Path

cards = [
    {'Name': 'Electro Spirit', 'Cost': 1, 'Attack': 1.0, 'Defense': 6.6, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 1, 'Reset': 1, 'AntiTank': 0},
    {'Name': 'Fire Spirit', 'Cost': 1, 'Attack': 1.5, 'Defense': 5.5, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Ice Spirit', 'Cost': 1, 'Attack': 1.0, 'Defense': 6.9, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 1, 'Reset': 1, 'AntiTank': 0},
    {'Name': 'Skeletons', 'Cost': 1, 'Attack': 1.3, 'Defense': 4.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 1, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Bats', 'Cost': 2, 'Attack': 1.3, 'Defense': 5.1, 'AirCounter': 1, 'GroundCounter': 0, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 1, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Berserker', 'Cost': 2, 'Attack': 1.3, 'Defense': 4.0, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Bomber', 'Cost': 2, 'Attack': 1.3, 'Defense': 4.9, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 1, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Giant Snowball', 'Cost': 2, 'Attack': 1.2, 'Defense': 6.3, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 1, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Goblins', 'Cost': 2, 'Attack': 1.3, 'Defense': 4.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 1, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Spear Goblins', 'Cost': 2, 'Attack': 1.3, 'Defense': 5.1, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 0, 'Swarm': 1, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Zap', 'Cost': 2, 'Attack': 1.2, 'Defense': 6.2, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 1, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 1, 'Reset': 1, 'AntiTank': 0},
    {'Name': 'Archers', 'Cost': 3, 'Attack': 3.5, 'Defense': 4.8, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 0, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Arrows', 'Cost': 3, 'Attack': 2.0, 'Defense': 7.0, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 1, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Cannon', 'Cost': 3, 'Attack': 0.8, 'Defense': 7.9, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 1, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Firecracker', 'Cost': 3, 'Attack': 3.5, 'Defense': 5.7, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 1, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Goblin Gang', 'Cost': 3, 'Attack': 3.5, 'Defense': 4.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 1, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Knight', 'Cost': 3, 'Attack': 3.5, 'Defense': 4.5, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 1, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Minions', 'Cost': 3, 'Attack': 3.5, 'Defense': 5.1, 'AirCounter': 1, 'GroundCounter': 0, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 1, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Royal Delivery', 'Cost': 3, 'Attack': 1.2, 'Defense': 5.7, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 1, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Skeleton Barrel', 'Cost': 3, 'Attack': 8.1, 'Defense': 2.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Mortar', 'Cost': 4, 'Attack': 8.1, 'Defense': 5.8, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 1, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Skeleton Dragons', 'Cost': 4, 'Attack': 3.9, 'Defense': 6.0, 'AirCounter': 1, 'GroundCounter': 0, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 1, 'Swarm': 1, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Tesla', 'Cost': 4, 'Attack': 0.8, 'Defense': 8.6, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 1, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Barbarians', 'Cost': 5, 'Attack': 4.2, 'Defense': 5.6, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 1, 'Support': 0, 'Reset': 0, 'AntiTank': 1},
    {'Name': 'Minion Horde', 'Cost': 5, 'Attack': 4.2, 'Defense': 5.1, 'AirCounter': 1, 'GroundCounter': 0, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 1, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Rascals', 'Cost': 5, 'Attack': 4.2, 'Defense': 5.1, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 0, 'Swarm': 1, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Elite Barbarians', 'Cost': 6, 'Attack': 4.8, 'Defense': 5.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 1},
    {'Name': 'Royal Giant', 'Cost': 6, 'Attack': 9.2, 'Defense': 2.0, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 1, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Royal Recruits', 'Cost': 7, 'Attack': 4.9, 'Defense': 4.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 1, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Heal Spirit', 'Cost': 1, 'Attack': 1.0, 'Defense': 3.2, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Ice Golem', 'Cost': 2, 'Attack': 1.3, 'Defense': 4.5, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 1, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Suspicious Bush', 'Cost': 2, 'Attack': 1.3, 'Defense': 4.0, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Dart Goblin', 'Cost': 3, 'Attack': 3.6, 'Defense': 4.8, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 0, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Earthquake', 'Cost': 3, 'Attack': 5.8, 'Defense': 3.0, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 1, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Elixir Golem', 'Cost': 3, 'Attack': 8.4, 'Defense': 2.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 1, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Mega Minion', 'Cost': 3, 'Attack': 3.5, 'Defense': 4.8, 'AirCounter': 1, 'GroundCounter': 0, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Tombstone', 'Cost': 3, 'Attack': 0.8, 'Defense': 8.2, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 1, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Battle Healer', 'Cost': 4, 'Attack': 3.9, 'Defense': 4.5, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 1, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Battle Ram', 'Cost': 4, 'Attack': 8.1, 'Defense': 2.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Bomb Tower', 'Cost': 4, 'Attack': 0.8, 'Defense': 8.4, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 1, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 1, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Fireball', 'Cost': 4, 'Attack': 4.5, 'Defense': 7.1, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 1, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Flying Machine', 'Cost': 4, 'Attack': 3.9, 'Defense': 4.8, 'AirCounter': 1, 'GroundCounter': 0, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 0, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Furnace', 'Cost': 4, 'Attack': 3.0, 'Defense': 5.0, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 1, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Goblin Cage', 'Cost': 4, 'Attack': 0.8, 'Defense': 8.2, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 1, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Goblin Demolisher', 'Cost': 4, 'Attack': 3.9, 'Defense': 4.0, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Goblin Hut', 'Cost': 4, 'Attack': 2.5, 'Defense': 5.0, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 1, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Hog Rider', 'Cost': 4, 'Attack': 9.0, 'Defense': 1.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Mini P.E.K.K.A', 'Cost': 4, 'Attack': 3.9, 'Defense': 5.8, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 1, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 1},
    {'Name': 'Minion Giant', 'Cost': 4, 'Attack': 3.9, 'Defense': 4.8, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 1, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Musketeer', 'Cost': 4, 'Attack': 3.9, 'Defense': 4.8, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 0, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Valkyrie', 'Cost': 4, 'Attack': 3.9, 'Defense': 5.4, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 1, 'Ranged': 0, 'Splash': 1, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Zappies', 'Cost': 4, 'Attack': 3.9, 'Defense': 5.5, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 0, 'Swarm': 1, 'Support': 1, 'Reset': 1, 'AntiTank': 0},
    {'Name': 'Giant', 'Cost': 5, 'Attack': 8.4, 'Defense': 2.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 1, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Inferno Tower', 'Cost': 5, 'Attack': 0.8, 'Defense': 9.0, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 1, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 1},
    {'Name': 'Royal Hogs', 'Cost': 5, 'Attack': 8.8, 'Defense': 2.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 1, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Wizard', 'Cost': 5, 'Attack': 4.2, 'Defense': 5.7, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 1, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Barbarian Hut', 'Cost': 6, 'Attack': 2.0, 'Defense': 4.5, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 1, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Elixir Collector', 'Cost': 6, 'Attack': 0.8, 'Defense': 1.0, 'AirCounter': 0, 'GroundCounter': 0, 'Building': 1, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Rocket', 'Cost': 6, 'Attack': 5.5, 'Defense': 5.6, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 1, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Three Musketeers', 'Cost': 9, 'Attack': 4.0, 'Defense': 6.4, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 0, 'Swarm': 1, 'Support': 1, 'Reset': 0, 'AntiTank': 1},
    {'Name': 'Barbarian Barrel', 'Cost': 2, 'Attack': 1.2, 'Defense': 7.2, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 1, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Goblin Curse', 'Cost': 2, 'Attack': 1.2, 'Defense': 5.7, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 1, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Rage', 'Cost': 2, 'Attack': 1.2, 'Defense': 2.0, 'AirCounter': 0, 'GroundCounter': 0, 'Building': 0, 'SmallSpell': 1, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Wall Breakers', 'Cost': 2, 'Attack': 8.2, 'Defense': 1.0, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Clone', 'Cost': 3, 'Attack': 1.2, 'Defense': 1.0, 'AirCounter': 0, 'GroundCounter': 0, 'Building': 0, 'SmallSpell': 1, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Goblin Barrel', 'Cost': 3, 'Attack': 8.7, 'Defense': 1.0, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Guards', 'Cost': 3, 'Attack': 3.5, 'Defense': 4.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 1, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Skeleton Army', 'Cost': 3, 'Attack': 3.5, 'Defense': 5.6, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 1, 'Support': 0, 'Reset': 0, 'AntiTank': 1},
    {'Name': 'Tornado', 'Cost': 3, 'Attack': 1.2, 'Defense': 5.7, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 1, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Vines', 'Cost': 3, 'Attack': 1.2, 'Defense': 5.7, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 1, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Baby Dragon', 'Cost': 4, 'Attack': 3.9, 'Defense': 5.7, 'AirCounter': 1, 'GroundCounter': 0, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 1, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Dark Prince', 'Cost': 4, 'Attack': 3.9, 'Defense': 5.4, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 1, 'Ranged': 0, 'Splash': 1, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Freeze', 'Cost': 4, 'Attack': 2.2, 'Defense': 4.5, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 1, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 1, 'Reset': 1, 'AntiTank': 0},
    {'Name': 'Goblin Drill', 'Cost': 4, 'Attack': 8.8, 'Defense': 2.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Hunter', 'Cost': 4, 'Attack': 3.9, 'Defense': 6.1, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 0, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 1},
    {'Name': 'Poison', 'Cost': 4, 'Attack': 4.8, 'Defense': 6.7, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 1, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Rune Giant', 'Cost': 4, 'Attack': 8.0, 'Defense': 2.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 1, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Balloon', 'Cost': 5, 'Attack': 9.2, 'Defense': 1.2, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Bowler', 'Cost': 5, 'Attack': 4.2, 'Defense': 4.9, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 1, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Cannon Cart', 'Cost': 5, 'Attack': 4.5, 'Defense': 4.0, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 0, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Electro Dragon', 'Cost': 5, 'Attack': 4.2, 'Defense': 6.1, 'AirCounter': 1, 'GroundCounter': 0, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 1, 'Swarm': 0, 'Support': 1, 'Reset': 1, 'AntiTank': 0},
    {'Name': 'Executioner', 'Cost': 5, 'Attack': 4.2, 'Defense': 5.7, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 1, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Prince', 'Cost': 5, 'Attack': 4.2, 'Defense': 5.8, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 1, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 1},
    {'Name': 'Void', 'Cost': 5, 'Attack': 2.2, 'Defense': 5.4, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 1, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Witch', 'Cost': 5, 'Attack': 4.2, 'Defense': 5.7, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 1, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Giant Skeleton', 'Cost': 6, 'Attack': 4.0, 'Defense': 4.9, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 1, 'MiniTank': 0, 'Ranged': 0, 'Splash': 1, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Goblin Giant', 'Cost': 6, 'Attack': 8.5, 'Defense': 2.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 1, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Lightning', 'Cost': 6, 'Attack': 4.0, 'Defense': 6.3, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 1, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 1, 'Reset': 1, 'AntiTank': 0},
    {'Name': 'X-Bow', 'Cost': 6, 'Attack': 9.0, 'Defense': 4.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 1, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Electro Giant', 'Cost': 7, 'Attack': 8.7, 'Defense': 2.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 1, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'P.E.K.K.A', 'Cost': 7, 'Attack': 3.5, 'Defense': 5.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 1},
    {'Name': 'Golem', 'Cost': 8, 'Attack': 9.4, 'Defense': 2.0, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 1, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Mirror', 'Cost': 1, 'Attack': 1.2, 'Defense': 2.0, 'AirCounter': 0, 'GroundCounter': 0, 'Building': 0, 'SmallSpell': 1, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'The Log', 'Cost': 2, 'Attack': 2.0, 'Defense': 7.0, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 1, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Bandit', 'Cost': 3, 'Attack': 4.5, 'Defense': 4.0, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Fisherman', 'Cost': 3, 'Attack': 3.5, 'Defense': 4.0, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Ice Wizard', 'Cost': 3, 'Attack': 3.5, 'Defense': 5.7, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 1, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Miner', 'Cost': 3, 'Attack': 7.4, 'Defense': 4.2, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Princess', 'Cost': 3, 'Attack': 3.7, 'Defense': 5.7, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 1, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Royal Ghost', 'Cost': 3, 'Attack': 4.0, 'Defense': 5.4, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 1, 'Ranged': 0, 'Splash': 1, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Electro Wizard', 'Cost': 4, 'Attack': 3.9, 'Defense': 6.1, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 1, 'Swarm': 0, 'Support': 1, 'Reset': 1, 'AntiTank': 0},
    {'Name': 'Inferno Dragon', 'Cost': 4, 'Attack': 3.9, 'Defense': 6.1, 'AirCounter': 1, 'GroundCounter': 0, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 1},
    {'Name': 'Lumberjack', 'Cost': 4, 'Attack': 3.9, 'Defense': 4.5, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 1, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Magic Archer', 'Cost': 4, 'Attack': 4.5, 'Defense': 4.8, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 0, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Mother Witch', 'Cost': 4, 'Attack': 3.9, 'Defense': 5.7, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 1, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Night Witch', 'Cost': 4, 'Attack': 3.9, 'Defense': 4.8, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 0, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Phoenix', 'Cost': 4, 'Attack': 3.9, 'Defense': 6.1, 'AirCounter': 1, 'GroundCounter': 0, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 1},
    {'Name': 'Goblin Machine', 'Cost': 5, 'Attack': 4.2, 'Defense': 4.8, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 0, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Graveyard', 'Cost': 5, 'Attack': 9.0, 'Defense': 1.0, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Ram Rider', 'Cost': 5, 'Attack': 8.7, 'Defense': 2.3, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Ronin', 'Cost': 5, 'Attack': 4.2, 'Defense': 4.5, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 1, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Sparky', 'Cost': 6, 'Attack': 4.5, 'Defense': 6.2, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 1, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 1},
    {'Name': 'Spirit Empress', 'Cost': 3, 'Attack': 3.5, 'Defense': 4.8, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Lava Hound', 'Cost': 7, 'Attack': 8.1, 'Defense': 2.0, 'AirCounter': 0, 'GroundCounter': 0, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 1, 'Tank': 1, 'MiniTank': 0, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Mega Knight', 'Cost': 7, 'Attack': 4.0, 'Defense': 4.9, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 1, 'MiniTank': 0, 'Ranged': 0, 'Splash': 1, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Little Prince', 'Cost': 3, 'Attack': 3.5, 'Defense': 4.8, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 0, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Golden Knight', 'Cost': 4, 'Attack': 3.9, 'Defense': 4.5, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 1, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Mighty Miner', 'Cost': 4, 'Attack': 3.9, 'Defense': 5.8, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 1, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 1},
    {'Name': 'Skeleton King', 'Cost': 4, 'Attack': 3.9, 'Defense': 4.5, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 1, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Archer Queen', 'Cost': 5, 'Attack': 4.2, 'Defense': 4.8, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 0, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Goblinstein', 'Cost': 5, 'Attack': 4.2, 'Defense': 6.1, 'AirCounter': 1, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 0, 'Ranged': 1, 'Splash': 0, 'Swarm': 0, 'Support': 1, 'Reset': 0, 'AntiTank': 1},
    {'Name': 'Monk', 'Cost': 5, 'Attack': 4.2, 'Defense': 4.5, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 1, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
    {'Name': 'Boss Bandit', 'Cost': 6, 'Attack': 4.6, 'Defense': 4.5, 'AirCounter': 0, 'GroundCounter': 1, 'Building': 0, 'SmallSpell': 0, 'BigSpell': 0, 'WinCondition': 0, 'Tank': 0, 'MiniTank': 1, 'Ranged': 0, 'Splash': 0, 'Swarm': 0, 'Support': 0, 'Reset': 0, 'AntiTank': 0},
]

data = [
    {'Name': 'Giant Graveyard Snowball', 'Cards': ['Giant Snowball', 'Bowler', 'Witch', 'Graveyard', 'Zappies', 'Guards', 'Giant', 'Arrows'], 'target': 7.61},
    {'Name': 'Hog Rider 2.6 Cycle', 'Cards': ['Skeletons', 'Musketeer', 'Cannon', 'Hog Rider', 'Fireball', 'Ice Spirit', 'Ice Golem', 'The Log'], 'target': 6.375},
    {'Name': 'Royal Hogs Earthquake Queen', 'Cards': ['Royal Hogs', 'Archer Queen', 'Cannon', 'The Log', 'Royal Delivery', 'Ice Spirit', 'Earthquake', 'Skeletons'], 'target': 8.058},
    {'Name': 'Goblin Barrel Wall Breakers', 'Cards': ['Goblin Barrel', 'Valkyrie', 'Skeleton Army', 'Cannon', 'Ice Spirit', 'Dart Goblin', 'Princess', 'Wall Breakers'], 'target': 7.5},
    {'Name': 'LavaLoon Fireball', 'Cards': ['Zap', 'Mega Minion', 'Baby Dragon', 'Tombstone', 'Balloon', 'Lava Hound', 'Fireball', 'Barbarians'], 'target': 8.023},
    {'Name': 'Cannon Graveyard Poison', 'Cards': ['Cannon', 'Ice Wizard', 'Bats', 'Graveyard', 'Poison', 'Skeletons', 'Knight', 'Barbarian Barrel'], 'target': 8.279},
    {'Name': 'Hog EQ Mighty Miner', 'Cards': ['Cannon', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Skeletons', 'Electro Spirit', 'Barbarian Barrel'], 'target': 8.406},
    {'Name': 'Classic Log Bait', 'Cards': ['Skeleton Army', 'Knight', 'Goblin Barrel', 'Dart Goblin', 'Princess', 'The Log', 'Ice Spirit', 'Inferno Tower'], 'target': 7.94},
    {'Name': 'Hog EQ Tesla Mighty Miner', 'Cards': ['Tesla', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Skeletons', 'Electro Spirit', 'Barbarian Barrel'], 'target': 8.348},
    {'Name': 'Goblin Drill Snowball Poison', 'Cards': ['Giant Snowball', 'Knight', 'Goblin Drill', 'Fire Spirit', 'Poison', 'Skeletons', 'Goblin Demolisher', 'Tesla'], 'target': 7.626},
    {'Name': 'Giant Skeleton Battle Ram', 'Cards': ['Battle Ram', 'Electro Wizard', 'Lumberjack', 'Giant Skeleton', 'Bandit', 'Furnace', 'Arrows', 'Heal Spirit'], 'target': 7.166},
    {'Name': 'X-Bow 3.0 Archers', 'Cards': ['Tesla', 'Knight', 'Archers', 'Fireball', 'X-Bow', 'Electro Spirit', 'Skeletons', 'The Log'], 'target': 7.836},
    {'Name': 'Royal Giant Fisherman', 'Cards': ['Royal Giant', 'Barbarian Barrel', 'Royal Ghost', 'Hunter', 'Fireball', 'Fisherman', 'Electro Spirit', 'Skeletons'], 'target': 8.492},
    {'Name': 'Mega Knight Ram Rider Empress', 'Cards': ['Mega Knight', 'Ice Wizard', 'Royal Ghost', 'Poison', 'Spirit Empress', 'Ram Rider', 'Bandit', 'Zap'], 'target': 7.81},
    {'Name': 'Golem Collector Berserker', 'Cards': ['Elite Barbarians', 'Berserker', 'Electro Dragon', 'Golem', 'Elixir Collector', 'Tornado', 'Skeleton Dragons', 'Barbarian Barrel'], 'target': 7.238},
    {'Name': 'Giant Skeleton Hog Lightning', 'Cards': ['Firecracker', 'Guards', 'Minion Horde', 'Giant Skeleton', 'Barbarians', 'Lightning', 'Hog Rider', 'The Log'], 'target': 8.059},
    {'Name': 'Royal Recruits Royal Hogs', 'Cards': ['Royal Recruits', 'Barbarian Barrel', 'Goblin Cage', 'Royal Hogs', 'Zappies', 'Flying Machine', 'Arrows', 'Electro Spirit'], 'target': 7.428},
    {'Name': 'Hog Freeze Ronin', 'Cards': ['Minion Horde', 'Boss Bandit', 'Elite Barbarians', 'Executioner', 'Freeze', 'Hog Rider', 'Ronin', 'Zap'], 'target': 7.746},
    {'Name': 'Giant Sparky Ebarbs', 'Cards': ['Elite Barbarians', 'Giant', 'Zap', 'Sparky', 'Mini P.E.K.K.A', 'Heal Spirit', 'Electro Wizard', 'Rage'], 'target': 7.595},
    {'Name': 'Splashyard', 'Cards': ['Knight', 'Ice Wizard', 'Tombstone', 'Poison', 'Baby Dragon', 'Barbarian Barrel', 'Tornado', 'Graveyard'], 'target': 8.32},
    {'Name': 'X-Bow Ice Wizard Rocket', 'Cards': ['Knight', 'Ice Wizard', 'Tesla', 'Rocket', 'The Log', 'Skeletons', 'X-Bow', 'Tornado'], 'target': 7.803},
    {'Name': 'Golem Night Witch Phoenix Fireball', 'Cards': ['Elite Barbarians', 'Mini P.E.K.K.A', 'Zap', 'Golem', 'Phoenix', 'Night Witch', 'Fireball', 'Bomber'], 'target': 8.431},
    {'Name': 'Mortar Goblinstein Cart', 'Cards': ['Mortar', 'Goblinstein', 'Minion Horde', 'Fireball', 'Barbarian Barrel', 'Goblin Gang', 'Mother Witch', 'Cannon Cart'], 'target': 7.796},
    {'Name': 'Goblin Giant Sparky Rage', 'Cards': ['Zap', 'Mini P.E.K.K.A', 'Goblin Giant', 'Sparky', 'Dark Prince', 'Electro Wizard', 'Heal Spirit', 'Rage'], 'target': 7.695},
    {'Name': 'Graveyard Furnace Goblin Hut', 'Cards': ['Furnace', 'Ice Wizard', 'Knight', 'Poison', 'Graveyard', 'Barbarian Barrel', 'Goblin Hut', 'Skeletons'], 'target': 7.761},
    {'Name': 'Golem Night Witch Phoenix Arrows', 'Cards': ['Elite Barbarians', 'Mini P.E.K.K.A', 'Zap', 'Arrows', 'Phoenix', 'Night Witch', 'Golem', 'Bomber'], 'target': 8.087},
    {'Name': 'Goblin Drill Snowball Bomber', 'Cards': ['Giant Snowball', 'Knight', 'Goblin Drill', 'Skeletons', 'Bomber', 'Poison', 'Fire Spirit', 'Cannon'], 'target': 7.554},
    {'Name': 'Mortar Skeleton Barrel Bait', 'Cards': ['Mortar', 'Ice Wizard', 'Skeleton Barrel', 'Cannon Cart', 'Rascals', 'Fireball', 'Goblin Gang', 'Barbarian Barrel'], 'target': 7.565},
    {'Name': 'Golem Elixir Golem', 'Cards': ['Inferno Dragon', 'Mini P.E.K.K.A', 'Witch', 'Golem', 'Elixir Golem', 'Night Witch', 'Arrows', 'Rage'], 'target': 8.271},
    {'Name': 'Balloon Miner Snowball', 'Cards': ['Musketeer', 'Balloon', 'Giant Snowball', 'Barbarian Barrel', 'Skeletons', 'Miner', 'Ice Golem', 'Bomb Tower'], 'target': 7.435},
    {'Name': 'Giant Sparky Vines Wizard', 'Cards': ['Giant', 'Mini P.E.K.K.A', 'Wizard', 'Vines', 'Zap', 'Tornado', 'Sparky', 'Heal Spirit'], 'target': 7.64},
    {'Name': 'Giant Graveyard Snowball (Guards -> Goblin Gang)', 'Cards': ['Giant Snowball', 'Bowler', 'Witch', 'Graveyard', 'Zappies', 'Goblin Gang', 'Giant', 'Arrows'], 'target': 7.61},
    {'Name': 'Giant Graveyard Snowball (Giant Snowball -> Zap)', 'Cards': ['Zap', 'Bowler', 'Witch', 'Graveyard', 'Zappies', 'Guards', 'Giant', 'Arrows'], 'target': 7.605},
    {'Name': 'Giant Graveyard Snowball (Giant Snowball -> The Log)', 'Cards': ['The Log', 'Bowler', 'Witch', 'Graveyard', 'Zappies', 'Guards', 'Giant', 'Arrows'], 'target': 7.669},
    {'Name': 'Giant Graveyard Snowball (Arrows -> The Log)', 'Cards': ['Giant Snowball', 'Bowler', 'Witch', 'Graveyard', 'Zappies', 'Guards', 'Giant', 'The Log'], 'target': 7.618},
    {'Name': 'Giant Graveyard Snowball (Zappies -> Flying Machine)', 'Cards': ['Giant Snowball', 'Bowler', 'Witch', 'Graveyard', 'Flying Machine', 'Guards', 'Giant', 'Arrows'], 'target': 7.58},
    {'Name': 'Hog Rider 2.6 Cycle (Skeletons -> Goblins)', 'Cards': ['Goblins', 'Musketeer', 'Cannon', 'Hog Rider', 'Fireball', 'Ice Spirit', 'Ice Golem', 'The Log'], 'target': 8.416},
    {'Name': 'Hog Rider 2.6 Cycle (Fireball -> Earthquake)', 'Cards': ['Skeletons', 'Musketeer', 'Cannon', 'Hog Rider', 'Earthquake', 'Ice Spirit', 'Ice Golem', 'The Log'], 'target': 8.545},
    {'Name': 'Hog Rider 2.6 Cycle (Ice Spirit -> Fire Spirit)', 'Cards': ['Skeletons', 'Musketeer', 'Cannon', 'Hog Rider', 'Fireball', 'Fire Spirit', 'Ice Golem', 'The Log'], 'target': 8.373},
    {'Name': 'Hog Rider 2.6 Cycle (Skeletons -> Guards)', 'Cards': ['Guards', 'Musketeer', 'Cannon', 'Hog Rider', 'Fireball', 'Ice Spirit', 'Ice Golem', 'The Log'], 'target': 8.435},
    {'Name': 'Hog Rider 2.6 Cycle (Musketeer -> Firecracker)', 'Cards': ['Skeletons', 'Firecracker', 'Cannon', 'Hog Rider', 'Fireball', 'Ice Spirit', 'Ice Golem', 'The Log'], 'target': 8.271},
    {'Name': 'Royal Hogs Earthquake Queen (Skeletons -> Goblins)', 'Cards': ['Royal Hogs', 'Archer Queen', 'Cannon', 'The Log', 'Royal Delivery', 'Ice Spirit', 'Earthquake', 'Goblins'], 'target': 8.067},
    {'Name': 'Royal Hogs Earthquake Queen (Archer Queen -> Little Prince)', 'Cards': ['Royal Hogs', 'Little Prince', 'Cannon', 'The Log', 'Royal Delivery', 'Ice Spirit', 'Earthquake', 'Skeletons'], 'target': 8.038},
    {'Name': 'Royal Hogs Earthquake Queen (Archer Queen -> Musketeer)', 'Cards': ['Royal Hogs', 'Musketeer', 'Cannon', 'The Log', 'Royal Delivery', 'Ice Spirit', 'Earthquake', 'Skeletons'], 'target': 8.049},
    {'Name': 'Royal Hogs Earthquake Queen (The Log -> Barbarian Barrel)', 'Cards': ['Royal Hogs', 'Archer Queen', 'Cannon', 'Barbarian Barrel', 'Royal Delivery', 'Ice Spirit', 'Earthquake', 'Skeletons'], 'target': 8.044},
    {'Name': 'Royal Hogs Earthquake Queen (Cannon -> Bomb Tower)', 'Cards': ['Royal Hogs', 'Archer Queen', 'Bomb Tower', 'The Log', 'Royal Delivery', 'Ice Spirit', 'Earthquake', 'Skeletons'], 'target': 8.091},
    {'Name': 'Goblin Barrel Wall Breakers (Cannon -> Bomb Tower)', 'Cards': ['Goblin Barrel', 'Valkyrie', 'Skeleton Army', 'Bomb Tower', 'Ice Spirit', 'Dart Goblin', 'Princess', 'Wall Breakers'], 'target': 7.533},
    {'Name': 'Goblin Barrel Wall Breakers (Valkyrie -> Mini P.E.K.K.A)', 'Cards': ['Goblin Barrel', 'Mini P.E.K.K.A', 'Skeleton Army', 'Cannon', 'Ice Spirit', 'Dart Goblin', 'Princess', 'Wall Breakers'], 'target': 7.553},
    {'Name': 'Goblin Barrel Wall Breakers (Cannon -> Tombstone)', 'Cards': ['Goblin Barrel', 'Valkyrie', 'Skeleton Army', 'Tombstone', 'Ice Spirit', 'Dart Goblin', 'Princess', 'Wall Breakers'], 'target': 7.515},
    {'Name': 'Goblin Barrel Wall Breakers (Wall Breakers -> Miner)', 'Cards': ['Goblin Barrel', 'Valkyrie', 'Skeleton Army', 'Cannon', 'Ice Spirit', 'Dart Goblin', 'Princess', 'Miner'], 'target': 7.509},
    {'Name': 'Goblin Barrel Wall Breakers (Valkyrie -> Dark Prince)', 'Cards': ['Goblin Barrel', 'Dark Prince', 'Skeleton Army', 'Cannon', 'Ice Spirit', 'Dart Goblin', 'Princess', 'Wall Breakers'], 'target': 7.5},
    {'Name': 'LavaLoon Fireball (Zap -> Arrows)', 'Cards': ['Arrows', 'Mega Minion', 'Baby Dragon', 'Tombstone', 'Balloon', 'Lava Hound', 'Fireball', 'Barbarians'], 'target': 7.972},
    {'Name': 'LavaLoon Fireball (Baby Dragon -> Electro Dragon)', 'Cards': ['Zap', 'Mega Minion', 'Electro Dragon', 'Tombstone', 'Balloon', 'Lava Hound', 'Fireball', 'Barbarians'], 'target': 8.087},
    {'Name': 'LavaLoon Fireball (Mega Minion -> Skeleton Dragons)', 'Cards': ['Zap', 'Skeleton Dragons', 'Baby Dragon', 'Tombstone', 'Balloon', 'Lava Hound', 'Fireball', 'Barbarians'], 'target': 8.018},
    {'Name': 'LavaLoon Fireball (Mega Minion -> Phoenix)', 'Cards': ['Zap', 'Phoenix', 'Baby Dragon', 'Tombstone', 'Balloon', 'Lava Hound', 'Fireball', 'Barbarians'], 'target': 8.018},
    {'Name': 'LavaLoon Fireball (Tombstone -> Cannon)', 'Cards': ['Zap', 'Mega Minion', 'Baby Dragon', 'Cannon', 'Balloon', 'Lava Hound', 'Fireball', 'Barbarians'], 'target': 8.008},
    {'Name': 'Cannon Graveyard Poison (Cannon -> Goblin Cage)', 'Cards': ['Goblin Cage', 'Ice Wizard', 'Bats', 'Graveyard', 'Poison', 'Skeletons', 'Knight', 'Barbarian Barrel'], 'target': 8.302},
    {'Name': 'Cannon Graveyard Poison (Skeletons -> Goblins)', 'Cards': ['Cannon', 'Ice Wizard', 'Bats', 'Graveyard', 'Poison', 'Goblins', 'Knight', 'Barbarian Barrel'], 'target': 8.287},
    {'Name': 'Cannon Graveyard Poison (Knight -> Royal Ghost)', 'Cards': ['Cannon', 'Ice Wizard', 'Bats', 'Graveyard', 'Poison', 'Skeletons', 'Royal Ghost', 'Barbarian Barrel'], 'target': 8.121},
    {'Name': 'Cannon Graveyard Poison (Bats -> Skeleton Dragons)', 'Cards': ['Cannon', 'Ice Wizard', 'Skeleton Dragons', 'Graveyard', 'Poison', 'Skeletons', 'Knight', 'Barbarian Barrel'], 'target': 8.307},
    {'Name': 'Cannon Graveyard Poison (Cannon -> Tombstone)', 'Cards': ['Tombstone', 'Ice Wizard', 'Bats', 'Graveyard', 'Poison', 'Skeletons', 'Knight', 'Barbarian Barrel'], 'target': 8.294},
    {'Name': 'Hog EQ Mighty Miner (Firecracker -> Musketeer)', 'Cards': ['Cannon', 'Mighty Miner', 'Musketeer', 'Hog Rider', 'Earthquake', 'Skeletons', 'Electro Spirit', 'Barbarian Barrel'], 'target': 8.543},
    {'Name': 'Hog EQ Mighty Miner (Skeletons -> Goblins)', 'Cards': ['Cannon', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Goblins', 'Electro Spirit', 'Barbarian Barrel'], 'target': 8.415},
    {'Name': 'Hog EQ Mighty Miner (Mighty Miner -> Mini P.E.K.K.A)', 'Cards': ['Cannon', 'Mini P.E.K.K.A', 'Firecracker', 'Hog Rider', 'Earthquake', 'Skeletons', 'Electro Spirit', 'Barbarian Barrel'], 'target': 8.406},
    {'Name': 'Hog EQ Mighty Miner (Cannon -> Goblin Cage)', 'Cards': ['Goblin Cage', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Skeletons', 'Electro Spirit', 'Barbarian Barrel'], 'target': 8.326},
    {'Name': 'Hog EQ Mighty Miner (Skeletons -> Ice Spirit)', 'Cards': ['Cannon', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Ice Spirit', 'Electro Spirit', 'Barbarian Barrel'], 'target': 8.441},
    {'Name': 'Classic Log Bait (The Log -> Giant Snowball)', 'Cards': ['Skeleton Army', 'Knight', 'Goblin Barrel', 'Dart Goblin', 'Princess', 'Giant Snowball', 'Ice Spirit', 'Inferno Tower'], 'target': 7.916},
    {'Name': 'Classic Log Bait (Dart Goblin -> Archers)', 'Cards': ['Skeleton Army', 'Knight', 'Goblin Barrel', 'Archers', 'Princess', 'The Log', 'Ice Spirit', 'Inferno Tower'], 'target': 7.94},
    {'Name': 'Classic Log Bait (The Log -> Zap)', 'Cards': ['Skeleton Army', 'Knight', 'Goblin Barrel', 'Dart Goblin', 'Princess', 'Zap', 'Ice Spirit', 'Inferno Tower'], 'target': 7.916},
    {'Name': 'Classic Log Bait (Skeleton Army -> Guards)', 'Cards': ['Guards', 'Knight', 'Goblin Barrel', 'Dart Goblin', 'Princess', 'The Log', 'Ice Spirit', 'Inferno Tower'], 'target': 7.94},
    {'Name': 'Classic Log Bait (Inferno Tower -> Goblin Cage)', 'Cards': ['Skeleton Army', 'Knight', 'Goblin Barrel', 'Dart Goblin', 'Princess', 'The Log', 'Ice Spirit', 'Goblin Cage'], 'target': 7.932},
    {'Name': 'Hog EQ Tesla Mighty Miner (Barbarian Barrel -> Zap)', 'Cards': ['Tesla', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Skeletons', 'Electro Spirit', 'Zap'], 'target': 8.339},
    {'Name': 'Hog EQ Tesla Mighty Miner (Barbarian Barrel -> The Log)', 'Cards': ['Tesla', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Skeletons', 'Electro Spirit', 'The Log'], 'target': 8.452},
    {'Name': 'Hog EQ Tesla Mighty Miner (Skeletons -> Goblins)', 'Cards': ['Tesla', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Goblins', 'Electro Spirit', 'Barbarian Barrel'], 'target': 8.356},
    {'Name': 'Hog EQ Tesla Mighty Miner (Electro Spirit -> Fire Spirit)', 'Cards': ['Tesla', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Skeletons', 'Fire Spirit', 'Barbarian Barrel'], 'target': 8.346},
    {'Name': 'Hog EQ Tesla Mighty Miner (Tesla -> Inferno Tower)', 'Cards': ['Inferno Tower', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Skeletons', 'Electro Spirit', 'Barbarian Barrel'], 'target': 8.356},
    {'Name': 'Goblin Drill Snowball Poison (Skeletons -> Electro Spirit)', 'Cards': ['Giant Snowball', 'Knight', 'Goblin Drill', 'Fire Spirit', 'Poison', 'Electro Spirit', 'Goblin Demolisher', 'Tesla'], 'target': 7.678},
    {'Name': 'Goblin Drill Snowball Poison (Knight -> Mini P.E.K.K.A)', 'Cards': ['Giant Snowball', 'Mini P.E.K.K.A', 'Goblin Drill', 'Fire Spirit', 'Poison', 'Skeletons', 'Goblin Demolisher', 'Tesla'], 'target': 7.863},
    {'Name': 'Goblin Drill Snowball Poison (Fire Spirit -> Bomber)', 'Cards': ['Giant Snowball', 'Knight', 'Goblin Drill', 'Bomber', 'Poison', 'Skeletons', 'Goblin Demolisher', 'Tesla'], 'target': 7.603},
    {'Name': 'Goblin Drill Snowball Poison (Knight -> Royal Ghost)', 'Cards': ['Giant Snowball', 'Royal Ghost', 'Goblin Drill', 'Fire Spirit', 'Poison', 'Skeletons', 'Goblin Demolisher', 'Tesla'], 'target': 7.628},
    {'Name': 'Mixed deck 01', 'Cards': ['Royal Hogs', 'Little Prince', 'Minions', 'The Log', 'Royal Delivery', 'Ice Spirit', 'Earthquake', 'Cannon Cart'], 'target': 7.946},
    {'Name': 'Mixed deck 02', 'Cards': ['Cannon', 'Mighty Miner', 'Firecracker', 'Royal Giant', 'Earthquake', 'Zappies', 'Electro Spirit', 'Barbarian Barrel'], 'target': 8.381},
    {'Name': 'Mixed deck 03', 'Cards': ['Dart Goblin', 'Ice Wizard', 'Tombstone', 'Poison', 'Baby Dragon', 'Electro Giant', 'Minion Horde', 'Barbarians'], 'target': 7.673},
    {'Name': 'Mixed deck 04', 'Cards': ['Giant Snowball', 'Executioner', 'Goblin Curse', 'Graveyard', 'Flying Machine', 'Princess', 'Giant', 'Goblin Hut'], 'target': 7.541},
    {'Name': 'Mixed deck 05', 'Cards': ['Skeletons', 'Electro Giant', 'Furnace', 'Hog Rider', 'Boss Bandit', 'Ice Spirit', 'Ice Golem', 'The Log'], 'target': 6.605},
    {'Name': 'Mixed deck 06', 'Cards': ['Minion Horde', 'Boss Bandit', 'Skeleton King', 'Executioner', 'Lightning', 'Hog Rider', 'Ronin', 'Zap'], 'target': 7.632},
    {'Name': 'Mixed deck 07', 'Cards': ['Goblin Barrel', 'Dark Prince', 'Night Witch', 'Cannon', 'Ice Spirit', 'Dart Goblin', 'Suspicious Bush', 'Wall Breakers'], 'target': 7.039},
    {'Name': 'Mixed deck 08', 'Cards': ['Cannon', 'Mighty Miner', 'X-Bow', 'Hog Rider', 'The Log', 'Elixir Collector', 'Valkyrie', 'Barbarian Barrel'], 'target': 5.971},
    {'Name': 'Mixed deck 09', 'Cards': ['Hog Rider', 'Berserker', 'Giant Skeleton', 'Inferno Tower', 'Goblin Drill', 'Cannon', 'Royal Delivery', 'Balloon'], 'target': 6.089},
    {'Name': 'Mixed deck 10', 'Cards': ['Royal Giant', 'Giant Snowball', 'Elite Barbarians', 'Spirit Empress', 'Clone', 'Fisherman', 'Elixir Golem', 'Skeletons'], 'target': 7.219},
    {'Name': 'Mixed deck 11', 'Cards': ['Spirit Empress', 'Sparky', 'Mega Knight', 'Golem', 'Elixir Collector', 'Tornado', 'Royal Hogs', 'Barbarian Barrel'], 'target': 6.963},
    {'Name': 'Mixed deck 12', 'Cards': ['Ram Rider', 'Ice Wizard', 'Bats', 'Minion Horde', 'Poison', 'Skeletons', 'Knight', 'Barbarian Barrel'], 'target': 7.719},
    {'Name': 'Mixed deck 13', 'Cards': ['Battle Ram', 'Electro Wizard', 'Lightning', 'Giant Skeleton', 'Bandit', 'Royal Ghost', 'Spirit Empress', 'Heal Spirit'], 'target': 7.287},
    {'Name': 'Mixed deck 14', 'Cards': ['Firecracker', 'Guards', 'Minion Horde', 'Baby Dragon', 'Lumberjack', 'Lightning', 'Hog Rider', 'Zap'], 'target': 7.679},
    {'Name': 'Mixed deck 15', 'Cards': ['Bomb Tower', 'Ronin', 'Bats', 'Ice Wizard', 'Goblin Barrel', 'Knight', 'Skeletons', 'Graveyard'], 'target': 7.142},
    {'Name': 'Mixed deck 16', 'Cards': ['Suspicious Bush', 'Ronin', 'Goblin Barrel', 'Dart Goblin', 'Princess', 'Giant Snowball', 'Ice Spirit', 'Inferno Tower'], 'target': 7.917},
    {'Name': 'Mixed deck 17', 'Cards': ['Goblin Demolisher', 'Guards', 'Skeleton Dragons', 'Ice Golem', 'Barbarians', 'Lightning', 'Bats', 'Rune Giant'], 'target': 7.041},
    {'Name': 'Mixed deck 18', 'Cards': ['Tombstone', 'Ice Wizard', 'Fire Spirit', 'Graveyard', 'Poison', 'Skeletons', 'Royal Hogs', 'Barbarian Barrel'], 'target': 8.044},
    {'Name': 'Mixed deck 19', 'Cards': ['Tesla', 'Executioner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Skeletons', 'Skeleton Barrel', 'Magic Archer'], 'target': 7.591},
    {'Name': 'Mixed deck 20', 'Cards': ['Goblin Demolisher', 'Royal Ghost', 'Goblin Drill', 'Fire Spirit', 'Bandit', 'Skeletons', 'Furnace', 'Tombstone'], 'target': 5.617},
    {'Name': 'Mixed deck 21', 'Cards': ['Knight', 'Ice Wizard', 'Tesla', 'Rocket', 'Skeleton Barrel', 'Skeletons', 'X-Bow', 'Golden Knight'], 'target': 7.351},
    {'Name': 'Mixed deck 22', 'Cards': ['Zap', 'Inferno Tower', 'Bats', 'Fireball', 'Barbarian Barrel', 'Knight', 'Skeletons', 'Royal Giant'], 'target': 7.831},
    {'Name': 'Mixed deck 23', 'Cards': ['Valkyrie', 'Heal Spirit', 'Vines', 'X-Bow', 'Fisherman', 'Elixir Collector', 'Rage', 'Three Musketeers'], 'target': 6.981},
    {'Name': 'Mixed deck 24', 'Cards': ['Elite Barbarians', 'Giant', 'Zap', 'Ice Wizard', 'Prince', 'Heal Spirit', 'Goblin Drill', 'Rage'], 'target': 7.588},
    {'Name': 'Mixed deck 25', 'Cards': ['Battle Ram', 'Inferno Tower', 'Lumberjack', 'Goblin Drill', 'Cannon Cart', 'Furnace', 'Zap', 'Heal Spirit'], 'target': 6.52},
    {'Name': 'Mixed deck 26', 'Cards': ['Heal Spirit', 'Elixir Golem', 'Prince', 'Executioner', 'Freeze', 'Hog Rider', 'Cannon Cart', 'Fireball'], 'target': 7.782},
    {'Name': 'Mixed deck 27', 'Cards': ['X-Bow', 'Mighty Miner', 'Cannon', 'Lightning', 'The Log', 'Electro Spirit', 'Minion Giant', 'Suspicious Bush'], 'target': 7.495},
    {'Name': 'Mixed deck 28', 'Cards': ['Cannon', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Ice Spirit', 'Skeletons', 'Flying Machine', 'Barbarian Barrel'], 'target': 7.867},
    {'Name': 'Mixed deck 29', 'Cards': ['Royal Giant', 'Zap', 'Knight', 'Hunter', 'Fireball', 'Void', 'Bomber', 'Skeletons'], 'target': 8.177},
    {'Name': 'Mixed deck 30', 'Cards': ['Miner', 'Mighty Miner', 'Firecracker', 'Royal Giant', 'Earthquake', 'Skeletons', 'Barbarians', 'Barbarian Barrel'], 'target': 7.485},
    {'Name': 'Mixed deck 31', 'Cards': ['Mega Knight', 'Ice Wizard', 'Sparky', 'Executioner', 'Clone', 'Ram Rider', 'Inferno Dragon', 'Giant Snowball'], 'target': 7.549},
    {'Name': 'Mixed deck 32', 'Cards': ['Cannon', 'Goblin Demolisher', 'Firecracker', 'Hog Rider', 'Earthquake', 'Goblins', 'Zappies', 'Barbarian Barrel'], 'target': 8.084},
    {'Name': 'Mixed deck 33', 'Cards': ['Elite Barbarians', 'Mini P.E.K.K.A', 'Zap', 'Golem', 'Musketeer', 'Archers', 'Fireball', 'Bomber'], 'target': 8.232},
    {'Name': 'Mixed deck 34', 'Cards': ['The Log', 'Bowler', 'Witch', 'Inferno Dragon', 'Zappies', 'Fireball', 'Giant', 'Arrows'], 'target': 8.095},
    {'Name': 'Mixed deck 35', 'Cards': ['Royal Giant', 'Barbarian Barrel', 'Royal Ghost', 'Hunter', 'Fireball', 'Dart Goblin', 'Clone', 'Skeletons'], 'target': 8.298},
    {'Name': 'Mixed deck 36', 'Cards': ['Giant', 'Mini P.E.K.K.A', 'Wizard', 'Bandit', 'Zap', 'Tornado', 'Sparky', 'Rune Giant'], 'target': 7.734},
    {'Name': 'Mixed deck 37', 'Cards': ['Zap', 'Bowler', 'Archers', 'Arrows', 'Zappies', 'Guards', 'Giant', 'Archer Queen'], 'target': 7.297},
    {'Name': 'Mixed deck 38', 'Cards': ['Vines', 'Ice Spirit', 'Tesla', 'Rocket', 'Minions', 'Skeletons', 'X-Bow', 'Tornado'], 'target': 7.395},
    {'Name': 'Mixed deck 39', 'Cards': ['Electro Giant', 'Mini P.E.K.K.A', 'Wizard', 'Vines', 'Zap', 'Tornado', 'Cannon Cart', 'Witch'], 'target': 7.669},
    {'Name': 'Mixed deck 40', 'Cards': ['Furnace', 'Ice Wizard', 'Knight', 'Mirror', 'Graveyard', 'Cannon', 'Goblin Hut', 'Skeletons'], 'target': 5.963},
    {'Name': 'Mixed deck 41', 'Cards': ['Boss Bandit', 'Ice Wizard', 'Royal Ghost', 'Lightning', 'Musketeer', 'Ram Rider', 'Bandit', 'Skeleton Army'], 'target': 7.704},
    {'Name': 'Mixed deck 42', 'Cards': ['Goblin Barrel', 'Tornado', 'Skeleton Army', 'Tombstone', 'Ice Spirit', 'Dart Goblin', 'Valkyrie', 'Wall Breakers'], 'target': 7.579},
    {'Name': 'Mixed deck 43', 'Cards': ['Minion Horde', 'Boss Bandit', 'Prince', 'Royal Giant', 'Lumberjack', 'Hog Rider', 'Ronin', 'Zap'], 'target': 6.964},
    {'Name': 'Mixed deck 44', 'Cards': ['Battle Ram', 'Boss Bandit', 'Elite Barbarians', 'Executioner', 'Phoenix', 'Hog Rider', 'Ronin', 'Arrows'], 'target': 7.554},
    {'Name': 'Mixed deck 45', 'Cards': ['Royal Hogs', 'Musketeer', 'Cannon', 'The Log', 'Valkyrie', 'Tombstone', 'Firecracker', 'Skeletons'], 'target': 7.236},
    {'Name': 'Weak deck 01', 'Cards': ['Cannon', 'Inferno Tower', 'Bomb Tower', 'X-Bow', 'Tombstone', 'Furnace', 'Phoenix', 'Electro Spirit'], 'target': 4.655},
    {'Name': 'Weak deck 02', 'Cards': ['Arrows', 'The Log', 'Goblin Curse', 'Royal Delivery', 'Lightning', 'Vines', 'Bandit', 'Wizard'], 'target': 3.3},
    {'Name': 'Weak deck 03', 'Cards': ['Cannon', 'Skeleton Army', 'Elixir Collector', 'Barbarians', 'Guards', 'Suspicious Bush', 'Goblin Gang', 'Skeletons'], 'target': 3.3},
    {'Name': 'Weak deck 04', 'Cards': ['Goblin Gang', 'Freeze', 'Bomb Tower', 'Goblinstein', 'Hunter', 'Mini P.E.K.K.A', 'Cannon Cart', 'Inferno Tower'], 'target': 3.3},
    {'Name': 'Weak deck 05', 'Cards': ['Mortar', 'Bomb Tower', 'Elixir Collector', 'Goblin Cage', 'Fire Spirit', 'Heal Spirit', 'Electro Spirit', 'Ice Spirit'], 'target': 5.302},
    {'Name': 'Weak deck 06', 'Cards': ['Lightning', 'Vines', 'Rocket', 'Rage', 'Earthquake', 'Zap', 'Electro Spirit', 'Ice Spirit'], 'target': 3.3},
    {'Name': 'Weak deck 07', 'Cards': ['Cannon Cart', 'Clone', 'Suspicious Bush', 'Goblin Demolisher', 'Sparky', 'Prince', 'P.E.K.K.A', 'Ronin'], 'target': 3.3},
    {'Name': 'Weak deck 08', 'Cards': ['Valkyrie', 'Rage', 'Hunter', 'Furnace', 'Clone', 'Giant Snowball', 'Dark Prince', 'The Log'], 'target': 3.3},
    {'Name': 'Weak deck 09', 'Cards': ['X-Bow', 'Inferno Tower', 'Furnace', 'Bomb Tower', 'Ice Spirit', 'Heal Spirit', 'Fire Spirit', 'Electro Spirit'], 'target': 5.644},
    {'Name': 'Weak deck 10', 'Cards': ['Tesla', 'Goblin Hut', 'Elixir Collector', 'Goblin Cage', 'Bomb Tower', 'Goblin Demolisher', 'Tornado', 'P.E.K.K.A'], 'target': 3.231},
    {'Name': 'Weak deck 11', 'Cards': ['Goblin Curse', 'Mirror', 'Vines', 'Earthquake', 'Rage', 'Zap', 'Berserker', 'Arrows'], 'target': 3.3},
    {'Name': 'Weak deck 12', 'Cards': ['Berserker', 'Boss Bandit', 'Clone', 'Royal Ghost', 'Ice Golem', 'Elite Barbarians', 'Knight', 'Rage'], 'target': 3.3},
    {'Name': 'Weak deck 13', 'Cards': ['Sparky', 'Ice Wizard', 'Mirror', 'Ice Golem', 'Boss Bandit', 'Electro Wizard', 'Skeletons', 'Suspicious Bush'], 'target': 3.3},
    {'Name': 'Weak deck 14', 'Cards': ['Elixir Collector', 'Goblin Cage', 'Bomb Tower', 'Barbarian Hut', 'Fire Spirit', 'Electro Spirit', 'Ice Spirit', 'Heal Spirit'], 'target': 3.3},
    {'Name': 'Weak deck 15', 'Cards': ['Tesla', 'Mortar', 'X-Bow', 'Cannon', 'Elixir Collector', 'Dark Prince', 'Baby Dragon', 'Firecracker'], 'target': 5.376},
    {'Name': 'Weak deck 16', 'Cards': ['Barbarian Barrel', 'Giant Snowball', 'Rocket', 'Mirror', 'Goblin Curse', 'Lightning', 'Ice Spirit', 'Royal Ghost'], 'target': 3.3},
    {'Name': 'Weak deck 17', 'Cards': ['Mighty Miner', 'Battle Healer', 'Cannon Cart', 'Prince', 'Heal Spirit', 'Inferno Tower', 'Knight', 'Giant Skeleton'], 'target': 3.3},
    {'Name': 'Weak deck 18', 'Cards': ['Baby Dragon', 'Golden Knight', 'Ice Spirit', 'Ronin', 'Hunter', 'Suspicious Bush', 'Barbarian Hut', 'Rascals'], 'target': 3.3},
    {'Name': 'Weak deck 19', 'Cards': ['Mortar', 'Tombstone', 'Furnace', 'X-Bow', 'Ice Spirit', 'Fire Spirit', 'Heal Spirit', 'Electro Spirit'], 'target': 5.315},
    {'Name': 'Weak deck 20', 'Cards': ['Furnace', 'Bomb Tower', 'Elixir Collector', 'Mortar', 'Goblin Cage', 'Spirit Empress', 'Skeleton Army', 'Ice Golem'], 'target': 4.347},
    {'Name': 'Weak deck 21', 'Cards': ['Tornado', 'The Log', 'Mirror', 'Rage', 'Freeze', 'Rocket', 'Elite Barbarians', 'Bomber'], 'target': 3.3},
    {'Name': 'Weak deck 22', 'Cards': ['Skeletons', 'Barbarian Barrel', 'Barbarian Hut', 'Rage', 'Elixir Collector', 'Skeleton Army', 'Barbarians', 'Earthquake'], 'target': 3.3},
    {'Name': 'Weak deck 23', 'Cards': ['Monk', 'Poison', 'Mirror', 'Heal Spirit', 'Witch', 'Zappies', 'Hunter', 'Fisherman'], 'target': 3.3},
    {'Name': 'Weak deck 24', 'Cards': ['Goblin Cage', 'Elixir Collector', 'Furnace', 'Bomb Tower', 'Heal Spirit', 'Ice Spirit', 'Electro Spirit', 'Fire Spirit'], 'target': 3.3},
    {'Name': 'Weak deck 25', 'Cards': ['Furnace', 'Goblin Cage', 'Cannon', 'Inferno Tower', 'Bomb Tower', 'Goblin Machine', 'Inferno Dragon', 'Elite Barbarians'], 'target': 3.254},
    {'Name': 'Weak deck 26', 'Cards': ['Mirror', 'Royal Delivery', 'Giant Snowball', 'Zap', 'Lightning', 'Tornado', 'Mother Witch', 'Goblin Cage'], 'target': 3.3},
    {'Name': 'Weak deck 27', 'Cards': ['Skeleton Army', 'Barbarian Hut', 'Barbarians', 'Battle Healer', 'Goblin Cage', 'Goblin Demolisher', 'Knight', 'Prince'], 'target': 3.3},
    {'Name': 'Weak deck 28', 'Cards': ['Archer Queen', 'Electro Wizard', 'Minions', 'Giant Snowball', 'Mirror', 'Ronin', 'Heal Spirit', 'Bowler'], 'target': 3.3},
    {'Name': 'Weak deck 29', 'Cards': ['Goblin Cage', 'Tesla', 'Barbarian Hut', 'Mortar', 'Electro Spirit', 'Heal Spirit', 'Fire Spirit', 'Ice Spirit'], 'target': 5.317},
    {'Name': 'Weak deck 30', 'Cards': ['Tombstone', 'Mortar', 'X-Bow', 'Tesla', 'Cannon', 'Fisherman', 'Ice Golem', 'Knight'], 'target': 4.802},
    {'Name': 'Weak deck 31', 'Cards': ['Arrows', 'Void', 'Poison', 'Goblin Curse', 'Zap', 'Royal Delivery', 'Ice Golem', 'Barbarians'], 'target': 3.3},
    {'Name': 'Weak deck 32', 'Cards': ['Skeleton Army', 'Lumberjack', 'Guards', 'Cannon Cart', 'Goblin Cage', 'Inferno Tower', 'Tombstone', 'Barbarians'], 'target': 3.3},
    {'Name': 'Weak deck 33', 'Cards': ['Firecracker', 'Bowler', 'Giant Skeleton', 'Cannon', 'Suspicious Bush', 'Minions', 'Zappies', 'Rocket'], 'target': 3.3},
    {'Name': 'Weak deck 34', 'Cards': ['Inferno Tower', 'Elixir Collector', 'Tombstone', 'Barbarian Hut', 'Ice Spirit', 'Electro Spirit', 'Fire Spirit', 'Heal Spirit'], 'target': 3.3},
    {'Name': 'Weak deck 35', 'Cards': ['Goblin Cage', 'Tesla', 'Tombstone', 'X-Bow', 'Inferno Tower', 'Fire Spirit', 'Goblin Demolisher', 'Archer Queen'], 'target': 5.65},
    {'Name': 'Weak deck 36', 'Cards': ['Fireball', 'Mirror', 'Zap', 'Barbarian Barrel', 'Void', 'Lightning', 'Vines', 'Minions'], 'target': 3.3},
    {'Name': 'Weak deck 37', 'Cards': ['Barbarian Hut', 'Royal Recruits', 'Cannon Cart', 'Battle Healer', 'Elixir Collector', 'Inferno Tower', 'Heal Spirit', 'Knight'], 'target': 3.267},
    {'Name': 'Weak deck 38', 'Cards': ['Little Prince', 'Suspicious Bush', 'Bomber', 'Arrows', 'Guards', 'Phoenix', 'Boss Bandit', 'Royal Delivery'], 'target': 3.3},
    {'Name': 'Weak deck 39', 'Cards': ['Tombstone', 'Goblin Hut', 'Inferno Tower', 'X-Bow', 'Fire Spirit', 'Ice Spirit', 'Electro Spirit', 'Heal Spirit'], 'target': 5.634},
    {'Name': 'Weak deck 40', 'Cards': ['Tornado', 'Lightning', 'Goblin Curse', 'Arrows', 'Fireball', 'Mirror', 'Goblin Gang', 'Monk'], 'target': 3.3},
    {'Name': 'Weak deck 41', 'Cards': ['Mini P.E.K.K.A', 'Barbarians', 'Royal Recruits', 'Royal Ghost', 'Golden Knight', 'Ice Golem', 'P.E.K.K.A', 'Goblin Cage'], 'target': 3.3},
    {'Name': 'Weak deck 42', 'Cards': ['Royal Delivery', 'Battle Healer', 'Skeleton Dragons', 'Boss Bandit', 'Bomb Tower', 'Suspicious Bush', 'Skeletons', 'Ice Spirit'], 'target': 3.3},
    {'Name': 'Weak deck 43', 'Cards': ['Cannon', 'Mortar', 'X-Bow', 'Bomb Tower', 'Fire Spirit', 'Heal Spirit', 'Ice Spirit', 'Electro Spirit'], 'target': 5.417},
    {'Name': 'Weak deck 44', 'Cards': ['Tesla', 'Goblin Cage', 'Mortar', 'Inferno Tower', 'Elixir Collector', 'Mini P.E.K.K.A', 'Skeletons', 'Fire Spirit'], 'target': 4.994},
    {'Name': 'Weak deck 45', 'Cards': ['Skeleton King', 'Battle Healer', 'Valkyrie', 'Bomber', 'Cannon', 'Giant Skeleton', 'Knight', 'Monk'], 'target': 3.3},
    {'Name': 'Weak deck 46', 'Cards': ['Zappies', 'Zap', 'Giant Snowball', 'Spear Goblins', 'Fisherman', 'Vines', 'Knight', 'Minions'], 'target': 3.3},
    {'Name': 'Weak deck 47', 'Cards': ['Tombstone', 'Bomb Tower', 'Cannon', 'Tesla', 'Fire Spirit', 'Heal Spirit', 'Ice Spirit', 'Electro Spirit'], 'target': 3.3},
    {'Name': 'Weak deck 48', 'Cards': ['Goblin Cage', 'Barbarian Hut', 'X-Bow', 'Tombstone', 'Cannon', 'Cannon Cart', 'Hunter', 'Goblin Gang'], 'target': 4.783},
    {'Name': 'Weak deck 49', 'Cards': ['Lightning', 'Goblin Curse', 'Freeze', 'Royal Delivery', 'Rocket', 'Clone', 'Barbarian Barrel', 'Zappies'], 'target': 3.3},
    {'Name': 'Weak deck 50', 'Cards': ['Bomber', 'Suspicious Bush', 'Skeletons', 'Elixir Collector', 'Earthquake', 'The Log', 'Berserker', 'Mega Knight'], 'target': 3.3},
    {'Name': 'Weak deck 51', 'Cards': ['Electro Dragon', 'Mega Minion', 'Goblin Cage', 'Ronin', 'Earthquake', 'Valkyrie', 'Bomb Tower', 'Baby Dragon'], 'target': 3.3},
    {'Name': 'Weak deck 52', 'Cards': ['Barbarian Hut', 'Furnace', 'Cannon', 'X-Bow', 'Electro Spirit', 'Ice Spirit', 'Heal Spirit', 'Fire Spirit'], 'target': 5.312},
    {'Name': 'Weak deck 53', 'Cards': ['Barbarian Hut', 'Furnace', 'Elixir Collector', 'Goblin Hut', 'Mortar', 'Mirror', 'Archers', 'Baby Dragon'], 'target': 4.94},
    {'Name': 'Weak deck 54', 'Cards': ['Lightning', 'Tornado', 'Vines', 'Mirror', 'Arrows', 'Fireball', 'Phoenix', 'Goblin Hut'], 'target': 3.3},
    {'Name': 'Weak deck 55', 'Cards': ['Earthquake', 'Sparky', 'Tombstone', 'Monk', 'Mighty Miner', 'Royal Ghost', 'Goblins', 'Skeleton King'], 'target': 3.3},
    {'Name': 'Weak deck 56', 'Cards': ['Electro Dragon', 'Berserker', 'Hunter', 'Mother Witch', 'Zappies', 'Goblin Hut', 'Battle Healer', 'Elixir Collector'], 'target': 3.3},
    {'Name': 'Weak deck 57', 'Cards': ['Goblin Hut', 'Mortar', 'Elixir Collector', 'Furnace', 'Ice Spirit', 'Electro Spirit', 'Fire Spirit', 'Heal Spirit'], 'target': 5.06},
    {'Name': 'Weak deck 58', 'Cards': ['Barbarian Hut', 'Tombstone', 'Goblin Hut', 'Goblin Cage', 'X-Bow', 'Zappies', 'Bomber', 'Night Witch'], 'target': 4.992},
    {'Name': 'Weak deck 59', 'Cards': ['Arrows', 'The Log', 'Freeze', 'Mirror', 'Lightning', 'Zap', 'Earthquake', 'Ice Wizard'], 'target': 3.3},
    {'Name': 'Weak deck 60', 'Cards': ['Bowler', 'Bomb Tower', 'Guards', 'Elixir Collector', 'Knight', 'Ice Golem', 'Skeletons', 'Mega Knight'], 'target': 3.3},
    {'Name': 'Weak deck 61', 'Cards': ['Berserker', 'Monk', 'Zappies', 'Bomb Tower', 'Earthquake', 'Tesla', 'Barbarian Hut', 'Lightning'], 'target': 3.3},
    {'Name': 'Weak deck 62', 'Cards': ['Bomb Tower', 'Cannon', 'Elixir Collector', 'Tombstone', 'Heal Spirit', 'Fire Spirit', 'Ice Spirit', 'Electro Spirit'], 'target': 3.3},
    {'Name': 'Weak deck 63', 'Cards': ['Bomb Tower', 'Goblin Cage', 'Tombstone', 'Cannon', 'Mortar', 'Skeleton Army', 'Rocket', 'Magic Archer'], 'target': 5.723},
    {'Name': 'Weak deck 64', 'Cards': ['Arrows', 'The Log', 'Void', 'Poison', 'Lightning', 'Earthquake', 'Boss Bandit', 'Minion Horde'], 'target': 3.3},
    {'Name': 'Weak deck 65', 'Cards': ['Barbarian Hut', 'Ice Golem', 'Ronin', 'Valkyrie', 'Goblin Gang', 'Skeleton Army', 'Sparky', 'Prince'], 'target': 3.3},
    {'Name': 'Weak deck 66', 'Cards': ['Goblin Curse', 'Tornado', 'Barbarian Hut', 'Skeleton Dragons', 'Zap', 'Ice Spirit', 'Elixir Collector', 'The Log'], 'target': 3.3},
    {'Name': 'Weak deck 67', 'Cards': ['Goblin Hut', 'Goblin Cage', 'Tesla', 'Tombstone', 'Electro Spirit', 'Ice Spirit', 'Fire Spirit', 'Heal Spirit'], 'target': 3.3},
    {'Name': 'Weak deck 68', 'Cards': ['Tombstone', 'Goblin Hut', 'Bomb Tower', 'Cannon', 'Tesla', 'Mighty Miner', 'Dart Goblin', 'Archers'], 'target': 3.3},
    {'Name': 'Weak deck 69', 'Cards': ['Void', 'Fireball', 'Earthquake', 'Arrows', 'Mirror', 'The Log', 'Electro Spirit', 'Monk'], 'target': 3.3},
    {'Name': 'Weak deck 70', 'Cards': ['Elite Barbarians', 'Goblin Cage', 'Barbarian Barrel', 'Mirror', 'Knight', 'Earthquake', 'Ice Golem', 'Sparky'], 'target': 3.3},
    {'Name': 'Weak deck 71', 'Cards': ['Earthquake', 'Lightning', 'Mega Knight', 'Goblin Machine', 'Minions', 'Royal Ghost', 'Prince', 'Mother Witch'], 'target': 3.3},
    {'Name': 'Weak deck 72', 'Cards': ['Barbarian Hut', 'Cannon', 'Goblin Hut', 'Goblin Cage', 'Ice Spirit', 'Heal Spirit', 'Fire Spirit', 'Electro Spirit'], 'target': 3.3},
    {'Name': 'Weak deck 73', 'Cards': ['Goblin Cage', 'Goblin Hut', 'Elixir Collector', 'Tombstone', 'Cannon', 'Fireball', 'Musketeer', 'Royal Delivery'], 'target': 3.3},
    {'Name': 'Weak deck 74', 'Cards': ['Goblin Curse', 'Barbarian Barrel', 'The Log', 'Zap', 'Earthquake', 'Rocket', 'Skeleton Dragons', 'Fire Spirit'], 'target': 3.3},
    {'Name': 'Weak deck 75', 'Cards': ['Inferno Tower', 'Skeleton Army', 'Barbarian Barrel', 'Cannon', 'Knight', 'Berserker', 'Royal Recruits', 'Elite Barbarians'], 'target': 3.3},
]

synergy_data = [
    {'Name': 'Giant Graveyard Snowball', 'Cards': ['Giant Snowball', 'Bowler', 'Witch', 'Graveyard', 'Zappies', 'Guards', 'Giant', 'Arrows'], 'Synergy': 5.7, 'Balance': 8.25},
    {'Name': 'Hog Rider 2.6 Cycle', 'Cards': ['Skeletons', 'Musketeer', 'Cannon', 'Hog Rider', 'Fireball', 'Ice Spirit', 'Ice Golem', 'The Log'], 'Synergy': 6.7, 'Balance': 9.15},
    {'Name': 'Royal Hogs Earthquake Queen', 'Cards': ['Royal Hogs', 'Archer Queen', 'Cannon', 'The Log', 'Royal Delivery', 'Ice Spirit', 'Earthquake', 'Skeletons'], 'Synergy': 5.1, 'Balance': 9.15},
    {'Name': 'Goblin Barrel Wall Breakers', 'Cards': ['Goblin Barrel', 'Valkyrie', 'Skeleton Army', 'Cannon', 'Ice Spirit', 'Dart Goblin', 'Princess', 'Wall Breakers'], 'Synergy': 5.7, 'Balance': 7.8},
    {'Name': 'LavaLoon Fireball', 'Cards': ['Zap', 'Mega Minion', 'Baby Dragon', 'Tombstone', 'Balloon', 'Lava Hound', 'Fireball', 'Barbarians'], 'Synergy': 5.7, 'Balance': 8.75},
    {'Name': 'Cannon Graveyard Poison', 'Cards': ['Cannon', 'Ice Wizard', 'Bats', 'Graveyard', 'Poison', 'Skeletons', 'Knight', 'Barbarian Barrel'], 'Synergy': 6.25, 'Balance': 9.15},
    {'Name': 'Hog EQ Mighty Miner', 'Cards': ['Cannon', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Skeletons', 'Electro Spirit', 'Barbarian Barrel'], 'Synergy': 6.0, 'Balance': 9.7},
    {'Name': 'Classic Log Bait', 'Cards': ['Skeleton Army', 'Knight', 'Goblin Barrel', 'Dart Goblin', 'Princess', 'The Log', 'Ice Spirit', 'Inferno Tower'], 'Synergy': 5.7, 'Balance': 8.8},
    {'Name': 'Hog EQ Tesla Mighty Miner', 'Cards': ['Tesla', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Skeletons', 'Electro Spirit', 'Barbarian Barrel'], 'Synergy': 5.55, 'Balance': 9.7},
    {'Name': 'Goblin Drill Snowball Poison', 'Cards': ['Giant Snowball', 'Knight', 'Goblin Drill', 'Fire Spirit', 'Poison', 'Skeletons', 'Goblin Demolisher', 'Tesla'], 'Synergy': 4.9, 'Balance': 8.2},
    {'Name': 'Giant Skeleton Battle Ram', 'Cards': ['Battle Ram', 'Electro Wizard', 'Lumberjack', 'Giant Skeleton', 'Bandit', 'Furnace', 'Arrows', 'Heal Spirit'], 'Synergy': 4.85, 'Balance': 8.25},
    {'Name': 'X-Bow 3.0 Archers', 'Cards': ['Tesla', 'Knight', 'Archers', 'Fireball', 'X-Bow', 'Electro Spirit', 'Skeletons', 'The Log'], 'Synergy': 5.55, 'Balance': 8.05},
    {'Name': 'Royal Giant Fisherman', 'Cards': ['Royal Giant', 'Barbarian Barrel', 'Royal Ghost', 'Hunter', 'Fireball', 'Fisherman', 'Electro Spirit', 'Skeletons'], 'Synergy': 6.15, 'Balance': 9.7},
    {'Name': 'Mega Knight Ram Rider Empress', 'Cards': ['Mega Knight', 'Ice Wizard', 'Royal Ghost', 'Poison', 'Spirit Empress', 'Ram Rider', 'Bandit', 'Zap'], 'Synergy': 5.15, 'Balance': 9.15},
    {'Name': 'Golem Collector Berserker', 'Cards': ['Elite Barbarians', 'Berserker', 'Electro Dragon', 'Golem', 'Elixir Collector', 'Tornado', 'Skeleton Dragons', 'Barbarian Barrel'], 'Synergy': 4.5, 'Balance': 7.715},
    {'Name': 'Giant Skeleton Hog Lightning', 'Cards': ['Firecracker', 'Guards', 'Minion Horde', 'Giant Skeleton', 'Barbarians', 'Lightning', 'Hog Rider', 'The Log'], 'Synergy': 5.15, 'Balance': 9.678},
    {'Name': 'Royal Recruits Royal Hogs', 'Cards': ['Royal Recruits', 'Barbarian Barrel', 'Goblin Cage', 'Royal Hogs', 'Zappies', 'Flying Machine', 'Arrows', 'Electro Spirit'], 'Synergy': 4.2, 'Balance': 8.25},
    {'Name': 'Hog Freeze Ronin', 'Cards': ['Minion Horde', 'Boss Bandit', 'Elite Barbarians', 'Executioner', 'Freeze', 'Hog Rider', 'Ronin', 'Zap'], 'Synergy': 4.9, 'Balance': 9.509},
    {'Name': 'Giant Sparky Ebarbs', 'Cards': ['Elite Barbarians', 'Giant', 'Zap', 'Sparky', 'Mini P.E.K.K.A', 'Heal Spirit', 'Electro Wizard', 'Rage'], 'Synergy': 5.15, 'Balance': 8.8},
    {'Name': 'Splashyard', 'Cards': ['Knight', 'Ice Wizard', 'Tombstone', 'Poison', 'Baby Dragon', 'Barbarian Barrel', 'Tornado', 'Graveyard'], 'Synergy': 6.25, 'Balance': 9.15},
    {'Name': 'X-Bow Ice Wizard Rocket', 'Cards': ['Knight', 'Ice Wizard', 'Tesla', 'Rocket', 'The Log', 'Skeletons', 'X-Bow', 'Tornado'], 'Synergy': 5.55, 'Balance': 8.05},
    {'Name': 'Golem Night Witch Phoenix Fireball', 'Cards': ['Elite Barbarians', 'Mini P.E.K.K.A', 'Zap', 'Golem', 'Phoenix', 'Night Witch', 'Fireball', 'Bomber'], 'Synergy': 6.25, 'Balance': 9.678},
    {'Name': 'Mortar Goblinstein Cart', 'Cards': ['Mortar', 'Goblinstein', 'Minion Horde', 'Fireball', 'Barbarian Barrel', 'Goblin Gang', 'Mother Witch', 'Cannon Cart'], 'Synergy': 4.2, 'Balance': 9.7},
    {'Name': 'Goblin Giant Sparky Rage', 'Cards': ['Zap', 'Mini P.E.K.K.A', 'Goblin Giant', 'Sparky', 'Dark Prince', 'Electro Wizard', 'Heal Spirit', 'Rage'], 'Synergy': 5.5, 'Balance': 8.8},
    {'Name': 'Graveyard Furnace Goblin Hut', 'Cards': ['Furnace', 'Ice Wizard', 'Knight', 'Poison', 'Graveyard', 'Barbarian Barrel', 'Goblin Hut', 'Skeletons'], 'Synergy': 6.25, 'Balance': 8.05},
    {'Name': 'Golem Night Witch Phoenix Arrows', 'Cards': ['Elite Barbarians', 'Mini P.E.K.K.A', 'Zap', 'Arrows', 'Phoenix', 'Night Witch', 'Golem', 'Bomber'], 'Synergy': 6.25, 'Balance': 8.8},
    {'Name': 'Goblin Drill Snowball Bomber', 'Cards': ['Giant Snowball', 'Knight', 'Goblin Drill', 'Skeletons', 'Bomber', 'Poison', 'Fire Spirit', 'Cannon'], 'Synergy': 4.9, 'Balance': 8.2},
    {'Name': 'Mortar Skeleton Barrel Bait', 'Cards': ['Mortar', 'Ice Wizard', 'Skeleton Barrel', 'Cannon Cart', 'Rascals', 'Fireball', 'Goblin Gang', 'Barbarian Barrel'], 'Synergy': 4.2, 'Balance': 9.15},
    {'Name': 'Golem Elixir Golem', 'Cards': ['Inferno Dragon', 'Mini P.E.K.K.A', 'Witch', 'Golem', 'Elixir Golem', 'Night Witch', 'Arrows', 'Rage'], 'Synergy': 7.2, 'Balance': 8.8},
    {'Name': 'Balloon Miner Snowball', 'Cards': ['Musketeer', 'Balloon', 'Giant Snowball', 'Barbarian Barrel', 'Skeletons', 'Miner', 'Ice Golem', 'Bomb Tower'], 'Synergy': 4.55, 'Balance': 8.25},
    {'Name': 'Giant Sparky Vines Wizard', 'Cards': ['Giant', 'Mini P.E.K.K.A', 'Wizard', 'Vines', 'Zap', 'Tornado', 'Sparky', 'Heal Spirit'], 'Synergy': 5.15, 'Balance': 8.8},
    {'Name': 'Giant Graveyard Snowball (Guards -> Goblin Gang)', 'Cards': ['Giant Snowball', 'Bowler', 'Witch', 'Graveyard', 'Zappies', 'Goblin Gang', 'Giant', 'Arrows'], 'Synergy': 5.7, 'Balance': 8.25},
    {'Name': 'Giant Graveyard Snowball (Giant Snowball -> Zap)', 'Cards': ['Zap', 'Bowler', 'Witch', 'Graveyard', 'Zappies', 'Guards', 'Giant', 'Arrows'], 'Synergy': 5.7, 'Balance': 8.25},
    {'Name': 'Giant Graveyard Snowball (Giant Snowball -> The Log)', 'Cards': ['The Log', 'Bowler', 'Witch', 'Graveyard', 'Zappies', 'Guards', 'Giant', 'Arrows'], 'Synergy': 5.7, 'Balance': 8.25},
    {'Name': 'Giant Graveyard Snowball (Arrows -> The Log)', 'Cards': ['Giant Snowball', 'Bowler', 'Witch', 'Graveyard', 'Zappies', 'Guards', 'Giant', 'The Log'], 'Synergy': 5.7, 'Balance': 8.25},
    {'Name': 'Giant Graveyard Snowball (Zappies -> Flying Machine)', 'Cards': ['Giant Snowball', 'Bowler', 'Witch', 'Graveyard', 'Flying Machine', 'Guards', 'Giant', 'Arrows'], 'Synergy': 5.7, 'Balance': 8.25},
    {'Name': 'Hog Rider 2.6 Cycle (Skeletons -> Goblins)', 'Cards': ['Goblins', 'Musketeer', 'Cannon', 'Hog Rider', 'Fireball', 'Ice Spirit', 'Ice Golem', 'The Log'], 'Synergy': 6.7, 'Balance': 9.15},
    {'Name': 'Hog Rider 2.6 Cycle (Fireball -> Earthquake)', 'Cards': ['Skeletons', 'Musketeer', 'Cannon', 'Hog Rider', 'Earthquake', 'Ice Spirit', 'Ice Golem', 'The Log'], 'Synergy': 7.7, 'Balance': 9.15},
    {'Name': 'Hog Rider 2.6 Cycle (Ice Spirit -> Fire Spirit)', 'Cards': ['Skeletons', 'Musketeer', 'Cannon', 'Hog Rider', 'Fireball', 'Fire Spirit', 'Ice Golem', 'The Log'], 'Synergy': 6.7, 'Balance': 9.15},
    {'Name': 'Hog Rider 2.6 Cycle (Skeletons -> Guards)', 'Cards': ['Guards', 'Musketeer', 'Cannon', 'Hog Rider', 'Fireball', 'Ice Spirit', 'Ice Golem', 'The Log'], 'Synergy': 6.7, 'Balance': 9.15},
    {'Name': 'Hog Rider 2.6 Cycle (Musketeer -> Firecracker)', 'Cards': ['Skeletons', 'Firecracker', 'Cannon', 'Hog Rider', 'Fireball', 'Ice Spirit', 'Ice Golem', 'The Log'], 'Synergy': 6.15, 'Balance': 9.15},
    {'Name': 'Royal Hogs Earthquake Queen (Skeletons -> Goblins)', 'Cards': ['Royal Hogs', 'Archer Queen', 'Cannon', 'The Log', 'Royal Delivery', 'Ice Spirit', 'Earthquake', 'Goblins'], 'Synergy': 5.1, 'Balance': 9.15},
    {'Name': 'Royal Hogs Earthquake Queen (Archer Queen -> Little Prince)', 'Cards': ['Royal Hogs', 'Little Prince', 'Cannon', 'The Log', 'Royal Delivery', 'Ice Spirit', 'Earthquake', 'Skeletons'], 'Synergy': 5.1, 'Balance': 9.15},
    {'Name': 'Royal Hogs Earthquake Queen (Archer Queen -> Musketeer)', 'Cards': ['Royal Hogs', 'Musketeer', 'Cannon', 'The Log', 'Royal Delivery', 'Ice Spirit', 'Earthquake', 'Skeletons'], 'Synergy': 5.1, 'Balance': 9.15},
    {'Name': 'Royal Hogs Earthquake Queen (The Log -> Barbarian Barrel)', 'Cards': ['Royal Hogs', 'Archer Queen', 'Cannon', 'Barbarian Barrel', 'Royal Delivery', 'Ice Spirit', 'Earthquake', 'Skeletons'], 'Synergy': 5.1, 'Balance': 9.15},
    {'Name': 'Royal Hogs Earthquake Queen (Cannon -> Bomb Tower)', 'Cards': ['Royal Hogs', 'Archer Queen', 'Bomb Tower', 'The Log', 'Royal Delivery', 'Ice Spirit', 'Earthquake', 'Skeletons'], 'Synergy': 5.1, 'Balance': 9.15},
    {'Name': 'Goblin Barrel Wall Breakers (Cannon -> Bomb Tower)', 'Cards': ['Goblin Barrel', 'Valkyrie', 'Skeleton Army', 'Bomb Tower', 'Ice Spirit', 'Dart Goblin', 'Princess', 'Wall Breakers'], 'Synergy': 5.7, 'Balance': 7.8},
    {'Name': 'Goblin Barrel Wall Breakers (Valkyrie -> Mini P.E.K.K.A)', 'Cards': ['Goblin Barrel', 'Mini P.E.K.K.A', 'Skeleton Army', 'Cannon', 'Ice Spirit', 'Dart Goblin', 'Princess', 'Wall Breakers'], 'Synergy': 5.7, 'Balance': 7.8},
    {'Name': 'Goblin Barrel Wall Breakers (Cannon -> Tombstone)', 'Cards': ['Goblin Barrel', 'Valkyrie', 'Skeleton Army', 'Tombstone', 'Ice Spirit', 'Dart Goblin', 'Princess', 'Wall Breakers'], 'Synergy': 5.7, 'Balance': 7.8},
    {'Name': 'Goblin Barrel Wall Breakers (Wall Breakers -> Miner)', 'Cards': ['Goblin Barrel', 'Valkyrie', 'Skeleton Army', 'Cannon', 'Ice Spirit', 'Dart Goblin', 'Princess', 'Miner'], 'Synergy': 5.7, 'Balance': 7.8},
    {'Name': 'Goblin Barrel Wall Breakers (Valkyrie -> Dark Prince)', 'Cards': ['Goblin Barrel', 'Dark Prince', 'Skeleton Army', 'Cannon', 'Ice Spirit', 'Dart Goblin', 'Princess', 'Wall Breakers'], 'Synergy': 5.7, 'Balance': 7.8},
    {'Name': 'LavaLoon Fireball (Zap -> Arrows)', 'Cards': ['Arrows', 'Mega Minion', 'Baby Dragon', 'Tombstone', 'Balloon', 'Lava Hound', 'Fireball', 'Barbarians'], 'Synergy': 5.4, 'Balance': 8.728},
    {'Name': 'LavaLoon Fireball (Baby Dragon -> Electro Dragon)', 'Cards': ['Zap', 'Mega Minion', 'Electro Dragon', 'Tombstone', 'Balloon', 'Lava Hound', 'Fireball', 'Barbarians'], 'Synergy': 6.0, 'Balance': 8.728},
    {'Name': 'LavaLoon Fireball (Mega Minion -> Skeleton Dragons)', 'Cards': ['Zap', 'Skeleton Dragons', 'Baby Dragon', 'Tombstone', 'Balloon', 'Lava Hound', 'Fireball', 'Barbarians'], 'Synergy': 5.7, 'Balance': 8.728},
    {'Name': 'LavaLoon Fireball (Mega Minion -> Phoenix)', 'Cards': ['Zap', 'Phoenix', 'Baby Dragon', 'Tombstone', 'Balloon', 'Lava Hound', 'Fireball', 'Barbarians'], 'Synergy': 5.7, 'Balance': 8.728},
    {'Name': 'LavaLoon Fireball (Tombstone -> Cannon)', 'Cards': ['Zap', 'Mega Minion', 'Baby Dragon', 'Cannon', 'Balloon', 'Lava Hound', 'Fireball', 'Barbarians'], 'Synergy': 5.7, 'Balance': 8.75},
    {'Name': 'Cannon Graveyard Poison (Cannon -> Goblin Cage)', 'Cards': ['Goblin Cage', 'Ice Wizard', 'Bats', 'Graveyard', 'Poison', 'Skeletons', 'Knight', 'Barbarian Barrel'], 'Synergy': 6.25, 'Balance': 9.15},
    {'Name': 'Cannon Graveyard Poison (Skeletons -> Goblins)', 'Cards': ['Cannon', 'Ice Wizard', 'Bats', 'Graveyard', 'Poison', 'Goblins', 'Knight', 'Barbarian Barrel'], 'Synergy': 6.25, 'Balance': 9.15},
    {'Name': 'Cannon Graveyard Poison (Knight -> Royal Ghost)', 'Cards': ['Cannon', 'Ice Wizard', 'Bats', 'Graveyard', 'Poison', 'Skeletons', 'Royal Ghost', 'Barbarian Barrel'], 'Synergy': 5.55, 'Balance': 9.15},
    {'Name': 'Cannon Graveyard Poison (Bats -> Skeleton Dragons)', 'Cards': ['Cannon', 'Ice Wizard', 'Skeleton Dragons', 'Graveyard', 'Poison', 'Skeletons', 'Knight', 'Barbarian Barrel'], 'Synergy': 6.25, 'Balance': 9.15},
    {'Name': 'Cannon Graveyard Poison (Cannon -> Tombstone)', 'Cards': ['Tombstone', 'Ice Wizard', 'Bats', 'Graveyard', 'Poison', 'Skeletons', 'Knight', 'Barbarian Barrel'], 'Synergy': 6.25, 'Balance': 9.15},
    {'Name': 'Hog EQ Mighty Miner (Firecracker -> Musketeer)', 'Cards': ['Cannon', 'Mighty Miner', 'Musketeer', 'Hog Rider', 'Earthquake', 'Skeletons', 'Electro Spirit', 'Barbarian Barrel'], 'Synergy': 6.55, 'Balance': 9.7},
    {'Name': 'Hog EQ Mighty Miner (Skeletons -> Goblins)', 'Cards': ['Cannon', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Goblins', 'Electro Spirit', 'Barbarian Barrel'], 'Synergy': 6.0, 'Balance': 9.7},
    {'Name': 'Hog EQ Mighty Miner (Mighty Miner -> Mini P.E.K.K.A)', 'Cards': ['Cannon', 'Mini P.E.K.K.A', 'Firecracker', 'Hog Rider', 'Earthquake', 'Skeletons', 'Electro Spirit', 'Barbarian Barrel'], 'Synergy': 6.0, 'Balance': 9.7},
    {'Name': 'Hog EQ Mighty Miner (Cannon -> Goblin Cage)', 'Cards': ['Goblin Cage', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Skeletons', 'Electro Spirit', 'Barbarian Barrel'], 'Synergy': 5.55, 'Balance': 9.7},
    {'Name': 'Hog EQ Mighty Miner (Skeletons -> Ice Spirit)', 'Cards': ['Cannon', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Ice Spirit', 'Electro Spirit', 'Barbarian Barrel'], 'Synergy': 6.0, 'Balance': 9.7},
    {'Name': 'Classic Log Bait (The Log -> Giant Snowball)', 'Cards': ['Skeleton Army', 'Knight', 'Goblin Barrel', 'Dart Goblin', 'Princess', 'Giant Snowball', 'Ice Spirit', 'Inferno Tower'], 'Synergy': 5.7, 'Balance': 8.8},
    {'Name': 'Classic Log Bait (Dart Goblin -> Archers)', 'Cards': ['Skeleton Army', 'Knight', 'Goblin Barrel', 'Archers', 'Princess', 'The Log', 'Ice Spirit', 'Inferno Tower'], 'Synergy': 5.7, 'Balance': 8.8},
    {'Name': 'Classic Log Bait (The Log -> Zap)', 'Cards': ['Skeleton Army', 'Knight', 'Goblin Barrel', 'Dart Goblin', 'Princess', 'Zap', 'Ice Spirit', 'Inferno Tower'], 'Synergy': 5.7, 'Balance': 8.8},
    {'Name': 'Classic Log Bait (Skeleton Army -> Guards)', 'Cards': ['Guards', 'Knight', 'Goblin Barrel', 'Dart Goblin', 'Princess', 'The Log', 'Ice Spirit', 'Inferno Tower'], 'Synergy': 5.7, 'Balance': 8.8},
    {'Name': 'Classic Log Bait (Inferno Tower -> Goblin Cage)', 'Cards': ['Skeleton Army', 'Knight', 'Goblin Barrel', 'Dart Goblin', 'Princess', 'The Log', 'Ice Spirit', 'Goblin Cage'], 'Synergy': 5.7, 'Balance': 8.8},
    {'Name': 'Hog EQ Tesla Mighty Miner (Barbarian Barrel -> Zap)', 'Cards': ['Tesla', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Skeletons', 'Electro Spirit', 'Zap'], 'Synergy': 5.55, 'Balance': 9.7},
    {'Name': 'Hog EQ Tesla Mighty Miner (Barbarian Barrel -> The Log)', 'Cards': ['Tesla', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Skeletons', 'Electro Spirit', 'The Log'], 'Synergy': 5.9, 'Balance': 9.7},
    {'Name': 'Hog EQ Tesla Mighty Miner (Skeletons -> Goblins)', 'Cards': ['Tesla', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Goblins', 'Electro Spirit', 'Barbarian Barrel'], 'Synergy': 5.55, 'Balance': 9.7},
    {'Name': 'Hog EQ Tesla Mighty Miner (Electro Spirit -> Fire Spirit)', 'Cards': ['Tesla', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Skeletons', 'Fire Spirit', 'Barbarian Barrel'], 'Synergy': 5.55, 'Balance': 9.7},
    {'Name': 'Hog EQ Tesla Mighty Miner (Tesla -> Inferno Tower)', 'Cards': ['Inferno Tower', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Skeletons', 'Electro Spirit', 'Barbarian Barrel'], 'Synergy': 5.55, 'Balance': 9.7},
    {'Name': 'Goblin Drill Snowball Poison (Skeletons -> Electro Spirit)', 'Cards': ['Giant Snowball', 'Knight', 'Goblin Drill', 'Fire Spirit', 'Poison', 'Electro Spirit', 'Goblin Demolisher', 'Tesla'], 'Synergy': 4.9, 'Balance': 8.2},
    {'Name': 'Goblin Drill Snowball Poison (Knight -> Mini P.E.K.K.A)', 'Cards': ['Giant Snowball', 'Mini P.E.K.K.A', 'Goblin Drill', 'Fire Spirit', 'Poison', 'Skeletons', 'Goblin Demolisher', 'Tesla'], 'Synergy': 4.9, 'Balance': 8.75},
    {'Name': 'Goblin Drill Snowball Poison (Fire Spirit -> Bomber)', 'Cards': ['Giant Snowball', 'Knight', 'Goblin Drill', 'Bomber', 'Poison', 'Skeletons', 'Goblin Demolisher', 'Tesla'], 'Synergy': 4.9, 'Balance': 8.2},
    {'Name': 'Goblin Drill Snowball Poison (Knight -> Royal Ghost)', 'Cards': ['Giant Snowball', 'Royal Ghost', 'Goblin Drill', 'Fire Spirit', 'Poison', 'Skeletons', 'Goblin Demolisher', 'Tesla'], 'Synergy': 4.9, 'Balance': 8.2},
    {'Name': 'Mixed deck 01', 'Cards': ['Royal Hogs', 'Little Prince', 'Minions', 'The Log', 'Royal Delivery', 'Ice Spirit', 'Earthquake', 'Cannon Cart'], 'Synergy': 5.1, 'Balance': 9.15},
    {'Name': 'Mixed deck 02', 'Cards': ['Cannon', 'Mighty Miner', 'Firecracker', 'Royal Giant', 'Earthquake', 'Zappies', 'Electro Spirit', 'Barbarian Barrel'], 'Synergy': 5.5, 'Balance': 9.7},
    {'Name': 'Mixed deck 03', 'Cards': ['Dart Goblin', 'Ice Wizard', 'Tombstone', 'Poison', 'Baby Dragon', 'Electro Giant', 'Minion Horde', 'Barbarians'], 'Synergy': 4.8, 'Balance': 8.678},
    {'Name': 'Mixed deck 04', 'Cards': ['Giant Snowball', 'Executioner', 'Goblin Curse', 'Graveyard', 'Flying Machine', 'Princess', 'Giant', 'Goblin Hut'], 'Synergy': 5.7, 'Balance': 8.25},
    {'Name': 'Mixed deck 05', 'Cards': ['Skeletons', 'Electro Giant', 'Furnace', 'Hog Rider', 'Boss Bandit', 'Ice Spirit', 'Ice Golem', 'The Log'], 'Synergy': 5.65, 'Balance': 5.55},
    {'Name': 'Mixed deck 06', 'Cards': ['Minion Horde', 'Boss Bandit', 'Skeleton King', 'Executioner', 'Lightning', 'Hog Rider', 'Ronin', 'Zap'], 'Synergy': 4.9, 'Balance': 8.959},
    {'Name': 'Mixed deck 07', 'Cards': ['Goblin Barrel', 'Dark Prince', 'Night Witch', 'Cannon', 'Ice Spirit', 'Dart Goblin', 'Suspicious Bush', 'Wall Breakers'], 'Synergy': 4.9, 'Balance': 7.25},
    {'Name': 'Mixed deck 08', 'Cards': ['Cannon', 'Mighty Miner', 'X-Bow', 'Hog Rider', 'The Log', 'Elixir Collector', 'Valkyrie', 'Barbarian Barrel'], 'Synergy': 4.4, 'Balance': 3.9},
    {'Name': 'Mixed deck 09', 'Cards': ['Hog Rider', 'Berserker', 'Giant Skeleton', 'Inferno Tower', 'Goblin Drill', 'Cannon', 'Royal Delivery', 'Balloon'], 'Synergy': 4.35, 'Balance': 4.5},
    {'Name': 'Mixed deck 10', 'Cards': ['Royal Giant', 'Giant Snowball', 'Elite Barbarians', 'Spirit Empress', 'Clone', 'Fisherman', 'Elixir Golem', 'Skeletons'], 'Synergy': 5.2, 'Balance': 7.85},
    {'Name': 'Mixed deck 11', 'Cards': ['Spirit Empress', 'Sparky', 'Mega Knight', 'Golem', 'Elixir Collector', 'Tornado', 'Royal Hogs', 'Barbarian Barrel'], 'Synergy': 4.2, 'Balance': 7.49},
    {'Name': 'Mixed deck 12', 'Cards': ['Ram Rider', 'Ice Wizard', 'Bats', 'Minion Horde', 'Poison', 'Skeletons', 'Knight', 'Barbarian Barrel'], 'Synergy': 4.55, 'Balance': 9.15},
    {'Name': 'Mixed deck 13', 'Cards': ['Battle Ram', 'Electro Wizard', 'Lightning', 'Giant Skeleton', 'Bandit', 'Royal Ghost', 'Spirit Empress', 'Heal Spirit'], 'Synergy': 5.15, 'Balance': 8.15},
    {'Name': 'Mixed deck 14', 'Cards': ['Firecracker', 'Guards', 'Minion Horde', 'Baby Dragon', 'Lumberjack', 'Lightning', 'Hog Rider', 'Zap'], 'Synergy': 4.55, 'Balance': 9.15},
    {'Name': 'Mixed deck 15', 'Cards': ['Bomb Tower', 'Ronin', 'Bats', 'Ice Wizard', 'Goblin Barrel', 'Knight', 'Skeletons', 'Graveyard'], 'Synergy': 5.6, 'Balance': 7.25},
    {'Name': 'Mixed deck 16', 'Cards': ['Suspicious Bush', 'Ronin', 'Goblin Barrel', 'Dart Goblin', 'Princess', 'Giant Snowball', 'Ice Spirit', 'Inferno Tower'], 'Synergy': 5.7, 'Balance': 8.8},
    {'Name': 'Mixed deck 17', 'Cards': ['Goblin Demolisher', 'Guards', 'Skeleton Dragons', 'Ice Golem', 'Barbarians', 'Lightning', 'Bats', 'Rune Giant'], 'Synergy': 4.5, 'Balance': 7.75},
    {'Name': 'Mixed deck 18', 'Cards': ['Tombstone', 'Ice Wizard', 'Fire Spirit', 'Graveyard', 'Poison', 'Skeletons', 'Royal Hogs', 'Barbarian Barrel'], 'Synergy': 5.2, 'Balance': 9.15},
    {'Name': 'Mixed deck 19', 'Cards': ['Tesla', 'Executioner', 'Firecracker', 'Hog Rider', 'Earthquake', 'Skeletons', 'Skeleton Barrel', 'Magic Archer'], 'Synergy': 5.2, 'Balance': 8.15},
    {'Name': 'Mixed deck 20', 'Cards': ['Goblin Demolisher', 'Royal Ghost', 'Goblin Drill', 'Fire Spirit', 'Bandit', 'Skeletons', 'Furnace', 'Tombstone'], 'Synergy': 4.2, 'Balance': 3.45},
    {'Name': 'Mixed deck 21', 'Cards': ['Knight', 'Ice Wizard', 'Tesla', 'Rocket', 'Skeleton Barrel', 'Skeletons', 'X-Bow', 'Golden Knight'], 'Synergy': 5.9, 'Balance': 7.05},
    {'Name': 'Mixed deck 22', 'Cards': ['Zap', 'Inferno Tower', 'Bats', 'Fireball', 'Barbarian Barrel', 'Knight', 'Skeletons', 'Royal Giant'], 'Synergy': 4.5, 'Balance': 8.75},
    {'Name': 'Mixed deck 23', 'Cards': ['Valkyrie', 'Heal Spirit', 'Vines', 'X-Bow', 'Fisherman', 'Elixir Collector', 'Rage', 'Three Musketeers'], 'Synergy': 4.55, 'Balance': 7.678},
    {'Name': 'Mixed deck 24', 'Cards': ['Elite Barbarians', 'Giant', 'Zap', 'Ice Wizard', 'Prince', 'Heal Spirit', 'Goblin Drill', 'Rage'], 'Synergy': 5.15, 'Balance': 8.8},
    {'Name': 'Mixed deck 25', 'Cards': ['Battle Ram', 'Inferno Tower', 'Lumberjack', 'Goblin Drill', 'Cannon Cart', 'Furnace', 'Zap', 'Heal Spirit'], 'Synergy': 4.55, 'Balance': 5.95},
    {'Name': 'Mixed deck 26', 'Cards': ['Heal Spirit', 'Elixir Golem', 'Prince', 'Executioner', 'Freeze', 'Hog Rider', 'Cannon Cart', 'Fireball'], 'Synergy': 5.5, 'Balance': 8.7},
    {'Name': 'Mixed deck 27', 'Cards': ['X-Bow', 'Mighty Miner', 'Cannon', 'Lightning', 'The Log', 'Electro Spirit', 'Minion Giant', 'Suspicious Bush'], 'Synergy': 4.8, 'Balance': 7.65},
    {'Name': 'Mixed deck 28', 'Cards': ['Cannon', 'Mighty Miner', 'Firecracker', 'Hog Rider', 'Ice Spirit', 'Skeletons', 'Flying Machine', 'Barbarian Barrel'], 'Synergy': 5.35, 'Balance': 8.8},
    {'Name': 'Mixed deck 29', 'Cards': ['Royal Giant', 'Zap', 'Knight', 'Hunter', 'Fireball', 'Void', 'Bomber', 'Skeletons'], 'Synergy': 5.15, 'Balance': 9.7},
    {'Name': 'Mixed deck 30', 'Cards': ['Miner', 'Mighty Miner', 'Firecracker', 'Royal Giant', 'Earthquake', 'Skeletons', 'Barbarians', 'Barbarian Barrel'], 'Synergy': 4.85, 'Balance': 7.95},
    {'Name': 'Mixed deck 31', 'Cards': ['Mega Knight', 'Ice Wizard', 'Sparky', 'Executioner', 'Clone', 'Ram Rider', 'Inferno Dragon', 'Giant Snowball'], 'Synergy': 4.8, 'Balance': 8.721},
    {'Name': 'Mixed deck 32', 'Cards': ['Cannon', 'Goblin Demolisher', 'Firecracker', 'Hog Rider', 'Earthquake', 'Goblins', 'Zappies', 'Barbarian Barrel'], 'Synergy': 5.65, 'Balance': 9.15},
    {'Name': 'Mixed deck 33', 'Cards': ['Elite Barbarians', 'Mini P.E.K.K.A', 'Zap', 'Golem', 'Musketeer', 'Archers', 'Fireball', 'Bomber'], 'Synergy': 5.5, 'Balance': 9.7},
    {'Name': 'Mixed deck 34', 'Cards': ['The Log', 'Bowler', 'Witch', 'Inferno Dragon', 'Zappies', 'Fireball', 'Giant', 'Arrows'], 'Synergy': 4.8, 'Balance': 9.7},
    {'Name': 'Mixed deck 35', 'Cards': ['Royal Giant', 'Barbarian Barrel', 'Royal Ghost', 'Hunter', 'Fireball', 'Dart Goblin', 'Clone', 'Skeletons'], 'Synergy': 5.5, 'Balance': 9.7},
    {'Name': 'Mixed deck 36', 'Cards': ['Giant', 'Mini P.E.K.K.A', 'Wizard', 'Bandit', 'Zap', 'Tornado', 'Sparky', 'Rune Giant'], 'Synergy': 5.75, 'Balance': 8.8},
    {'Name': 'Mixed deck 37', 'Cards': ['Zap', 'Bowler', 'Archers', 'Arrows', 'Zappies', 'Guards', 'Giant', 'Archer Queen'], 'Synergy': 4.8, 'Balance': 8.25},
    {'Name': 'Mixed deck 38', 'Cards': ['Vines', 'Ice Spirit', 'Tesla', 'Rocket', 'Minions', 'Skeletons', 'X-Bow', 'Tornado'], 'Synergy': 5.2, 'Balance': 7.1},
    {'Name': 'Mixed deck 39', 'Cards': ['Electro Giant', 'Mini P.E.K.K.A', 'Wizard', 'Vines', 'Zap', 'Tornado', 'Cannon Cart', 'Witch'], 'Synergy': 5.5, 'Balance': 8.778},
    {'Name': 'Mixed deck 40', 'Cards': ['Furnace', 'Ice Wizard', 'Knight', 'Mirror', 'Graveyard', 'Cannon', 'Goblin Hut', 'Skeletons'], 'Synergy': 4.65, 'Balance': 4.3},
    {'Name': 'Mixed deck 41', 'Cards': ['Boss Bandit', 'Ice Wizard', 'Royal Ghost', 'Lightning', 'Musketeer', 'Ram Rider', 'Bandit', 'Skeleton Army'], 'Synergy': 5.6, 'Balance': 8.7},
    {'Name': 'Mixed deck 42', 'Cards': ['Goblin Barrel', 'Tornado', 'Skeleton Army', 'Tombstone', 'Ice Spirit', 'Dart Goblin', 'Valkyrie', 'Wall Breakers'], 'Synergy': 4.55, 'Balance': 8.8},
    {'Name': 'Mixed deck 43', 'Cards': ['Minion Horde', 'Boss Bandit', 'Prince', 'Royal Giant', 'Lumberjack', 'Hog Rider', 'Ronin', 'Zap'], 'Synergy': 4.5, 'Balance': 7.659},
    {'Name': 'Mixed deck 44', 'Cards': ['Battle Ram', 'Boss Bandit', 'Elite Barbarians', 'Executioner', 'Phoenix', 'Hog Rider', 'Ronin', 'Arrows'], 'Synergy': 4.9, 'Balance': 8.609},
    {'Name': 'Mixed deck 45', 'Cards': ['Royal Hogs', 'Musketeer', 'Cannon', 'The Log', 'Valkyrie', 'Tombstone', 'Firecracker', 'Skeletons'], 'Synergy': 4.9, 'Balance': 7.15},
    {'Name': 'Weak deck 01', 'Cards': ['Cannon', 'Inferno Tower', 'Bomb Tower', 'X-Bow', 'Tombstone', 'Furnace', 'Phoenix', 'Electro Spirit'], 'Synergy': 1.8, 'Balance': 1.35},
    {'Name': 'Weak deck 02', 'Cards': ['Arrows', 'The Log', 'Goblin Curse', 'Royal Delivery', 'Lightning', 'Vines', 'Bandit', 'Wizard'], 'Synergy': 4.2, 'Balance': 4.05},
    {'Name': 'Weak deck 03', 'Cards': ['Cannon', 'Skeleton Army', 'Elixir Collector', 'Barbarians', 'Guards', 'Suspicious Bush', 'Goblin Gang', 'Skeletons'], 'Synergy': 4.2, 'Balance': 1.0},
    {'Name': 'Weak deck 04', 'Cards': ['Goblin Gang', 'Freeze', 'Bomb Tower', 'Goblinstein', 'Hunter', 'Mini P.E.K.K.A', 'Cannon Cart', 'Inferno Tower'], 'Synergy': 4.9, 'Balance': 2.478},
    {'Name': 'Weak deck 05', 'Cards': ['Mortar', 'Bomb Tower', 'Elixir Collector', 'Goblin Cage', 'Fire Spirit', 'Heal Spirit', 'Electro Spirit', 'Ice Spirit'], 'Synergy': 3.0, 'Balance': 3.0},
    {'Name': 'Weak deck 06', 'Cards': ['Lightning', 'Vines', 'Rocket', 'Rage', 'Earthquake', 'Zap', 'Electro Spirit', 'Ice Spirit'], 'Synergy': 4.2, 'Balance': 3.1},
    {'Name': 'Weak deck 07', 'Cards': ['Cannon Cart', 'Clone', 'Suspicious Bush', 'Goblin Demolisher', 'Sparky', 'Prince', 'P.E.K.K.A', 'Ronin'], 'Synergy': 4.9, 'Balance': 1.759},
    {'Name': 'Weak deck 08', 'Cards': ['Valkyrie', 'Rage', 'Hunter', 'Furnace', 'Clone', 'Giant Snowball', 'Dark Prince', 'The Log'], 'Synergy': 4.9, 'Balance': 3.7},
    {'Name': 'Weak deck 09', 'Cards': ['X-Bow', 'Inferno Tower', 'Furnace', 'Bomb Tower', 'Ice Spirit', 'Heal Spirit', 'Fire Spirit', 'Electro Spirit'], 'Synergy': 3.0, 'Balance': 3.55},
    {'Name': 'Weak deck 10', 'Cards': ['Tesla', 'Goblin Hut', 'Elixir Collector', 'Goblin Cage', 'Bomb Tower', 'Goblin Demolisher', 'Tornado', 'P.E.K.K.A'], 'Synergy': 2.4, 'Balance': 1.0},
    {'Name': 'Weak deck 11', 'Cards': ['Goblin Curse', 'Mirror', 'Vines', 'Earthquake', 'Rage', 'Zap', 'Berserker', 'Arrows'], 'Synergy': 4.2, 'Balance': 3.1},
    {'Name': 'Weak deck 12', 'Cards': ['Berserker', 'Boss Bandit', 'Clone', 'Royal Ghost', 'Ice Golem', 'Elite Barbarians', 'Knight', 'Rage'], 'Synergy': 4.2, 'Balance': 1.0},
    {'Name': 'Weak deck 13', 'Cards': ['Sparky', 'Ice Wizard', 'Mirror', 'Ice Golem', 'Boss Bandit', 'Electro Wizard', 'Skeletons', 'Suspicious Bush'], 'Synergy': 5.6, 'Balance': 3.7},
    {'Name': 'Weak deck 14', 'Cards': ['Elixir Collector', 'Goblin Cage', 'Bomb Tower', 'Barbarian Hut', 'Fire Spirit', 'Electro Spirit', 'Ice Spirit', 'Heal Spirit'], 'Synergy': 3.0, 'Balance': 1.0},
    {'Name': 'Weak deck 15', 'Cards': ['Tesla', 'Mortar', 'X-Bow', 'Cannon', 'Elixir Collector', 'Dark Prince', 'Baby Dragon', 'Firecracker'], 'Synergy': 3.75, 'Balance': 2.827},
    {'Name': 'Weak deck 16', 'Cards': ['Barbarian Barrel', 'Giant Snowball', 'Rocket', 'Mirror', 'Goblin Curse', 'Lightning', 'Ice Spirit', 'Royal Ghost'], 'Synergy': 4.2, 'Balance': 3.1},
    {'Name': 'Weak deck 17', 'Cards': ['Mighty Miner', 'Battle Healer', 'Cannon Cart', 'Prince', 'Heal Spirit', 'Inferno Tower', 'Knight', 'Giant Skeleton'], 'Synergy': 5.2, 'Balance': 1.0},
    {'Name': 'Weak deck 18', 'Cards': ['Baby Dragon', 'Golden Knight', 'Ice Spirit', 'Ronin', 'Hunter', 'Suspicious Bush', 'Barbarian Hut', 'Rascals'], 'Synergy': 5.6, 'Balance': 2.7},
    {'Name': 'Weak deck 19', 'Cards': ['Mortar', 'Tombstone', 'Furnace', 'X-Bow', 'Ice Spirit', 'Fire Spirit', 'Heal Spirit', 'Electro Spirit'], 'Synergy': 3.0, 'Balance': 3.0},
    {'Name': 'Weak deck 20', 'Cards': ['Furnace', 'Bomb Tower', 'Elixir Collector', 'Mortar', 'Goblin Cage', 'Spirit Empress', 'Skeleton Army', 'Ice Golem'], 'Synergy': 2.4, 'Balance': 1.0},
    {'Name': 'Weak deck 21', 'Cards': ['Tornado', 'The Log', 'Mirror', 'Rage', 'Freeze', 'Rocket', 'Elite Barbarians', 'Bomber'], 'Synergy': 4.2, 'Balance': 3.65},
    {'Name': 'Weak deck 22', 'Cards': ['Skeletons', 'Barbarian Barrel', 'Barbarian Hut', 'Rage', 'Elixir Collector', 'Skeleton Army', 'Barbarians', 'Earthquake'], 'Synergy': 4.2, 'Balance': 1.0},
    {'Name': 'Weak deck 23', 'Cards': ['Monk', 'Poison', 'Mirror', 'Heal Spirit', 'Witch', 'Zappies', 'Hunter', 'Fisherman'], 'Synergy': 4.9, 'Balance': 4.6},
    {'Name': 'Weak deck 24', 'Cards': ['Goblin Cage', 'Elixir Collector', 'Furnace', 'Bomb Tower', 'Heal Spirit', 'Ice Spirit', 'Electro Spirit', 'Fire Spirit'], 'Synergy': 3.0, 'Balance': 1.0},
    {'Name': 'Weak deck 25', 'Cards': ['Furnace', 'Goblin Cage', 'Cannon', 'Inferno Tower', 'Bomb Tower', 'Goblin Machine', 'Inferno Dragon', 'Elite Barbarians'], 'Synergy': 2.4, 'Balance': 1.0},
    {'Name': 'Weak deck 26', 'Cards': ['Mirror', 'Royal Delivery', 'Giant Snowball', 'Zap', 'Lightning', 'Tornado', 'Mother Witch', 'Goblin Cage'], 'Synergy': 4.2, 'Balance': 4.05},
    {'Name': 'Weak deck 27', 'Cards': ['Skeleton Army', 'Barbarian Hut', 'Barbarians', 'Battle Healer', 'Goblin Cage', 'Goblin Demolisher', 'Knight', 'Prince'], 'Synergy': 4.2, 'Balance': 1.0},
    {'Name': 'Weak deck 28', 'Cards': ['Archer Queen', 'Electro Wizard', 'Minions', 'Giant Snowball', 'Mirror', 'Ronin', 'Heal Spirit', 'Bowler'], 'Synergy': 4.9, 'Balance': 3.15},
    {'Name': 'Weak deck 29', 'Cards': ['Goblin Cage', 'Tesla', 'Barbarian Hut', 'Mortar', 'Electro Spirit', 'Heal Spirit', 'Fire Spirit', 'Ice Spirit'], 'Synergy': 3.0, 'Balance': 3.0},
    {'Name': 'Weak deck 30', 'Cards': ['Tombstone', 'Mortar', 'X-Bow', 'Tesla', 'Cannon', 'Fisherman', 'Ice Golem', 'Knight'], 'Synergy': 3.4, 'Balance': 1.0},
    {'Name': 'Weak deck 31', 'Cards': ['Arrows', 'Void', 'Poison', 'Goblin Curse', 'Zap', 'Royal Delivery', 'Ice Golem', 'Barbarians'], 'Synergy': 4.2, 'Balance': 3.65},
    {'Name': 'Weak deck 32', 'Cards': ['Skeleton Army', 'Lumberjack', 'Guards', 'Cannon Cart', 'Goblin Cage', 'Inferno Tower', 'Tombstone', 'Barbarians'], 'Synergy': 3.95, 'Balance': 1.0},
    {'Name': 'Weak deck 33', 'Cards': ['Firecracker', 'Bowler', 'Giant Skeleton', 'Cannon', 'Suspicious Bush', 'Minions', 'Zappies', 'Rocket'], 'Synergy': 4.8, 'Balance': 3.05},
    {'Name': 'Weak deck 34', 'Cards': ['Inferno Tower', 'Elixir Collector', 'Tombstone', 'Barbarian Hut', 'Ice Spirit', 'Electro Spirit', 'Fire Spirit', 'Heal Spirit'], 'Synergy': 3.0, 'Balance': 1.0},
    {'Name': 'Weak deck 35', 'Cards': ['Goblin Cage', 'Tesla', 'Tombstone', 'X-Bow', 'Inferno Tower', 'Fire Spirit', 'Goblin Demolisher', 'Archer Queen'], 'Synergy': 3.4, 'Balance': 3.4},
    {'Name': 'Weak deck 36', 'Cards': ['Fireball', 'Mirror', 'Zap', 'Barbarian Barrel', 'Void', 'Lightning', 'Vines', 'Minions'], 'Synergy': 4.2, 'Balance': 3.1},
    {'Name': 'Weak deck 37', 'Cards': ['Barbarian Hut', 'Royal Recruits', 'Cannon Cart', 'Battle Healer', 'Elixir Collector', 'Inferno Tower', 'Heal Spirit', 'Knight'], 'Synergy': 4.3, 'Balance': 1.0},
    {'Name': 'Weak deck 38', 'Cards': ['Little Prince', 'Suspicious Bush', 'Bomber', 'Arrows', 'Guards', 'Phoenix', 'Boss Bandit', 'Royal Delivery'], 'Synergy': 4.55, 'Balance': 3.7},
    {'Name': 'Weak deck 39', 'Cards': ['Tombstone', 'Goblin Hut', 'Inferno Tower', 'X-Bow', 'Fire Spirit', 'Ice Spirit', 'Electro Spirit', 'Heal Spirit'], 'Synergy': 3.0, 'Balance': 3.55},
    {'Name': 'Weak deck 40', 'Cards': ['Tornado', 'Lightning', 'Goblin Curse', 'Arrows', 'Fireball', 'Mirror', 'Goblin Gang', 'Monk'], 'Synergy': 4.2, 'Balance': 3.1},
    {'Name': 'Weak deck 41', 'Cards': ['Mini P.E.K.K.A', 'Barbarians', 'Royal Recruits', 'Royal Ghost', 'Golden Knight', 'Ice Golem', 'P.E.K.K.A', 'Goblin Cage'], 'Synergy': 4.2, 'Balance': 1.0},
    {'Name': 'Weak deck 42', 'Cards': ['Royal Delivery', 'Battle Healer', 'Skeleton Dragons', 'Boss Bandit', 'Bomb Tower', 'Suspicious Bush', 'Skeletons', 'Ice Spirit'], 'Synergy': 4.2, 'Balance': 2.2},
    {'Name': 'Weak deck 43', 'Cards': ['Cannon', 'Mortar', 'X-Bow', 'Bomb Tower', 'Fire Spirit', 'Heal Spirit', 'Ice Spirit', 'Electro Spirit'], 'Synergy': 3.0, 'Balance': 3.0},
    {'Name': 'Weak deck 44', 'Cards': ['Tesla', 'Goblin Cage', 'Mortar', 'Inferno Tower', 'Elixir Collector', 'Mini P.E.K.K.A', 'Skeletons', 'Fire Spirit'], 'Synergy': 2.4, 'Balance': 2.45},
    {'Name': 'Weak deck 45', 'Cards': ['Skeleton King', 'Battle Healer', 'Valkyrie', 'Bomber', 'Cannon', 'Giant Skeleton', 'Knight', 'Monk'], 'Synergy': 4.2, 'Balance': 1.0},
    {'Name': 'Weak deck 46', 'Cards': ['Zappies', 'Zap', 'Giant Snowball', 'Spear Goblins', 'Fisherman', 'Vines', 'Knight', 'Minions'], 'Synergy': 4.9, 'Balance': 3.15},
    {'Name': 'Weak deck 47', 'Cards': ['Tombstone', 'Bomb Tower', 'Cannon', 'Tesla', 'Fire Spirit', 'Heal Spirit', 'Ice Spirit', 'Electro Spirit'], 'Synergy': 3.0, 'Balance': 1.0},
    {'Name': 'Weak deck 48', 'Cards': ['Goblin Cage', 'Barbarian Hut', 'X-Bow', 'Tombstone', 'Cannon', 'Cannon Cart', 'Hunter', 'Goblin Gang'], 'Synergy': 2.4, 'Balance': 1.627},
    {'Name': 'Weak deck 49', 'Cards': ['Lightning', 'Goblin Curse', 'Freeze', 'Royal Delivery', 'Rocket', 'Clone', 'Barbarian Barrel', 'Zappies'], 'Synergy': 4.2, 'Balance': 4.05},
    {'Name': 'Weak deck 50', 'Cards': ['Bomber', 'Suspicious Bush', 'Skeletons', 'Elixir Collector', 'Earthquake', 'The Log', 'Berserker', 'Mega Knight'], 'Synergy': 4.2, 'Balance': 1.35},
    {'Name': 'Weak deck 51', 'Cards': ['Electro Dragon', 'Mega Minion', 'Goblin Cage', 'Ronin', 'Earthquake', 'Valkyrie', 'Bomb Tower', 'Baby Dragon'], 'Synergy': 4.2, 'Balance': 1.0},
    {'Name': 'Weak deck 52', 'Cards': ['Barbarian Hut', 'Furnace', 'Cannon', 'X-Bow', 'Electro Spirit', 'Ice Spirit', 'Heal Spirit', 'Fire Spirit'], 'Synergy': 3.0, 'Balance': 3.0},
    {'Name': 'Weak deck 53', 'Cards': ['Barbarian Hut', 'Furnace', 'Elixir Collector', 'Goblin Hut', 'Mortar', 'Mirror', 'Archers', 'Baby Dragon'], 'Synergy': 2.4, 'Balance': 3.85},
    {'Name': 'Weak deck 54', 'Cards': ['Lightning', 'Tornado', 'Vines', 'Mirror', 'Arrows', 'Fireball', 'Phoenix', 'Goblin Hut'], 'Synergy': 4.2, 'Balance': 3.65},
    {'Name': 'Weak deck 55', 'Cards': ['Earthquake', 'Sparky', 'Tombstone', 'Monk', 'Mighty Miner', 'Royal Ghost', 'Goblins', 'Skeleton King'], 'Synergy': 4.2, 'Balance': 1.0},
    {'Name': 'Weak deck 56', 'Cards': ['Electro Dragon', 'Berserker', 'Hunter', 'Mother Witch', 'Zappies', 'Goblin Hut', 'Battle Healer', 'Elixir Collector'], 'Synergy': 4.9, 'Balance': 1.6},
    {'Name': 'Weak deck 57', 'Cards': ['Goblin Hut', 'Mortar', 'Elixir Collector', 'Furnace', 'Ice Spirit', 'Electro Spirit', 'Fire Spirit', 'Heal Spirit'], 'Synergy': 3.0, 'Balance': 3.0},
    {'Name': 'Weak deck 58', 'Cards': ['Barbarian Hut', 'Tombstone', 'Goblin Hut', 'Goblin Cage', 'X-Bow', 'Zappies', 'Bomber', 'Night Witch'], 'Synergy': 2.4, 'Balance': 2.85},
    {'Name': 'Weak deck 59', 'Cards': ['Arrows', 'The Log', 'Freeze', 'Mirror', 'Lightning', 'Zap', 'Earthquake', 'Ice Wizard'], 'Synergy': 4.2, 'Balance': 4.05},
    {'Name': 'Weak deck 60', 'Cards': ['Bowler', 'Bomb Tower', 'Guards', 'Elixir Collector', 'Knight', 'Ice Golem', 'Skeletons', 'Mega Knight'], 'Synergy': 5.2, 'Balance': 1.0},
    {'Name': 'Weak deck 61', 'Cards': ['Berserker', 'Monk', 'Zappies', 'Bomb Tower', 'Earthquake', 'Tesla', 'Barbarian Hut', 'Lightning'], 'Synergy': 3.95, 'Balance': 1.0},
    {'Name': 'Weak deck 62', 'Cards': ['Bomb Tower', 'Cannon', 'Elixir Collector', 'Tombstone', 'Heal Spirit', 'Fire Spirit', 'Ice Spirit', 'Electro Spirit'], 'Synergy': 3.0, 'Balance': 1.0},
    {'Name': 'Weak deck 63', 'Cards': ['Bomb Tower', 'Goblin Cage', 'Tombstone', 'Cannon', 'Mortar', 'Skeleton Army', 'Rocket', 'Magic Archer'], 'Synergy': 2.4, 'Balance': 4.3},
    {'Name': 'Weak deck 64', 'Cards': ['Arrows', 'The Log', 'Void', 'Poison', 'Lightning', 'Earthquake', 'Boss Bandit', 'Minion Horde'], 'Synergy': 4.2, 'Balance': 3.078},
    {'Name': 'Weak deck 65', 'Cards': ['Barbarian Hut', 'Ice Golem', 'Ronin', 'Valkyrie', 'Goblin Gang', 'Skeleton Army', 'Sparky', 'Prince'], 'Synergy': 4.2, 'Balance': 1.0},
    {'Name': 'Weak deck 66', 'Cards': ['Goblin Curse', 'Tornado', 'Barbarian Hut', 'Skeleton Dragons', 'Zap', 'Ice Spirit', 'Elixir Collector', 'The Log'], 'Synergy': 4.2, 'Balance': 1.1},
    {'Name': 'Weak deck 67', 'Cards': ['Goblin Hut', 'Goblin Cage', 'Tesla', 'Tombstone', 'Electro Spirit', 'Ice Spirit', 'Fire Spirit', 'Heal Spirit'], 'Synergy': 3.0, 'Balance': 1.0},
    {'Name': 'Weak deck 68', 'Cards': ['Tombstone', 'Goblin Hut', 'Bomb Tower', 'Cannon', 'Tesla', 'Mighty Miner', 'Dart Goblin', 'Archers'], 'Synergy': 3.1, 'Balance': 1.0},
    {'Name': 'Weak deck 69', 'Cards': ['Void', 'Fireball', 'Earthquake', 'Arrows', 'Mirror', 'The Log', 'Electro Spirit', 'Monk'], 'Synergy': 4.2, 'Balance': 3.1},
    {'Name': 'Weak deck 70', 'Cards': ['Elite Barbarians', 'Goblin Cage', 'Barbarian Barrel', 'Mirror', 'Knight', 'Earthquake', 'Ice Golem', 'Sparky'], 'Synergy': 4.2, 'Balance': 1.9},
    {'Name': 'Weak deck 71', 'Cards': ['Earthquake', 'Lightning', 'Mega Knight', 'Goblin Machine', 'Minions', 'Royal Ghost', 'Prince', 'Mother Witch'], 'Synergy': 6.2, 'Balance': 3.465},
    {'Name': 'Weak deck 72', 'Cards': ['Barbarian Hut', 'Cannon', 'Goblin Hut', 'Goblin Cage', 'Ice Spirit', 'Heal Spirit', 'Fire Spirit', 'Electro Spirit'], 'Synergy': 3.0, 'Balance': 1.0},
    {'Name': 'Weak deck 73', 'Cards': ['Goblin Cage', 'Goblin Hut', 'Elixir Collector', 'Tombstone', 'Cannon', 'Fireball', 'Musketeer', 'Royal Delivery'], 'Synergy': 2.4, 'Balance': 1.0},
    {'Name': 'Weak deck 74', 'Cards': ['Goblin Curse', 'Barbarian Barrel', 'The Log', 'Zap', 'Earthquake', 'Rocket', 'Skeleton Dragons', 'Fire Spirit'], 'Synergy': 4.2, 'Balance': 3.1},
    {'Name': 'Weak deck 75', 'Cards': ['Inferno Tower', 'Skeleton Army', 'Barbarian Barrel', 'Cannon', 'Knight', 'Berserker', 'Royal Recruits', 'Elite Barbarians'], 'Synergy': 4.2, 'Balance': 1.0},
]

card_weights = {
    card["Name"]: {
        "w_attack":  random.uniform(-0.1, 0.1),
        "w_cost":    random.uniform(-0.1, 0.1),
        "w_defense": random.uniform(-0.1, 0.1),
        "w_synergy": random.uniform(-0.1, 0.1),
        "w_balance": random.uniform(-0.1, 0.1),
        "bias":      0.0
    }
    for card in cards
}


def calculate_average_attack_and_cost_and_defense(card_names):
    deck_cards = [card for card in cards if card["Name"] in card_names]
    if len(card_names) != 8 or len(set(card_names)) != 8 or len(deck_cards) != 8:
        raise ValueError("Enter 8 different valid card names")

    count = lambda key: sum(card[key] for card in deck_cards)
    win_conditions = count("WinCondition")
    buildings = count("Building")
    air = count("AirCounter")
    ground = count("GroundCounter")
    anti_tank = count("AntiTank")
    total_cost = sum(card["Cost"] for card in deck_cards)
    average_cost = total_cost / 8

    main_attack = max((card["Attack"] for card in deck_cards if card["WinCondition"]), default=0)
    support_attack = sum(card["Attack"] for card in deck_cards if not card["WinCondition"]) / 7
    spell_attack = sum(card["Attack"] for card in deck_cards if card["SmallSpell"] or card["BigSpell"])
    attack = 0.7 + 0.69 * main_attack + 0.15 * min(8, support_attack) + 0.11 * spell_attack - 0.35 * max(0, win_conditions - 2)
    if win_conditions == 0:
        attack = min(attack, 3.0)

    strongest_defenders = sorted((card["Defense"] for card in deck_cards), reverse=True)
    defense = 0.7 + 0.29 * sum(strongest_defenders[:4]) + 0.25 * min(3, air) + 0.25 * min(2, anti_tank) + 0.18 * min(2, ground) - 0.3 * max(0, buildings - 2)

    return max(1, min(10, attack)), average_cost, max(1, min(10, defense))

def calculate_synergy_balance(card_names):
    deck_cards = [
        card for card in cards
        if card["Name"] in card_names
    ]

    if len(card_names) != 8 or len(set(card_names)) != 8 or len(deck_cards) != 8:
        raise ValueError("Enter 8 different valid card names")

    x1 = sum(card["AirCounter"] for card in deck_cards)
    x2 = sum(card["GroundCounter"] for card in deck_cards)
    x3 = sum(card["Building"] for card in deck_cards)
    x4 = sum(card["SmallSpell"] for card in deck_cards)
    x5 = sum(card["BigSpell"] for card in deck_cards)
    x6 = sum(card["WinCondition"] for card in deck_cards)

    synergy = (
        s_w1*x1 + s_w2*x2 + s_w3*x3 +
        s_w4*x4 + s_w5*x5 + s_w6*x6 + s_bias
    )

    balance = (
        b_w1*x1 + b_w2*x2 + b_w3*x3 +
        b_w4*x4 + b_w5*x5 + b_w6*x6 + b_bias
    )

    return (
        round(max(1, min(10, synergy)), 2),
        round(max(1, min(10, balance)), 2)
    )

TRAIN = False
epochs = 10000
lr = 0.01

def Locate_Model(Name):
    filename = Name if Name.endswith(".json") else f"{Name}.json"
    
    current = Path(__file__).resolve().parent
    for parent in [current] + list(current.parents):
        match = next(parent.glob(f"**/{filename}"), None)
        if match:
            return match

    match = next(Path.cwd().glob(f"**/{filename}"), None)
    if match:
        return match

    raise FileNotFoundError(f"Could not locate '{filename}' anywhere in the workspace.")


def Save_Card_Weights(name):
    filename = name if name.endswith(".json") else f"{name}.json"
    
    try:
        model_ref = Locate_Model("Balance_And_Synergy.json")
        target_path = model_ref.parent / filename
    except FileNotFoundError:
        target_path = Path(__file__).resolve().parent / filename

    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(card_weights, f, indent=2)

    print(f"Successfully saved card weights to: {target_path}")




MODEL_PARAMETERS = (
    "s_w1", "s_w2", "s_w3", "s_w4", "s_w5", "s_w6", "s_bias",
    "b_w1", "b_w2", "b_w3", "b_w4", "b_w5", "b_w6", "b_bias")

Parameters2 = ("w_attack", "w_cost", "w_defense", "w_synergy", "w_balance", "bias")


def Load_Model(ModelFile, Parameters):
    
    if not ModelFile.exists():
        raise FileNotFoundError(
            f"No saved model at {ModelFile}. Set TRAIN = True and run once first."
        )
    saved = json.loads(ModelFile.read_text(encoding="utf-8"))
    missing = [name for name in Parameters if name not in saved]
    if missing:
        raise ValueError(f"Saved model is missing parameters: {missing}")
    for name in Parameters:
        globals()[name] = float(saved[name])
    

Load_Model(Locate_Model("Balance_And_Synergy.json"), MODEL_PARAMETERS)

w_attack = random.uniform(-1, 1)
w_cost = random.uniform(-1, 1)
w_defense = random.uniform(-1, 1)
w_synergy = random.uniform(-1, 1)
w_balance = random.uniform(-1, 1)
bias = random.uniform(-1, 1)
def Train_Card_Weights(Set_attack, Set_cost, Set_defense, Set_synergy, Set_balance):
    all_card_names = [card["Name"] for card in cards]

    for epoch in range(epochs):
        scores = {}
        for name in all_card_names:
            w = card_weights[name]
            score = (
                (Set_attack  * w["w_attack"])  +
                (Set_cost    * w["w_cost"])    +
                (Set_defense * w["w_defense"]) +
                (Set_synergy * w["w_synergy"]) +
                (Set_balance * w["w_balance"]) +
                w["bias"]
            )
            scores[name] = score + random.uniform(-1.0, 1.0)

        chosen_deck = sorted(scores, key=scores.get, reverse=True)[:8]

        att, cost, df = calculate_average_attack_and_cost_and_defense(chosen_deck)
        syn, bal = calculate_synergy_balance(chosen_deck)

        err_attack  = att - Set_attack
        err_cost    = cost - Set_cost
        err_defense = df - Set_defense
        err_synergy = syn - Set_synergy
        err_balance = bal - Set_balance

        total_loss = (
            abs(err_attack) +
            abs(err_cost) * 2.0 +
            abs(err_defense) +
            abs(err_synergy) +
            abs(err_balance)
        )

        reward = -total_loss

        for name in chosen_deck:
            w = card_weights[name]
            w["w_attack"]  += lr * reward * Set_attack  * 0.01
            w["w_cost"]    += lr * reward * Set_cost    * 0.01
            w["w_defense"] += lr * reward * Set_defense * 0.01
            w["w_synergy"] += lr * reward * Set_synergy * 0.01
            w["w_balance"] += lr * reward * Set_balance * 0.01
            w["bias"]      += lr * reward * 0.01




def Use_Deck_Model(Set_attack, Set_cost, Set_defense, Set_synergy, Set_balance):
    if TRAIN:
        Train_Card_Weights(Set_attack, Set_cost, Set_defense, Set_synergy, Set_balance)

    all_card_names = [card["Name"] for card in cards]
    final_scores = {}

    for name in all_card_names:
        w = card_weights[name]
        final_scores[name] = (
            (Set_attack  * w["w_attack"])  +
            (Set_cost    * w["w_cost"])    +
            (Set_defense * w["w_defense"]) +
            (Set_synergy * w["w_synergy"]) +
            (Set_balance * w["w_balance"]) +
            w["bias"]
        )

    return sorted(final_scores, key=final_scores.get, reverse=True)[:8]



AttackRating = 7
DefenceRating = 8.5
CostRating = 3
SynergyRating = 8
BalanceRating = 9

print(Use_Deck_Model(AttackRating, CostRating, DefenceRating, SynergyRating, BalanceRating))

if TRAIN:
    Save_Card_Weights("Deck_Builder_Weights.json")