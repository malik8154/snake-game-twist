import pygame
import random
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Twist")

# Colors
BG_COLOR = (30, 30, 60)          # Dark blue background
SNAKE_COLOR = (0, 200, 0)        # Green snake
FOOD_COLOR = (255, 0, 0)         # Red apple
GOLDEN_COLOR = (255, 215, 0)     # Golden apple
TEXT_COLOR = (255, 255, 255)     # White text

# Fonts
font = pygame.font.SysFont("arial", 24, bold=True)
big_font = pygame.font.SysFont("arial", 48, bold=True)

clock = pygame.time.Clock()

# Functions
def draw_text(text, size, color, x, y, center=False):
    font_obj = pygame.font.SysFont("arial", size, bold=True)
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def game_intro():
    name = ""
    active = False
    input_box = pygame.Rect(WIDTH/2 - 100, HEIGHT/2, 200, 40)
    
    while True:
        screen.fill(BG_COLOR)
        draw_text("Snake Twist", 50, TEXT_COLOR, WIDTH/2, HEIGHT/4, True)
        draw_text("Enter Your Name:", 30, TEXT_COLOR, WIDTH/2, HEIGHT/2 - 50, True)
        
        # Input box
        pygame.draw.rect(screen, (200, 200, 200), input_box, 2)
        txt_surface = font.render(name, True, TEXT_COLOR)
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if name.strip():
                            return name
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if len(name) < 12:
                            name += event.unicode
        
        pygame.display.flip()
        clock.tick(30)

def game_loop(player_name):
    snake = [(100, 100)]
    snake_dir = (BLOCK_SIZE, 0)
    food = (random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
            random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE)
    golden_food = None
    score = 0
    speed = 10
    golden_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dir != (0, BLOCK_SIZE):
                    snake_dir = (0, -BLOCK_SIZE)
                elif event.key == pygame.K_DOWN and snake_dir != (0, -BLOCK_SIZE):
                    snake_dir = (0, BLOCK_SIZE)
                elif event.key == pygame.K_LEFT and snake_dir != (BLOCK_SIZE, 0):
                    snake_dir = (-BLOCK_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake_dir != (-BLOCK_SIZE, 0):
                    snake_dir = (BLOCK_SIZE, 0)

        # Move snake
        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        snake.insert(0, new_head)

        # Check collisions
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in snake[1:]):
            game_over(player_name, score)
            return

        # Eat food
        if new_head == food:
            score += 1
            food = (random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                    random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE)
            # Chance to spawn golden apple
            if random.randint(1, 5) == 1:
                golden_food = (random.randrange(0, WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                               random.randrange(0, HEIGHT // BLOCK_SIZE) * BLOCK_SIZE)
                golden_timer = 50
        elif golden_food and new_head == golden_food:
            score += 5
            speed += 2
            golden_food = None
        else:
            snake.pop()

        # Golden apple timer
        if golden_food:
            golden_timer -= 1
            if golden_timer <= 0:
                golden_food = None

        # Draw everything
        screen.fill(BG_COLOR)
        draw_text(f"{player_name} | Score: {score}", 24, TEXT_COLOR, 10, 10)
        pygame.draw.rect(screen, FOOD_COLOR, (*food, BLOCK_SIZE, BLOCK_SIZE))
        if golden_food:
            pygame.draw.rect(screen, GOLDEN_COLOR, (*golden_food, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, (255, 140, 0), (*golden_food, BLOCK_SIZE, BLOCK_SIZE), 2)  # Border
        for block in snake:
            pygame.draw.rect(screen, SNAKE_COLOR, (*block, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.flip()
        clock.tick(speed)

def game_over(player_name, score):
    while True:
        screen.fill(BG_COLOR)
        draw_text("Game Over", 50, TEXT_COLOR, WIDTH/2, HEIGHT/3, True)
        draw_text(f"{player_name} - Score: {score}", 30, TEXT_COLOR, WIDTH/2, HEIGHT/2, True)
        draw_text("Press R to Restart or Q to Quit", 24, TEXT_COLOR, WIDTH/2, HEIGHT/2 + 50, True)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop(player_name)
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    while True:
        player = game_intro()
        game_loop(player)
