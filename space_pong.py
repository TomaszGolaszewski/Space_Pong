import pygame
#import os
pygame.font.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Title and icon
pygame.display.set_caption("Space pong")
ICON = pygame.image.load("ikona.png")
pygame.display.set_icon(ICON)

# HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
HEALTH_FONT = pygame.font.Font("freesansbold.ttf", 30)
# WINNER_FONT = pygame.font.SysFont('comicsans', 100)
WINNER_FONT = pygame.font.Font("freesansbold.ttf", 80)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5
SPACESHIP_WIDTH = 64
SPACESHIP_HEIGHT = 64

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load("x-wing.png")
#YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (55,40))
YELLOW_SPACESHIP = pygame.transform.rotate(YELLOW_SPACESHIP_IMAGE, 270)
RED_SPACESHIP_IMAGE = pygame.image.load("tie_fighter.png")
#os.path.join("Assets","spaceship_yellow.png")
RED_SPACESHIP = pygame.transform.rotate(RED_SPACESHIP_IMAGE, 90)

# Background
SPACE = pygame.image.load("space.png")

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # WIN.fill(WHITE)
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width()-10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: # down
        yellow.y += VEL

def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red. width < WIDTH: # right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: # down
        red.y += VEL

def bullets_movement(yellow, red, yellow_bullets, red_bullets):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(700, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    yellow_health = 10
    red_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
# Yellow shot
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
# Red shot
                if event.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
# Close
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    run = False
                    pygame.quit()

            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1

        winner_text = ""
        if red_health <= 0:
            winner_text = "Rebel alliance wins!!!"

        if yellow_health <= 0:
            winner_text = "Empire wins!!!"

        keys_pressed=pygame.key.get_pressed()
# Yellow starship movement
        yellow_movement(keys_pressed, yellow)
# Red starship movement
        red_movement(keys_pressed, red)
# Bullets Movement
        bullets_movement(yellow, red, yellow_bullets, red_bullets)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

        if winner_text != "":
            draw_winner(winner_text)
            break

    # pygame.quit()
    main() # new game

if __name__ == "__main__":
    main()