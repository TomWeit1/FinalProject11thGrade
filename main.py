import pygame
from sys import exit


class Player(pygame.sprite.Sprite):
    def __init__(self, step):
        super().__init__()
        self.width = 80
        self.height = 74
        self.image = pygame.transform.scale(pygame.image.load('images/FighterBase.png').convert_alpha(), (self.width, self.height)) # player skin - (120, 110)
        self.rec = self.image.get_rect(midbottom=(background_width / 2, background_height - 100))
        self.step = step  # controls the speed and direction
        self.move_x = 0
        self.move_y = 0

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
        if self.rec.y >= background_height - self.height:  # create floor
            self.rec.y += min(0, self.move_y)
        elif self.rec.y <= background_height / 2 + split_height:  # create ceiling
            self.rec.y += max(0, self.move_y)
        else:
            self.rec.y += self.move_y

        if self.rec.x >= background_width - self.width:  # create side 1
            self.rec.x += min(0, self.move_x)
        elif self.rec.x <= 0:  # create side 2
            self.rec.x += max(0, self.move_x)
        else:
            self.rec.x += self.move_x


class Bullet (pygame.sprite.Sprite):
    def __init__(self, step):
        super().__init__()
        self.width = 5
        self.height = 3
        self.rec = pygame.Surface((self.width, self.height))
        self.step = step  # controls the speed and direction


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1010, 705))
    pygame.display.set_caption("DUAL")
    clock = pygame.time.Clock()
    game_active = True

    background_width = 1010
    background_height = 705
    background = pygame.Surface((background_width, background_height))  # create background
    background.fill((46, 34, 47, 255))

    split_height = 5
    s = pygame.Surface((background_width, split_height)) # split screen
    s.fill((75, 50, 50, 200))

    player = Player(3)

    while True:
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

        player.move_in_border()
        screen.blit(player.image, player.rec)

        pygame.display.update()
        clock.tick(80)
