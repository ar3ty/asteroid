import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from filemanagement import *

pygame.init()
pygame.display.set_caption("Астероиды")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.Font(None, FONT_SIZE) 
score = 0
players = download_score()
current_user = ""


def exit():
    global current_user, players, score
    if current_user != "":
        if score > players[current_user]:
            players[current_user] = score
    print(players)
    upload_score(players)
    sys.exit()

def draw_score():
    global current_user
    if current_user == "":
        user = "Счет"
    else:
        user = current_user
    score_text = font.render(f"{user}: {score}", True, GREEN)
    screen.blit(score_text, (10, 10))

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_button(surface, color, x, y, width, height, text):
    pygame.draw.rect(surface, color, (x, y, width, height))
    draw_text(text, font, BLACK, surface, x + width // 2, y + height // 2)

def main_menu():
    global score
    while True:
        screen.fill(BLACK)
        
        # Заголовок меню
        draw_text("Астероиды", font, WHITE, screen, SCREEN_WIDTH // 2, 100)

        button_start = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_quit = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 500, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_new_player = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 300, BUTTON_WIDTH, BUTTON_HEIGHT)
        button_score = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 400, BUTTON_WIDTH, BUTTON_HEIGHT)


        draw_button(screen, WHITE, button_start.x, button_start.y, BUTTON_WIDTH, BUTTON_HEIGHT, "Начать игру")
        draw_button(screen, WHITE, button_quit.x, button_quit.y, BUTTON_WIDTH, BUTTON_HEIGHT, "Выход")
        draw_button(screen, WHITE, button_new_player.x, button_new_player.y, BUTTON_WIDTH, BUTTON_HEIGHT, "Новый игрок")
        draw_button(screen, WHITE, button_score.x, button_score.y, BUTTON_WIDTH, BUTTON_HEIGHT, "Таблица лидеров")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_start.collidepoint(mouse_pos):
                    main()
                if button_new_player.collidepoint(mouse_pos):
                    input_name()
                if button_score.collidepoint(mouse_pos):
                    leader_table()
                if button_quit.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()
        draw_score()

    
        pygame.display.flip()

def input_name():
    global score, current_user
    input_rect = pygame.Rect(SCREEN_WIDTH // 2 - 70, 334, 140, 32) 
    user_text = ""
    while True:
        screen.fill(BLACK)
        
        draw_text("Введите имя игрока:", font, WHITE, screen, SCREEN_WIDTH // 2, 250)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    players[user_text] = score
                    score = 0
                    current_user = user_text
                    return
                else: 
                    user_text += event.unicode

        pygame.draw.rect(screen, GRAY, input_rect)
        draw_text(user_text, font, WHITE, screen, SCREEN_WIDTH // 2, 350)

        pygame.display.flip()

def leader_table():
    while True:
        screen.fill(BLACK)

        button_menu = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 400, BUTTON_WIDTH, BUTTON_HEIGHT)
        draw_button(screen, WHITE, button_menu.x, button_menu.y, BUTTON_WIDTH, BUTTON_HEIGHT, "Выйти в меню")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_menu.collidepoint(mouse_pos):
                    return
                
        if len(players) != 0:
            players_set = list(players.items())
            lines = 10
            if len(players_set) < 10:
                lines = len(players_set)
            for i in range (lines):
                draw_text(f"{players_set[i][0]} --- {players_set[i][1]}", font, WHITE, screen, 200, 200 + i * 50)



        pygame.display.flip()

def main():
    global score, current_user, players, player
    score = 0
    running = True
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Asteroid.containers = (asteroids, drawable, updatable) 
    AsteroidField.containers = updatable  
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
        for object in updatable:
            object.update(dt)    

        for object in asteroids:
            if object.collision_check(player) == True:
                if current_user != "":
                    if score > players[current_user]:
                        players[current_user] = score
                return
            
            for bullet in shots:
                if object.collision_check(bullet) == True:
                    bullet.kill()
                    object.split()
                    if object.radius == ASTEROID_MAX_RADIUS: 
                        score += 1
                    elif object.radius == ASTEROID_MAX_RADIUS - ASTEROID_MIN_RADIUS:
                        score += 2
                    else:
                        score += 3
                    
        screen.fill("black")
        for object in drawable:
            object.draw(screen, dt)
        
        draw_score()

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main_menu()