import pygame, random

# config
cols, rows, block = 10, 20, 30
width, height = cols * block, rows * block
shapes = [
    [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']],
    [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']],
    [['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['..0..',
      '.00..',
      '..0..',
      '.....',
      '.....'],
     ['..0..',
      '.000.',
      '.....',
      '.....',
      '.....'],
     ['..0..',
      '..00.',
      '..0..',
      '.....',
      '.....']],
    [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']],
    [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']],
]
colors = [(0,255,255),(0,255,0),(255,0,0),(255,255,0),(128,0,128)]

class Piece:
    def __init__(self, x, y, shape):
        self.x, self.y, self.shape = x, y, shape
        self.color = random.choice(colors)
        self.rot = 0

def create_grid(locked):
    grid = [[(0,0,0) for _ in range(cols)] for _ in range(rows)]
    for (r,c), color in locked.items():
        grid[r][c] = color
    return grid

def convert(p):
    positions = []
    fmt = p.shape[p.rot % len(p.shape)]
    for i, line in enumerate(fmt):
        for j, c in enumerate(line):
            if c == '0':
                positions.append((p.y + i - 2, p.x + j - 2))
    return positions

def valid(p, grid):
    for r, c in convert(p):
        if c < 0 or c >= cols or r >= rows:      # side‐ or bottom‐bounds
            return False
        if r >= 0 and grid[r][c] != (0,0,0):      # only collide inside the grid
            return False
    return True

def clear_rows(grid, locked):
    cleared = 0
    for i in range(rows-1, -1, -1):
        if (0,0,0) not in grid[i]:
            cleared += 1
            for j in range(cols):
                locked.pop((i,j), None)
    if cleared:
        for (r,c) in sorted(list(locked), key=lambda x: x[0])[::-1]:
            if r < i:
                locked[(r+cleared, c)] = locked.pop((r,c))
    return cleared

def draw(win, grid):
    win.fill((0,0,0))
    for r in range(rows):
        for c in range(cols):
            pygame.draw.rect(win, grid[r][c],
                             (c*block, r*block, block, block), 0)
    for i in range(rows+1):
        pygame.draw.line(win, (50,50,50), (0, i*block), (width, i*block))
    for j in range(cols+1):
        pygame.draw.line(win, (50,50,50), (j*block, 0), (j*block, height))
    pygame.display.update()

def main():
    pygame.init()
    win = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    locked = {}
    current = Piece(cols//2, 0, random.choice(shapes))
    next_p = Piece(cols//2, 0, random.choice(shapes))
    fall_time, speed = 0, 0.5
    run = True

    while run:
        grid = create_grid(locked)
        dt = clock.tick()
        fall_time += dt / 1000
        if fall_time > speed:
            fall_time = 0
            current.y += 1
            if not valid(current, grid):
                current.y -= 1
                for r, c in convert(current):
                    if 0 <= r < rows and 0 <= c < cols:
                        locked[(r,c)] = current.color
                current, next_p = next_p, Piece(cols//2, 0, random.choice(shapes))
                clear_rows(grid, locked)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                run = False
            if ev.type == pygame.KEYDOWN:
                orig = (current.x, current.y, current.rot)
                if ev.key == pygame.K_LEFT:  current.x -= 1
                if ev.key == pygame.K_RIGHT: current.x += 1
                if ev.key == pygame.K_DOWN:  current.y += 1
                if ev.key == pygame.K_UP:    current.rot += 1
                if not valid(current, grid):
                    current.x, current.y, current.rot = orig

        for r, c in convert(current):
            if 0 <= r < rows and 0 <= c < cols:
                grid[r][c] = current.color

        draw(win, grid)

    pygame.quit()

if __name__ == '__main__':
    main()
