import game_launcher


class Wall_Detect:
    def __init__(self, x, y, direction, the_map):
        self.x_in = x
        self.y_in = y
        self.direction = direction
        self.map = the_map
        self.x_pane = 0
        self.y_pane = 0
        self.x_out_left = 0
        self.x_out_right = 0
        self.y_out_up = 0
        self.y_out_down = 0

    def pixel_pane(self, x, y):
        self.x_pane = x // game_launcher.SIZE_PANE
        self.y_pane = y // game_launcher.SIZE_PANE

    def pane_pixel_player(self, x, y):
        if self.direction == "left":
            self.x_out_left = (x + 1) * game_launcher.SIZE_PANE
        elif self.direction == "right":
            self.x_out_right = x * game_launcher.SIZE_PANE
        elif self.direction == "up":
            self.y_out_up = (y + 1) * game_launcher.SIZE_PANE
        elif self.direction == "down":
            self.y_out_down = y * game_launcher.SIZE_PANE

    def pane_pixel_enemy(self, x, y, direction):
        if direction == "left":
            self.x_out_left = (x + 1) * game_launcher.SIZE_PANE
        elif direction == "right":
            self.x_out_right = x * game_launcher.SIZE_PANE
        elif direction == "up":
            self.y_out_up = (y + 1) * game_launcher.SIZE_PANE
        elif direction == "down":
            self.y_out_down = y * game_launcher.SIZE_PANE

    def wall_player(self):
        self.pixel_pane(self.x_in, self.y_in)
        x = self.x_pane
        y = self.y_pane
        if self.direction == "left":
            while self.map.get_type(self.x_pane, self.y_pane) != 1 and self.x_pane > 0:
                self.x_pane -= 1
            if self.y_in % game_launcher.SIZE_PANE != 0:
                while self.map.get_type(x, y + 1) != 1 and x > 0:
                    x -= 1
                if x > self.x_pane:
                    self.x_pane = x
            self.pane_pixel_player(self.x_pane, self.y_pane)
        elif self.direction == "right":
            while self.map.get_type(self.x_pane, self.y_pane) != 1 and self.x_pane < game_launcher.WIDTH_PANE:
                self.x_pane += 1
            if self.y_in % game_launcher.SIZE_PANE != 0:
                while self.map.get_type(x, y + 1) != 1 and x < game_launcher.WIDTH_PANE:
                    x += 1
                if x < self.x_pane:
                    self.x_pane = x
            self.pane_pixel_player(self.x_pane, self.y_pane)
        elif self.direction == "up":
            while self.map.get_type(self.x_pane, self.y_pane) != 1 and self.y_pane > 0:
                self.y_pane -= 1
            if self.x_in % game_launcher.SIZE_PANE != 0:
                while self.map.get_type(x + 1, y) != 1 and y > 0:
                    y -= 1
                if y > self.y_pane:
                    self.y_pane = y
            self.pane_pixel_player(self.x_pane, self.y_pane)
        elif self.direction == "down":
            while self.map.get_type(self.x_pane, self.y_pane) != 1 and self.y_pane < game_launcher.HEIGHT_PANE:
                self.y_pane += 1
            if self.x_in % game_launcher.SIZE_PANE != 0:
                while self.map.get_type(x + 1, y) != 1 and y < game_launcher.HEIGHT_PANE:
                    y += 1
                if y < self.y_pane:
                    self.y_pane = y
            self.pane_pixel_player(self.x_pane, self.y_pane)

    def wall_enemy(self):
        self.pixel_pane(self.x_in, self.y_in)
        x = self.x_pane
        y = self.y_pane
        if self.direction == "left" or self.direction == "right":
            while self.map.get_type(x, y) != 1 and x > 0:
                x -= 1
            self.pane_pixel_enemy(x, y, "left")
            while self.map.get_type(self.x_pane, self.y_pane) != 1 and self.x_pane < game_launcher.WIDTH_PANE:
                self.x_pane += 1
            self.pane_pixel_enemy(self.x_pane, self.y_pane, "right")
        elif self.direction == "up" or self.direction == "down":
            while self.map.get_type(x, y) != 1 and y > 0:
                y -= 1
            self.pane_pixel_enemy(x, y, "up")
            while self.map.get_type(self.x_pane, self.y_pane) != 1 and self.y_pane < game_launcher.HEIGHT_PANE:
                self.y_pane += 1
            self.pane_pixel_enemy(self.x_pane, self.y_pane, "down")

    def wall_bullet(self):
        self.pixel_pane(self.x_in, self.y_in)
        x = self.x_pane
        y = self.y_pane
        if self.direction == "left":
            while self.map.get_type(self.x_pane, self.y_pane) != 1 and self.x_pane > 0:
                self.x_pane -= 1
            if self.y_in % game_launcher.SIZE_PANE > 10:
                while self.map.get_type(x, y + 1) == 0 and x > 0:
                    x -= 1
                if x > self.x_pane:
                    self.x_pane = x
            self.pane_pixel_player(self.x_pane, self.y_pane)
        elif self.direction == "right":
            while self.map.get_type(self.x_pane, self.y_pane) != 1 and self.x_pane < game_launcher.WIDTH_PANE:
                self.x_pane += 1
            if self.y_in % game_launcher.SIZE_PANE > 10:
                while self.map.get_type(x, y + 1) == 0 and x < game_launcher.WIDTH_PANE:
                    x += 1
                if x < self.x_pane:
                    self.x_pane = x
            self.pane_pixel_player(self.x_pane, self.y_pane)
        elif self.direction == "up":
            while self.map.get_type(self.x_pane, self.y_pane) != 1 and self.y_pane > 0:
                self.y_pane -= 1
            if self.x_in % game_launcher.SIZE_PANE > 10:
                while self.map.get_type(x + 1, y) == 0 and y > 0:
                    y -= 1
                if y > self.y_pane:
                    self.y_pane = y
            self.pane_pixel_player(self.x_pane, self.y_pane)
        elif self.direction == "down":
            while self.map.get_type(self.x_pane, self.y_pane) != 1 and self.y_pane < game_launcher.HEIGHT_PANE:
                self.y_pane += 1
            if self.x_in % game_launcher.SIZE_PANE > 10:
                while self.map.get_type(x + 1, y) == 0 and y < game_launcher.HEIGHT_PANE:
                    y += 1
                if y < self.y_pane:
                    self.y_pane = y
            self.pane_pixel_player(self.x_pane, self.y_pane)
