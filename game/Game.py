import pygame
from game.Player import Player
from game.constants import WHITE, SIZE
from game.Food import Food


class Board:
    def __init__(self, display: pygame.display):
        self.width = SIZE[0]
        self.height = SIZE[1]
        self.background_color = WHITE
        self.display = display
        self.screen = display.set_mode(SIZE)
        self.screen.fill(self.background_color)
        self.display.set_caption("Evolution Game")

    def reset(self):
        self.screen.fill(self.background_color)

    def update(self):
        self.display.update()


class Game:
    def __init__(self):
        self.board = Board(display=pygame.display)
        self.players: list[Player] = []
        self.foods: list[Food] = []

        self.going = False

    def set_population(self, nb_player):
        for i in range(nb_player):
            self.players.append(Player(self.board.width, self.board.height))

    def start(self):
        self.going = True
        while self.going:
            pygame.time.delay(30)
            self.handle_events()  # Disconnection event or more
            self.board.reset()
            self.update_player_moves()

            self.update_food()
            self.spawn_food()
            self.draw_food()
            self.board.update()
        pygame.quit()

    def draw_food(self):
        for food in self.foods:
            food.draw(self.board.screen)

    def update_food(self):
        self.foods = [food for food in self.foods if not food.destroy()]

    def spawn_food(self):
        food = Food(spawn_chance=0.1, max_food = 10) # 1% chance to spawn a food and max 10 food
        has_spawned = food.spawn( amount = len(self.foods), board_width= self.board.width, board_height= self.board.height)
        if has_spawned : self.foods.append(food)

    def update_player_moves(self):
        for player in self.players:
            if player.is_too_old(): # If the player is too old, he dies
                self.players.remove(player)
                continue
            closest_food = player.find_closest_food(self.foods)
            player.move(closest_food, self.board.width, self.board.height)
            if closest_food and player.eat(closest_food):
                player.stop()
                self.foods.remove(closest_food)
            player.draw(draw = pygame.draw,screen = self.board.screen)

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.going = False


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.set_population(2)
    game.start()
