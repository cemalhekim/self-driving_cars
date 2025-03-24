import pygame
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 800
ROAD_WIDTH = 200
LANE_WIDTH = ROAD_WIDTH // 2
BLOCK_SIZE = 50
CAR_WIDTH, CAR_HEIGHT = 40, 60
CAR_SPEED = 3
SWITCH_DISTANCE = 50  # 1 meter in pixels
AVOIDANCE_STEP = 10

# Colors
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
YELLOW = (255, 204, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2-Way Road with Dynamic Roadblocks")

# Buttons
reset_button = pygame.Rect(50, 20, 100, 40)
add_block_button = pygame.Rect(200, 20, 150, 40)

# Variables
blocks = []
car_x, car_y = WIDTH // 2 + LANE_WIDTH // 2 - CAR_WIDTH // 2, HEIGHT - 100
car_left_lane = WIDTH // 2 - LANE_WIDTH // 2 - CAR_WIDTH // 2
dragging_block = None
switching = False
switching_back = False
smooth_path = []

# Function to reset simulation
def reset_simulation():
    global car_x, car_y, blocks, switching, switching_back, smooth_path
    car_x, car_y = WIDTH // 2 + LANE_WIDTH // 2 - CAR_WIDTH // 2, HEIGHT - 100
    blocks.clear()
    switching = False
    switching_back = False
    smooth_path = []

# Function to add a new roadblock
def add_roadblock():
    blocks.append([WIDTH // 2 + LANE_WIDTH // 2 - BLOCK_SIZE // 2, HEIGHT // 2])

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Draw road
    pygame.draw.rect(screen, GRAY, (WIDTH // 2 - ROAD_WIDTH // 2, 0, ROAD_WIDTH, HEIGHT))
    pygame.draw.line(screen, YELLOW, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)  # Lane divider

    # Draw buttons
    pygame.draw.rect(screen, GREEN, reset_button)
    pygame.draw.rect(screen, RED, add_block_button)
    font = pygame.font.SysFont(None, 24)
    screen.blit(font.render("Reset", True, WHITE), (reset_button.x + 30, reset_button.y + 10))
    screen.blit(font.render("Add Block", True, WHITE), (add_block_button.x + 30, add_block_button.y + 10))

    # Draw roadblocks
    for block in blocks:
        pygame.draw.rect(screen, RED, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

    # Move car
    if car_y > 0:
        for block in blocks:
            block_x, block_y = block
            if abs(car_y - block_y) < SWITCH_DISTANCE:
                if not switching:
                    switching = True
                    smooth_path = [(car_x, car_y)]
                    for i in range(AVOIDANCE_STEP):
                        smooth_path.append((car_left_lane, car_y - i * (SWITCH_DISTANCE // AVOIDANCE_STEP)))
                    for i in range(AVOIDANCE_STEP):
                        smooth_path.append((car_x, car_y - SWITCH_DISTANCE - i * (SWITCH_DISTANCE // AVOIDANCE_STEP)))
                break
        else:
            switching = False
            switching_back = False

        if switching and smooth_path:
            car_x, car_y = smooth_path.pop(0)
        else:
            car_y -= CAR_SPEED

    # Draw car
    pygame.draw.rect(screen, BLUE, (car_x, car_y, CAR_WIDTH, CAR_HEIGHT))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if reset_button.collidepoint(event.pos):
                reset_simulation()
            elif add_block_button.collidepoint(event.pos):
                add_roadblock()
            else:
                for block in blocks:
                    if block[0] < event.pos[0] < block[0] + BLOCK_SIZE and block[1] < event.pos[1] < block[1] + BLOCK_SIZE:
                        dragging_block = block
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_block = None
        elif event.type == pygame.MOUSEMOTION and dragging_block:
            dragging_block[0], dragging_block[1] = event.pos

    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()
