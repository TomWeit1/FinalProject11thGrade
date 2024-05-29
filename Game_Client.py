import pygame
from sys import exit
import socket
import threading
import time

game_phase = "start"
background_width = 1062
background_height = 708
split_height = 8
IP = 'localhost'
PORT = 12345


class Player(pygame.sprite.Sprite):
    def __init__(self, step):
        super().__init__()
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
            self.move_y = max(self.move_y, 0)
        if key == "down":
            self.move_y = min(self.move_y, 0)
        if key == "left":
            self.move_x = max(self.move_x, 0)
        if key == "right":
            self.move_x = min(self.move_x, 0)

    def move_in_border(self):
        if self.rect.y >= background_height - self.height:  # create floor
            self.rect.y += min(0, self.move_y)
        elif self.rect.y <= background_height / 2 + split_height / 2 + 2:  # create ceiling
            self.rect.y += max(0, self.move_y)
        else:
            self.rect.y += self.move_y

        if self.rect.x >= background_width - self.width:  # create side 1
            self.rect.x += min(0, self.move_x)
        elif self.rect.x <= 0:  # create side 2
            self.rect.x += max(0, self.move_x)
        else:
            self.rect.x += self.move_x

    def ammo_regen(self, enemy):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= player.regen_ammo * 1000:
            if self.ammo < self.max_ammo:
                player.ammo += 1
            if enemy.ammo < enemy.max_ammo:
                enemy.ammo += 1
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
        global game_phase
        if self.health <= 0:
            game_over_msg = "OVER"
            game_over_msg += str(id)
            client.send(game_over_msg.encode())


class Bullet (pygame.sprite.Sprite):
    def __init__(self, step, x, y):
        super().__init__()
        self.width = 25
        self.height = 25
        self.image = pygame.transform.scale(pygame.image.load('images/Bullet.png').convert_alpha(), (self.width, self.height))  # player skin - (120, 110)
        if step < 0:
            self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.step = step  # controls the speed and direction

    def update(self):
        self.rect.y -= self.step
        if self.rect.y <= 0 or self.rect.y >= background_height:
            self.kill()
        if pygame.sprite.spritecollide(enemy, player.bullets, True):
            enemy.health -= 1
        if pygame.sprite.spritecollide(player, enemy.bullets, True):
            player.health -= 1
            player.is_alive()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, step):
        super().__init__()
        self.alive = True
        self.width = 80
        self.height = 74
        self.image = pygame.transform.scale(pygame.image.load('images/FighterBase.png').convert_alpha(),
                                            (self.width, self.height))  # player skin - (120, 110)
        self.image = pygame. transform. rotate(self.image, 180)
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

    def shoot_bullet(self):
        if self.ammo > 0:
            self.ammo -= 1
            self.bullets.add(Bullet(-5, self.rect.x + self.width / 2, self.rect.y + self.height))


def init_phase0_background():
    start_background_image = pygame.transform.scale(pygame.image.load('images/background.png').convert_alpha(), (background_width, background_height))

    start_background_rect = start_background_image.get_rect(topleft=(0, 0))
    return start_background_image, start_background_rect


def create_MOVE_msg(press, direction):
    msg = "MOVE"
    msg += str(press)  # press = 0/1, 0 meaning up, 1 meaning down
    msg += str(direction)  # dir = 1,2,3,4
    return msg


def key_to_num(key):
    # from a key w,a,s,d to int 1,2,3,4
    if key == pygame.K_w:
        return 1
    if key == pygame.K_a:
        return 2
    if key == pygame.K_s:
        return 3
    if key == pygame.K_d:
        return 4


def num_to_key(num):
    # from an int 1,2,3,4 to a direction
    if num == 1:
        return "up"
    if num == 2:
        return "left"
    if num == 3:
        return "down"
    if num == 4:
        return "right"


def handle_recv(cli, id):
    while True:
        try:
            msg = cli.recv(7).decode()
            if msg[0:4] == "MOVE":
                if id == int(msg[4]):
                    if int(msg[5]) == 0:
                        player.move_unpressed_key(num_to_key(int(msg[6])))
                    if int(msg[5]) == 1:
                        player.move_pressed_key(num_to_key(int(msg[6])))
                else:
                    if int(msg[5]) == 0:
                        enemy.move_unpressed_key(num_to_key(int(msg[6])))
                    if int(msg[5]) == 1:
                        enemy.move_pressed_key(num_to_key(int(msg[6])))
            elif msg[0:4] == "SHOT":
                if id == int(msg[4]):
                    player.shoot_bullet()
                else:
                    enemy.shoot_bullet()
            if msg[0:4] == "OVER":
                overrc_msg = "OVRC"  # Over received by client
                cli.send(overrc_msg.encode())
                reset_game(int(msg[4]))
            if msg[0:4] == "EXIT" and int(msg[4]) != id:
                exitrc_msg = "EXRC"  # Exit received by client
                cli.send(exitrc_msg.encode())
                reset_game(3)
        except:
            break


