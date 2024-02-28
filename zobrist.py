import random
from settings import *

MAX63 = 2**63 - 1  # Shoule be a random 64 bit binary number
sets = set()  # Make sure no duplicates


while (
    len(sets) < WIDTH * HEIGHT * 3 + 1
):  # For each space there is three state and the empty space
    code = random.randint(0, MAX63)
    sets.add(code)

sets = list(sets)

coords = []
for row in range(WIDTH):
    for col in range(HEIGHT):
        coords.append((row, col))

players = ["None", "Player.black", "Player.white"]  # None for capture

print("HASH_CODE = {")

i = 0
for k in coords:
    for j in players:
        print(" (%r, %s): %r," % (k, j, sets[i]))
        i += 1
print("}")

print("EMPTY_BOARD = %d" % (sets[-1]))
