from __future__ import annotations

import random
import pygame

from algorithms import reset_search_colors, search
from node import Node

pygame.init()

WIDTH, HEIGHT = 600, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer (DFS/BFS/UCS/Greedy/A*)")

ROWS = 30
GRID_AREA = 600  # top 600x600
DASHBOARD_H = 100

FONT = pygame.font.SysFont("consolas", 18)

MODES = ["DFS", "BFS", "UCS", "Greedy", "A*"]
MODE_KEYS = {
    pygame.K_1: "DFS",
    pygame.K_2: "BFS",
    pygame.K_3: "UCS",
    pygame.K_4: "Greedy",
    pygame.K_5: "A*",
}


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for r in range(rows):
        grid.append([])
        for c in range(rows):
            grid[r].append(Node(r, c, gap, rows))
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, (200, 200, 200), (0, i * gap), (width, i * gap))
        pygame.draw.line(win, (200, 200, 200), (i * gap, 0), (i * gap, width))


def draw_dashboard(win, mode, dynamic_mode, obstacle_prob, status):
    y0 = GRID_AREA
    pygame.draw.rect(win, (245, 245, 245), (0, y0, WIDTH, DASHBOARD_H))

    lines = [
        f"Mode: {mode}   |   Dynamic: {'ON' if dynamic_mode else 'OFF'}   |   Spawn p={obstacle_prob:.2f}",
        "Controls: L-Click=Start/Goal/Walls   |   R-Click=Erase",
        "SPACE=Run   |   D=Toggle Dynamic   |   C=Clear",
        "1=DFS  2=BFS  3=UCS  4=Greedy  5=A*",
        f"Status: {status}",
    ]

    for i, txt in enumerate(lines):
        surf = FONT.render(txt, True, (20, 20, 20))
        win.blit(surf, (10, y0 + 8 + i * 18))


def draw(win, grid, mode, dynamic_mode, obstacle_prob, status):
    win.fill((255, 255, 255))

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, ROWS, GRID_AREA)
    draw_dashboard(win, mode, dynamic_mode, obstacle_prob, status)

    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    x, y = pos
    gap = width // rows
    row = y // gap
    col = x // gap
    return row, col


def update_all_neighbors(grid):
    for row in grid:
        for node in row:
            node.update_neighbors(grid)


def spawn_dynamic_obstacle(grid, start, goal):
    """
    Spawns a wall only on an empty cell:
    - not a wall
    - not start
    - not goal
    """
    empties = []
    for row in grid:
        for node in row:
            if node.is_wall():
                continue
            if node == start or node == goal:
                continue
            # Only truly empty cells (white)
            if node.color == (255, 255, 255):
                empties.append(node)

    if not empties:
        return None

    chosen = random.choice(empties)
    chosen.make_wall()
    return chosen


def mark_path(path, start, goal):
    # path includes [start..goal]
    for node in path:
        if node != start and node != goal and not node.is_wall():
            node.make_path()
    start.make_start()
    goal.make_end()


