const GRID_SIZE = 10;
const MINE_COUNT = 10;

class Cell {
    constructor(row, col) {
        this.row = row;
        this.col = col;
        this.mine = false;
        this.adjacentMines = 0;
        this.revealed = false;
    }
}

function generateMines(grid, mineCount) {
    let minesPlaced = 0;
    while (minesPlaced < mineCount) {
        const row = Math.floor(Math.random() * GRID_SIZE);
        const col = Math.floor(Math.random() * GRID_SIZE);
        const cell = grid[row][col];
        if (!cell.mine) {
            cell.mine = true;
            minesPlaced++;
        }
    }
}

function countAdjacentMines(grid, row, col) {
    let count = 0;
    for (let r = -1; r <= 1; r++) {
        for (let c = -1; c <= 1; c++) {
            const newRow = row + r;
            const newCol = col + c;
            if (newRow >= 0 && newRow < GRID_SIZE && newCol >= 0 && newCol < GRID_SIZE) {
                const cell = grid[newRow][newCol];
                if (cell.mine) {
                    count++;
                }
            }
        }
    }
    return count;
}

function floodFill(grid, row, col) {
    if (row < 0 || row >= GRID_SIZE || col < 0 || col >= GRID_SIZE) return;

    const cell = grid[row][col];
    if (cell.revealed || cell.mine) return;

    cell.revealed = true;
    cell.element.textContent = cell.adjacentMines || "";
    cell.element.style.backgroundColor = "#ddd";

    if (cell.adjacentMines === 0) {
        for (let r = -1; r
