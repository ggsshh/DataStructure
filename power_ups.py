import pygame.sprite
import game_launcher
import os


class Power_Ups(pygame.sprite.Sprite):
    def __init__(self, _x, _y, _kind: int):
        pygame.sprite.Sprite.__init__(self)

        self.kind = _kind
        # Create different view according to kind.
        # self.image = pygame.surface.Surface((game_launcher.WIDTH_POWER_UPS, game_launcher.HEIGHT_POWER_UPS))
        if self.kind == 0:
            self.image = pygame.image.load(os.path.join('assets', 'blood.png'))
            self.image = pygame.transform.scale(self.image, (
                game_launcher.WIDTH_POWER_UPS * 1.5, game_launcher.HEIGHT_POWER_UPS * 1.5))
            # self.image.fill("red")
        elif self.kind == 1:
            self.image = pygame.image.load(os.path.join('assets', 'shield.png'))
            self.image = pygame.transform.scale(self.image, (
                game_launcher.WIDTH_POWER_UPS * 1.5, game_launcher.HEIGHT_POWER_UPS * 1.5))
            # self.image.fill("blue")
        elif self.kind == 2:
            self.image = pygame.image.load(os.path.join('assets', 'damage.png'))
            self.image = pygame.transform.scale(self.image, (
                game_launcher.WIDTH_POWER_UPS * 1.5, game_launcher.HEIGHT_POWER_UPS * 1.5))
            # self.image.fill("yellow")
        elif self.kind == 3:
            self.image = pygame.image.load(os.path.join('assets', 'speed.png'))
            self.image = pygame.transform.scale(self.image, (
                game_launcher.WIDTH_POWER_UPS * 1.5, game_launcher.HEIGHT_POWER_UPS * 1.5))
            # self.image.fill("green")

        self.rect = self.image.get_rect()
        self.rect.x = _x
        self.rect.y = _y
