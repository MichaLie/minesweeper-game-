import pygame
import random

# Screen size and cell size
SCREEN_SIZE = (800, 800)
CELL_SIZE = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Grid dimensions and mine count
GRID_SIZE = 20
MINE_COUNT = 40

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Minesweeper")

# Load font
font = pygame.font.SysFont("Arial", 24)

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.revealed = False
        self.flagged = False
        self.mine = False
        self.adjacent_mines = 0

    def toggle_flag(self):
        self.flagged = not self.flagged

def generate_mines(grid, mine_count):
    mines = random.sample(range(GRID_SIZE * GRID_SIZE), mine_count)
    for mine in mines:
        row, col = divmod(mine, GRID_SIZE)
        grid[row][col].mine = True

def count_adjacent_mines(grid, row, col):
    count = 0
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                count += grid[r][c].mine
    return count

def flood_fill(grid, row, col):
    if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
        return

    cell = grid[row][col]
    if cell.revealed or cell.flagged:
        return

    cell.revealed = True

    if cell.adjacent_mines > 0:
        return

    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            flood_fill(grid, r, c)

def draw_grid():
    for row in grid:
        for cell in row:
            x, y = cell.col * CELL_SIZE, cell.row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            if cell.revealed:
                pygame.draw.rect(screen, GRAY, rect)
                if cell.mine:
                    pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE // 4)
                elif cell.adjacent_mines > 0:
                    text = font.render(str(cell.adjacent_mines), True, BLACK)
                    screen.blit(text, (x + CELL_SIZE // 3, y + CELL_SIZE // 4))
            else:
                pygame.draw.rect(screen, WHITE, rect)

            if cell.flagged:
                pygame.draw.polygon(screen, BLACK, [
                    (x + CELL_SIZE // 4,
                    y + CELL_SIZE // 4),
                    (x + CELL_SIZE // 4, y + 3 * CELL_SIZE // 4),
                    (x + 3 * CELL_SIZE // 4, y + CELL_SIZE // 2)
                ])

            pygame.draw.rect(screen, BLACK, rect, 1)

def main():
    global grid
    grid = [[Cell(row, col) for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]
    generate_mines(grid, MINE_COUNT)

    for row in grid:
        for cell in row:
            cell.adjacent_mines = count_adjacent_mines(grid, cell.row, cell.col)

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                col, row = pygame.mouse.get_pos()
                col, row = col // CELL_SIZE, row // CELL_SIZE

                cell = grid[row][col]

                if event.button == 1:  # Left click
                    if not cell.flagged:
                        if cell.mine:
                            print("Game Over!")
                            running = False
                        else:
                            flood_fill(grid, row, col)
                elif event.button == 3:  # Right click
                    cell.toggle_flag()

        draw_grid()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
                     
