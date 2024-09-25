import pygame
import sys
import random

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# Pygame Setup
pygame.init()
screen_width = 1020
screen_height = 512
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Colors
bg_color = (135, 206, 235)
floor_color = (225, 215, 188)

# Fonts
font = pygame.font.Font('freesansbold.ttf', 50)

# Background
bg_surface = pygame.Surface((screen_width, screen_height))
bg_surface.fill(bg_color)

# Floor
floor_surface = pygame.Surface((screen_width, 112))
floor_surface.fill(floor_color)
floor_x_pos = 0

# Bird
bird_surface = pygame.Surface((20, 20))
bird_surface.fill((255, 255, 255))
bird_rect = bird_surface.get_rect(center=(100, 256))

# Pipes
pipe_surface = pygame.Surface((50, 600))
pipe_surface.fill((50, 205, 50))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 800)  # Reduced time to spawn pipes
pipe_height = [200, 300, 400]

def create_pipe():
    random_pipe = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(300, random_pipe))
    top_pipe = pipe_surface.get_rect(midbottom=(300, random_pipe - 150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_surface, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 400:
        return False

    return True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 256)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            bottom_pipe, top_pipe = create_pipe()
            pipe_list.append(bottom_pipe)
            pipe_list.append(top_pipe)

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score
        score += 0.01
        score_display = font.render(str(int(score)), True, (255, 255, 255))
        screen.blit(score_display, (144, 50))

        # Remove off-screen pipes
        if pipe_list:
            if pipe_list[0].right < 0:
                pipe_list.pop(0)
                pipe_list.pop(0)

    if game_active == False:
        game_over_display = font.render('Game Over', True, (255, 255, 255))
        screen.blit(game_over_display, (75, 100))
        score_display = font.render(f'Score: {int(score)}', True, (255, 255, 255))
        screen.blit(score_display, (100, 150))
        if score > high_score:
            high_score = score
        high_score_display = font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        screen.blit(high_score_display, (60, 200))

    # Floor
    floor_x_pos -= 1
    screen.blit(floor_surface, (floor_x_pos, 400))
    screen.blit(floor_surface, (floor_x_pos + screen_width, 400))
    if floor_x_pos <= -screen_width:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(60)