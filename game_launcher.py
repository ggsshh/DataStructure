import random
import pygame

import enemy
import map
import player
import power_ups
import linked_list

REC_SIZE = 15
REC_WIDTH = 60
REC_HEIGHT = 35
WIDTH = REC_WIDTH * REC_SIZE
HEIGHT = REC_HEIGHT * REC_SIZE + 50

WIDTH_BASIC = REC_SIZE
HEIGHT_BASIC = REC_SIZE

WIDTH_PLAYER = WIDTH_BASIC
HEIGHT_PLAYER = HEIGHT_BASIC

WIDTH_ENEMY = WIDTH_BASIC
HEIGHT_ENEMY = HEIGHT_BASIC

WIDTH_POWER_UPS = 10
HEIGHT_POWER_UPS = 10

WIDTH_BULLET = 10
HEIGHT_BULLET = 10

POS_PLAYER_BLOOD_X = 90
POS_PLAYER_BLOOD_Y = HEIGHT - 20
WIDTH_PLAYER_BLOOD = 90
HEIGHT_PLAYER_BLOOD = 10

BLOOD_ENEMY = 5
BLOOD_PLAYER = 3
BLOOD_BULLET = 1

SHIELD_PLAYER = 1

TIME_DAMAGE = 5
TIME_SPEED = 5

SIZE_PANE = REC_SIZE
WIDTH_PANE = REC_WIDTH
HEIGHT_PANE = REC_HEIGHT

SPEED_PLAYER = 3
SPEED_ENEMY = 2.5
SPEED_BULLET = 20

HURT_ENEMY = 0.003
ENEMY_NUM = 500

MAP = map.Map(REC_WIDTH, REC_HEIGHT)


