from math import sqrt
import random
import copy



def generate_maze(rows, cols, wall_prob, start_x, start_y, end_x, end_y):
    maze = [[" "] * cols for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            if row == 0 or row == rows - 1:
                maze[row][col] = '─'  # Top and Bottom border of maze
            if (col == 0 or col == cols - 1) and row != 0 and row != rows - 1:
                maze[row][col] = '|'  # Side border of maze
            if row != 0 and col != 0 and row != rows - 1 and col != cols-1 and random.random() < wall_prob:
                maze[row][col] = '■'    # ■ Represents obstacles
    maze[start_x][start_y] = " "
    maze[end_x][end_y] = " "
    print("Generated Maze:")
    print_maze(maze)
    return maze

def print_maze(maze):
    for row in maze:
        print(" ".join(map(str, row)))

def heuristic(current, goal):
    # Manhattan distance heuristic
    if current is None: 
        return 0 
    else:
        #return abs(current[0] - goal[0]) + abs(current[1] - goal[1])
        return sqrt((current[0] - goal[0])**2 + (current[1] - goal[1])**2)

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from and came_from[current] is not None:
        current = came_from[current]
        path.insert(0, current)
    return path

def get_neighbors(node, rows, cols):
    neighbors = [(node[0] + 1, node[1]), (node[0] - 1, node[1]), (node[0], node[1] + 1), (node[0], node[1] - 1)]
    return [(r, c) for r, c in neighbors if 0 <= r < rows and 0 <= c < cols]

def coords_in_list(l, coords):
    # print("entered coords_in_list with " + str(l) + " " + str(coords))
    for cost, l_coords in l:
        if l_coords == coords:
            return True
    return False

def get_cost(l, coords):
    for cost, l_coords in l:
        if coords == l_coords:
            return cost
    return 9999999

def drop_by_coords(l, coords):
    for i in range(len(l)):
        cost, l_coords = l[i]
        if coords[0] == l_coords and coords[1] == l_coords:
            l.pop(i)
            #print("Dropped: " + str(l[i]))
            return True
    return False

def insert_by_cost(l, cost, coords):
    if len(l) == 0:
        l.append((cost, coords))
    largest = True
    for i in range(len(l)):
        if l[i][0] < cost:
            continue
        else:
            l.insert(i, (cost, coords))
            largest = False
            break
    
    if largest:
        l.append((cost, coords))
    return l


def astar_pathfind_gen(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    open_set = [(heuristic(start, goal), start)]
    came_from = {start: None}
    explored = {}
    goal_found = False
    actual_cost = 0
    while open_set and not goal_found:
        current_cost, current_node = open_set.pop(0)
        actual_cost = len(reconstruct_path(came_from, current_node))    #actual cost is length of path-1 (since start does not move)
        print(str(actual_cost-1) + " cost for " + str(current_node))    #print for debugging
        explored[current_node] = actual_cost
        
        yield current_node

        #end condition
        if current_node == goal:
            goal_found = True
            print("Goal found!")
        

        # print("Neighbors of " + str(current_node) + ": " + str(get_neighbors(current_node, rows, cols)))

        print("After pop before additions/updates:\nexplored:", end=" ")
        print(explored.keys())
        print("frontier:", end=" ")
        print(open_set)

        for neighbor in get_neighbors(current_node, rows, cols):
            if maze[neighbor[0]][neighbor[1]] != '■' and maze[neighbor[0]][neighbor[1]] != '─' and maze[neighbor[0]][neighbor[1]] != '|' and neighbor not in explored.keys():
                if not coords_in_list(open_set, neighbor):
                    # print("Adding: " + str(neighbor) + " with cost: " + str(actual_cost+heuristic(neighbor, goal)))
                    open_set = insert_by_cost(open_set, actual_cost+heuristic(neighbor, goal), neighbor)
                    came_from[neighbor] = current_node

                else:
                    # coords are in list, need to check if cost function should be updated
                    if get_cost(open_set, neighbor) > heuristic(neighbor, goal) + actual_cost:
                        #print("Updating cost of: " + str(neighbor) + " to " + str(heuristic(neighbor, goal) + actual_cost) + " from " + str(get_cost(open_set, neighbor)))
                        #remove current tuple with oldcost, neighbor coordinates MOVED
                        #drop_by_coords(open_set, neighbor)
                        open_set = insert_by_cost(open_set, actual_cost+heuristic(neighbor, goal), neighbor)
                        came_from[neighbor] = current_node


                # remove duplicate
                first_instance = []
                for i in range(len(open_set)):
                    if open_set[i][1] not in first_instance:
                        first_instance.append(open_set[i][1])
                    else:
                        open_set.pop(i)
                        break
                
                

    return None  # No path found


def finish(new_maze, start_x, start_y, end_x, end_y):
    start = (start_x, start_y)
    goal = (end_x, end_y)
    temp = copy.deepcopy(new_maze)
    astar_pgen = astar_pathfind_gen(temp, start, goal)
    astar_path = []
    for node in astar_pgen:
        #print(node, end=", ")
        astar_path.append(node)

    if goal not in astar_path:
        return None

    num = 0
    x = 'A'
    for i in range(len(astar_path)):
        if num <= 25:
            val=chr(ord(x) + num)
            num += 1
        else:
            num = 1
        temp[astar_path[i][0]][astar_path[i][1]] = val

    # print("A is the start position, " + chr(ord('A') + len(astar_path) - 1) + " is the goal position")
    return temp
