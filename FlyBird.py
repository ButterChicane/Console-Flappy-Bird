import pygame
import sys
import random

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
pipe_speed = 3

# Pygame Setup
pygame.init()
screen_width = 1020
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font('freesansbold.ttf', 50)

# Load and scale images
bg_surface = pygame.image.load('background.png').convert()
bg_surface = pygame.transform.scale(
    bg_surface, (screen_width, screen_height))  # Scale to screen size

bird_surface = pygame.image.load('bird.png').convert_alpha()
# Resize the bird to a reasonable size
bird_surface = pygame.transform.scale(bird_surface, (50, 35))

pipe_surface = pygame.image.load('pipe.png').convert_alpha()
# Adjust the pipe's width and height
pipe_surface = pygame.transform.scale(pipe_surface, (80, 600))

# Bird setup
bird_rect = bird_surface.get_rect(center=(100, 256))

# Pipe setup
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 3000)
pipe_height = [200, 300, 400]


def create_pipe():
    random_pipe = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(1020, random_pipe))
    top_pipe = pipe_surface.get_rect(midbottom=(1020, random_pipe - 150))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_speed
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_surface, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= screen_height:  # Adjusted for no floor
        return False
    return True


def rotate_bird(bird_surface):
    """Rotate the bird surface with transparency."""
    new_bird = pygame.transform.rotozoom(bird_surface, -bird_movement * 3, 1)
    return new_bird


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 4
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 256)
                bird_movement = 0
                score = 0
                pipe_speed = 3
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    # Background
    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = rotate_bird(bird_surface)
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score and Speed Increment
        score += 0.01
        if score % 10 == 0:
            pipe_speed += 0.01
        score_display = font.render(str(int(score)), True, (255, 255, 255))
        screen.blit(score_display, (144, 50))

        # Remove off-screen pipes
        if pipe_list and pipe_list[0].right < 0:
            pipe_list.pop(0)
            pipe_list.pop(0)

    else:
        # Game over
        game_over_display = font.render('Game Over', True, (255, 255, 255))
        screen.blit(game_over_display, (75, 100))
        score_display = font.render(
            f'Score: {int(score)}', True, (255, 255, 255))
        screen.blit(score_display, (100, 150))
        if score > high_score:
            high_score = score
        high_score_display = font.render(
            f'High Score: {int(high_score)}', True, (255, 255, 255))
        screen.blit(high_score_display, (60, 200))

    pygame.display.update()
    clock.tick(60)
