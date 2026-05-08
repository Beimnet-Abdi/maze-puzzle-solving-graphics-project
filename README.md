# Maze Generator and Solver

This project is build to generate maze and then solves it using Python, Pygame, and OpenGL.

Stack-based Depth First Search (DFS) algorithm is used to create the maze. A virtual “mouse” moves through the grid, randomly choosing unvisited neighbors, breaking walls, and backtracking with a stack whenever it reaches a dead end. This continues until the entire maze is generated.

The program then solves the maze using another DFS-based search:

- The final solution path is shown in red
- Dead ends are marked with blue dot
- Start and end points are highlighted with pink dot

As a bonus feature, the program may randomly remove one extra wall to create a cycle (loop) in the maze. The broken wall is briefly highlighted in yellow.

## Features

- Animated snake like movement maze generation
- Stack-based DFS generation and solving
- OpenGL visualization
- Dead-end highlighting
- Optional cycle creation

## Technologies

- Python
- Pygame
- PyOpenGL

## Run

python maze.py

##PERSONAL INFO
Name: Beimnet Abdi
ID: UGR/8524/16
section 1

