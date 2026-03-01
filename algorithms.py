import pygame
from queue import PriorityQueue
import math

def h_manhattan(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def h_euclidean(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def reconstruct_path(came_from, current, draw):
    path = []
    while current in came_from:
        current = came_from[current]
        path.append(current)
        current.make_path()
        draw()
    return path

def search(draw, grid, start, goal, mode="A*", heuristic="manhattan"):
    count = 0
    open_set = PriorityQueue()
    # (score, tie_breaker, node)
    open_set.put((0, count, start))
    came_from = {}
    
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    
    f_score = {node: float("inf") for row in grid for node in row}
    
    h_func = h_manhattan if heuristic == "manhattan" else h_euclidean
    f_score[start] = h_func(start.get_pos(), goal.get_pos())

    open_set_hash = {start}
    nodes_visited = 0

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)
        nodes_visited += 1

        if current == goal:
            path = reconstruct_path(came_from, goal, draw)
            return path, nodes_visited

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                
                # Logic Switch: A* uses G+H, Greedy uses only H
                h_val = h_func(neighbor.get_pos(), goal.get_pos())
                if mode == "A*":
                    f_score[neighbor] = temp_g_score + h_val
                else:
                    f_score[neighbor] = h_val
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_frontier()

        draw()
        if current != start:
            current.make_visited()

    return None, nodes_visited
