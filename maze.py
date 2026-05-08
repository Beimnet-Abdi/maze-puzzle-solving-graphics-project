import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

# ---------------- CONFIG ----------------
R, C = 15, 20
CELL_SIZE = 40
WIDTH = C * CELL_SIZE
HEIGHT = R * CELL_SIZE

# ---------------- COLORS ----------------
BG_COLOR = (143/255, 178/255, 126/255)
SNAKE_TRAIL = (245/255, 232/255, 213/255)
WALL_COLOR = (133/255, 162/255, 116/255)
SOLVER_RED = (1.0, 0.4, 0.4)
SOLVER_BLUE = (0.4, 0.6, 1.0)
START_END_COLOR = (1.0, 0.635, 0.741)

# ---------------- WALL ARRAYS ----------------
# Row 0 is phantom row for bottom edge; Col 0 is phantom for left edge
northWall = [[1 for _ in range(C + 1)] for _ in range(R + 1)]
eastWall = [[1 for _ in range(C + 1)] for _ in range(R + 1)]

trail_cells = []
show_points = False
final_dead_ends = set()

# Random Start / End
start_cell = (random.randint(1, R), random.randint(1, C))
end_cell = (random.randint(1, R), random.randint(1, C))
while end_cell == start_cell:
    end_cell = (random.randint(1, R), random.randint(1, C))

# ---------------- OPENGL ----------------
def init_graphics():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glViewport(0, 0, WIDTH, HEIGHT)
    glClearColor(*BG_COLOR, 1.0)

def draw_filled_box(r, c, color):
    x, y = (c - 1) * CELL_SIZE, (r - 1) * CELL_SIZE
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + CELL_SIZE, y)
    glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
    glVertex2f(x, y + CELL_SIZE)
    glEnd()

def draw_dots(cells, color, size):
    glColor3f(*color)
    glPointSize(size)
    glBegin(GL_POINTS)
    for r, c in cells:
        glVertex2f((c - 0.5) * CELL_SIZE, (r - 0.5) * CELL_SIZE)
    glEnd()

def draw_maze(path=None, dead=None):
    glClear(GL_COLOR_BUFFER_BIT)
    for r, c in trail_cells:
        draw_filled_box(r, c, SNAKE_TRAIL)
    glColor3f(*WALL_COLOR)
    glLineWidth(3)
    glBegin(GL_LINES)
    for r in range(1, R + 1):
        for c in range(1, C + 1):
            x, y = (c - 1) * CELL_SIZE, (r - 1) * CELL_SIZE
            if northWall[r][c]:
                glVertex2f(x, y + CELL_SIZE); glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
            if eastWall[r][c]:
                glVertex2f(x + CELL_SIZE, y); glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
    for r in range(1, R + 1):
        glVertex2f(0, (r - 1) * CELL_SIZE); glVertex2f(0, r * CELL_SIZE)
    for c in range(1, C + 1):
        glVertex2f((c - 1) * CELL_SIZE, 0); glVertex2f(c * CELL_SIZE, 0)
    glEnd()
    if show_points:
        draw_dots([start_cell, end_cell], START_END_COLOR, 16)
    pygame.display.flip()
def generate():
    visited = [[False for _ in range(C + 1)] for _ in range(R + 1)]
    stack = []
    r, c = start_cell
    visited[r][c] = True
    trail_cells.append((r, c))
    count = 1
    while count < R * C:
        pygame.event.pump()
        neighbors = []
        if r < R and not visited[r + 1][c]: neighbors.append((r + 1, c, 'N'))
        if r > 1 and not visited[r - 1][c]: neighbors.append((r - 1, c, 'S'))
        if c < C and not visited[r][c + 1]: neighbors.append((r, c + 1, 'E'))
        if c > 1 and not visited[r][c - 1]: neighbors.append((r, c - 1, 'W'))
        if neighbors:
            nr, nc, direction = random.choice(neighbors)
            if direction == 'N': northWall[r][c] = 0
            elif direction == 'S': northWall[r - 1][c] = 0
            elif direction == 'E': eastWall[r][c] = 0
            elif direction == 'W': eastWall[r][c - 1] = 0
            stack.append((r, c))
            r, c = nr, nc
            visited[r][c] = True
            trail_cells.append((r, c))
            count += 1
            draw_maze()
            pygame.time.delay(30)
        elif stack:
            r, c = stack.pop()
            draw_maze()
            pygame.time.delay(15)

# Update Main:
def main():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    init_graphics()
    draw_maze()
    pygame.time.wait(500)
    generate()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.quit(); 
                return
    
if __name__ == "__main__":
    main()