import pygame
import random

pygame.init()

WIDTH, HEIGHT = 500, 600
BG_COLOR = "white"

# Grid of game
ROWS, COLS = 30, 30
MINES = 15

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")


def GetNeighbors(row, col, rows, cols):
	"""
		Get neigbor cells (8 direction)
		Input: coordinate of that cell, number of rows, cols in field
		Out: Array of neighbors' coordinate
	"""
	neighbors = []

	if row > 0:	# UP
		neighbors.append((row - 1, col))
	if row < len(rows) - 1:	# DOWN
		neighbors.append((row + 1, col))
	if col > 0: # LEFT
		neighbors.append((row, col - 1))
	if col < len(cols) - 1:
		neighbors.append((row, col + 1))

	if row > 0 and col > 0:	# Top left
		neighbors.append((row - 1, col - 1))
	if row < len(rows) - 1 and col < len(cols) - 1:	# Bot right
		neighbors.append((row + 1, col + 1))
	if row < len(rows) - 1 and col > 0:	# Top right
		neighbors.append((row + 1, col - 1))
	if row > 0 and col < len(cols) - 1:	# Bot left
		neighbors.append((row - 1, col + 1))

	return neighbors

def CreateGrid(rows, cols, mines):
	"""
		Input: number of row, col and mine in game
	"""
	# 2D Array as game grid
	field = [[0 for _ in range(cols)] for _ in range(rows)]
	# Set of mine's position (unique)
	minePosition = set()

	# Random create position of mine
	while len(minePosition) < mines:
		row = random.randrange(0, rows)
		col = random.randrange(0, cols)
		pos = row, col

		if pos in minePosition:	# Nếu vị trí đã có sẵn, continue
			continue

		minePosition.add(pos)
		field[row][col] = -1


def draw(screen):
	screen.fill(BG_COLOR)
	pygame.display.update()

def main():
	run = True

	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				break

		draw(screen)

	pygame.quit()

if __name__ == "__main__":
	main()