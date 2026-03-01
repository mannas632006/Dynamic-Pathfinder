Dynamic Pathfinder (Enhanced Version)
Overview

This project is an interactive Pathfinding Visualizer built using Python and Pygame.

It demonstrates multiple search algorithms used in Artificial Intelligence, including both uninformed and informed search strategies. The system also supports dynamic obstacle generation with real-time replanning, simulating a changing environment.

The application allows users to:

Place a Start node

Place a Goal node

Create Walls (obstacles)

Select different search algorithms

Enable dynamic obstacles

Watch the agent move step-by-step toward the goal

Automatically replan if a new obstacle blocks the path

Implemented Algorithms

The following search strategies are supported:

Depth-First Search (DFS)

Breadth-First Search (BFS)

Uniform Cost Search (UCS)

Greedy Best-First Search

A* Search

Each algorithm can be selected using keyboard controls.

Features

• Grid-based environment (30 × 30)
• Visual animation of open set and closed set
• Step-by-step agent movement
• Dynamic obstacle spawning during execution
• Automatic replanning if the path becomes blocked
• Real-time algorithm switching
• Clean dashboard displaying mode and status

How to Run

Make sure Python is installed.

Install dependencies:

pip install -r requirements.txt

Run the program:

python main.py

Controls

Mouse Controls:

• Left Click

First click → Set Start node

Second click → Set Goal node

Additional clicks → Place Walls

• Right Click

Erase a cell (removes wall/start/goal)

Keyboard Controls:

• SPACE → Run selected algorithm
• D → Toggle Dynamic Obstacles (ON/OFF)
• C → Clear entire board
• ESC → Cancel agent movement

Algorithm Selection:

• 1 → DFS
• 2 → BFS
• 3 → UCS
• 4 → Greedy Best-First
• 5 → A*

Dynamic Obstacle Mode

When Dynamic Mode is enabled:

Random obstacles may appear during agent movement.

Obstacles only spawn on empty cells.

If the next step in the planned path becomes blocked:

The algorithm automatically replans from the agent’s current position.

The agent continues toward the goal using the new path.

This simulates a partially observable and dynamic environment.

Environment Characteristics (AI Perspective)

From an AI classification standpoint, this environment is:

• Partially Observable
• Dynamic
• Stochastic (when dynamic mode is enabled)
• Discrete (grid-based states)
• Single-Agent

Project Structure

main.py
Handles UI, input, dynamic logic, and movement.

algorithms.py
Contains implementations of DFS, BFS, UCS, Greedy, and A* search.

node.py
Defines the Node (grid cell) class and visualization behavior.

requirements.txt
Lists required Python packages.

Educational Purpose

This project is designed to demonstrate:

Tree vs Graph Search

Uninformed vs Informed Search

Heuristic-based search (A*)

Real-time replanning

Dynamic environments in AI

It is suitable for AI coursework and search algorithm demonstrations.

Author : Anas MM - (24F-0576)
Email : f240576@cfd.nu.edu.pk

Course Instructor : Assistant Professor Dr. Ali Haider Khan 
Email :  ali.haider@nu.edu.pk


Developed for AI Course Project – Pathfinding and Search Strategies.