def reset_game(loser):
    global over_msg, game_phase
    if id == loser:
        over_msg = "You lost the match"
        game_phase = "player_dead"
    elif loser == 3:  # if other player quit
        over_msg = "Other player quit"
        game_phase = "reset_game"
    else:
        over_msg = "You won! good job!"
        game_phase = "reset_game"




def main():
    global background_width, background_height, split_height, player, enemy, game_phase, id, client
    pygame.init()
    screen = pygame.display.set_mode((1062, 708))
    pygame.display.set_caption("DUAL")
    clock = pygame.time.Clock()
    game_active = True
    start_time = 0

    start_background = init_phase0_background()

    background = pygame.Surface((background_width, background_height))  # create background
    background.fill((46, 34, 47, 255))

    split = pygame.Surface((background_width, split_height)) # split screen
    split.fill((75, 50, 50, 200))

    player = Player(3)
    enemy = Enemy(-3)
    i = 1

    while game_active:
        if game_phase == "start":
            screen.blit(start_background[0], start_background[1])
            font = pygame.font.Font("font/Pixeltype.ttf", 100)
            text = font.render("Press space to join game", False, "white")
            screen.blit(text, (150, background_height/2 - 100))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_phase = "set_wait_background"
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        elif game_phase == "set_wait_background":  # in between phases to set background
            screen.blit(start_background[0], start_background[1])
            font = pygame.font.Font("font/Pixeltype.ttf", 80)
            text = font.render("Waiting for another player to join", False, "white")
            screen.blit(text, (120, background_height / 2 - 100))
            game_phase = "connecting_to_game"
        elif game_phase == "connecting_to_game":
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((IP, PORT))

            data = ""
            while not data:
                data = client.recv(5).decode()
            id = int(data[4])
            game_phase = "gameplay"
            recv_thread = threading.Thread(target=handle_recv, args=(client, id))
            recv_thread.start()
        elif game_phase == "gameplay":
            player.ammo_regen(enemy)
            screen.blit(background, (0, 0))  # initiate background
            screen.blit(split, (0, (background_height - split_height) / 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_msg = "EXIT"
                    client.send(exit_msg.encode())
                    pygame.quit()
                    game_active = False

                if event.type == pygame.KEYUP:  # player movement
                    if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                        msg_up = create_MOVE_msg(0, key_to_num(event.key))
                        client.send(msg_up.encode())
                    # player.move_unpressed_key(event.key)

                if event.type == pygame.KEYDOWN:
                    # player.move_pressed_key(event.key)
                    if event.key == pygame.K_SPACE:
                        shoot_msg = "SHOT"
                        client.send(shoot_msg.encode())
                        # player.shoot_bullet()
                    elif event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                        msg_down = create_MOVE_msg(1, key_to_num(event.key))
                        client.send(msg_down.encode())

            if not game_active:
                break

            #render player
            player.move_in_border()
            screen.blit(player.image, player.rect)

            #render enemy
            enemy.move_in_border()
            screen.blit(enemy.image, enemy.rect)

            # player bullets shot
            player.bullets.update()
            player.bullets.draw(screen)

            # player bullets shot
            enemy.bullets.update()
            enemy.bullets.draw(screen)

            # display player ammo and health
            screen.blit(player.display_health(), (20, background_height - 40))
            screen.blit(player.display_ammo(), (background_width - 150, background_height - 40))

            # display enemy ammo and health
            screen.blit(enemy.display_health(), (20, 15))
        elif game_phase == "reset_game":  #reseting game
            start_background = init_phase0_background()
            screen.blit(start_background[0], start_background[1])

            font = pygame.font.Font("font/Pixeltype.ttf", 80)
            text = font.render(over_msg, False, "white")
            screen.blit(text, (120, background_height / 2 - 100))
            text2 = font.render("press space to go back to the menu", False, "white")
            screen.blit(text2, (120, background_height / 2))
            client.close()
            game_phase = "continue_reset"
        elif game_phase == "continue_reset":
            wait = True
            while wait:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            wait = False
                            break
            player = Player(3)
            enemy = Enemy(-3)
            game_phase = "start"
        elif game_phase == "player_dead":
            p_image = pygame.image.load(f'images/Destruction_fighter/Destruction{i}.png')
            player.image = pygame.transform.scale(p_image.convert_alpha(), (p_image.get_width() * (80/24), p_image.get_height() * (74/22)))
            print(p_image.get_width())
            player.rect = player.image.get_rect(midbottom=(background_width / 2, background_height - 100))
            screen.blit(player.image, player.rect)
            i += 1
            time.sleep(0.05)
            if i > 8:
                game_phase = "reset_game"
                i = 1


        pygame.display.update()
        clock.tick(60)
    try:
        client.close()
    except:
        pass
    recv_thread.join()


if __name__ == '__main__':
    main()
