# Written by Tiago Perez

import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (34, 177, 76)  # Green field
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BALL_COLOR = (255, 255, 0)
PLAYER_RADIUS = 15
BALL_RADIUS = 10
LINE_COLOR = WHITE
LINE_WIDTH = 2

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Soccer Tactics Board')

# Player and ball positions with numbers
players = {
    'team1': [(100, 100, 1), (150, 150, 2), (200, 200, 3), (250, 250, 4), (300, 300, 5),
              (350, 350, 6), (400, 400, 7), (450, 450, 8), (500, 500, 9), (550, 550, 10), (600, 100, 11)],
    'team2': [(100, 500, 1), (150, 450, 2), (200, 400, 3), (250, 350, 4), (300, 300, 5),
              (350, 250, 6), (400, 200, 7), (450, 150, 8), (500, 100, 9), (550, 50, 10), (600, 500, 11)],
    'ball': [(WIDTH // 2, HEIGHT // 2)]  # Store ball position as a list with one tuple
}

selected = None

def draw_field():
    screen.fill(BACKGROUND_COLOR)
    # Draw field edges
    pygame.draw.rect(screen, LINE_COLOR, (50, 50, WIDTH - 100, HEIGHT - 100), LINE_WIDTH)
    # Center circle
    pygame.draw.circle(screen, LINE_COLOR, (WIDTH // 2, HEIGHT // 2), 100, LINE_WIDTH)
    # Middle field line
    pygame.draw.line(screen, LINE_COLOR, (WIDTH // 2, 50), (WIDTH // 2, HEIGHT - 50), LINE_WIDTH)
    # Left goal area
    pygame.draw.rect(screen, LINE_COLOR, (50, HEIGHT // 2 - 50, 20, 100), LINE_WIDTH)
    # Right goal area
    pygame.draw.rect(screen, LINE_COLOR, (WIDTH - 70, HEIGHT // 2 - 50, 20, 100), LINE_WIDTH)

def draw_players():
    for player in players['team1']:
        pygame.draw.circle(screen, BLUE, player[:2], PLAYER_RADIUS)
        # Draw player number
        font = pygame.font.Font(None, 20)
        text = font.render(str(player[2]), True, WHITE)
        text_rect = text.get_rect(center=player[:2])
        screen.blit(text, text_rect)
    for player in players['team2']:
        pygame.draw.circle(screen, RED, player[:2], PLAYER_RADIUS)
        # Draw player number
        font = pygame.font.Font(None, 20)
        text = font.render(str(player[2]), True, WHITE)
        text_rect = text.get_rect(center=player[:2])
        screen.blit(text, text_rect)
    pygame.draw.circle(screen, BALL_COLOR, players['ball'][0], BALL_RADIUS)

def get_selected(pos):
    for team, player_list in players.items():
        for i, player in enumerate(player_list):
            if (pos[0] - player[0]) ** 2 + (pos[1] - player[1]) ** 2 <= PLAYER_RADIUS ** 2:
                return team, i
    if (pos[0] - players['ball'][0][0]) ** 2 + (pos[1] - players['ball'][0][1]) ** 2 <= BALL_RADIUS ** 2:
        return 'ball', None
    return None

# Main loop
running = True
while running:
    draw_field()
    draw_players()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            selected = get_selected(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
            selected = None
        elif event.type == pygame.MOUSEMOTION:
            if selected:
                team, index = selected
                if team == 'ball':
                    players['ball'][0] = pygame.mouse.get_pos()
                else:
                    players[team][index] = pygame.mouse.get_pos() + (players[team][index][2],)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
