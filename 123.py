import pygame as pg
from random import random
from collections import deque
import numpy as np


def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2


start_fire = (0, 0)
queue_fire = deque([start_fire])
visited_fire = {start_fire: None}
cur_node_fire = start_fire


def fire(queue_fire, visited_fire, grid):
    for x, y in visited_fire:
        pg.draw.rect(sc, pg.Color('red'), get_rect(x, y))
        grid[x][y] = 1
    [pg.draw.rect(sc, pg.Color('grey'), get_rect(x, y)) for x, y in queue_fire]
    if queue_fire:
        cur_node_fire = queue_fire.popleft()
        next_nodes_fire = graph[cur_node_fire]
        for next_node_fire in next_nodes_fire:
            if next_node_fire not in visited_fire:
                queue_fire.append(next_node_fire)
                visited_fire[next_node_fire] = cur_node_fire

        clock.tick(20)
        pg.display.update()


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


cols, rows = 50, 30
TILE = 30

pg.init()
sc = pg.display.set_mode([1800, rows * TILE])
clock = pg.time.Clock()

grid = [[1 if random() < 0.1 else 0 for col in range(cols)] for row in range(rows)]
# dict of adjacency lists
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if not col:
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)


def is_gone(Agents, stop):
    if stop == 0:
        long = 0
        for i in Agents:
            long += i.long
        if long != 0:
            return True
    else:
        return False


class Agent:
    def __init__(self, x, y, path, goal=(1, 1), queue=deque([(1, 1)]), visited=None, long=0, list_of_goals=None):
        if list_of_goals is None:
            list_of_goals = []
        if visited is None:
            visited = {(1, 1): None}
        self.start = (x, y)
        self.path = path
        self.goal = goal
        self.list_of_goals = list_of_goals
        self.queue = queue
        self.visited = visited
        self.long = long

    def shortest_path(self):
        longs = []
        for i in self.list_of_goals:
            self.queue, self.visited = bfs(self.start, i, graph)

            self.goal = goal

            # draw path
            self.path = []
            path_head, path_segment = self.goal, self.goal
            while path_segment and path_segment in self.visited:
                self.path.append(path_segment)
                path_segment = self.visited[path_segment]
            pg.draw.rect(sc, pg.Color('magenta'), get_rect(*path_head), border_radius=TILE // 3)
            longs.append(len(self.path))
        pathh = 1000
        for i in longs:
            if i < pathh:
                pathh = i
        return pathh


# BFS settings

pause_text = pg.font.SysFont('Consolas', 32).render('', True, pg.color.Color('White'))

A1 = Agent(1, 1, [])
A2 = Agent(20, 20, [])
A3 = Agent(1, 10, [])
A4 = Agent(8, 1, [])
Agents_A = [A1, A2, A3]
for agent in Agents_A:
    agent.queue = ([agent.start])
    agent.visited = {agent.start: None}

# queue = deque([start])
# visited = {start: None}
goal = (5, 14)
goal2 = (20, 20)
goal_list = [goal, goal2]
stop = 0
running = True
RUNNING, PAUSE = 0, 1
PAUSE = 1
state = 0

Agent_amaunt = len(Agents_A)
while True:

    for e in pg.event.get():
        if e.type == pg.QUIT: exit()
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_p: state = PAUSE
            if e.key == pg.K_s: state = RUNNING
    if state == PAUSE or Agent_amaunt == 0:
        sc.blit(pause_text, (500, 500))
    else:

        pg.display.update()
        # fill screen
        sc.fill(pg.Color('black'))
        pg.draw.rect(sc, pg.Color('silver'), pg.Rect(1500, 0, rows * TILE, cols * TILE))
        agent_text = pg.font.Font(None, 20)
        agents_len = 'Кол-во людей:' + str(Agent_amaunt)
        agent_dead = 'померло: ' + str(abs(Agent_amaunt - len(Agents_A)))
        agent_texts = agent_text.render(agents_len, True, (0, 0, 0))
        agent_deads = agent_text.render(agent_dead, True, (0, 0, 0))
        sc.blit(agent_deads, (1510, 30))
        # draw grid
        if Agent_amaunt != 0:
            [[pg.draw.rect(sc, pg.Color('darkorange'), get_rect(x, y), border_radius=TILE // 5)
              for x, col in enumerate(row) if col] for y, row in enumerate(grid)]

        for agent in Agents_A:
            #       for goal in goal_list:
            finalle_goal = agent.shortest_path()
            agent.queue, agent.visited = bfs(agent.start, finalle_goal, graph)

            agent.goal = goal

        # draw path
        for Agent in Agents_A:

            Agent.path = []
            path_head, path_segment = Agent.goal, Agent.goal
            while path_segment and path_segment in Agent.visited:
                Agent.path.append(path_segment)
                # pg.draw.rect(sc, pg.Color('white'), get_rect(*path_segment), TILE, border_radius=TILE // 3)
                path_segment = Agent.visited[path_segment]
            pg.draw.rect(sc, pg.Color('magenta'), get_rect(*path_head), border_radius=TILE // 3)
        # for i in Agents_A:
        #     if len(i.path) - 1 != -1:
        #
        for Agent in Agents_A:
            Agent.long = len(Agent.path)
            print(Agent.long)

        sorted(Agents_A, key=lambda i: i.long, reverse=True)
        print(Agents_A)
        sc.blit(agent_texts, (1510, 10))

        while is_gone(Agents_A, stop):

            for Agent in Agents_A:
                for e in pg.event.get():
                    if e.type == pg.QUIT: exit()
                    if e.type == pg.KEYDOWN:
                        if e.key == pg.K_p: state = PAUSE
                        if e.key == pg.K_s: state = RUNNING
                if state == PAUSE:
                    sc.blit(pause_text, (500, 500))
                    sc.blit(agent_deads, (1510, 30))

                else:
                    if Agent.long == 0:
                        Agent_amaunt -= 1
                        if Agent_amaunt < 0:
                            Agent_amaunt = 0
                        pg.draw.rect(sc, pg.Color('silver'), pg.Rect(1500, 0, rows * TILE, cols * TILE))

                        agents_len = 'Кол-во людей:' + str(Agent_amaunt)
                        agent_texts = agent_text.render(agents_len, True, (0, 0, 0))
                        sc.blit(agent_texts, (1510, 10))
                        sc.blit(agent_deads, (1510, 30))

                        pass
                    else:
                        if Agent.long < 0:
                            Agent.long = 0
                        else:
                            Agent.long -= 1
                        fire(queue_fire, visited_fire, grid)
                        pg.draw.rect(sc, pg.Color('blue'),
                                     get_rect(Agent.path[Agent.long][0], Agent.path[Agent.long][1]),
                                     border_radius=TILE // 5)

                        if Agent.long == len(Agent.path) - 1:
                            pass
                        else:
                            pg.draw.rect(sc, pg.Color('white'),
                                         get_rect(Agent.path[Agent.long + 1][0], Agent.path[Agent.long + 1][1]))

                        pg.display.update()
                pg.display.update()
        else:
            stop = 1
            fire(queue_fire, visited_fire, grid)
            agents_len = 'Кол-во людей:' + str(Agent_amaunt)



            if Agent_amaunt < 0:
                Agent_amaunt = 0

        # if A1.long == A2.long == 0:
        #     running = False

        # pygame necessary lines
        # [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.update()
    pg.display.flip()
    clock.tick(300)
