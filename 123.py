import pygame as pg
from random import random
from collections import deque
import numpy as np


def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2


def get_next_nodes(x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]


def get_click_mouse_pos():
    x, y = pg.mouse.get_pos()
    grid_x, grid_y = x // TILE, y // TILE
    pg.draw.rect(sc, pg.Color('red'), get_rect(grid_x, grid_y))
    click = pg.mouse.get_pressed()
    return (grid_x, grid_y) if click[0] else False


def bfs(start, goal, graph):
    queue = deque([start])
    visited = {start: None}

    while queue:
        cur_node = queue.popleft()
        if cur_node == goal:
            break

        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node
    return queue, visited


cols, rows = 35, 20
TILE = 50

pg.init()
sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()
# grid
# grid = [[1 if random() < 0.2 else 0 for col in range(cols)] for row in range(rows)]
# grid = [[0 for col in range(cols)] for row in range(rows)]
grid = [[1 if random() < 0.2 else 0 for col in range(cols)] for row in range(rows)]
# dict of adjacency lists
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if not col:
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)


class Agent:
    def __init__(self, x, y, path, goal=(1, 1), queue=deque([(1, 1)]), visited=None, long=0):
        if visited is None:
            visited = {(1, 1): None}
        self.start = (x, y)
        self.path = path
        self.goal = goal
        self.queue = queue
        self.visited = visited
        self.long = long


# BFS settings     visited = {(1, 1): None}


A1 = Agent(1, 1, [])
A2 = Agent(8, 19, [])
Agents_A = (A1, A2)
for agent in Agents_A:
    agent.queue = ([agent.start])
    agent.visited = {agent.start: None}

# queue = deque([start])
# visited = {start: None}
goal = (25, 10)
running = True
while running:
    pg.display.update()
    # fill screen
    sc.fill(pg.Color('black'))
    # draw grid
    [[pg.draw.rect(sc, pg.Color('darkorange'), get_rect(x, y), border_radius=TILE // 5)
      for x, col in enumerate(row) if col] for y, row in enumerate(grid)]
    # bfs, get path to mouse click
    # mouse_pos = get_click_mouse_pos()
    # if mouse_pos and not grid[mouse_pos[1]][mouse_pos[0]]:
    #     for agent in Agents_A:
    #         agent.queue, agent.visited = bfs(agent.start, mouse_pos, graph)
    #         agent.goal = mouse_pos

    for agent in Agents_A:
        agent.queue, agent.visited = bfs(agent.start, goal, graph)
        agent.goal = goal

    # draw path
    for Agent in Agents_A:
        Agent.path = []
        path_head, path_segment = Agent.goal, Agent.goal
        while path_segment and path_segment in Agent.visited:
            Agent.path.append(path_segment)
            pg.draw.rect(sc, pg.Color('white'), get_rect(*path_segment), TILE, border_radius=TILE // 3)
            path_segment = Agent.visited[path_segment]
        pg.draw.rect(sc, pg.Color('magenta'), get_rect(*path_head), border_radius=TILE // 3)
    # for i in Agents_A:
    #     if len(i.path) - 1 != -1:
    #
    for Agent in Agents_A:
        Agent.long = len(Agent.path)

    while A1.long != 0 or A2.long != 0:

        for Agent in Agents_A:
            if Agent.long == 0:
                pass
            else:
                if Agent.long < 0:
                    Agent.long = 0
                else:
                    Agent.long -= 1

                pg.draw.rect(sc, pg.Color('blue'), get_rect(Agent.path[Agent.long][0], Agent.path[Agent.long][1]),
                             border_radius=TILE // 5)
                if Agent.long == len(Agent.path) - 1:
                    pass
                else:
                    pg.draw.rect(sc, pg.Color('brown'),
                                 get_rect(Agent.path[Agent.long + 1][0], Agent.path[Agent.long + 1][1]),
                                 border_radius=TILE // 5)
                clock.tick(20)
                pg.display.update()
            pg.display.update()
    if A1.long == A2.long == 0:
        running = False

    # pygame necessary lines
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(60)
