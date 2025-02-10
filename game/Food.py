from game.constants import RED
import random

class Food:
    def __init__(self,spawn_chance, max_food):
        self.size = 10
        self.color = RED
        self.x = None
        self.y = None
        self.spawn_chance = spawn_chance
        self.max_food = max_food
        self.max_duration = 255
    def destroy(self):
        self.max_duration -= 1
        self.color = (max(0,self.max_duration), 0, 0)
        return self.max_duration < 100
    def spawn(self,amount, board_width, board_height):
        random_number = random.random()
        if random_number < self.spawn_chance and amount < self.max_food:
            self.x = random.randint(0, board_width - self.size)
            self.y = random.randint(0, board_height - self.size)
            return True
        return False
    def draw(self, screen):
        if self.x is not None and self.y is not None:
            screen.fill(self.color, (self.x, self.y, self.size, self.size))
