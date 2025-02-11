import random
from game.constants import BLUE, lGREEN


class Player:
    def __init__(self, board_width, board_height):
        self.spawn_position = (board_width//2, board_height//2)
        self.color = BLUE
        self.x, self.y = self.spawn_position
        self.direction_x, self.direction_y = 0, 0

        self.stats = PlayerStats()

    def find_closest_food(self, foods):
        """
        search for the closest food
        """
        if not foods :
            return None  # No food in vision
        closest_food = []

        for food in foods:
            if food.x is None or food.y is None:
                return None
            if abs(self.x - food.x) < self.stats.vision and abs(self.y - food.y) < self.stats.vision:
                closest_food.append(food)
        if not closest_food:
            return None
        return min(closest_food, key=lambda f: abs(self.x - f.x) + abs(self.y - f.y))
    def stop(self):
        self.direction_x, self.direction_y = 0, 0
    def eat(self, food):
        """
        :param food: the food to check
        :return: True if the player is eating the food, False otherwise
        """
        if food is None or food.x is None or food.y is None:
            return False
        if (self.x < food.x + food.size and self.x + self.stats.size > food.x and
                self.y < food.y + food.size and self.y + self.stats.size > food.y):
            self.stats.score += 1
            self.stats.time_last_eat = 0
            return True
        return False

    def get_direction(self, food):
        """
        Get a random direction for the player
        :return: an x, y tuple
        """
        if random.random() < 0.1:
            if food is None or food.x is None or food.y is None:
                return random.choice([(self.stats.speed, 0), (-self.stats.speed, 0), (0, self.stats.speed), (0, -self.stats.speed)])
            if food:
                return self.direction_to_food(food)
        return self.direction_x, self.direction_y

    def direction_to_food(self, food):
        if food.x > self.x and food.y > self.y:
            return self.stats.speed//2, self.stats.speed//2
        if food.x > self.x and food.y < self.y:
            return self.stats.speed//2, -self.stats.speed//2
        if food.x < self.x and food.y > self.y:
            return -self.stats.speed//2, self.stats.speed//2
        if food.x < self.x and food.y < self.y:
            return -self.stats.speed//2, -self.stats.speed//2
        if food.x == self.x and food.y > self.y:
            return 0, self.stats.speed
        if food.x == self.x and food.y < self.y:
            return 0, -self.stats.speed
        if food.x > self.x and food.y == self.y:
            return self.stats.speed, 0
        if food.x < self.x and food.y == self.y:
            return -self.stats.speed, 0
        return 0, 0
    def move(self,food,board_width, board_height):
        """
        Move the player in a random direction
        """
        self.direction_x, self.direction_y = self.get_direction(food)

        self.x += self.direction_x
        self.y += self.direction_y
        self.x = max(0, min(board_width - self.stats.size, self.x))
        self.y = max(0, min(board_height - self.stats.size, self.y))

    def draw(self,draw, screen):
        """
        Draw the player on the screen
        """
        # draw range in low opacity green
        draw.circle(screen, lGREEN, (self.x + self.stats.size//2, self.y + self.stats.size//2), self.stats.vision, 1)
        screen.fill(self.color, (self.x, self.y, self.stats.size, self.stats.size))
        # draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
    def is_too_old(self):
        self.stats.update()
        self.color = self.stats.get_color()
        print(self.stats)
        return self.stats.starvation()

class PlayerStats:
    def __init__(self):
        self.score = 0
        self.lifetime = 0
        self.max_lifetime = 0
        self.time_last_eat = 0
        self.max_size = random.randint(45,55)
        self.min_size = random.randint(10, 20)
        self.size = self.min_size
        self.min_vision = random.randint(40, 50)
        self.max_vision = random.randint(90, 110)
        self.vision = self.min_vision
        self.speed = self.calculate_speed()
        # TODO : add energy consumption
    def calculate_speed(self):
        self.speed = 50/((self.size//5) + (self.vision//15))
        return self.speed

    def update(self):
        self.lifetime += 1
        self.time_last_eat += 1
        self.calculate_speed()

        if self.size < self.max_size and self.growth():
            self.size += 0.1
        if self.vision < self.max_vision and self.growth():
            self.vision += 0.1

    def starvation(self):
        return self.time_last_eat > 500

    def growth(self):
        return self.time_last_eat < 100 and self.score > 0

    def get_color(self):
        return 0, 0, max(0, 255 - self.time_last_eat // 2)
    def __str__(self):
        return f"Player Stats: {self.speed} - {self.size} - {self.vision}"