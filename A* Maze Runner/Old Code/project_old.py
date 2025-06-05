# Program will randomly generate a maze and will use the A* algorithm to give the shortest path to solve the maze, given that a path exists.
# Will output "No valid path found" if there is no valid path.

import heapq
import random

def generate_maze(rows, cols, wall_prob):
    maze = [[0] * cols for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            if row == 0 or col == 0 or row == rows - 1 or col == cols - 1 or random.random() < wall_prob:
                maze[row][col] = 1  # 1 represents a wall
    return maze

def print_maze(maze):
    for row in maze:
        print(" ".join(map(str, row)))

def heuristic(current, goal):
    # Manhattan distance heuristic
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])

def astar(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {start: None}
    g_score = {start: 0}

    while open_set:
        current_cost, current_node = heapq.heappop(open_set)

        if current_node == goal:
            path = reconstruct_path(came_from, goal)
            return path

        for neighbor in get_neighbors(current_node, rows, cols):
            tentative_g_score = g_score[current_node] + 1

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] != 1:
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))
                    came_from[neighbor] = current_node

    return None  # No path found

def get_neighbors(node, rows, cols):
    neighbors = [(node[0] + 1, node[1]), (node[0] - 1, node[1]), (node[0], node[1] + 1), (node[0], node[1] - 1)]
    return [(r, c) for r, c in neighbors if 0 <= r < rows and 0 <= c < cols]

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from and came_from[current] is not None:
        current = came_from[current]
        path.insert(0, current)
    return path

if __name__ == "__main__":
    import random

    rows, cols = 10, 10
    start = (1, 1)
    goal = (rows - 2, cols - 2)
    wall_probability = 0.3

    maze = generate_maze(rows, cols, wall_probability)
    print("Generated Maze:")
    print_maze(maze)

    path = astar(maze, start, goal)

    if path:
        print("\nShortest Path:")
        for row, col in path:
            maze[row][col] = 2  # 2 represents the path
        print_maze(maze)
    else:
        print("\nNo valid path found.")
