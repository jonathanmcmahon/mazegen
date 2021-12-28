"""A maze generator.

This script takes a single integer parameter indicating the size of the maze.
"""
import sys
import numpy as np
import matplotlib.pyplot as plt


def get_square(cur, d):
    """Get coordinates of a square relative to the current square."""
    return tuple(x - y for x, y in zip(cur, d))


def get_unvisited_neighbors(cur):
    """Return list of unvisited neighbors of current square."""
    unvisited = []
    for d in directions:
        neighbor = get_square(cur, d)
        if 0 <= neighbor[0] < n and 0 <= neighbor[1] < n:
            if m[neighbor] != VISITED:
                unvisited.append(neighbor)
    return unvisited


def remove_wall(cur, nxt):
    """Remove a wall between two squares."""
    direction = tuple(x - y for x, y in zip(cur, nxt))
    halfway = tuple(x // 2 for x in direction)
    wall = get_square(current, halfway)
    m[wall] = 0


if len(sys.argv) > 1:
    n = int(sys.argv[1])
else:
    n = 51

assert n % 2 == 1, "n must be odd"

VISITED = -1
up, down, left, right = (-2, 0), (2, 0), (0, -2), (0, 2)
directions = [up, down, left, right]

# Create the maze grid
m = np.zeros((n, n))

# Create walls between all cells
for i in range(0, n + 1, 2):
    m[:, i] = 1
    m[i, :] = 1

# Create entrance / exit
m[0:2,0:2] = 0
m[n-2:n,n-2:n] = 0

stack = []
current = (n - 2, n - 2)  # start in bottom right corner
m[current] = VISITED
stack.append(current)

print("Generating maze of size %i x %i..." % (n, n))
while stack:
    unvisited_neighbors = get_unvisited_neighbors(current)
    if unvisited_neighbors:
        next_idx = np.random.choice(len(unvisited_neighbors))
        next_square = unvisited_neighbors[next_idx]
        stack.append(current)
        remove_wall(current, next_square)
        current = next_square
        m[current] = VISITED
    else:
        current = stack.pop()
print("Generate maze completed.")

# Clean up the explored square markers
m[m == -1] = 0

# Display the maze
print("Plotting maze...")
plt.imshow(m, cmap=plt.cm.binary)
plt.axis("off")
plt.show()
print("Plot maze completed.")
