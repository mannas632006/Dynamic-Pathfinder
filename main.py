import pygame
import random
import time
from node import Node
from algorithms import search

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH + 100)) # Extra space for metrics
pygame.display.set_caption("Dynamic Pathfinding Agent")
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 18)

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, (128, 128, 128), (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, (128, 128, 128), (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width, metrics):
    win.fill((255, 255, 255))
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    
    # Dashboard
    pygame.draw.rect(win, (200, 200, 200), (0, width, width, 100))
    txt = f"Nodes: {metrics['nodes']} | Cost: {metrics['cost']} | Time: {metrics['time']}ms | Mode: {metrics['mode']}"
    img = FONT.render(txt, True, (0, 0, 0))
    win.blit(img, (10, width + 10))
    
    controls = "L-Click: Wall/Start | R-Click: Reset | SPACE: Start | D: Toggle Dynamic"
    img2 = FONT.render(controls, True, (50, 50, 50))
    win.blit(img2, (10, width + 40))
    
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    ROWS = 30
    grid = make_grid(ROWS, width)
    start = None
    goal = None
    run = True
    dynamic_mode = False
    
    metrics = {"nodes": 0, "cost": 0, "time": 0, "mode": "A*"}

    while run:
        draw(win, grid, ROWS, width, metrics)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # LEFT CLICK
                pos = pygame.mouse.get_pos()
                if pos[1] < width:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    if not start and node != goal:
                        start = node
                        start.make_start()
                    elif not goal and node != start:
                        goal = node
                        goal.make_goal()
                    elif node != goal and node != start:
                        node.make_wall()

            elif pygame.mouse.get_pressed()[2]: # RIGHT CLICK
                pos = pygame.mouse.get_pos()
                if pos[1] < width:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    grid[row][col].reset()
                    if grid[row][col] == start: start = None
                    if grid[row][col] == goal: goal = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    dynamic_mode = not dynamic_mode
                    print(f"Dynamic Mode: {dynamic_mode}")

                if event.key == pygame.K_SPACE and start and goal:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    
                    start_t = time.time()
                    path, visited = search(lambda: draw(win, grid, ROWS, width, metrics), grid, start, goal, mode=metrics['mode'])
                    end_t = time.time()
                    
                    metrics["nodes"] = visited
                    metrics["time"] = round((end_t - start_t) * 1000, 2)
                    metrics["cost"] = len(path) if path else 0
                    
                    # SIMULATE DYNAMIC AGENT MOTION
                    if path:
                        path.reverse() # Start to Goal
                        for step in path:
                            if dynamic_mode and random.random() < 0.15: # 15% chance of obstacle
                                # Spawn random wall in future path
                                r_row, r_col = random.randint(0, ROWS-1), random.randint(0, ROWS-1)
                                grid[r_row][r_col].make_wall()
                                
                                # RE-PLANNING if path is blocked
                                if grid[r_row][r_col] in path:
                                    print("Obstacle detected! Re-planning...")
                                    for r in grid: 
                                        for n in r: n.update_neighbors(grid)
                                    # Recursive call or re-run search from current 'step'
                                    break 

                if event.key == pygame.K_c: # Clear
                    start = None
                    goal = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)
