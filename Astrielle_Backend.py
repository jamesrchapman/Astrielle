from typing import Dict, List
import random

# Abstract Currency System
class Currency:
    """Represents different types of in-game currency."""
    def __init__(self):
        self.balances = {
            "Base Coins": 0,
            "Bonus Coins": 0,
            "Milestone Coins": 0,
            "Gacha Tokens": 0
        }

    def add(self, currency_type: str, amount: int):
        """Add currency of a given type."""
        if currency_type in self.balances:
            self.balances[currency_type] += amount

    def spend(self, currency_type: str, amount: int) -> bool:
        """Attempt to spend currency."""
        if self.balances.get(currency_type, 0) >= amount:
            self.balances[currency_type] -= amount
            return True
        return False

    def get_balances(self) -> Dict[str, int]:
        """Return all currency balances."""
        return self.balances

# Abstract Game Class
class Game:
    """Abstract base class for game types like Running, Idle, and Mini-games."""
    def __init__(self, name: str):
        self.name = name

    def progress(self, **kwargs):
        """Abstract method to progress the game."""
        raise NotImplementedError

# Running Game
class RunningGame(Game):
    """Handles running-based currency generation."""
    DISTANCE_PER_COIN = 10
    TIME_PER_BONUS_COIN = 30
    MILESTONE_FEET = 1000

    def __init__(self):
        super().__init__("Running Game")

    def progress(self, distance: int, time_seconds: int, currency: Currency):
        """Calculate and apply rewards from running."""
        currency.add("Base Coins", distance // self.DISTANCE_PER_COIN)
        currency.add("Bonus Coins", time_seconds // self.TIME_PER_BONUS_COIN)
        currency.add("Milestone Coins", distance // self.MILESTONE_FEET)

# Idle Game
class IdleGame(Game):
    """Represents an idle game where running speeds up progress."""
    def __init__(self, name: str):
        super().__init__(name)
        self.progress_value = 0
        self.speed_multiplier = 1  # Running increases this

    def progress(self, time_elapsed: int):
        """Idle progress grows over time."""
        self.progress_value += time_elapsed * self.speed_multiplier

    def boost_progress(self, multiplier: float):
        """Boost progress when the player runs."""
        self.speed_multiplier += multiplier

    def get_status(self) -> str:
        return f"{self.name} Progress: {self.progress_value:.2f} (Speed Multiplier: {self.speed_multiplier})"

# Collectible System
class Collectible:
    """Represents a collectible item in the game."""
    def __init__(self, name: str, rarity: str, description: str):
        self.name = name
        self.rarity = rarity
        self.description = description

    def __repr__(self):
        return f"{self.rarity} Collectible: {self.name} - {self.description}"

# Gacha System
class Gacha:
    """Handles the gacha roll system for earning collectibles."""
    def __init__(self, collectibles: List[Collectible]):
        self.collectibles = collectibles
        self.rarity_weights = {
            "Common": 60,
            "Rare": 25,
            "Epic": 10,
            "Legendary": 5
        }

    def roll(self) -> Collectible:
        """Perform a gacha roll and return a collectible."""
        weighted_collectibles = []
        for collectible in self.collectibles:
            weighted_collectibles.extend([collectible] * self.rarity_weights[collectible.rarity])
        return random.choice(weighted_collectibles)

# User System
class User:
    """Represents a player with all game data."""
    def __init__(self, name: str):
        self.name = name
        self.currency = Currency()
        self.inventory = []
        self.games = {
            "Running": RunningGame(),
            "Idle": IdleGame("Space Colony Expansion")
        }
        self.gacha = Gacha(self.load_collectibles())

    def load_collectibles(self) -> List[Collectible]:
        """Simulates loading collectibles from external data."""
        return [
            Collectible("Meteorite Fragment", "Common", "A small chunk of space rock."),
            Collectible("Lost Astronaut Patch", "Rare", "A patch from an unknown space mission."),
            Collectible("Alien Artifact", "Epic", "A mysterious object with strange engravings."),
            Collectible("Black Hole Core", "Legendary", "A fragment of infinite density."),
        ]

    def run(self, distance: int, time_seconds: int):
        """Process a running session."""
        self.games["Running"].progress(distance, time_seconds, self.currency)

    def idle_progress(self, time_elapsed: int):
        """Progress the idle game."""
        self.games["Idle"].progress(time_elapsed)

    def roll_gacha(self):
        """Attempt a gacha roll."""
        if self.currency.spend("Gacha Tokens", 1):
            collectible = self.gacha.roll()
            self.inventory.append(collectible)
            return collectible
        return None

    def get_status(self):
        """Return a summary of the user's progress."""
        return {
            "Name": self.name,
            "Currency": self.currency.get_balances(),
            "Inventory": [str(item) for item in self.inventory],
            "Idle Game": self.games["Idle"].get_status()
        }

# Simulating a session
user = User("Astrielle Pilot")
user.run(2500, 120)  # Simulate a run
user.idle_progress(60)  # Simulate idle progress
user.currency.add("Gacha Tokens", 3)  # Give some gacha rolls
gacha_results = [user.roll_gacha() for _ in range(3)]  # Perform gacha rolls

# Display results
game_state = user.get_status()
game_state["Gacha Rolls"] = [str(item) for item in gacha_results]

# Display game state in a structured format
df = pd.DataFrame(game_state.items(), columns=["Category", "Details"])
tools.display_dataframe_to_user(name="Astrielle Game State (Abstracted)", dataframe=df)


# Updating the structure to rename "Collectible" to "Item" for better abstraction.

class Item:
    """Represents an item in the game, which could be collectibles, equipment, etc."""
    def __init__(self, name: str, rarity: str, description: str):
        self.name = name
        self.rarity = rarity  # Common, Rare, Epic, Legendary
        self.description = description

    def __repr__(self):
        return f"{self.rarity} Item: {self.name} - {self.description}"

# Updating the Gacha system to reflect the terminology change.
class Gacha:
    """Handles the gacha roll system for earning items."""
    def __init__(self, items: List[Item]):
        self.items = items
        self.rarity_weights = {
            "Common": 60,
            "Rare": 25,
            "Epic": 10,
            "Legendary": 5
        }

    def roll(self) -> Item:
        """Perform a gacha roll and return an item."""
        weighted_items = []
        for item in self.items:
            weighted_items.extend([item] * self.rarity_weights[item.rarity])
        return random.choice(weighted_items)

# Updating the User class to reflect the terminology change.
class User:
    """Represents a player with all game data."""
    def __init__(self, name: str):
        self.name = name
        self.currency = Currency()
        self.inventory = []
        self.games = {
            "Running": RunningGame(),
            "Idle": IdleGame("Space Colony Expansion")
        }
        self.gacha = Gacha(self.load_items())

    def load_items(self) -> List[Item]:
        """Simulates loading items from external data."""
        return [
            Item("Meteorite Fragment", "Common", "A small chunk of space rock."),
            Item("Lost Astronaut Patch", "Rare", "A patch from an unknown space mission."),
            Item("Alien Artifact", "Epic", "A mysterious object with strange engravings."),
            Item("Black Hole Core", "Legendary", "A fragment of infinite density."),
        ]

    def run(self, distance: int, time_seconds: int):
        """Process a running session."""
        self.games["Running"].progress(distance, time_seconds, self.currency)

    def idle_progress(self, time_elapsed: int):
        """Progress the idle game."""
        self.games["Idle"].progress(time_elapsed)

    def roll_gacha(self):
        """Attempt a gacha roll."""
        if self.currency.spend("Gacha Tokens", 1):
            item = self.gacha.roll()
            self.inventory.append(item)
            return item
        return None

    def get_status(self):
        """Return a summary of the user's progress."""
        return {
            "Name": self.name,
            "Currency": self.currency.get_balances(),
            "Inventory": [str(item) for item in self.inventory],
            "Idle Game": self.games["Idle"].get_status()
        }

# Simulating a session
user = User("Astrielle Pilot")
user.run(2500, 120)  # Simulate a run
user.idle_progress(60)  # Simulate idle progress
user.currency.add("Gacha Tokens", 3)  # Give some gacha rolls
gacha_results = [user.roll_gacha() for _ in range(3)]  # Perform gacha rolls

# Displaying game state
print("=== Astrielle Game State ===")
print(f"User: {user.name}")
print("Currency:", user.currency.get_balances())
print("Inventory:", user.inventory)
print("Idle Game:", user.games["Idle"].get_status())
print("Gacha Rolls:", gacha_results)


# Updating the system to include game unlocking, playtime tracking, and item usage.

class Game:
    """Abstract base class for different types of games."""
    def __init__(self, name: str, required_item: str = None):
        self.name = name
        self.required_item = required_item  # Special item required to access
        self.playtime_remaining = 0  # How long the game can be played

    def add_playtime(self, time_seconds: int):
        """Add playtime to the game, earned from running or other activities."""
        self.playtime_remaining += time_seconds

    def play(self, time_seconds: int) -> bool:
        """Attempts to play the game for the given time, returns success status."""
        if self.playtime_remaining >= time_seconds:
            self.playtime_remaining -= time_seconds
            return True
        return False

    def can_play(self, user) -> bool:
        """Checks if the user has the required item to play the game."""
        if self.required_item and not any(item.name == self.required_item for item in user.inventory):
            return False
        return True

    def get_status(self) -> str:
        """Returns the status of the game."""
        return f"{self.name}: Playtime Remaining {self.playtime_remaining}s, Requires: {self.required_item if self.required_item else 'None'}"

class RunningGame(Game):
    """Handles running-based playtime generation and currency rewards."""
    DISTANCE_PER_COIN = 10
    TIME_PER_BONUS_COIN = 30
    MILESTONE_FEET = 1000

    def __init__(self):
        super().__init__("Running Game")

    def progress(self, distance: int, time_seconds: int, currency: Currency, user):
        """Calculate rewards and add playtime to unlockable games."""
        currency.add("Base Coins", distance // self.DISTANCE_PER_COIN)
        currency.add("Bonus Coins", time_seconds // self.TIME_PER_BONUS_COIN)
        currency.add("Milestone Coins", distance // self.MILESTONE_FEET)

        # Running contributes to game playtime
        for game in user.games.values():
            if game.name != "Running Game":
                game.add_playtime(time_seconds)

class Item:
    """Represents an item that can be used, equipped, or required for games."""
    def __init__(self, name: str, rarity: str, description: str, item_type: str):
        self.name = name
        self.rarity = rarity  # Common, Rare, Epic, Legendary
        self.description = description
        self.item_type = item_type  # "Equippable" or "Consumable"

    def __repr__(self):
        return f"{self.rarity} {self.item_type} Item: {self.name} - {self.description}"

class User:
    """Represents a player with all game data."""
    def __init__(self, name: str):
        self.name = name
        self.currency = Currency()
        self.inventory = []
        self.games = {
            "Running": RunningGame(),
            "Idle": IdleGame("Space Colony Expansion"),
            "Asteroid Mining": Game("Asteroid Mining", required_item="Mining Laser"),
            "Zero-G Racing": Game("Zero-G Racing", required_item="Gravity Boots")
        }
        self.gacha = Gacha(self.load_items())

    def load_items(self) -> List[Item]:
        """Simulates loading items from external data."""
        return [
            Item("Meteorite Fragment", "Common", "A small chunk of space rock.", "Collectible"),
            Item("Mining Laser", "Rare", "Required to play Asteroid Mining.", "Equippable"),
            Item("Gravity Boots", "Epic", "Required to play Zero-G Racing.", "Equippable"),
            Item("Fuel Cell", "Legendary", "Doubles playtime of any game when used.", "Consumable"),
        ]

    def run(self, distance: int, time_seconds: int):
        """Process a running session."""
        self.games["Running"].progress(distance, time_seconds, self.currency, self)

    def idle_progress(self, time_elapsed: int):
        """Progress the idle game."""
        self.games["Idle"].progress(time_elapsed)

    def roll_gacha(self):
        """Attempt a gacha roll."""
        if self.currency.spend("Gacha Tokens", 1):
            item = self.gacha.roll()
            self.inventory.append(item)
            return item
        return None

    def use_item(self, item_name: str, game_name: str):
        """Use a consumable item on a specific game."""
        for item in self.inventory:
            if item.name == item_name and item.item_type == "Consumable":
                game = self.games.get(game_name)
                if game:
                    game.add_playtime(game.playtime_remaining)  # Double playtime
                    self.inventory.remove(item)
                    return f"Used {item_name} on {game_name}. Playtime doubled!"
        return "Item not found or not usable."

    def get_status(self):
        """Return a summary of the user's progress."""
        return {
            "Name": self.name,
            "Currency": self.currency.get_balances(),
            "Inventory": [str(item) for item in self.inventory],
            "Games": {game_name: game.get_status() for game_name, game in self.games.items()}
        }

# Simulating a session
user = User("Astrielle Pilot")
user.run(2500, 120)  # Simulate a run, adding playtime to locked games
user.idle_progress(60)  # Simulate idle progress
user.currency.add("Gacha Tokens", 3)  # Give some gacha rolls
gacha_results = [user.roll_gacha() for _ in range(3)]  # Perform gacha rolls

# Using an item (if it was rolled)
if any(item.name == "Fuel Cell" for item in user.inventory):
    user.use_item("Fuel Cell", "Asteroid Mining")

# Displaying game state
print("=== Astrielle Game State ===")
print(f"User: {user.name}")
print("Currency:", user.currency.get_balances())
print("Inventory:", user.inventory)
print("Games:")
for game in user.games.values():
    print(f" - {game.get_status()}")
print("Gacha Rolls:", gacha_results)


# Fixing the IdleGame class to inherit and correctly handle playtime

class IdleGame(Game):
    """Represents an idle game where running speeds up progress."""
    def __init__(self, name: str):
        super().__init__(name)
        self.progress_value = 0
        self.speed_multiplier = 1  # Running increases this

    def progress(self, time_elapsed: int):
        """Idle progress grows over time."""
        self.progress_value += time_elapsed * self.speed_multiplier

    def boost_progress(self, multiplier: float):
        """Boost progress when the player runs."""
        self.speed_multiplier += multiplier

    def add_playtime(self, time_seconds: int):
        """Idle game should be able to receive playtime contributions like other games."""
        self.playtime_remaining += time_seconds  # Fixing the issue

    def get_status(self) -> str:
        return f"{self.name}: Progress {self.progress_value:.2f}, Speed Multiplier {self.speed_multiplier}, Playtime Remaining {self.playtime_remaining}s"

# Re-initialize the user and test again
user = User("Astrielle Pilot")
user.run(2500, 120)  # Simulate a run, adding playtime to locked games
user.idle_progress(60)  # Simulate idle progress
user.currency.add("Gacha Tokens", 3)  # Give some gacha rolls
gacha_results = [user.roll_gacha() for _ in range(3)]  # Perform gacha rolls

# Using an item (if it was rolled)
if any(item.name == "Fuel Cell" for item in user.inventory):
    user.use_item("Fuel Cell", "Asteroid Mining")

# Displaying game state
print("=== Astrielle Game State ===")
print(f"User: {user.name}")
print("Currency:", user.currency.get_balances())
print("Inventory:", user.inventory)
print("Games:")
for game in user.games.values():
    print(f" - {game.get_status()}")
print("Gacha Rolls:", gacha_results)
