import pygame
from sys import exit

game_phase = 1
background_width = 1062
background_height = 708
split_height = 8


class Player(pygame.sprite.Sprite):
    def __init__(self, step):
        super().__init__()
        self.alive = True
        self.width = 80
        self.height = 74
        self.image = pygame.transform.scale(pygame.image.load('images/FighterBase.png').convert_alpha(), (self.width, self.height)) # player skin - (120, 110)
        self.rect = self.image.get_rect(midbottom=(background_width / 2, background_height - 100))
        self.step = step  # controls the speed and direction
        self.move_x = 0
        self.move_y = 0
        self.ammo = 5
        self.regen_ammo = 1  # regen every regen_ammo seconds
        self.max_ammo = 10
        self.health = 10
        self.start_time = 0
        self.bullets = pygame.sprite.Group()

    def move_pressed_key(self, key):
        if key == pygame.K_w:
            self.move_y = -self.step
        if key == pygame.K_s:
            self.move_y = self.step
        if key == pygame.K_a:
            self.move_x = -self.step
        if key == pygame.K_d:
            self.move_x = self.step

    def move_unpressed_key(self, key):
        if key == pygame.K_w:
            self.move_y = max(self.move_y, 0)
        if key == pygame.K_s:
            self.move_y = min(self.move_y, 0)
        if key == pygame.K_a:
            self.move_x = max(self.move_x, 0)
        if key == pygame.K_d:
            self.move_x = min(self.move_x, 0)

    def move_in_border(self):
        if self.rect.y >= background_height - self.height:  # create floor
            self.rect.y += min(0, self.move_y)
        elif self.rect.y <= background_height / 2 + split_height:  # create ceiling
            self.rect.y += max(0, self.move_y)
        else:
            self.rect.y += self.move_y

        if self.rect.x >= background_width - self.width:  # create side 1
            self.rect.x += min(0, self.move_x)
        elif self.rect.x <= 0:  # create side 2
            self.rect.x += max(0, self.move_x)
        else:
            self.rect.x += self.move_x

    def ammo_regen(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= player.regen_ammo * 1000 and self.ammo < self.max_ammo:
            player.ammo += 1
            self.start_time = current_time

    def shoot_bullet(self):
        if self.ammo > 0:
            self.ammo -= 1
            self.bullets.add(Bullet(5, self.rect.x + self.width / 2, self.rect.y))

    def display_health(self):
        font = pygame.font.Font("font/Pixeltype.ttf", 50)
        health = font.render("health: " + str(self.health), False, (75, 100, 100, 200))
        return health

    def display_ammo(self):
        font = pygame.font.Font("font/Pixeltype.ttf", 50)
        ammo = font.render("ammo: " + str(self.ammo), False, (75, 100, 100, 200))
        return ammo

    def is_alive(self):
        if self.health <= 0:
            self.alive = False


class Bullet (pygame.sprite.Sprite):
    def __init__(self, step, x, y):
        super().__init__()
        self.width = 25
        self.height = 25
        self.image = pygame.transform.scale(pygame.image.load('images/Bullet.png').convert_alpha(), (self.width, self.height))  # player skin - (120, 110)
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.step = step  # controls the speed and direction

    def update(self):
        self.rect.y -= self.step
        if self.rect.y <= 0 or self.rect.y >= background_height:
            self.kill()
        if pygame.sprite.spritecollide(enemy, player.bullets, True):
            enemy.health -= 1
            enemy.is_alive()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, step):
        super().__init__()
        self.alive = True
        self.width = 80
        self.height = 74
        self.image = pygame.transform.scale(pygame.image.load('images/FighterBase.png').convert_alpha(), (self.width, self.height))  # player skin - (120, 110)
        self.rect = self.image.get_rect(midbottom=(background_width / 2, 100 + self.height))
        self.step = step  # controls the speed and direction
        self.move_x = 0
        self.move_y = 0
        self.ammo = 5
        self.regen_ammo = 1  # regen every regen_ammo seconds
        self.max_ammo = 10
        self.health = 10
        self.start_time = 0
        self.bullets = pygame.sprite.Group()

    def display_health(self):
        font = pygame.font.Font("font/Pixeltype.ttf", 50)
        health = font.render("health: " + str(self.health), False, (75, 100, 100, 200))
        return health

    def move_pressed_key(self, key):
        if key == "up":
            self.move_y = -self.step
        if key == "down":
            self.move_y = self.step
        if key == "left":
            self.move_x = -self.step
        if key == "right":
            self.move_x = self.step

    def move_unpressed_key(self, key):
        if key == "up":
            self.move_y = min(self.move_y, 0)
        if key == "down":
            self.move_y = max(self.move_y, 0)
        if key == "left":
            self.move_x = min(self.move_x, 0)
        if key == "right":
            self.move_x = max(self.move_x, 0)

    def move_in_border(self):
        if self.rect.y >= (background_height - split_height) / 2 - self.height - 2:  # create floor
            self.rect.y += min(0, self.move_y)
        elif self.rect.y <= 0:  # create ceiling
            self.rect.y += max(0, self.move_y)
        else:
            self.rect.y += self.move_y

        if self.rect.x >= background_width - self.width:  # create side 1
            self.rect.x += min(0, self.move_x)
        elif self.rect.x <= 0:  # create side 2
            self.rect.x += max(0, self.move_x)
        else:
            self.rect.x += self.move_x

    def is_alive(self):
        if self.health <= 0:
            self.alive = False


def init_phase0_background():
    start_background_image = pygame.transform.scale(pygame.image.load('images/background.png').convert_alpha(), (background_width, background_height))

    start_background_rect = start_background_image.get_rect(topleft=(0, 0))
    return start_background_image, start_background_rect


def main():
    global background_width, background_height, split_height, player, enemy
    pygame.init()
    screen = pygame.display.set_mode((1062, 708))
    pygame.display.set_caption("DUAL")
    clock = pygame.time.Clock()
    game_active = True
    start_time = 0

    start_background = init_phase0_background()

    background = pygame.Surface((background_width, background_height))  # create background
    background.fill((46, 34, 47, 255))

    s = pygame.Surface((background_width, split_height)) # split screen
    s.fill((75, 50, 50, 200))

    player = Player(3)
    enemy = Enemy(-3)

    while True:
        if game_phase == 0:
            screen.blit(start_background[0], start_background[1])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        if game_phase == 1:
            player.ammo_regen()
            screen.blit(background, (0, 0))  # initiate background
            screen.blit(s, (0, 350))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYUP:  # player movement
                    player.move_unpressed_key(event.key)

                if event.type == pygame.KEYDOWN:
                    player.move_pressed_key(event.key)
                    if event.key == pygame.K_SPACE:
                        player.shoot_bullet()

            #render enemy
            #render player
            player.move_in_border()
            screen.blit(player.image, player.rect)

            enemy.move_pressed_key("down")
            enemy.move_in_border()
            screen.blit(enemy.image, enemy.rect)
            # player bullets shot
            player.bullets.update()
            player.bullets.draw(screen)

            # display player ammo and health
            screen.blit(player.display_health(), (20, background_height - 40))
            screen.blit(player.display_ammo(), (background_width - 150, background_height - 40))

            # display enemy ammo and health
            screen.blit(enemy.display_health(), (20, 15))


        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()