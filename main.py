import pygame
from enum import Enum
from qiskit import *
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

white_pawn = pygame.image.load("white-pawn.png")
white_knight = pygame.image.load("white-knight.png")
black_pawn = pygame.image.load("black-pawn.png")
black_knight = pygame.image.load("black-knight.png")


class CellType(Enum):
    Empty = 0
    WPawn = 1
    WKnight = 2
    BPawn = 3
    BKnight = 4


class GameCell(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, cell_type: CellType):
        super().__init__()
        self.cell_type = cell_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surf = pygame.Surface((width, height))
        self.surf.fill((118, 150, 86), (1, 1, width - 2, height - 2))
        self.rect = self.surf.get_rect(center=(x + width / 2, y + height / 2))


class OverlayCell(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surf = pygame.Surface((width, height))
        self.surf.fill((0, 100, 220), (1, 1, width - 2, height - 2))
        self.surf.set_alpha(128)
        self.rect = self.surf.get_rect(center=(x + width / 2, y + height / 2))


grid = [[], [], [], [], []]
for i in range(5):
    for j in range(5):
        # sprites.add(GameCell(i * 60 + 50, j * 60 + 50, 60, 60))
        grid[i].append(GameCell(i * 60 + 50, j * 60 + 50, 60, 60, CellType.Empty))

WPawns = [grid[1][0], grid[2][0], grid[3][0], grid[0][1], grid[4][1]]
WKnights = [grid[0][0], grid[4][0]]
BPawns = [grid[1][4], grid[2][4], grid[3][4], grid[0][3], grid[4][3]]
BKnights = [grid[0][4], grid[4][4]]
for pawn in WPawns:
    pawn.cell_type = CellType.WPawn
for knight in WKnights:
    knight.cell_type = CellType.WKnight
for pawn in BPawns:
    pawn.cell_type = CellType.BPawn
for knight in BKnights:
    knight.cell_type = CellType.BKnight


def convert_to_grid(x, y):
    return x // 60, y // 60


def get_moves(cell: GameCell):
    Returns = []
    if cell.cell_type == CellType.WPawn:
        cellX = convert_to_grid(cell.x, cell.y)[0]
        cellY = convert_to_grid(cell.x, cell.y)[1]
        startingPlace = False
        if cellY == 0:
            startingPlace = True
        elif cellY == 1:
            if cellX == 0 or cellX == 4:
                startingPlace = True

        if cellY + 1 < 5:
            if startingPlace:
                if grid[cellX][cellY + 1].cell_type == CellType.Empty and grid[cellX][cellY + 2].cell_type == CellType.Empty:
                    Returns.append(grid[cellX][cellY + 1])
                    Returns.append(grid[cellX][cellY + 2])
                elif grid[cellX][cellY + 1].cell_type == CellType.Empty:
                    Returns.append(grid[cellX][cellY + 1])
            else:
                if grid[cellX][cellY + 1].cell_type == CellType.Empty:
                    Returns.append(grid[cellX][cellY + 1])

            # check if there is an enemy piece to the top left or top right
            if cellX - 1 >= 0:
                if grid[cellX - 1][cellY + 1].cell_type == CellType.BPawn or grid[cellX - 1][cellY + 1].cell_type == CellType.BKnight:
                    Returns.append(grid[cellX - 1][cellY + 1])
            if cellX + 1 < 5:
                if grid[cellX + 1][cellY + 1].cell_type == CellType.BPawn or grid[cellX + 1][cellY + 1].cell_type == CellType.BKnight:
                    Returns.append(grid[cellX + 1][cellY + 1])

    elif cell.cell_type == CellType.WKnight:
        cellX = convert_to_grid(cell.x, cell.y)[0]
        cellY = convert_to_grid(cell.x, cell.y)[1]
        if cellY + 2 < 5:
            if cellX - 1 >= 0:
                if grid[cellX - 1][cellY + 2].cell_type == CellType.Empty or \
                        grid[cellX - 1][cellY + 2].cell_type == CellType.BPawn or \
                        grid[cellX - 1][cellY + 2].cell_type == CellType.BKnight:
                    Returns.append(grid[cellX - 1][cellY + 2])
            if cellX + 1 < 5:
                if grid[cellX + 1][cellY + 2].cell_type == CellType.Empty or \
                        grid[cellX + 1][cellY + 2].cell_type == CellType.BPawn or \
                        grid[cellX + 1][cellY + 2].cell_type == CellType.BKnight:
                    Returns.append(grid[cellX + 1][cellY + 2])
        if cellY - 2 >= 0:
            if cellX - 1 >= 0:
                if grid[cellX - 1][cellY - 2].cell_type == CellType.Empty or \
                        grid[cellX - 1][cellY - 2].cell_type == CellType.BPawn or \
                        grid[cellX - 1][cellY - 2].cell_type == CellType.BKnight:
                    Returns.append(grid[cellX - 1][cellY - 2])
            if cellX + 1 < 5:
                if grid[cellX + 1][cellY - 2].cell_type == CellType.Empty or \
                        grid[cellX + 1][cellY - 2].cell_type == CellType.BPawn or \
                        grid[cellX + 1][cellY - 2].cell_type == CellType.BKnight:
                    Returns.append(grid[cellX + 1][cellY - 2])
        if cellX + 2 < 5:
            if cellY - 1 >= 0:
                if grid[cellX + 2][cellY - 1].cell_type == CellType.Empty or \
                        grid[cellX + 2][cellY - 1].cell_type == CellType.BPawn or \
                        grid[cellX + 2][cellY - 1].cell_type == CellType.BKnight:
                    Returns.append(grid[cellX + 2][cellY - 1])
            if cellY + 1 < 5:
                if grid[cellX + 2][cellY + 1].cell_type == CellType.Empty or \
                        grid[cellX + 2][cellY + 1].cell_type == CellType.BPawn or \
                        grid[cellX + 2][cellY + 1].cell_type == CellType.BKnight:
                    Returns.append(grid[cellX + 2][cellY + 1])
        if cellX - 2 >= 0:
            if cellY - 1 >= 0:
                if grid[cellX - 2][cellY - 1].cell_type == CellType.Empty or \
                        grid[cellX - 2][cellY - 1].cell_type == CellType.BPawn or \
                        grid[cellX - 2][cellY - 1].cell_type == CellType.BKnight:
                    Returns.append(grid[cellX - 2][cellY - 1])
            if cellY + 1 < 5:
                if grid[cellX - 2][cellY + 1].cell_type == CellType.Empty or \
                        grid[cellX - 2][cellY + 1].cell_type == CellType.BPawn or \
                        grid[cellX - 2][cellY + 1].cell_type == CellType.BKnight:
                    Returns.append(grid[cellX - 2][cellY + 1])

    elif cell.cell_type == CellType.BPawn:
        cellX = convert_to_grid(cell.x, cell.y)[0]
        cellY = convert_to_grid(cell.x, cell.y)[1]
        startingPlace = False
        if cellY == 4:
            startingPlace = True
        elif cellY == 3:
            if cellX == 0 or cellX == 4:
                startingPlace = True

        if cellY - 1 >= 0:
            if startingPlace:
                if grid[cellX][cellY - 1].cell_type == CellType.Empty and grid[cellX][cellY - 2].cell_type == CellType.Empty:
                    Returns.append(grid[cellX][cellY - 1])
                    Returns.append(grid[cellX][cellY - 2])
                elif grid[cellX][cellY - 1].cell_type == CellType.Empty:
                    Returns.append(grid[cellX][cellY - 1])
            else:
                if grid[cellX][cellY - 1].cell_type == CellType.Empty:
                    Returns.append(grid[cellX][cellY - 1])

            # check if there is an enemy piece to the bottom left or bottom right
            if cellX - 1 >= 0:
                if grid[cellX - 1][cellY - 1].cell_type == CellType.WPawn or grid[cellX - 1][cellY - 1].cell_type == CellType.WKnight:
                    Returns.append(grid[cellX - 1][cellY - 1])
            if cellX + 1 < 5:
                if grid[cellX + 1][cellY - 1].cell_type == CellType.WPawn or grid[cellX + 1][cellY - 1].cell_type == CellType.WKnight:
                    Returns.append(grid[cellX + 1][cellY - 1])

    elif cell.cell_type == CellType.BKnight:
        cellX = convert_to_grid(cell.x, cell.y)[0]
        cellY = convert_to_grid(cell.x, cell.y)[1]

        if cellX - 1 >= 0:
            if cellY + 2 < 5:
                if grid[cellX - 1][cellY + 2].cell_type == CellType.Empty or \
                        grid[cellX - 1][cellY + 2].cell_type == CellType.WPawn or \
                        grid[cellX - 1][cellY + 2].cell_type == CellType.WKnight:
                    Returns.append(grid[cellX - 1][cellY + 2])
            if cellY - 2 >= 0:
                if grid[cellX - 1][cellY - 2].cell_type == CellType.Empty or \
                        grid[cellX - 1][cellY - 2].cell_type == CellType.WPawn or \
                        grid[cellX - 1][cellY - 2].cell_type == CellType.WKnight:
                    Returns.append(grid[cellX - 1][cellY - 2])
        if cellX + 1 < 5:
            if cellY - 2 >= 0:
                if grid[cellX + 1][cellY - 2].cell_type == CellType.Empty or \
                        grid[cellX + 1][cellY - 2].cell_type == CellType.WPawn or \
                        grid[cellX + 1][cellY - 2].cell_type == CellType.WKnight:
                    Returns.append(grid[cellX + 1][cellY - 2])
            if cellY + 2 < 5:
                if grid[cellX + 1][cellY + 2].cell_type == CellType.Empty or \
                        grid[cellX + 1][cellY + 2].cell_type == CellType.WPawn or \
                        grid[cellX + 1][cellY + 2].cell_type == CellType.WKnight:
                    Returns.append(grid[cellX + 1][cellY + 2])
        if cellX + 2 < 5:
            if cellY - 1 >= 0:
                if grid[cellX + 2][cellY - 1].cell_type == CellType.Empty or \
                        grid[cellX + 2][cellY - 1].cell_type == CellType.WPawn or \
                        grid[cellX + 2][cellY - 1].cell_type == CellType.WKnight:
                    Returns.append(grid[cellX + 2][cellY - 1])
            if cellY + 1 < 5:
                if grid[cellX + 2][cellY + 1].cell_type == CellType.Empty or \
                        grid[cellX + 2][cellY + 1].cell_type == CellType.WPawn or \
                        grid[cellX + 2][cellY + 1].cell_type == CellType.WKnight:
                    Returns.append(grid[cellX + 2][cellY + 1])
        if cellX - 2 >= 0:
            if cellY - 1 >= 0:
                if grid[cellX - 2][cellY - 1].cell_type == CellType.Empty or \
                        grid[cellX - 2][cellY - 1].cell_type == CellType.WPawn or \
                        grid[cellX - 2][cellY - 1].cell_type == CellType.WKnight:
                    Returns.append(grid[cellX - 2][cellY - 1])
            if cellY + 1 < 5:
                if grid[cellX - 2][cellY + 1].cell_type == CellType.Empty or \
                        grid[cellX - 2][cellY + 1].cell_type == CellType.WPawn or \
                        grid[cellX - 2][cellY + 1].cell_type == CellType.WKnight:
                    Returns.append(grid[cellX - 2][cellY + 1])

    return Returns


def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Quantum Apocalypse")
    running = True
    waitingForClick = False
    selectedCell = None
    possible_moves = []

    circuit = QuantumCircuit(2, 2)

    circuit.h(0)
    circuit.cs(0, 1)
    circuit.measure([0, 1], [0, 1])

    circuit.draw(output='mpl')

    simulator = AerSimulator()
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1001)
    result = job.result()
    counts = result.get_counts(circuit)
    print("\nTotal count for 00 and 11 are:", counts)

    screen.fill((255, 255, 255))

    for entity in grid:
        for cell in entity:
            screen.blit(cell.surf, cell.rect)

    clock = pygame.time.Clock()

    while running:
        clock.tick(30)
        pygame.display.update()

        for entity in grid:
            for cell in entity:
                if cell.cell_type == CellType.WPawn:
                    cell.surf.blit(white_pawn, (6, 6))
                elif cell.cell_type == CellType.WKnight:
                    cell.surf.blit(white_knight, (6, 6))
                elif cell.cell_type == CellType.BPawn:
                    cell.surf.blit(black_pawn, (6, 6))
                elif cell.cell_type == CellType.BKnight:
                    cell.surf.blit(black_knight, (6, 6))
                elif cell.cell_type == CellType.Empty:
                    cell.surf.fill((118, 150, 86), (1, 1, 58, 58))
                screen.blit(cell.surf, cell.rect)

        if waitingForClick:
            for move in possible_moves:
                overlay = OverlayCell(move.x, move.y, 60, 60)
                screen.blit(overlay.surf, overlay.rect)
            selectedOverlay = OverlayCell(selectedCell.x, selectedCell.y, 60, 60)
            selectedOverlay.surf.fill((0, 255, 0), (1, 1, 58, 58))
            screen.blit(selectedOverlay.surf, selectedOverlay.rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                for entity in grid:
                    for cell in entity:
                        if cell.rect.collidepoint(event.pos):
                            if waitingForClick:
                                if cell == selectedCell:
                                    waitingForClick = False
                                    pygame.display.update()
                                    break
                                if cell in possible_moves:
                                    cell.surf.fill((118, 150, 86), (1, 1, 58, 58))
                                    cell.cell_type = selectedCell.cell_type
                                    selectedCell.cell_type = CellType.Empty
                                    waitingForClick = False
                                    pygame.display.update()
                                    break
                            if event.button == 3:  # right click; entanglement function
                                if cell.cell_type != CellType.Empty:
                                    cell.surf.fill((200, 200, 0), (1, 1, 58, 58))
                                    possible_moves = get_moves(cell)
                                    if possible_moves is not None:
                                        selectedCell = cell
                                        waitingForClick = True
                                        pygame.display.update()
                            else:
                                if cell.cell_type != CellType.Empty:
                                    possible_moves = get_moves(cell)
                                    if possible_moves is not None:
                                        selectedCell = cell
                                        waitingForClick = True
                                        pygame.display.update()
                                    break


if __name__ == "__main__":
    # call the main function
    main()