class GameLauncher:
    def __init__(self) -> None:
        # --------------------------------------------------------------------
        # 初始化窗口、载入素材
        pygame.init()
        pygame.display.set_caption("Tomb Raider Game")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.img_wall = pygame.image.load("assets/wall.png")
        self.img_road = pygame.image.load("assets/road.png")
        self.img_destination = pygame.image.load("assets/destination.png")
        self.img_wall = pygame.transform.scale(self.img_wall, (REC_SIZE, REC_SIZE))
        self.img_road = pygame.transform.scale(self.img_road, (REC_SIZE, REC_SIZE))
        self.img_destination = pygame.transform.scale(self.img_destination, (REC_SIZE, REC_SIZE))
        # --------------------------------------------------------------------
        # 实例化精灵列表和组件（各个游戏元素）

        self.map = MAP
        self.map.generate_map()

        self.enemyGroup = pygame.sprite.Group()
        self.bulletGroup = pygame.sprite.Group()
        self.powerUpsGroup = pygame.sprite.Group()

        # 游戏时钟
        self.clock = pygame.time.Clock()

        self.list = linked_list.Linked_List()
        # 游戏运行函数

        # 添加空格子到链表
        for data_y in range(REC_HEIGHT):
            for data_x in range(REC_WIDTH):
                rec_type = MAP.get_type(data_x, data_y)
                if rec_type == 0:
                    self.list.add(data_x, data_y)
        self.enemy_value = random.randint(0, self.list.length)
        self.player_value = random.randint(0, self.list.length)
        self.power_ups_value = random.randint(0, self.list.length)
        self.in_x, self.in_y = self.map.starting_point[0], self.map.starting_point[1]
        self.player = player.Player(self.screen, self.in_x * REC_SIZE, self.in_y * REC_SIZE)

        self.f = pygame.font.Font("assets/consola.ttf", 30)
        self.die_text = self.f.render(
            "You died. Press space to back to menu.", True, (0, 0, 0), (255, 255, 255)
        )

        self.end_text = self.f.render(
            "You win. Press space to back to menu.", True, (0, 0, 0), (255, 255, 255)
        )

        self.dieTextRect = self.die_text.get_rect()
        self.dieTextRect.center = (
            int(WIDTH * (1 / 2)),
            int(HEIGHT * (1 / 3)),
        )

        self.endTextRect = self.end_text.get_rect()
        self.endTextRect.center = (
            int(WIDTH * (1 / 2)),
            int(HEIGHT * (1 / 3)),
        )

        self.reachToExit = False

    def launch(self):
        while True:
            # ----------------------------------------------------------------
            self.screen.fill(color=(23, 145, 87))
            self.draw_map()

            ft = pygame.font.SysFont(" ", 15)
            Blood = ft.render("Blood", True, "red")
            Shield = ft.render("Shield", True, "blue")
            self.screen.blit(Blood, (POS_PLAYER_BLOOD_X - 40, POS_PLAYER_BLOOD_Y))
            self.screen.blit(Shield, (POS_PLAYER_BLOOD_X - 40, POS_PLAYER_BLOOD_Y - 15))

            if not self.player.life or self.reachToExit:
                return

            # 事件监测
            for event in pygame.event.get():
                # 关闭窗口
                if event.type == pygame.QUIT:
                    return

                if self.map.player_is_at_end_point(self.player.rect.x, self.player.rect.y):
                    self.reachToExit = True
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

                    # SPACE、W、方向上键
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.player.go_up_begin()
                        self.player.go_down_end()
                        self.player.go_left_end()
                        self.player.go_right_end()

                    # 按下S、方向下键
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.player.go_down_begin()
                        self.player.go_up_end()
                        self.player.go_left_end()
                        self.player.go_right_end()

                    # 按下A、方向左键
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.player.go_left_begin()
                        self.player.go_up_end()
                        self.player.go_down_end()
                        self.player.go_right_end()

                    # 按下D、方向右键
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.player.go_right_begin()
                        self.player.go_up_end()
                        self.player.go_down_end()
                        self.player.go_left_end()

                    if event.key == pygame.K_SPACE:
                        self.bulletGroup.add(self.player.fire())

                if event.type == pygame.KEYUP:
                    # SPACE、W、方向上键
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.player.go_up_end()

                        # 松开S、方向下键
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.player.go_down_end()

                        # 按下A、方向左键
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.player.go_left_end()

                        # 按下D、方向右键
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.player.go_right_end()

            # 生成随机数量的敌人
            self.generate_enemy()
            self.generate_power_ups()

            # 画子弹
            self.bulletGroup.draw(self.screen)

            # 画敌人
            self.enemyGroup.draw(self.screen)

            # 画道具
            self.powerUpsGroup.draw(self.screen)

            # 画玩家
            self.screen.blit(self.player.image, self.player.rect)

            # 检测互动

            self.check_player_enemy()
            self.check_player_power_ups()
            self.check_bullet_enemy()
            self.check_bullet_wall()


            # ----------------------------------------------------------------
            # 更新组件的状态
            self.bulletGroup.update()
            self.enemyGroup.update()
            self.powerUpsGroup.update()

            self.player.update()

            # ----------------------------------------------------------------
            # 更新窗口、设置帧率
            pygame.display.update()
            self.clock.tick(60)

    # ----------------------------------------------------------------
    # 游戏结束界面函数
    def gameOver(self) -> bool:
        # --------------------------------------------------------------------
        if not self.player.life or self.reachToExit:
            while True:
                # ------------------------------------------------------------
                # 事件监测
                for event in pygame.event.get():
                    # 关闭窗口
                    if event.type == pygame.QUIT:
                        return False

                    if event.type == pygame.KEYDOWN:
                        # Esc键返回False
                        if event.key == pygame.K_ESCAPE:
                            return False

                        # SPACE、W、方向上键返回True
                        if (
                                event.key == pygame.K_SPACE
                                or event.key == pygame.K_w
                                or event.key == pygame.K_UP
                        ):
                            return True

                # 背景颜色
                self.screen.fill("white")


                if self.reachToExit:
                    self.screen.blit(self.end_text, self.endTextRect)
                else:
                    self.screen.blit(self.die_text, self.dieTextRect)
                pygame.display.update()
                self.clock.tick(60)

        # --------------------------------------------------------------------
        # 玩家手动返回菜单时
        else:
            return False

    # ------------------------------------------------------------------------
    # ------------------------------------------------------------------------
    # 画地图
    def draw_map(self):

        for y in range(self.map.height):
            for x in range(self.map.width):
                the_rect = pygame.Rect(
                    REC_SIZE * x,
                    REC_SIZE * y,
                    REC_SIZE,
                    REC_SIZE,
                )
                node_type = self.map.get_type(x, y)
                if node_type == 0:
                    img_final = self.img_road
                elif node_type == 1:
                    img_final = self.img_wall
                else:
                    color = "pink"
                    pygame.draw.rect(self.screen, color, the_rect)
                    img_final = self.img_destination

                self.screen.blit(img_final, (
                    REC_SIZE * x,
                    REC_SIZE * y,
                    REC_SIZE,
                    REC_SIZE,
                ))

    def generate_enemy(self):
        """Generate Enemy when it is less than 5"""
        random.seed()
        while len(self.enemyGroup.sprites()) < ENEMY_NUM:
            rand_x, rand_y = self.list.move_and_extract(self.enemy_value)
            direction_list = ["right", "left", "up", "down"]
            enemy_direction = direction_list[random.randint(0, 3)]
            self.enemyGroup.add(enemy.Enemy(rand_x * REC_SIZE, rand_y * REC_SIZE, enemy_direction, self.screen))

    def generate_power_ups(self):
        """Generate Power-Ups when it is less than 3"""

        while len(self.powerUpsGroup.sprites()) < 3:
            rand_x, rand_y = self.list.move_and_extract(self.power_ups_value)
            rand_kind = random.randint(0, 3)
            self.powerUpsGroup.add(power_ups.Power_Ups(rand_x * REC_SIZE, rand_y * REC_SIZE, rand_kind))

    # 玩家碰撞敌人时扣血
    def check_player_enemy(self):
        if (
                pygame.sprite.spritecollideany(
                    self.player, self.enemyGroup, collided=pygame.sprite.collide_rect
                )
                is not None
        ):
            self.player.hurt(HURT_ENEMY)
            # print("Player Enemy Collide" + str(self.player.blood) + " " + str(self.player.shields))

    # 玩家碰撞道具时道具生效a
    def check_player_power_ups(self):
        gets_hit = pygame.sprite.spritecollideany(
            self.player, self.powerUpsGroup, collided=pygame.sprite.collide_rect
        )
        if gets_hit is not None:
            self.powerUpsGroup.remove(gets_hit)
            # 回血
            if gets_hit.kind == 0:
                self.player.add_blood()
            elif gets_hit.kind == 1:
                self.player.add_shields()
            elif gets_hit.kind == 2:
                self.player.damage_up()
            elif gets_hit.kind == 3:
                self.player.speed_up()

    # 子弹碰撞敌人时敌人扣血
    def check_bullet_enemy(self):
        bullet_list = self.bulletGroup.sprites()
        list_size = len(bullet_list)
        for i in range(list_size):
            hit_list = pygame.sprite.spritecollide(
                bullet_list[i],
                self.enemyGroup,
                dokill=False,
                collided=pygame.sprite.collide_rect,
            )
            if len(hit_list) > 0:
                bullet_list[i].kill()
                for j in range(len(hit_list)):
                    hit_list[j].blood = hit_list[j].blood - bullet_list[i].damage

    def check_bullet_wall(self):
        bullet_list = self.bulletGroup.sprites()
        list_size = len(bullet_list)
        for i in range(list_size):
            if bullet_list[i].direction == "left":
                if bullet_list[i].rect.x <= bullet_list[i].wall.x_out_left:
                    bullet_list[i].kill()
            elif bullet_list[i].direction == "right":
                if bullet_list[i].rect.x >= bullet_list[i].wall.x_out_right - WIDTH_BULLET:
                    bullet_list[i].kill()
            elif bullet_list[i].direction == "up":
                if bullet_list[i].rect.y <= bullet_list[i].wall.y_out_up:
                    bullet_list[i].kill()
            elif bullet_list[i].direction == "down":
                if bullet_list[i].rect.y >= bullet_list[i].wall.y_out_down - HEIGHT_BULLET:
                    bullet_list[i].kill()
