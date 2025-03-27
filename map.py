from random import randint, choice
from enum import Enum
from math import dist
import game_launcher


class MAP_ENTRY_TYPE(Enum):
    """The type of the node in the map.

    MAP_EMPTY

    MAP_BLOCK

    MAP_TARGET

    MAP_PATH

    MAP_DONE"""
    MAP_PATH = (0,)
    MAP_WALL = (1,)
    MAP_END_POINT = (2,)


class Map:
    width: int
    height: int
    map: [int]
    starting_point: (int, int)
    end_point: (int, int)

    def __init__(self, width, height, default_type=1):
        self.width = width
        self.height = height
        self.map = [[default_type for _ in range(self.width)] for _ in range(self.height)]

    def set_node(self, x, y, value):
        if value == MAP_ENTRY_TYPE.MAP_PATH:
            self.map[y][x] = 0
        elif value == MAP_ENTRY_TYPE.MAP_WALL:
            self.map[y][x] = 1
        elif value == MAP_ENTRY_TYPE.MAP_END_POINT:
            self.map[y][x] = 2
        elif value == MAP_ENTRY_TYPE.MAP_PATH:
            self.map[y][x] = 3
        else:
            self.map[y][x] = 4

    def reset_map(self, value):
        for y in range(self.height):
            for x in range(self.width):
                self.set_node(x, y, value)

    def get_type(self, x, y):
        return self.map[y][x]

    def is_valid(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return True

    def is_edge(self, x, y):
        if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
            return True
        else:
            return False

    def is_wall(self, x, y):
        if self.is_valid(x, y) and self.map[y][x] == 1:
            return True
        else:
            return False

    def generate_map(self):
        result = (False, (-1, -1), (-1, -1))
        while not result[0]:
            self.reset_map(MAP_ENTRY_TYPE.MAP_WALL)
            self.generate_map_path_with_all_blocks()
            result = self.calculate_starting_point_and_end_point()
        self.starting_point = result[1]
        self.end_point = result[2]
        self.generate_starting_point_and_end_point()

    def generate_map_path_with_all_blocks(self):
        startX, startY = (randint(2, self.width - 3), randint(2, self.height - 3))
        start_direction = randint(0, 3)

        drawing_man = DrawingMan(startX, startY, start_direction, self)
        drawing_man.paint()

        route_list = [(drawing_man.x, drawing_man.y, drawing_man.direction)]
        while len(route_list) > 0:
            while drawing_man.try_move(route_list):
                pass

            # Roll back configuration
            if len(route_list) > 5:
                for i in range(randint(2, 5)):
                    route_list.pop()
            elif len(route_list) > 1:
                for i in range(randint(2, len(route_list))):
                    route_list.pop()
            else:
                route_list.pop()

            if len(route_list):
                drawing_man.go_to(route_list[-1][0], route_list[-1][1], route_list[-1][2])

    def calculate_starting_point_and_end_point(self) -> (bool, (int, int), (int, int)):
        possible_points_up = []
        possible_points_right = []
        possible_points_down = []
        possible_points_left = []
        for i in range(2, self.width - 2):
            if not self.is_wall(i, 1):
                possible_points_up.append((i, 1))
            if not self.is_wall(i, self.height - 2):
                possible_points_down.append((i, self.height - 2))

        for i in range(2, self.height - 2):
            if not self.is_wall(1, i):
                possible_points_left.append((1, i))
            if not self.is_wall(self.width - 2, i):
                possible_points_right.append((self.width - 2, i))

        possible_points = possible_points_up + possible_points_right + possible_points_down + possible_points_left

        rand_pos = randint(0, len(possible_points) - 1)
        starting_point = possible_points[rand_pos]

        found_it = False
        end_point = (-1, -1)
        rand_pos = randint(0, len(possible_points) - 1)
        for i in range(rand_pos + 1, len(possible_points)):
            end_point = possible_points[i]
            distance = dist(starting_point, end_point)
            if distance > min(self.width, self.height):
                found_it = True
                break

        if not found_it:
            for i in range(rand_pos):
                end_point = possible_points[i]
                distance = dist(starting_point, end_point)
                if distance > min(self.width, self.height):
                    found_it = True
                    break

        if found_it:
            print(starting_point, end_point)
            return found_it, starting_point, end_point
        else:
            print(-1, -1)
            return found_it, (-1, -1), (-1, -1)

    def generate_starting_point_and_end_point(self):
        if not self.starting_point == (-1, -1) and not self.end_point == (-1, -1):
            self.set_node(self.end_point[0], self.end_point[1], MAP_ENTRY_TYPE.MAP_END_POINT)

    def player_is_at_end_point(self, x, y):
        x = (x + int(game_launcher.WIDTH_PLAYER / 2)) // game_launcher.SIZE_PANE
        y = (y + int(game_launcher.HEIGHT_PLAYER / 2)) // game_launcher.SIZE_PANE
        if self.get_type(x, y) == 2:
            return True
        else:
            return False


class DrawingMan:
    def __init__(self, pos_x, pos_y, direction, map_where_the_drawing_man_is_in: Map):
        self.x = pos_x
        self.y = pos_y
        self.direction = direction

        self.map_parent = map_where_the_drawing_man_is_in
        self.force_forward = 0


    def forward(self, steps: int = 1):
        if self.direction == 0:
            self.y -= steps
        elif self.direction == 1:
            self.x += steps
        elif self.direction == 2:
            self.y += steps
        elif self.direction == 3:
            self.x -= steps

    def backward(self, steps: int = 1):
        if self.direction == 0:
            self.y += steps
        elif self.direction == 1:
            self.x -= steps
        elif self.direction == 2:
            self.y -= steps
        elif self.direction == 3:
            self.x += steps

    def left(self, steps: int = 1):
        if self.direction == 0:
            self.x -= steps
        elif self.direction == 1:
            self.y -= steps
        elif self.direction == 2:
            self.x += steps
        elif self.direction == 3:
            self.y += steps

    def right(self, steps: int = 1):
        if self.direction == 0:
            self.x += steps
        elif self.direction == 1:
            self.y += steps
        elif self.direction == 2:
            self.x -= steps
        elif self.direction == 3:
            self.y -= steps

    def turn_left(self):
        if self.direction == 0:
            self.direction = 3
        elif self.direction == 1:
            self.direction = 0
        elif self.direction == 2:
            self.direction = 1
        elif self.direction == 3:
            self.direction = 2

    def turn_right(self):
        if self.direction == 0:
            self.direction = 1
        elif self.direction == 1:
            self.direction = 2
        elif self.direction == 2:
            self.direction = 3
        elif self.direction == 3:
            self.direction = 0

    def turn_around(self):
        if self.direction == 0:
            self.direction = 2
        elif self.direction == 1:
            self.direction = 3
        elif self.direction == 2:
            self.direction = 0
        elif self.direction == 3:
            self.direction = 1

    def move_by_relative_coordinate(self, relative_x: int, relative_y: int):
        if self.direction == 0:
            self.x += relative_x
            self.y += relative_y
        elif self.direction == 1:
            self.y += relative_x
            self.x -= relative_y
        elif self.direction == 2:
            self.x -= relative_x
            self.y -= relative_y
        elif self.direction == 3:
            self.x += relative_y
            self.y -= relative_x

    def go_to(self, cor_x: int, cor_y: int, direction: int) -> None:
        self.x = cor_x
        self.y = cor_y
        self.direction = direction

    def paint(self):
        self.map_parent.set_node(self.x, self.y, MAP_ENTRY_TYPE.MAP_PATH)
        self.backward()
        self.map_parent.set_node(self.x, self.y, MAP_ENTRY_TYPE.MAP_PATH)
        self.left()
        self.map_parent.set_node(self.x, self.y, MAP_ENTRY_TYPE.MAP_PATH)
        self.forward()
        self.map_parent.set_node(self.x, self.y, MAP_ENTRY_TYPE.MAP_PATH)
        self.forward()
        self.map_parent.set_node(self.x, self.y, MAP_ENTRY_TYPE.MAP_PATH)
        self.right()
        self.map_parent.set_node(self.x, self.y, MAP_ENTRY_TYPE.MAP_PATH)
        self.right()
        self.map_parent.set_node(self.x, self.y, MAP_ENTRY_TYPE.MAP_PATH)
        self.backward()
        self.map_parent.set_node(self.x, self.y, MAP_ENTRY_TYPE.MAP_PATH)
        self.backward()
        self.map_parent.set_node(self.x, self.y, MAP_ENTRY_TYPE.MAP_PATH)
        self.left()
        self.forward()

    def can_move_forward_and_paint(self) -> bool:
        original_x = self.x
        original_y = self.y
        return_bool = False

        self.left(2)
        self.forward(2)
        if self.map_parent.is_wall(self.x, self.y):
            self.right(4)
            if self.map_parent.is_wall(self.x, self.y):
                self.left(2)
                if not self.map_parent.is_edge(self.x, self.y):
                    return_bool = True

        self.go_to(original_x, original_y, self.direction)
        return return_bool

    def move_forward_and_paint(self):
        self.forward()
        self.paint()

    def can_turn_right_move_and_paint(self) -> bool:
        original_x = self.x
        original_y = self.y
        return_bool = False

        self.right(2)
        self.forward(2)
        if self.map_parent.is_wall(self.x, self.y):
            self.backward(4)
            if self.map_parent.is_wall(self.x, self.y):
                self.forward(2)
                if not self.map_parent.is_edge(self.x, self.y):
                    return_bool = True

        self.go_to(original_x, original_y, self.direction)
        return return_bool

    def turn_right_move_and_paint(self):
        self.turn_right()
        self.forward()
        self.paint()

        self.force_forward = 2

    def can_turn_left_move_and_paint(self) -> bool:
        original_x = self.x
        original_y = self.y
        return_bool = False

        self.left(2)
        self.forward(2)
        if self.map_parent.is_wall(self.x, self.y):
            self.backward(4)
            if self.map_parent.is_wall(self.x, self.y):
                self.forward(2)
                if not self.map_parent.is_edge(self.x, self.y):
                    return_bool = True

        self.go_to(original_x, original_y, self.direction)
        return return_bool

    def turn_left_move_and_paint(self):
        self.turn_left()
        self.forward()
        self.paint()

        self.force_forward = 2

    def can_turn_around_move_and_paint(self):
        original_x = self.x
        original_y = self.y
        return_bool = False

        self.backward(2)
        self.left(2)
        if self.map_parent.is_wall(self.x, self.y):
            self.right(4)
            if self.map_parent.is_wall(self.x, self.y):
                return_bool = True

        self.go_to(original_x, original_y, self.direction)
        return return_bool

    def turn_around_move_paint(self):
        self.turn_around()
        self.forward()
        self.paint()

    def try_forward(self, steps: int = 1):
        can_we_move = False
        for i in range(steps):
            if self.can_move_forward_and_paint():
                self.move_forward_and_paint()
                can_we_move = True
            else:
                can_we_move = False
                pass
        return can_we_move

    def try_forward_and_paint(self, steps=1) -> bool:
        can_we_move = True
        for i in range(steps):
            if self.can_move_forward_and_paint():
                self.move_forward_and_paint()
            else:
                can_we_move = False
                break
        return can_we_move

    def try_move(self, route_list: []) -> bool:

        move_forward_steps_choosing_list = [2, 2, 3, 3, 3, 4, 4, 5]  # CONFIG

        can_we_move = False
        movable_direction = []
        if self.can_move_forward_and_paint():
            can_we_move = True
            for i in range(8):  # CONFIG
                movable_direction.append(0)

        if self.can_turn_left_move_and_paint():  # CONFIG
            can_we_move = True
            movable_direction.append(3)

        if self.can_turn_right_move_and_paint():  # CONFIG
            can_we_move = True
            movable_direction.append(1)

        if not can_we_move:
            return False

        random_index = randint(0, len(movable_direction) - 1)

        if movable_direction[random_index] == 0:
            steps = choice(move_forward_steps_choosing_list)
            self.try_forward_and_paint(steps)
        elif movable_direction[random_index] == 1:
            self.turn_right_move_and_paint()
            self.try_forward(6)  # CONFIG
        elif movable_direction[random_index] == 3:
            self.turn_left_move_and_paint()
            self.try_forward(6)  # CONFIG

        route_list.append((self.x, self.y, self.direction))
        return True
