import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Asteroid Dodge")

BG = pygame.transform.scale(pygame.image.load("space_bg.jpg"), (WIDTH, HEIGHT))

SPACESHIP_WIDTH = 40
SPACESHIP_HEIGHT = 60

SPACESHIP_VEL = 5

ASTEROID_WIDTH = 10
ASTEROID_HEIGHT = 20

ASTEROID_VEL = 3

SPACESHIP_IMG = pygame.transform.scale(pygame.image.load("spaceship.png"), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
ASTEROID_IMG = pygame.transform.scale(pygame.image.load("asteroid.png"), (ASTEROID_WIDTH, ASTEROID_HEIGHT))

FONT = pygame.font.SysFont("sans", 30)

def draw(spaceship, elapsed_time, asteroids):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))
    WIN.blit(SPACESHIP_IMG, (spaceship.x, spaceship.y))

    for asteroid in asteroids:
        WIN.blit(ASTEROID_IMG, (asteroid.x, asteroid.y))

    pygame.display.update()

def main():
    run = True

    spaceship = pygame.Rect(200, HEIGHT - SPACESHIP_HEIGHT, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    clock = pygame.time.Clock()

    start_time = time.time()
    elapsed_time = 0

    asteroid_add_increment = 2000
    asteroid_count = 0

    asteroids = []
    hit = False

    while run:
        asteroid_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if asteroid_count > asteroid_add_increment:
            for _ in range(3):
                start_x = random.randint(0, WIDTH - ASTEROID_WIDTH)
                start = pygame.Rect(start_x, -ASTEROID_HEIGHT, ASTEROID_WIDTH, ASTEROID_HEIGHT)
                asteroids.append(start)

            asteroid_add_increment = max(200, asteroid_add_increment - 50)
            asteroid_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and spaceship.x - SPACESHIP_VEL >= 0:
            spaceship.x -= SPACESHIP_VEL

        if keys[pygame.K_RIGHT] and spaceship.x + SPACESHIP_VEL + SPACESHIP_WIDTH <= WIDTH:
            spaceship.x += SPACESHIP_VEL

        for asteroid in asteroids[:]:
            asteroid.y += ASTEROID_VEL

            if asteroid.y > HEIGHT:
                asteroids.remove(asteroid)
            elif asteroid.y + asteroid.height > spaceship.y and asteroid.colliderect(spaceship):
                asteroids.remove(asteroid)
                hit = True
                break        

        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))   
            pygame.display.update()
            pygame.time.delay(4000)
            break 

        draw(spaceship, elapsed_time, asteroids)

    pygame.quit()

if __name__ == "__main__":
    main()