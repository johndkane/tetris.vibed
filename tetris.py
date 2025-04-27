import pygame, random, sys

# config
cols, rows, block = 10, 20, 30
width, height = cols * block, rows * block
shapes = [
    [['.....','.....','..00.','.00..','.....'],
     ['.....','..0..','..00.','...0.','.....']],
    [['.....','.....','.00..','..00.','.....'],
     ['.....','..0..','.00..','.0...','.....']],
    [['.....','.....','.000.','..0..','.....'],
     ['..0..','.00..','..0..','.....','.....'],
     ['..0..','.000.','.....','.....','.....'],
     ['..0..','..00.','..0..','.....','.....']],
    [['..0..','..0..','..0..','..0..','.....'],
     ['.....','0000.','.....','.....','.....']],
    [['.....','.....','.00..','.00..','.....']],
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
        if c < 0 or c >= cols or r >= rows: return False
        if r >= 0 and grid[r][c] != (0,0,0): return False
    return True

def clear_rows(grid, locked):
    rows_to_clear = [i for i in range(rows) if (0,0,0) not in grid[i]]
    if not rows_to_clear: return 0
    for r in rows_to_clear:
        for c in range(cols):
            locked.pop((r,c), None)
    rows_to_clear.sort()
    new_locked = {}
    for (r,c), color in locked.items():
        shift = sum(1 for cleared in rows_to_clear if r < cleared)
        new_locked[(r+shift, c)] = color
    locked.clear(); locked.update(new_locked)
    return len(rows_to_clear)

def draw(win, grid):
    win.fill((0,0,0))
    for r in range(rows):
        for c in range(cols):
            pygame.draw.rect(win, grid[r][c], (c*block, r*block, block, block))
    for i in range(rows+1):
        pygame.draw.line(win, (50,50,50), (0, i*block), (width, i*block))
    for j in range(cols+1):
        pygame.draw.line(win, (50,50,50), (j*block, 0), (j*block, height))
    pygame.display.update()

def run_game(win):
    locked = {}
    current = Piece(cols//2, 0, random.choice(shapes))
    next_p = Piece(cols//2, 0, random.choice(shapes))
    fall_time, speed = 0, 0.5
    clock = pygame.time.Clock()
    while True:
        grid = create_grid(locked)
        fall_time += clock.tick() / 1000
        piece_locked = False

        if fall_time > speed:
            fall_time = 0
            current.y += 1
            if not valid(current, grid):
                current.y -= 1
                piece_locked = True

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    while True:
                        current.y += 1
                        if not valid(current, grid):
                            current.y -= 1
                            piece_locked = True
                            break
                    continue
                orig = (current.x, current.y, current.rot)
                if ev.key == pygame.K_LEFT:  current.x -= 1
                elif ev.key == pygame.K_RIGHT: current.x += 1
                elif ev.key == pygame.K_UP:    current.rot += 1
                elif ev.key == pygame.K_DOWN:
                    current.y += 1
                    if not valid(current, grid):
                        current.y -= 1
                        piece_locked = True
                if not valid(current, grid):
                    current.x, current.y, current.rot = orig

        if piece_locked:
            for r,c in convert(current):
                if 0 <= r < rows and 0 <= c < cols:
                    locked[(r,c)] = current.color
            grid = create_grid(locked)
            clear_rows(grid, locked)
            current, next_p = next_p, Piece(cols//2, 0, random.choice(shapes))
            if not valid(current, grid):
                return

        for r,c in convert(current):
            if 0 <= r < rows and 0 <= c < cols:
                grid[r][c] = current.color

        draw(win, grid)

def game_over_screen(win):
    font = pygame.font.SysFont(None, 72)
    msg = font.render('GAME OVER', True, random.choice(colors))
    rect = msg.get_rect(center=(width//2, height//2 - 30))
    info = pygame.font.SysFont(None, 36).render('Press any key to restart', True, (255,255,255))
    info_rect = info.get_rect(center=(width//2, height//2 + 30))
    win.fill((0,0,0))
    win.blit(msg, rect); win.blit(info, info_rect)
    pygame.display.update()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                return

def main():
    pygame.init()
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Tetris')
    while True:
        run_game(win)
        game_over_screen(win)

if __name__ == '__main__':
    main()