def main():
    grid = make_grid(ROWS, GRID_AREA)

    start = None
    goal = None

    mode = "A*"
    dynamic_mode = False
    obstacle_prob = 0.15

    status = "Place start, goal, and walls. Press SPACE to run."

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)

        draw(WIN, grid, mode, dynamic_mode, obstacle_prob, status)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                if pos[1] < GRID_AREA:  # only inside grid
                    row, col = get_clicked_pos(pos, ROWS, GRID_AREA)
                    if 0 <= row < ROWS and 0 <= col < ROWS:
                        node = grid[row][col]

                        if start is None and node != goal and not node.is_wall():
                            start = node
                            start.make_start()
                            status = "Start set. Now set goal."
                        elif goal is None and node != start and not node.is_wall():
                            goal = node
                            goal.make_end()
                            status = "Goal set. Add walls or press SPACE to run."
                        elif node != start and node != goal:
                            node.make_wall()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                if pos[1] < GRID_AREA:
                    row, col = get_clicked_pos(pos, ROWS, GRID_AREA)
                    if 0 <= row < ROWS and 0 <= col < ROWS:
                        node = grid[row][col]
                        node.reset()
                        if node == start:
                            start = None
                        if node == goal:
                            goal = None
                        status = "Erased."

            if event.type == pygame.KEYDOWN:
                if event.key in MODE_KEYS:
                    mode = MODE_KEYS[event.key]
                    status = f"Mode switched to {mode}."

                if event.key == pygame.K_d:
                    dynamic_mode = not dynamic_mode
                    status = f"Dynamic mode {'ON' if dynamic_mode else 'OFF'}."

                if event.key == pygame.K_c:
                    start = None
                    goal = None
                    grid = make_grid(ROWS, GRID_AREA)
                    status = "Cleared."

                if event.key == pygame.K_SPACE:
                    if start is None or goal is None:
                        status = "You must place start and goal first."
                        continue

                    # Always update neighbors before searching
                    update_all_neighbors(grid)

                    # Clean old markings (keep walls/start/goal)
                    reset_search_colors(grid, start, goal)

                    status = f"Searching with {mode}..."
                    draw(WIN, grid, mode, dynamic_mode, obstacle_prob, status)

                    found, path = search(
                        lambda: draw(WIN, grid, mode, dynamic_mode, obstacle_prob, status),
                        grid,
                        start,
                        goal,
                        mode=mode,
                        heuristic="manhattan",
                    )

                    if not found:
                        status = "No path found."
                        continue

                    # Show the initial planned path
                    mark_path(path, start, goal)
                    status = "Path found. Moving agent..."

                    # --- Agent movement + dynamic replanning ---
                    current = start
                    agent_prev = None

                    # Move along path index
                    idx = 0  # path[0] == start

                    moving = True
                    while moving:
                        clock.tick(30)  # movement speed

                        # Handle quit during movement
                        for e in pygame.event.get():
                            if e.type == pygame.QUIT:
                                pygame.quit()
                                return
                            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                                status = "Movement cancelled (ESC)."
                                moving = False

                        if not moving:
                            break

                        # If dynamic enabled, possibly spawn a new obstacle
                        if dynamic_mode and random.random() < obstacle_prob:
                            spawned = spawn_dynamic_obstacle(grid, start, goal)
                            if spawned is not None:
                                update_all_neighbors(grid)

                        # If we reached goal
                        if current == goal:
                            status = "Reached goal!"
                            start.make_start()
                            goal.make_end()
                            draw(WIN, grid, mode, dynamic_mode, obstacle_prob, status)
                            break

                        # If path is exhausted, stop
                        if idx >= len(path) - 1:
                            status = "Agent stopped (no further steps)."
                            break

                        next_node = path[idx + 1]

                        # If next step got blocked by a new wall → replan from current
                        if next_node.is_wall():
                            reset_search_colors(grid, start, goal)
                            update_all_neighbors(grid)

                            status = "Blocked! Replanning from current..."
                            draw(WIN, grid, mode, dynamic_mode, obstacle_prob, status)

                            found2, new_path = search(
                                lambda: draw(WIN, grid, mode, dynamic_mode, obstacle_prob, status),
                                grid,
                                current,
                                goal,
                                mode=mode,
                                heuristic="manhattan",
                            )

                            if not found2:
                                status = "Replan failed. No path exists."
                                draw(WIN, grid, mode, dynamic_mode, obstacle_prob, status)
                                break

                            path = new_path
                            idx = 0
                            # Re-mark the new path
                            reset_search_colors(grid, start, goal)
                            mark_path(path, current, goal)
                            status = "Replanned. Continuing..."
                            draw(WIN, grid, mode, dynamic_mode, obstacle_prob, status)
                            continue

                        # Move agent one step
                        if agent_prev and agent_prev != start and agent_prev != goal and not agent_prev.is_wall():
                            # Restore path color behind agent
                            agent_prev.make_path()

                        current = next_node
                        agent_prev = current

                        # Paint agent
                        if current != start and current != goal:
                            current.make_current()

                        start.make_start()
                        goal.make_end()

                        draw(WIN, grid, mode, dynamic_mode, obstacle_prob, status)

                        idx += 1

    pygame.quit()


if __name__ == "__main__":
    main()
