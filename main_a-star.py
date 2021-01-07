import pygame
import pygame_menu
from queue import PriorityQueue

#window properties - block_size should be divisible by screen_size
screen_size = 600
pygame.init()
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption('Pathfinding using A* Algorithm')

def main():
    menu = pygame_menu.Menu(height=600,
                        width=600,
                        theme=pygame_menu.themes.THEME_BLUE,
                        title='Pathfinder: A* Algorithm')
    menu.add_button('Free Run', free_run)
    menu.add_button('Google Map', gmap)
    #menu.add_button('Middle-Earth', dummy)
    menu.add_button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)

def dummy():
    pass

def free_run():
    block_size = 20
    pygame.display.flip()
    grid = make_grid(screen_size,block_size)
    running = True
    start,end = [0,0],[0,0]
    while running:
        #Various events that may happen
        for event in pygame.event.get():
            #For Exiting Window
            if event.type == pygame.QUIT:
                running = False
            # Escape key for reseting the 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start,end = [0,0],[0,0]
                    grid = make_grid(screen_size,block_size)
                    pygame.display.flip()
                    continue
            #Left Click for adding start,end and obstacles
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row,col=get_grid_pos(pos,block_size)
                if grid[start[0]][start[1]] == 'V' and grid[row][col] == 'V':
                    start = [row,col]
                    grid[row][col] = 'S'
                elif grid[end[0]][end[1]] == 'V' and grid[row][col] == 'V':
                    end=[row,col]
                    grid[row][col] = 'D'
                elif grid[start[0]][start[1]] != 'V' and grid[end[0]][end[1]] != 'V' and grid[row][col] == 'V':
                    grid[row][col] = 'B'
            #Right click for deleting cell
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row,col = get_grid_pos(pos,block_size)
                grid[row][col] = 'V'
            #Space Bar for Starting the Path finding
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    a_star(grid,start,end)
        draw(screen,grid,screen_size,block_size)
        pygame.display.update()

#Making square grids of equal sizes
def make_grid(screen_size, block_size):
    grid = []
    row = screen_size // block_size
    for i in range(row):
        grid.append([])
        for j in range(row):
            grid[i].append('V')
    return grid

#Mapping window position to grid position
def get_grid_pos(pos, block_size):
    x,y = pos
    row = y // block_size
    col = x // block_size
    return row,col
    
BLACK = (0 , 0, 0) 
WHITE = (255, 255, 255) 
RED = (255, 0 , 0) 
GREEN = (0, 255, 0) 
YELLOW = (255 , 255, 0)
BLUE = (77, 77, 225)
LIGHT_BLUE = (200, 255, 255)
GRAY = (220, 220, 220)
PINK = (249, 28, 234)
#Drawing the matrix grid
def draw(screen, grid, screen_size, block_size):
    for i in range(0, screen_size, block_size):
        for j in range(0, screen_size, block_size):
            row = i//block_size
            col = j//block_size
            if grid[row][col] == 'S':
                pygame.draw.rect(screen, RED, pygame.Rect(j, i, block_size, block_size))
            elif grid[row][col] == 'D':
                pygame.draw.rect(screen, BLUE, pygame.Rect(j, i, block_size, block_size))
            elif grid[row][col] == 'B':
                pygame.draw.rect(screen, BLACK, pygame.Rect(j, i, block_size, block_size))
            elif grid[row][col] == 'V':
                pygame.draw.rect(screen, WHITE, pygame.Rect(j, i, block_size, block_size))
            elif grid[row][col] == 'X':
                pygame.draw.rect(screen, GREEN, pygame.Rect(j, i, block_size, block_size))
            elif grid[row][col] == 'O':
                pygame.draw.rect(screen, LIGHT_BLUE, pygame.Rect(j, i, block_size, block_size))

