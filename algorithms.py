from __future__ import annotations

from collections import deque
from queue import PriorityQueue
from typing import Callable, Dict, List, Optional, Tuple

from node import Node


def h_manhattan(a: Node, b: Node) -> int:
    ar, ac = a.get_pos()
    br, bc = b.get_pos()
    return abs(ar - br) + abs(ac - bc)


def reconstruct_path(came_from: Dict[Node, Node], start: Node, goal: Node) -> List[Node]:
    # Returns [start, ..., goal]
    path = [goal]
    cur = goal
    while cur in came_from:
        cur = came_from[cur]
        path.append(cur)
    path.reverse()
    if path and path[0] != start:
        return []
    return path


def reset_search_colors(grid, start: Node, goal: Node):
    # Clears open/closed/path/current markings but keeps walls + start + goal
    for row in grid:
        for node in row:
            if node.is_wall():
                continue
            if node == start:
                node.make_start()
            elif node == goal:
                node.make_end()
            else:
                node.reset()


def search(
    draw: Callable[[], None],
    grid,
    start: Node,
    goal: Node,
    mode: str = "A*",
    heuristic: str = "manhattan",
) -> Tuple[bool, List[Node]]:
    """
    Supported modes:
      - DFS
      - BFS
      - UCS
      - Greedy
      - A*
    Returns: (found, path [start..goal])
    """
    if heuristic != "manhattan":
        raise ValueError("Only 'manhattan' heuristic is supported in this version.")

    h = h_manhattan

    # Make sure neighbors are updated before search is called
    # (main.py does it globally)

    came_from: Dict[Node, Node] = {}

    # DFS / BFS (unweighted)
    if mode in ("DFS", "BFS"):
        frontier = deque([start])
        visited = {start}

        while frontier:
            current = frontier.pop() if mode == "DFS" else frontier.popleft()

            if current != start and current != goal:
                current.make_closed()

            if current == goal:
                path = reconstruct_path(came_from, start, goal)
                return (len(path) > 0), path

            for neighbor in current.neighbors:
                if neighbor not in visited and not neighbor.is_wall():
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    if neighbor != goal:
                        neighbor.make_open()
                    frontier.append(neighbor)

            draw()

        return False, []

    # UCS / Greedy / A* (priority-based)
    open_set = PriorityQueue()
    open_set.put((0, 0, start))
    open_set_hash = {start}

    g_score: Dict[Node, float] = {start: 0}
    count = 0

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.discard(current)

        if current != start and current != goal:
            current.make_closed()

        if current == goal:
            path = reconstruct_path(came_from, start, goal)
            return (len(path) > 0), path

        for neighbor in current.neighbors:
            if neighbor.is_wall():
                continue

            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                if mode == "UCS":
                    priority = tentative_g
                elif mode == "Greedy":
                    priority = h(neighbor, goal)
                else:  # A*
                    priority = tentative_g + h(neighbor, goal)

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((priority, count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != goal:
                        neighbor.make_open()

        draw()

    return False, []
