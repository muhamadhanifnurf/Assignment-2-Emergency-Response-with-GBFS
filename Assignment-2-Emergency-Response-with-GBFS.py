import heapq
import time

# Grid Assignment 2
city_map = [
    ["S", ".", ".", "T", "."],
    [".", "T", ".", "T", "."],
    [".", ".", ".", ".", "."],
    ["T", ".", "T", "T", "."],
    [".", ".", ".", ".", "H"]
]

# GBFS dan A* dengan Manhattan Heuristic
start = None
goal = None

# Temukan posisi Start dan Hospital
for i in range(len(city_map)):
    for j in range(len(city_map[0])):
        if city_map[i][j] == "S":
            start = (i, j)
        elif city_map[i][j] == "H":
            goal = (i, j)

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def gbfs(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    open_list = [(manhattan(start, goal), start, [start])]
    node_count = 0

    start_time = time.time()

    while open_list:
        open_list.sort()  # sort by heuristic value
        h, current, path = open_list.pop(0)
        node_count += 1
        if current == goal:
            elapsed_time = (time.time() - start_time) * 1000
            return path, node_count, elapsed_time
        if current in visited:
            continue
        visited.add(current)
        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] != "T" and (nx, ny) not in visited:
                    open_list.append((manhattan((nx, ny), goal), (nx, ny), path + [(nx, ny)]))
    return None, node_count, 0

def a_star(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    open_list = [(0 + manhattan(start, goal), 0, start, [start])]
    node_count = 0

    start_time = time.time()

    while open_list:
        open_list.sort()  # sort by f(n) = g(n) + h(n)
        f, g, current, path = open_list.pop(0)
        node_count += 1
        if current == goal:
            elapsed_time = (time.time() - start_time) * 1000
            return path, g, node_count, elapsed_time
        if current in visited:
            continue
        visited.add(current)
        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] != "T" and (nx, ny) not in visited:
                    new_g = g + 1  # Assume uniform cost for each step
                    new_f = new_g + manhattan((nx, ny), goal)
                    open_list.append((new_f, new_g, (nx, ny), path + [(nx, ny)]))
    return None, float('inf'), node_count, 0

def visualize_grid(grid, path):
    """
    Visualisasi grid dengan jalur yang ditemukan.
    """
    visual_grid = [row[:] for row in grid]  # Salin grid
    for x, y in path:
        if visual_grid[x][y] not in ("S", "H"):
            visual_grid[x][y] = "*"
    print("\nGrid Visualization:")
    for row in visual_grid:
        print(" ".join(row))

# Menjalankan algoritma GBFS
print("\n=== Greedy Best-First Search (GBFS) ===")
start_time = time.perf_counter()
gbfs_path, gbfs_nodes, gbfs_time = gbfs(city_map, start, goal)
end_time = time.perf_counter()
elapsed_time = (end_time - start_time) * 1000  # Hitung waktu eksekusi dalam milidetik

if gbfs_path:
    print(f"Path: {gbfs_path}")
    print(f"Nodes explored: {gbfs_nodes}")
    print(f"Elapsed time: {elapsed_time:.4f} ms")  # Waktu dengan presisi tinggi
    visualize_grid(city_map, gbfs_path)
else:
    print("No path found using GBFS.")

# Menjalankan algoritma A*
print("\n=== A* Search ===")
start_time = time.perf_counter()
astar_path, astar_cost, astar_nodes, astar_time = a_star(city_map, start, goal)
end_time = time.perf_counter()
elapsed_time = (end_time - start_time) * 1000  # Hitung waktu eksekusi dalam milidetik

if astar_path:
    print(f"Path: {astar_path}")
    print(f"Cost: {astar_cost}")
    print(f"Nodes explored: {astar_nodes}")
    print(f"Elapsed time: {elapsed_time:.4f} ms")  # Waktu dengan presisi tinggi
    visualize_grid(city_map, astar_path)
else:
    print("No path found using A*.")
