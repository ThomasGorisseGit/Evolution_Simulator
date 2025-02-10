import random
from game.constants import BLUE, lGREEN


class Player:
    def __init__(self, board_width, board_height):
        self.speed = 5
        self.size = random.randint(10, 20)
        self.max_size = random.randint(45,55)
        self.spawn_position = (board_width//2, board_height//2)
        self.color = BLUE
        self.x, self.y = self.spawn_position
        self.direction_x, self.direction_y = 0, 0
        self.vision_range = self.size+50
        self.score = 1
        self.lifetime = 0
        self.time_last_eat = 0
    def find_closest_food(self, foods):
        """
        Trouve la nourriture la plus proche du joueur.
        """
        if not foods :
            return None  # Aucune nourriture sur la carte
        closest_food = []

        for food in foods:
            if food.x is None or food.y is None:
                return None
            if abs(self.x - food.x) < self.vision_range and abs(self.y - food.y) < self.vision_range:
                closest_food.append(food)
        if not closest_food:
            return None
        return min(closest_food, key=lambda food: abs(self.x - food.x) + abs(self.y - food.y))
    def stop(self):
        self.direction_x, self.direction_y = 0, 0
    def eat(self, food):
        """
        Check if the player is eating the food
        :param food: the food to check
        :return: True if the player is eating the food, False otherwise
        """
        if food is None or food.x is None or food.y is None:
            return False
        if (self.x < food.x + food.size and self.x + self.size > food.x and
            self.y < food.y + food.size and self.y + self.size > food.y):
            self.score += 1
            self.time_last_eat = 0
            return True
        return False

    def get_direction(self, food):
        """
        Get a random direction for the player
        :return: an x, y tuple
        """
        if random.random() < 0.1:
            if food is None or food.x is None or food.y is None:
                return random.choice([(self.speed, 0), (-self.speed, 0), (0, self.speed), (0, -self.speed)])
            if food:
                return self.direction_to_food(food)
        return self.direction_x, self.direction_y

    def direction_to_food(self, food):
        if food.x > self.x and food.y > self.y:
            return self.speed//2, self.speed//2
        if food.x > self.x and food.y < self.y:
            return self.speed//2, -self.speed//2
        if food.x < self.x and food.y > self.y:
            return -self.speed//2, self.speed//2
        if food.x < self.x and food.y < self.y:
            return -self.speed//2, -self.speed//2
        if food.x == self.x and food.y > self.y:
            return 0, self.speed
        if food.x == self.x and food.y < self.y:
            return 0, -self.speed
        if food.x > self.x and food.y == self.y:
            return self.speed, 0
        if food.x < self.x and food.y == self.y:
            return -self.speed, 0
        return 0, 0
    def move(self,food,board_width, board_height):
        """
        Move the player in a random direction
        """
        self.direction_x, self.direction_y = self.get_direction(food)

        self.x += self.direction_x
        self.y += self.direction_y
        self.x = max(0, min(board_width - self.size, self.x))
        self.y = max(0, min(board_height - self.size, self.y))

    def draw(self,draw, screen):
        """
        Draw the player on the screen
        """
        # draw range in low opacity green
        draw.circle(screen, lGREEN, (self.x + self.size//2, self.y + self.size//2), self.vision_range, 1)
        screen.fill(self.color, (self.x, self.y, self.size, self.size))
        # draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
    def is_too_old(self):
        self.lifetime += 1
        self.time_last_eat += 1
        self.color = (0, 0, max(0, 255 - self.time_last_eat//2))
        if self.time_last_eat > 500:
            # The player is not eating enough and die
            print("Player is dead")
            return True
        if self.size<self.max_size and self.time_last_eat < 100:
            self.size += 0.1
            self.vision_range = self.size+50
        return False