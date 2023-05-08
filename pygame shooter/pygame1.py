import pygame
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1400, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship vs Alien")

WHITE = (255, 255, 255)
DARKBLUE = (0, 31, 61)
RED = (255, 0, 0)
PURPLE = (115, 0, 186)
ANGLE = 1

BORDER = pygame.Rect(0, HEIGHT//2, WIDTH, 10)



BULLET_HIT_SOUND = pygame.mixer.Sound (os.path.join('Assets', 'RobloxRocketExplosionSound.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound (os.path.join( 'Assets', 'SpaceLaserSound.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 75, 50

PURPLE_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

PURPLE_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_purple.png'))
PURPLE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    PURPLE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 0)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.jpg')), (WIDTH, HEIGHT))

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(os.path.join('Assets', f'frame{num}.gif'))
            img = pygame.transform.scale(img, (150, 150))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
    def update(self):
        explosion_speed = 4
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


explosion_group = pygame.sprite.Group()

def draw_window(red, purple, red_bullets, purple_bullets, red_health, purple_health):
    WIN.blit(SPACE, (0, 0))
    
    pygame.draw.rect(WIN, DARKBLUE, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    purple_health_text = HEALTH_FONT.render(
        "Health: " + str(purple_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(purple_health_text, (10, 10))

    WIN.blit(PURPLE_SPACESHIP, (purple.x, purple.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in purple_bullets:
        pygame.draw.rect(WIN, PURPLE, bullet)
    pygame.display.update()

    

def purple_handle_movement(keys_pressed, purple):
    if keys_pressed[pygame.K_a] and purple.x - VEL > 0: # LEFT
        purple.x -= VEL
    if keys_pressed[pygame.K_d] and purple.x + VEL + purple.width < WIDTH:  # RIGHT
        purple.x += VEL
    if keys_pressed[pygame.K_w] and purple.y - VEL > 0:  # UP
        purple.y -= VEL
    if keys_pressed[pygame.K_s] and purple.y + VEL + purple.height < HEIGHT - 410:  # DOWN
        purple.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > 0:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL + red.height > HEIGHT - 350:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL
explosion = Explosion

def handle_bullets(purple_bullets, red_bullets, purple, red):
    for bullet in purple_bullets:
        bullet.y += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            explosion = Explosion(bullet[0], bullet[1])
            explosion_group.add(explosion)
            purple_bullets.remove(bullet)
        elif bullet.y > WIDTH:
            purple_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.y -= BULLET_VEL
        if purple.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PURPLE_HIT))
            explosion = Explosion(bullet[0], bullet[1])
            explosion_group.add(explosion)
            red_bullets.remove(bullet)
        elif bullet.y < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text =WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(660, 750, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    purple = pygame.Rect(660, 20, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    red_bullets = []
    purple_bullets = []
    red_health = 10
    purple_health = 10
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        explosion_group.draw(SPACE)
        explosion_group.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(purple_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(purple.x - 42 + purple.width, purple.y + purple.height//2 - 2, 10, 15)
                    purple_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x - -32, red.y + red.height//2 - 2, 10, 15)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == PURPLE_HIT:
                purple_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Purple Wins!"

        if purple_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        purple_handle_movement(keys_pressed, purple)
        red_handle_movement(keys_pressed, red)

        handle_bullets(purple_bullets, red_bullets, purple, red)

        draw_window(red, purple, red_bullets, purple_bullets, red_health, purple_health)

    main()

if __name__ == "__main__":
    main()