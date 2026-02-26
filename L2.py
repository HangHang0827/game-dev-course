# Lecture 2
# - Section 1:　List, Dictionary, Set and Lambda

# List Without comprehension - Example

entities = [
    {"type": "player", "hp": 100},
    {"type": "enemy", "hp": 50},
    {"type": "enemy", "hp": 0},
    {"type": "npc", "hp": 10},
    {"type": "enemy", "hp": 20},
]

# 1. Initialize empty list
active_enemies = []

# 2. Iterate and check conditions
for e in entities:
    if e["type"] == "enemy" and e["hp"] > 0:
        active_enemies.append(e)

print(f"Active enemies found: {len(active_enemies)}")


# List With comprehension - Example

entities = [
    {"type": "player", "hp": 100},
    {"type": "enemy", "hp": 50},
    {"type": "enemy", "hp": 0},
    {"type": "npc", "hp": 10},
    {"type": "enemy", "hp": 20},
]

# List Comprehension to get only active enemies
active_enemies = [e for e in entities if e["type"] == "enemy" and e["hp"] > 0]

print(f"Active enemies found: {len(active_enemies)}")







# List (advanced) Without comprehension - Example
matrix = [[1,2,3], [4,5,6]]
flat = []

for row in matrix:        # Outer loop
    for num in row:       # Inner loop
        flat.append(num)

# List (advanced) With comprehension - Example
matrix = [[1,2,3], [4,5,6]]
flat = [num for row in matrix for num in row]



# List (advanced) Without comprehension - Practice
even_gt_10 = [x for x in range(30) if x % 2 == 0 if x > 10]

# List (advanced) With comprehension - Practice
# Please write the coding here.
###################################################

even_gt_10 = []

for x in range(30):
    if x % 2 == 0:
        if x > 10:
            even_gt_10.append(x)

####################################################


# List (advanced) Without comprehension - More Example

bullets = ["bullet1", "bullet2"]
enemies = ["orc1", "orc2", "orc3"]
collision_checks = []

for b in bullets:
    for e in enemies:
        pair = (b, e)
        collision_checks.append(pair)

# List (advanced) With comprehension - More Example

bullets = ["bullet1", "bullet2"]
enemies = ["orc1", "orc2", "orc3"]

# Generate pairs to check
collision_checks = [(b, e) for b in bullets for e in enemies]
# Result: [('bullet1', 'orc1'), ('bullet1', 'orc2'), ...]




# Dictionary With comprehension - Example
squares_dict = {i: i**2 for i in range(5)}

# Conditional dictionary With comprehension - Example
high_scores = {name: score for name, score in zip(names, scores) if score > 80}