#A* algorithm implementation
def a_star(grid, start, end):
    possible_paths = [(0,1),(0,-1),(1,0),(-1,0),(1,-1),(1,1),(-1,-1),(-1,1)]
    row = len(grid)
    col = len(grid[0])
    x1,y1 = start
    que = PriorityQueue()
    g_value = [[float('inf') for i in range(row)] for j in range(col)]
    f_value = [[float('inf') for i in range(row)] for j in range(col)]
    f_value[x1][y1] = manhattan(start,end)
    g_value[x1][y1] = 0
    que.put((f_value[x1][y1], x1, y1))
    record = []
    visited = {}
    count = 0
    record.append((f_value[x1][y1], x1, y1))
    while not que.empty():
        count+=1
        current=que.get()
        if [current[1],current[2]] == end:
            grid[current[1]][current[2]]='D'
            draw_path(grid,visited,end)
            return True
        for i,j in possible_paths:
            if (current[1]+i >= 0 and current[1]+i < row) and (current[2]+j >= 0 and current[2]+j < col):
                x,y = current[1]+i, current[2]+j
            if grid[x][y] != 'B' and f_value[x][y] == float('inf') and  (f_value[x][y],x,y) not in record:
                g_value[x][y] = g_value[current[1]][current[2]] + 1
                f_value[x][y] = g_value[current[1]][current[2]] + manhattan((x,y),end) + 1
                grid[x][y] = 'O'
                que.put((f_value[x][y], x, y))
                record.append((f_value[x][y], x, y))
                visited[(x,y)] = (current[1],current[2])
    print("No Solution")

def manhattan(p1, end):
    x1, y1 = p1
    x2, y2 = end
    return abs(x1 - x2) + abs(y1 - y2)    

def draw_path(grid, visited, end):
    end = tuple(end)
    distance=0
    while end in visited:
        distance+=1
        x,y = end
        end = visited[end]
        if grid[x][y] == 'V' or grid[x][y] == 'O':
            grid[x][y] = 'X'
        pygame.display.update()
    print("The Distance is ",distance," units")

def gmap():
    block_size = 6
    image_loc = r"map\\gmap_pta.jpg"
    file_loc = r"map\\gmap_list.txt"
    file = open(file_loc, "r")
    grid = []
    for line in file:
        whole_line = line.strip()
        letter = whole_line.split()
        grid.append(letter)
    file.close()
    background = pygame.image.load(image_loc)
    screen.blit(background,(0,0))
    pygame.display.flip()
    running = True
    start,end = [0,0],[0,0]
    while running:
        #Various events that may happen
        for event in pygame.event.get():
            #For Exiting Window
            if event.type == pygame.QUIT:
                running = False
            # Escape key for reseting 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start,end = [0,0],[0,0]
                    grid = []
                    file = open(file_loc, "r")
                    for line in file:
                        whole_line = line.strip()
                        letter = whole_line.split()
                        grid.append(letter)
                    file.close()
                    background = pygame.image.load(image_loc)
                    screen.blit(background,(0,0))
                    pygame.display.update()
                    continue
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row,col=get_grid_pos(pos,block_size)
                if grid[row][col] == 'V' and start == [0,0]:
                    start = [row,col]
                    grid[row][col] = 'S'
                elif grid[row][col] == 'V' and end == [0,0]:
                    end=[row,col]
                    grid[row][col] = 'D'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    a_star(grid,start,end)
            draw_gmap(screen,grid,screen_size,block_size)
            pygame.display.update()

def draw_gmap(screen, grid, screen_size, block_size):
    for i in range(0, screen_size, block_size):
        for j in range(0, screen_size, block_size):
            row = i//block_size
            col = j//block_size
            if grid[row][col] == 'S':
                pygame.draw.rect(screen, PINK, pygame.Rect(j, i, block_size, block_size))
            elif grid[row][col] == 'D':
                pygame.draw.rect(screen, BLUE, pygame.Rect(j, i, block_size, block_size))
            elif grid[row][col] == 'X':
                pygame.draw.rect(screen, RED, pygame.Rect(j, i, block_size, block_size))
            elif grid[row][col] == 'O':
                pygame.draw.rect(screen, LIGHT_BLUE, pygame.Rect(j, i, block_size, block_size))
#############
main()