import pygame
import random
import heapq
import time
import math

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

SCREEN_WIDTH = SCREEN_HEIGHT = 720
MAZE_SIZE = 40
pygame.init()
width = SCREEN_WIDTH / MAZE_SIZE
height = SCREEN_HEIGHT / MAZE_SIZE
diagonals_allowed = False

class MazeSquare(pygame.Rect):
    def __init__(self, row, col, is_wall=False):
        super(MazeSquare, self).__init__(col * width, row * height, width, height)
        self.is_wall = is_wall
        self.loc = (row, col)

def render_maze(maze, screen, square):
        for i in xrange(len(maze)):
            for j in xrange(len(maze)):
                    color = (0, 0, 0)
                    if maze[i][j] in costs_so_far:
                        color = (255, 0, 0)
                        pygame.draw.rect(screen, color, maze[i][j])
                    else:
                        pygame.draw.rect(screen, color, maze[i][j], 0 if maze[i][j].is_wall else 1)
        while square != None:
            pygame.draw.rect(screen, (0, 255, 0), square)
            square = came_from[square]

done = False
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((255, 255, 255))
maze = [[MazeSquare(i, j, True if random.randint(0, 100) < 29 else False) for j in xrange(MAZE_SIZE)] for i in xrange(MAZE_SIZE)]
maze[0][0].is_wall = False
maze[MAZE_SIZE - 1][MAZE_SIZE - 1].is_wall = False

#print maze
start = (0,0)
end = (MAZE_SIZE - 1, MAZE_SIZE - 1)

queue = PriorityQueue()
costs_so_far = {maze[0][0]: 0}
came_from = {}
came_from[maze[0][0]] = None
queue.put(maze[0][0], 0)
finished = False
def get_neighbors(square, maze):
    row, col = square.loc
    list_increments = [(0,1), (1,0), (-1,0), (0, -1)]
    if diagonals_allowed:
        list_increments += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    for row_inc, col_inc in list_increments:
        new_row = row + row_inc
        new_col = col + col_inc
        if new_row >= 0 and new_row < MAZE_SIZE and new_col >= 0 and new_col < MAZE_SIZE \
             and not maze[new_row][new_col].is_wall:
            yield maze[new_row][new_col]

def heuristic(loc1, loc2):
    return math.sqrt((loc2[0] - loc1[0])**2 + (loc2[1] - loc1[1])**2) if diagonals_allowed else (loc2[0] - loc1[0]) + abs(loc2[1] - loc1[1])

def step():
    current = queue.get()
    if current.loc == end:
        render_maze(maze, screen, current)
        return True
    for neighbor in get_neighbors(current, maze):
        cost = costs_so_far[current] + 1
        if neighbor not in costs_so_far or cost < costs_so_far[neighbor]:
            costs_so_far[neighbor] = cost
            came_from[neighbor] = current
            priority = cost + heuristic(neighbor.loc, end)
            queue.put(neighbor, priority)
    render_maze(maze, screen, current)

while not done:
        if not finished and not queue.empty() and step():
            finished = True
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        pygame.display.flip()
        #time.sleep(0.001)