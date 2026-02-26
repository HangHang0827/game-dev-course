##################################################################
# Don't waste the exercises!
# Please try yourself first before asking, e.g. ChatGPT! 
##################################################################

# Exercise 1: The Loot Filter (List Comprehension)
# Scenario: After defeating a boss, a list of loot drops. However, the player's inventory is full, so they only want to pick up "Legendary" items.
# Task: Use a list comprehension to create a new list called legendary_drops that only contains items with a rarity of 10.

loot_pool = [
    {"item": "Rusty Sword", "rarity": 1},
    {"name": "Dragon Scale", "rarity": 10},
    {"name": "Common Potion", "rarity": 2},
    {"name": "Excalibur", "rarity": 10}
]

# Write your comprehension here:
legendary_drops = [l for l in loot_pool if l["rarity"] == 10]

print(legendary_drops)
# Expected Output: [{'name': 'Dragon Scale', 'rarity': 10}, {'name': 'Excalibur', 'rarity': 10}]



# Exercise 2: The Currency Exchange (Dict Comprehension)
# Scenario: You are coding a global game server. You have a dictionary of item prices in Gold, but you need to convert them all to Silver (1 Gold = 100 Silver).
# Task: Use a dictionary comprehension to create silver_prices by multiplying every value in gold_prices by 100.

gold_prices = {
    "Shield": 5,
    "Helmet": 3,
    "Boots": 2
}

# Write your comprehension here:
silver_prices = 

print(silver_prices)
# Expected Output: {'Shield': 500, 'Helmet': 300, 'Boots': 200}



# Exercise 3: The Stealth Radar (Nested & Conditional)
# Scenario: You have a 2D grid representing a battlefield. You want to identify "Safe Zones" for a stealth mission. A coordinate (x, y) is safe only if:
# 1. It is within the 3 x 3 grid (range 0 to 2).
# 2. The x and y coordinates are not equal (the diagonal is guarded by a sniper).
# Task: Use a nested list comprehension to generate a list of tuples safe_zones for all (x, y) pairs where x is not equal to y within a 3 x 3 grid.

# Hint: Use two 'for' clauses and one 'if' clause
# range(3) will give you 0, 1, 2

safe_zones = [(x,y)for x in range(3) for y in range(3) if x != y]

print(safe_zones)
# Expected Output: [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]



# Exercise 4: The Color Match (Puzzle Game)
# Scenario: In a "Match-3" puzzle game (like Candy Crush), you have a grid of gems. You want to find the coordinates of all gems that are Red so you can check if they form a line.
# Task: Use a list comprehension to find the (x, y) coordinates of all gems where the color is "Red".

# A grid represented as a list of dictionaries with coordinates and colors
gem_grid = [
    {"pos": (0, 0), "color": "Red"},
    {"pos": (0, 1), "color": "Blue"},
    {"pos": (1, 0), "color": "Green"},
    {"pos": (1, 1), "color": "Red"}
]

# Write your comprehension here:
red_gem_positions = [g["pos"] for g in gem_grid if g["color"] == "Red"]

print(red_gem_positions)
# Expected Output: [(0, 0), (1, 1)]



# Exercise 5: The Speed Trap (Racing Game)
# Scenario: You are building a racing game. At the end of a lap, you have a dictionary of lap_times (in seconds) for 4 different players. You want to identify which players are "Elite" (those who finished in under 60 seconds).
# Task: Use a dictionary comprehension to create elite_drivers containing only the players whose lap time was less than 60.0.

lap_times = {
    "TurboTom": 58.2,
    "SlowSam": 72.5,
    "NitroNick": 55.8,
    "DriftDaisy": 61.2
}

# Write your comprehension here:
# Create a new dict only if time < 60.0
elite_drivers = 

print(elite_drivers)
# Expected Output: {'TurboTom': 58.2, 'NitroNick': 55.8}



# Exercise 6: The Ultimate Damage Calculator (lambda function)
# Scenario: You have a base damage value for a player's attack. Depending on which "Power-Up" the player picks up, the damage calculation changes instantly.
# Task:
# Create a variable power_up that holds a lambda function.
# The lambda should take one input (dmg) and return the modified damage.
# Test it with two different scenarios:
# Critical Strike: Add a flat 50 points to the damage.
# Weakened State: Reduce the damage by 50% (divide by 2).

base_damage = 100

# --- EXERCISE START ---

# 1. Define a lambda for "Critical Strike" (add 50)
crit_strike = lambda dmg: # Your code here

# 32. Define a lambda for "Weakened" (50% of damage)
weakened = lambda dmg: # Your code here

# --- TEST YOUR WORK ---
print(f"Critical Strike: {crit_strike(base_damage)}") # Expected: 150
print(f"Weakened State: {weakened(base_damage)}")    # Expected: 50.0



# The Challenge: The Pro-Athlete Training System
# This exercise is based on a Sports Management Sim (like Football Manager or NBA 2K). In these games, you often have different "Training Drills" that improve player stats in different ways.
# Your Task: 
# 1. Complete the training_drills dictionary by writing three lambdas.
# 2. Use the apply_training function to execute the drill on a player's stat.

# The Player's current stat
player_stamina = 50

# --- TASK: Complete the Lambdas below ---
training_drills = {
    # 1. "Sprints": Increase stamina by 10% (multiply by 1.1)
    "Sprints": lambda s: s * 1.1,
    
    # 2. "Marathon": Increase stamina by a flat 15 points
    "Marathon": lambda s: # Your Code Here,
    
    # 3. "Rest": Reduce stamina by 5 (to simulate fatigue/cooldown)
    "Rest": lambda s: # Your Code Here
}

def apply_training(current_stat, drill_name):
    # Check if the drill exists in our dictionary
    if drill_name in training_drills:
        # Get the lambda and run it
        return training_drills[drill_name](current_stat)
    else:
        print("Drill not found!")
        return current_stat

# --- TEST YOUR WORK ---
# Try running the "Marathon" drill
new_stamina = apply_training(player_stamina, "Marathon")
print(f"Stamina after Marathon: {new_stamina}") # Should be 65

# Try running the "Sprints" drill
new_stamina = apply_training(player_stamina, "Sprints")
print(f"Stamina after Sprints: {new_stamina}")  # Should be 55.0