import pygame
import game_launcher
import wall_detect


class Bullet(pygame.sprite.Sprite):

    def __init__(self, coordinate_x, coordinate_y, direction, damage):
        """Create a bullet.
        :param coordinate_x: The initial x coordinate of the bullet
        :param coordinate_y: The initial y coordinate of the bullet
        :param """
        pygame.sprite.Sprite.__init__(self)
        self.damage = damage
        self.speed = game_launcher.SPEED_BULLET
        self.direction = direction

        img = pygame.image.load("assets/bullet1.png")
        self.image = pygame.transform.scale(img, (game_launcher.WIDTH_BULLET, game_launcher.HEIGHT_BULLET))
        self.rect = self.image.get_rect()

        self.rect.x = coordinate_x
        self.rect.y = coordinate_y
        self.wall = wall_detect.Wall_Detect(self.rect.x, self.rect.y, self.direction, game_launcher.MAP)
        self.wall.wall_bullet()

    def update(self):

        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
