# Written by Tiago Perez

import pygame
import sys
import numpy as np
from scipy.spatial import Voronoi

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
BACKGROUND_COLOR = (34, 177, 76)  # Green field
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BALL_COLOR = (255, 255, 0)
PLAYER_RADIUS = 17
BALL_RADIUS = 10
LINE_COLOR = WHITE
LINE_WIDTH = 2
GREY_POINT_COLOR = (150, 150, 150)
GREY_POINT_RADIUS = 5

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Soccer Tactics Board')

# Font
font_size = 25
font = pygame.font.Font(None, font_size)

# Player and ball positions with numbers
players = {
    'team1': [(76, 400, 1), (375, 667, 2), (375, 133, 3), (225, 267, 4), (225, 533, 5),
              (450, 400, 6), (900, 133, 7), (675, 267, 8), (975, 400, 9), (675, 533, 10), (900, 667, 11)],
    'team2': [(1124, 400, 1), (825, 667, 2), (825, 133, 3), (900, 267, 4), (900, 533, 5),
              (750, 400, 6), (600, 133, 7), (600, 267, 8), (225, 400, 9), (600, 533, 10), (450, 600, 11)],        'ball': [(WIDTH // 3, HEIGHT // 3)]  # Store ball position as a list with one tuple
}

# Grey points (boundary points for Voronoi diagram)
grey_points = [(50, 50), (WIDTH - 50, 50), (WIDTH - 50, HEIGHT - 50), (50, HEIGHT - 50)]

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

    # Draw grey points at the corners
    for point in grey_points:
        pygame.draw.circle(screen, GREY_POINT_COLOR, point, GREY_POINT_RADIUS)

def fill_red_player_area():
    # Create a mask to represent the area around red players
    mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(mask, (0, 0, 0, 0), (0, 0, WIDTH, HEIGHT))  # Transparent background

    # Draw circles around red players to define the area
    for player in players['team2']:
        pygame.draw.circle(mask, (255, 255, 255), player[:2], PLAYER_RADIUS + 20)

    # Create a surface for the stripes
    stripes_surface = pygame.Surface((WIDTH, HEIGHT))
    stripes_surface.fill((255, 255, 255))  # White background

    # Draw horizontal stripes
    stripe_height = 5  # Adjust as needed
    for y in range(0, HEIGHT, stripe_height * 2):
        pygame.draw.rect(stripes_surface, (0, 0, 0), (0, y, WIDTH, stripe_height))

    # Apply the mask to the stripes surface
    stripes_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    # Blit the stripes onto the screen
    screen.blit(stripes_surface, (0, 0))

def draw_players():
    for player in players['team1']:
        pygame.draw.circle(screen, BLUE, player[:2], PLAYER_RADIUS)
        # Draw player number
        text = font.render(str(player[2]), True, WHITE)
        text_rect = text.get_rect(center=player[:2])
        screen.blit(text, text_rect)
    for player in players['team2']:
        pygame.draw.circle(screen, RED, player[:2], PLAYER_RADIUS)
        # Draw player number
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

# Function to compute and draw Voronoi diagram
# Modified draw_voronoi() function to color Voronoi regions based on player proximity
def draw_voronoi():
    points = [player[:2] for player in players['team1']] + [player[:2] for player in players['team2']]
    points.extend(grey_points)
    vor = Voronoi(points)

    for region_index, region in enumerate(vor.regions):
        if not -1 in region and region:  # Check if the region is finite
            polygon = [vor.vertices[i] for i in region]
            centroid = np.mean(polygon, axis=0)
            closest_player = None
            min_distance = float('inf')

            # Find the closest player to the centroid of the region
            for player in players['team1'] + players['team2']:
                distance = np.linalg.norm(np.array(player[:2]) - centroid)
                if distance < min_distance:
                    min_distance = distance
                    if player in players['team1']:
                        closest_player = 'team1'
                    else:
                        closest_player = 'team2'

            # Color the region based on the closest player
            if closest_player == 'team1':
                draw_stripes_in_region(polygon, BLUE)
            elif closest_player == 'team2':
                draw_stripes_in_region(polygon, RED)

    # Draw Voronoi diagram lines
    for simplex in vor.ridge_vertices:
        simplex = np.asarray(simplex)
        if np.all(simplex >= 0):
            pygame.draw.line(screen, (0, 0, 0), vor.vertices[simplex[0]], vor.vertices[simplex[1]], 1)

def draw_stripes_in_region(region_polygon, color):
    # Calculate bounding box of the region
    min_x = min(point[0] for point in region_polygon)
    max_x = max(point[0] for point in region_polygon)
    min_y = min(point[1] for point in region_polygon)
    max_y = max(point[1] for point in region_polygon)

    # Draw diagonal stripes within the bounding box
    stripe_width = 20
    stripe_height = 20
    x = min_x
    while x <= max_x:
        y_start = min_y
        y_end = max_y
        for point1, point2 in zip(region_polygon, region_polygon[1:] + [region_polygon[0]]):
            if (point1[0] <= x <= point2[0]) or (point2[0] <= x <= point1[0]):
                y_intersect = point1[1] + (point2[1] - point1[1]) * (x - point1[0]) / (point2[0] - point1[0])
                if min_y <= y_intersect <= max_y:
                    if point1[0] < point2[0]:
                        y_start = max(y_start, y_intersect)
                    else:
                        y_end = min(y_end, y_intersect)
        pygame.draw.line(screen, color, (x, y_start), (x + stripe_width, y_end))
        x += stripe_width

    # Draw horizontal stripes within the bounding box
    y = min_y
    while y <= max_y:
        x_start = min_x
        x_end = max_x
        for point1, point2 in zip(region_polygon, region_polygon[1:] + [region_polygon[0]]):
            if (point1[1] <= y <= point2[1]) or (point2[1] <= y <= point1[1]):
                x_intersect = point1[0] + (point2[0] - point1[0]) * (y - point1[1]) / (point2[1] - point1[1])
                if min_x <= x_intersect <= max_x:
                    if point1[1] < point2[1]:
                        x_start = max(x_start, x_intersect)
                    else:
                        x_end = min(x_end, x_intersect)
        pygame.draw.line(screen, color, (x_start, y), (x_end, y + stripe_height))
        y += stripe_height

def draw_players_in_region(region_polygon, team):
    # Draw field marks within the region
    for point in grey_points:
        if is_point_inside_polygon(point, region_polygon):
            pygame.draw.circle(screen, GREY_POINT_COLOR, point, GREY_POINT_RADIUS)
    
    # Draw players within the region
    for player in players[team]:
        if is_point_inside_polygon(player[:2], region_polygon):
            pygame.draw.circle(screen, BLUE if team == 'team1' else RED, player[:2], PLAYER_RADIUS)
            # Draw player number
            text = font.render(str(player[2]), True, WHITE)
            text_rect = text.get_rect(center=player[:2])
            screen.blit(text, text_rect)

def is_point_inside_polygon(point, polygon):
    # Implementation of ray casting algorithm to check if a point is inside a polygon
    x, y = point
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# Main loop
running = True
while running:
    draw_field()
    draw_players()
    draw_voronoi()  # Draw Voronoi diagram
    
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
