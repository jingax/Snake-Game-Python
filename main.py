import pygame
import random
import os

pygame.mixer.init()
# Checking if highest score file exists or not
# creating if not exist with 0 as highest
if not os.path.exists("score.txt"):
    with open("score.txt", "w") as f:
        f.write("0")

# opening highest score file
with open("score.txt", "r") as f:
    high_score = int(f.read())

pygame.init()

# Declaring colors in RGB format
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 77)

# dimension of one unit length of snake and dimension of food/apple
size = 10
# Increment value of game speed after eating food
incri_val = 2
# Height and Width of the game window

height = 400
width = 600

# game variables
gameExit = False
gameOver = False

# creating game window
gameWindow = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jinga Snakes")
pygame.display.update()
clock = pygame.time.Clock()

# font with size 50
font = pygame.font.SysFont(None, 50)
# font with size 20
font_internal = pygame.font.SysFont(None, 20)

# loading and formating background image
back_img = pygame.image.load("home.jpg")
back_img = pygame.transform.scale(back_img, (width, height)).convert_alpha()

# loading and formating snake body image
snake_img = pygame.image.load("snake.jpg")
snake_img = pygame.transform.scale(snake_img, (size, size)).convert_alpha()


# set text with font size 50
def set_text(text, x, y, color):
    score_text = font.render(f"{text}", True, color)
    gameWindow.blit(score_text, [x, y])


# set text with font size 20
def set_text_internal(text, x, y):
    score_text = font_internal.render(f"{text}", True, green)
    gameWindow.blit(score_text, [x, y])


# function to plot sanke
def plot_snake(snk_list):
    for x, y in snk_list:
        # pygame.draw.rect(gameWindow, black, [x, y, size, size])
        gameWindow.blit(snake_img, (x, y))


# GAMELOOP
def game_loop():
    global high_score
    global gameExit
    global gameOver
    snake_x = 210  # Snake position in X Direction
    snake_y = 30  # Snake position in Y Direction
    velocityX = 0  # Snake velocity in X Direction
    velocityY = 0  # Snake velocity in Y Direction
    apple_x = random.randint(0, width - size)  # Apple position in X Direction
    apple_y = random.randint(20, height - size)  # Apple position in Y Direction
    apple_x = apple_x - apple_x % 10
    apple_y = apple_y - apple_y % 10
    fps = 15  # Frame rate per sec (to increase speed of game)
    score = 0
    snk_list = []  # List to record previous positions of snake
    snk_length = 1  # Length of snake

    while not gameExit:
        if gameOver:
            with open("score.txt", "w") as f:
                f.write(str(high_score))

            set_text("Game Over!", 200, 160, red)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Exit event
                    gameExit = True

                elif event.type == pygame.KEYDOWN:  # Key pressed event
                    if event.key == pygame.K_RETURN:  # Key is Return key
                        # reintialise game variables to starting values
                        gameOver = False
                        snake_x = 210
                        snake_y = 30
                        velocityX = 0
                        velocityY = 0
                        snk_length = 1
                        apple_x = random.randint(0, width - size)
                        apple_y = random.randint(0, height - size)
                        apple_x = apple_x - apple_x % 10
                        apple_y = apple_y - apple_y % 10
                        score = 0
                        fps = 15
                        snk_list.clear()

                        # play background music
                        pygame.mixer.music.load('beliver.mp3')
                        pygame.mixer.music.play(loops=1, start=27)

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:  # Handles right movement
                        if velocityX != -10:
                            velocityX = 10
                            velocityY = 0
                    if event.key == pygame.K_LEFT:  # Handles left movement
                        if velocityX != 10:
                            velocityX = -10
                            velocityY = 0
                    if event.key == pygame.K_DOWN:  # Handles down movement
                        if velocityY != -10:
                            velocityY = 10
                            velocityX = 0
                    if event.key == pygame.K_UP:  # Handles up movement
                        if velocityY != 10:
                            velocityY = -10
                            velocityX = 0

            # updating the postion of snake according to velocity
            snake_x += velocityX
            snake_y += velocityY

            # Check if snake has eaten apple
            if snake_x == apple_x and snake_y == apple_y:
                score += 10
                apple_x = random.randint(0, width - size)
                apple_y = random.randint(0, height - size)
                apple_x = apple_x - apple_x % 10
                apple_y = apple_y - apple_y % 10
                snk_length += 1  # Increase snake Length if eaten
                fps += incri_val  # Increase game speed if eaten

                # Update High score
                if score > high_score:
                    high_score = score
            # check if snake has bitten itself
            if [snake_x, snake_y] in snk_list[:-1]:
                gameOver = True
                # play game over music
                pygame.mixer.music.load('over.mp3')
                pygame.mixer.music.play(loops=1, start=0)

            # add current position of snake to snake list
            snk_list.append([snake_x, snake_y])

            # Delete the positions farther than snake length
            if len(snk_list) > snk_length:
                del snk_list[0]

            gameWindow.blit(back_img, (0, 0))  # background image

            # check if snake has collided with the wall
            if snake_x > width or snake_x < 0 or snake_y > height or snake_y < 0:
                gameOver = True
                pygame.mixer.music.load('over.mp3')
                pygame.mixer.music.play(loops=1, start=0)

            # Print score and high score
            set_text_internal(f"Score : {score}", 10, 10)
            set_text_internal(f" High-Score : {high_score}", 100, 10)

            plot_snake(snk_list)  # plot the snake
            pygame.draw.rect(gameWindow, red, [apple_x, apple_y, size, size])  # plot the food/apple

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


def home_page():
    global gameExit
    gameExit = False
    while not gameExit:
        gameWindow.blit(back_img, (0, 0))

        set_text("Welcome to Jinga Snakes!", 90, 90, green)
        set_text("Press any Key to Play", 100, 220, green)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:  # start game on any key pressed
                pygame.mixer.music.load('beliver.mp3')
                pygame.mixer.music.play(loops=1, start=27)
                game_loop()  # call game loop/ start game
        clock.tick(30)


if __name__ == "__main__":
    home_page()  # call home page function
