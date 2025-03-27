import pygame.sprite
import game_launcher
import wall_detect


class Enemy(pygame.sprite.Sprite):

    def __init__(self, _x, _y, _direction, _surface):
        """Create Enemy

        :param _x: initial x coordinate
        :param _y: initial y coordinate
        :return: nothing
        """
        pygame.sprite.Sprite.__init__(self)

        self.main_screen = _surface

        # 设置怪物速度和方向
        self.speed = game_launcher.SPEED_ENEMY
        self.direction = _direction

        # 设置血量
        self.blood = game_launcher.BLOOD_ENEMY

        img = pygame.image.load("assets/monster1.png")
        self.image = pygame.transform.scale(
            img, (game_launcher.WIDTH_ENEMY, game_launcher.HEIGHT_ENEMY)
        )
        self.rect = self.image.get_rect()

        # 设置怪物初始位置
        self.rect.x = _x
        self.rect.y = _y

        self.wall = wall_detect.Wall_Detect(
            self.rect.x, self.rect.y, self.direction, game_launcher.MAP
        )
        self.wall.wall_enemy()

    def update(self):
        if self.blood <= 0:
            self.kill()
        if self.direction == "left":
            self.rect.x -= self.speed
            if self.rect.x < self.wall.x_out_left:
                self.rect.x = self.wall.x_out_left
                self.reverse_direction()
        elif self.direction == "right":
            self.rect.x += self.speed
            if self.rect.x > self.wall.x_out_right - game_launcher.WIDTH_ENEMY:
                self.rect.x = self.wall.x_out_right - game_launcher.WIDTH_ENEMY
                self.reverse_direction()
        elif self.direction == "up":
            self.rect.y -= self.speed
            if self.rect.y < self.wall.y_out_up:
                self.rect.y = self.wall.y_out_up
                self.reverse_direction()
        elif self.direction == "down":
            self.rect.y += self.speed
            if self.rect.y > self.wall.y_out_down - game_launcher.HEIGHT_ENEMY:
                self.rect.y = self.wall.y_out_down - game_launcher.HEIGHT_ENEMY
                self.reverse_direction()

        self.draw_enemy_blood()

    def reverse_direction(self):
        if self.direction == "up":
            self.direction = "down"
        elif self.direction == "down":
            self.direction = "up"
        elif self.direction == "left":
            self.direction = "right"
        elif self.direction == "right":
            self.direction = "left"
        else:
            print("ERROR! Reverse direction error.")

    def draw_enemy_blood(self):
        x = self.rect.x
        y = self.rect.y
        if self.direction == "up":
            y = self.rect.y + 3
        elif self.direction == "down":
            y = self.rect.y - 3
        elif self.direction == "left":
            x = self.rect.x + 3
        elif self.direction == "right":
            x = self.rect.x - 3
        pygame.draw.rect(self.main_screen, "grey", (x, y - 2,
                                                    game_launcher.WIDTH_ENEMY,
                                                    game_launcher.HEIGHT_ENEMY / 9))
        pygame.draw.rect(self.main_screen, "red", (x, y - 2,
                                                   game_launcher.WIDTH_ENEMY *
                                                   (self.blood / game_launcher.BLOOD_ENEMY),
                                                   game_launcher.HEIGHT_ENEMY / 9))
