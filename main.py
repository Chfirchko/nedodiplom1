import pygame
import sympy
from tabulate import tabulate
import os
from collections import deque
width = 1000
height = 800

blockSize = 25

blockWidth = width // blockSize
blockHeight = height // blockSize

print('size: ', blockWidth, blockHeight)

fps = 30
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Dredd')
clock = pygame.time.Clock()
screen.fill(white)

def get_next_nodes(x, y, grid): #x and y = ячейки
    check_next_node = lambda x, y: True if blockHeight > x >= 0 == int(grid[x][y]) and 0 <= y < blockWidth else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]


def main():
    grid = []

    if os.stat('preplanning.txt').st_size == 0:
        grid = [[0 for x in range(blockWidth)] for y in range(blockHeight)]
    else:
        with open('preplanning.txt') as f:
            for count, line in enumerate(f):
                print(count)
                grid.append(list(line.strip('')))

    for i in grid:
        for j in i:
            if j == '\n':
                i.pop(width // blockSize)
                continue
    print(grid)
    running = True

    start = (0, 0)
    goal = (0, 0)
    queue = deque([start])
    visited = {start: None}
    cur_node = start
    graph = {}
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y, grid)



    while running:
        if queue:
            cur_node = queue.popleft()
            next_nodes = graph[cur_node]
            for next_node in next_nodes:
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = cur_node

        f = open('preplanning.txt', 'w')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (blockSize)
                row = pos[1] // (blockSize)
                grid[row][column] = '1'
                print("Click ", pos, "Grid coordinates: ", row, column)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (blockSize)
                row = pos[1] // (blockSize)
                grid[row][column] = '0'
                print("Click ", pos, "Grid coordinates: ", row, column)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    pos = pygame.mouse.get_pos()
                    column = pos[0] // (blockSize)
                    row = pos[1] // (blockSize)
                    grid[row][column] = '2'
                    print("Click ", pos, "Grid coordinates: ", row, column)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    pos = pygame.mouse.get_pos()
                    column = pos[0] // (blockSize)
                    row = pos[1] // (blockSize)
                    grid[row][column] = '3'
                    print("Click ", pos, "Grid coordinates: ", row, column)

        for i in range(0, width, blockSize):
            for j in range(0, height, blockSize):
                rect = pygame.Rect(i, j, blockSize, blockSize)
                color = black
                num = 1
                if grid[j // blockSize][i // blockSize] == '1':
                    pygame.draw.rect(screen, color, rect)
                elif grid[j // blockSize][i // blockSize] == '2':
                    color = green
                    start = (j // blockSize, i // blockSize)
                    pygame.draw.rect(screen, color, rect)
                elif grid[j // blockSize][i // blockSize] == '3':
                    color = red
                    goal = (j // blockSize, i // blockSize)
                    pygame.draw.rect(screen, color, rect)
                else:
                    pygame.draw.rect(screen, color, rect, num)
        path_head, path_segment = cur_node, cur_node
        while path_segment:
            pygame.draw.rect(screen, pygame.Color('magenta'), pygame.Rect(3, 3, 6 ,6))
            path_segment = visited[path_segment]
        for count, i in enumerate(grid):
            if count == 0:
                pass
            else:
                f.write('\n')
            for j in i:
                f.write(str(j))


        clock.tick(fps)
        pygame.display.flip()

    print('start:', start, 'goal', goal)


if __name__ == "__main__":
    main()

pygame.quit()

