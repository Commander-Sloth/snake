import pygame, random, sys
from pygame.locals import *
# Made on  2/24/2020

#Initialize all imported pygame modules.
pygame.init()

#Define game variables.
WIN_WIDTH = 360
WIN_HEIGHT = 360
backgroudColour = (0,0,0)

timeElapsed = 0
clock = pygame.time.Clock()

cursorEvent = pygame.event.poll()

gameOver = False

gameArray = []
for rows in range(9):
	gameArray.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

snakePath = []
score = 0

#Set up the Pygame window.
gameDisplay = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Snake')

gameDisplay.fill(backgroudColour)

# Reusable function to return desired text object, which can be displayed.
def drawText(labelText, xPos, yPos):
	font = pygame.font.Font('freesansbold.ttf', 16)
	text = font.render(labelText, True, (255, 255, 255))
	textRect = text.get_rect()
	#textRect.center = (xPos // 2, yPos // 2)
	textRect.center = (xPos, yPos)
	return gameDisplay.blit(text, textRect)


def placeFood():
	global gameArray
	# Erase the other piece of food
	for r in range(9):
		for c in range(9):
			if gameArray[r][c] == 2:
				gameArray[r][c] = 0

	randomRow = random.randint(0,8)
	randomCol = random.randint(0,8)
	cell = [randomRow, randomCol]

	for value in range(len(snakePath)):
		if cell != snakePath[value]:
			gameArray[randomRow][randomCol] = 2


class snakeBody:
	def __init__(self):
		self.x = 4
		self.y = 4
		directions = ["Up", "Down", "Left", "Right"]
		self.direction = random.choice(directions)

	def updatePosition(self):
		global score


		if len(snakePath) > 0 and len(snakePath) > score:
			snakePath.pop(0)
		snakePath.append([self.y, self.x])

		if self.direction == "Down":
			self.y = self.y + 1
		elif self.direction == "Up":
			self.y = self.y - 1
		if self.direction == "Right":
			self.x = self.x + 1
		if self.direction == "Left":
			self.x = self.x - 1

		# Keep the snake inside of the screen.
		if self.y > 8:
			self.y = 0
		elif self.y < 0:
			self.y = 8
		if self.x > 8:
			self.x = 0
		elif self.x < 0:
			self.x = 8


	def testForSomethingAhead(self):
		global gameOver
		global score
		
		if gameArray[self.y][self.x] == 2:
			score+=1
			placeFood()


		for i in range(len(snakePath)):
			if snakePath[i][0] == self.y and snakePath[i][1] == self.x:
				gameOver = True


	def process(self):
		
		self.updatePosition()
		self.testForSomethingAhead()
		

SNAKE = snakeBody()
placeFood()

def startGame():
	global SNAKE, score, gameOver, snakePath, gameArray
	
	gameArray = []
	for rows in range(9):
		gameArray.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

	snakePath = []
	score = 0
	SNAKE = snakeBody()
	placeFood()
	gameOver = False

	# Now that the variables area reset, make sure to run the game again using them, or else the program will end.
	gameLoop()


def drawGame():
	global score

	for row in range(9):
		for col in range(9):
			#Display the food.
			if gameArray[row][col] == 2:
				pygame.draw.rect(gameDisplay, (0, 250, 0), (col*40, row*40, 40, 40))		

	SNAKE.process()

	# For some reason the array of body pieces bugs out if  I draw the rect based on self.type in the object.
	for elem in range(len(snakePath)):
		pygame.draw.rect(gameDisplay, (255, 255, 255), (snakePath[elem][1]*40, snakePath[elem][0]*40, 40, 40))

	# Display the score.
	#drawText(str(score), 340, 340)

	# Check the grid to make sure food is available.	
	if not any(2 in sublist for sublist in gameArray):
		placeFood()


# Main loop to update and draw the game in gameDisplay.
def gameLoop():
	global gameOver
	timeTracker = 0

	while not gameOver:
		timeTracker += 1

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if  event.key == pygame.K_q:
					pygame.quit()
				elif  event.key == pygame.K_UP:
					if SNAKE.direction != "Down":
						SNAKE.direction = "Up"
				elif  event.key == pygame.K_DOWN:
					if SNAKE.direction != "Up":
						SNAKE.direction = "Down"
				elif  event.key == pygame.K_RIGHT:
					if SNAKE.direction != "Left":
						SNAKE.direction = "Right"
				elif  event.key == pygame.K_LEFT:
					if SNAKE.direction != "Right":
						SNAKE.direction = "Left"

		# Do not update the images every single frame, however, key events are detected every frame.
		if timeTracker % 10 == 0:
			gameDisplay.fill(backgroudColour)
			drawGame()

		pygame.display.flip()	
		clock.tick(60)

	#Stop processing coverField, wait for user to restart the game.
	while gameOver: 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYUP:
				if  event.key == pygame.K_SPACE:
					startGame()
			
		gameDisplay.fill(backgroudColour)

		for elem in range(len(snakePath)):
			pygame.draw.rect(gameDisplay, (255,69,0), (snakePath[elem][1]*40, snakePath[elem][0]*40, 40, 40))

		#drawGame()
		drawText("Press space to restart.", 175, 175)
		drawText("Score: " + str(score), 175, 210)

		pygame.display.flip()

		clock.tick(60)

gameLoop()