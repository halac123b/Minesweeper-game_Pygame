import pygame
import random
import queue
import time

pygame.init()

WIDTH, HEIGHT = 500, 600
BG_COLOR = "white"

# Grid of game
ROWS, COLS = 15, 15
MINES = 15
SIZE = WIDTH / ROWS	# Size mỗi cell

FONT = pygame.font.SysFont("comicsans", 15)
LOST_FONT = pygame.font.SysFont("comicsans", 40)
TIME_FONT = pygame.font.SysFont("comicsans", 30)
# Vì 1 cell có thể có value lên đến 8 (8 neighbor) nên cần tối đa 8 số
NUM_COLOR = {1: "black", 2: "green", 3: "red", 4: "orange", 5: "yellow", 6: "purple", 7: "blue", 8: "pink"}
RECT_COLOR = (200, 200, 200)
CLICKED_RECT_COLOR = (140, 140, 140)
FLAG_RECT_COLOR = "green"
MINE_COLOR = "red"

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
	if row < rows - 1:	# DOWN
		neighbors.append((row + 1, col))
	if col > 0: # LEFT
		neighbors.append((row, col - 1))
	if col < cols - 1:
		neighbors.append((row, col + 1))

	if row > 0 and col > 0:	# Top left
		neighbors.append((row - 1, col - 1))
	if row < rows - 1 and col < cols - 1:	# Bot right
		neighbors.append((row + 1, col + 1))
	if row < rows - 1 and col > 0:	# Top right
		neighbors.append((row + 1, col - 1))
	if row > 0 and col < cols - 1:	# Bot left
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

	for mine in minePosition:
		neighbors = GetNeighbors(*mine, rows, cols)
		# Những ô nằm kề 1 quả bom sẽ cộng giá trị thêm 1
		for row, col in neighbors:
			if field[row][col] != -1:
				field[row][col] += 1

	return field

def Draw(screen, field, coverField, currentTime):
	"""
	Vẽ grid board của field:
		Input: screen (window của game), field (matrix chứa data của grid), coverField (image đại diện cho 1 cell)
	"""
	screen.fill(BG_COLOR)

	timeText = TIME_FONT.render(f"Time Elapsed: {round(currentTime)}", 1, "black")
	screen.blit(timeText, (100, HEIGHT - timeText.get_height()))

	for i, row in enumerate(field):
		y = i * SIZE
		for j, value in enumerate(row):
			x = j * SIZE

			# Check xem cell đó đã đc lật hay chưa, nếu chưa vẽ 1 hcn che lại
			isCover = coverField[i][j] == 0
			isFlag = coverField[i][j] == -2
			isMine = value == -1

			if isFlag:
				pygame.draw.rect(screen, FLAG_RECT_COLOR, (x, y, SIZE, SIZE))
				pygame.draw.rect(screen, "black", (x, y, SIZE, SIZE), 2)
				continue
			if isCover:
				pygame.draw.rect(screen, RECT_COLOR, (x, y, SIZE, SIZE))
				pygame.draw.rect(screen, "black", (x, y, SIZE, SIZE), 2)
				continue
			else:
				pygame.draw.rect(screen, CLICKED_RECT_COLOR, (x, y, SIZE, SIZE))
				pygame.draw.rect(screen, "black", (x, y, SIZE, SIZE), 2)
				if isMine:
					pygame.draw.circle(screen, MINE_COLOR, (x + SIZE / 2, y + SIZE / 2), SIZE / 2 - 4)

			if value > 0:
				text = FONT.render(str(value), 1, NUM_COLOR[value])
				# Vẽ text ở giữa cell
				screen.blit(text, (x + (SIZE / 2 - text.get_width()), y + (SIZE / 2 - text.get_width())))

	pygame.display.update()

def GetGridPos(mousePos):
	"""
	Get tọa độ của ô đc chọn khi click chuột
		Input: mousePos(tọa độ click chuột)
	"""
	mouseX, mouseY = mousePos
	row = int(mouseY // SIZE)
	col = int(mouseX // SIZE)

	return row, col

def ExploreFromPos(row, col, coverField, field):
	"""
	Tìm kiếm và lật tất cả những ô không nằm gần bom (value = 0) chứa bom khi click chuột
		Input: (row, col): tọa độ hiện tại
			coverField, field: data từ grid
	"""
	q = queue.Queue()
	q.put((row, col))
	visited = set()

	while not q.empty():
		current = q.get()

		neighbors = GetNeighbors(*current, ROWS, COLS)
		for r, c in neighbors:
			if (r, c) in visited:
				continue

			value = field[r][c]

			# Chỉ exlpore các cell k có cờ và có value = 0
			if value == 0 and coverField[row][col] != -2:
				q.put((r, c))

			if coverField[row][col] != -2:
				coverField[r][c] = 1
			visited.add((r, c))

def DrawLost(screen, text):
	text = LOST_FONT.render(text, 1, "black")
	screen.blit(text, (WIDTH * 0.8 - text.get_width(), HEIGHT / 2 - text.get_height()))

	pygame.display.update()


def main():
	run = True
	field = CreateGrid(ROWS, COLS, MINES)
	coverField = [[0 for _ in range(COLS)] for _ in range(ROWS)]

	flagNumber = MINES	# Tổng số flag = tổng bom
	clickNumber = 0

	lost = False

	startTime = 0

	while run:
		if startTime > 0:
			currentTime = time.time() - startTime
		else:
			currentTime = 0

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				break

			if event.type == pygame.MOUSEBUTTONDOWN:
				row, col = GetGridPos(pygame.mouse.get_pos())
				if row >= ROWS or col >= COLS:
					continue

				mousePressed = pygame.mouse.get_pressed()
				if mousePressed[0] and coverField[row][col] != -2:	# Left click, không click lên flag đc
					coverField[row][col] = 1

					if field[row][col] == -1:	# Click trúng bom
						lost = True

					if clickNumber == 0 or field[row][col] == 0:
						ExploreFromPos(row, col, coverField, field)

					if clickNumber == 0:
						startTime = time.time()
					clickNumber += 1

				elif mousePressed[2]:	# Right click
					# Nếu đã có sẵn cờ, bỏ cờ đó
					if coverField[row][col] == -2:
						coverField[row][col] = 0
						flagNumber += 1
					else:
						flagNumber -= 1
						coverField[row][col] = -2

		if lost:
			Draw(screen, field, coverField, currentTime)
			DrawLost(screen, "You lost! Try again...")
			pygame.time.delay(5000)

			field = CreateGrid(ROWS, COLS, MINES)
			coverField = [[0 for _ in range(COLS)] for _ in range(ROWS)]

			flagNumber = MINES	# Tổng số flag = tổng bom
			clickNumber = 0
			lost = False

		Draw(screen, field, coverField, currentTime)

	pygame.quit()

if __name__ == "__main__":
	main()