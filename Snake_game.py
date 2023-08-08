import pygame, sys, random
import pygame.time
from pygame import Vector2

pygame.init()

title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)
intro_font = pygame.font.Font(None, 70)

dark_green = (43, 51, 24)
beige = (205, 198, 115)

cell_size = 29
num_of_cells = 25  # cell size * number of cells will cover an area of 750x750 area pixels

OFFSET = 74  # width of the border

class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)
        self.add_segment = False
        self.eat_sound = pygame.mixer.Sound('eat.mp3')
        self.wall_hit_sound = pygame.mixer.Sound('wall.mp3')

    def draw(self):
        for segment in self.body:
            segment_rect = (OFFSET + segment.x * cell_size, OFFSET + segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, dark_green, segment_rect, 0, 11)

    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1]

    def reset(self):
        self.body = [Vector2(6,9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1,0)

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_new_position(snake_body)

    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        screen.blit(food_surf, food_rect)

    def generate_position(self):
        x = random.randint(0, num_of_cells - 1)
        y = random.randint(0, num_of_cells - 1)
        return (Vector2(x, y))

    def generate_new_position(self, snake_body):  # checks if food spawns on top of the snake
        position = self.generate_position()
        while position in snake_body:
            position = self.generate_position()
        return position

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "STOP"
        self.score = 0
        self.backgroud_music = pygame.mixer.Sound('background.wav')

    def draw(self):
        self.food.draw()
        self.snake.draw()

    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.check_collision()
            self.check_collision_with_edges()
            self.check_collision_body()

    def check_collision(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_new_position(self.snake.body)
            self.snake.add_segment = True
            self.score += 1
            self.snake.eat_sound.play()

    def check_collision_with_edges(self):
        if self.snake.body[0].x == num_of_cells or self.snake.body[0].x == -1:   # checks if snake passess the x-axis of the grid
            self.game_over()
        if self.snake.body[0].y == num_of_cells or self.snake.body[0].y == -1:   # checks if snake passess the y-axis of the grid
            self.game_over()

    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_new_position(self.snake.body)
        self.state = "STOP"
        self.score = 0
        self.snake.wall_hit_sound.play()

    def check_collision_body(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()

screen = pygame.display.set_mode((2*OFFSET + cell_size * num_of_cells, 2*OFFSET + cell_size * num_of_cells))
pygame.display.set_caption("Pixel Python")
clock = pygame.time.Clock()

game = Game()
food_surf = pygame.image.load('food.png')

snake_update = pygame.USEREVENT  # custom user event
pygame.time.set_timer(snake_update, 150)  # timer that triggers snake_update every 200 milliseconds
intro_screen = pygame.Rect(0, 0, 2*OFFSET + cell_size * num_of_cells,  2*OFFSET + cell_size * num_of_cells)

game.backgroud_music.play(loops=-1)
game.backgroud_music.set_volume(0.6)

while True:
    for currevent in pygame.event.get():
        if currevent.type == snake_update:
            game.update()
        if currevent.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game.state == "STOP":
        pygame.draw.rect(screen, dark_green, intro_screen)
        intro_surface = intro_font.render('Welcome to Pixel Python', True, beige)
        screen.blit(intro_surface, (150, 370))
        intro_surface2 = intro_font.render('Press any key to start!', True, beige)
        screen.blit(intro_surface2, (180, 420))

    if currevent.type == pygame.KEYDOWN:
        game.state = "RUNNING"  # any key starts the game
        if currevent.key == pygame.K_UP and game.snake.direction != (0, 1):
                game .snake.direction = Vector2(0, -1)
        if currevent.key == pygame.K_DOWN and game.snake.direction != (0, -1):
                game.snake.direction = Vector2(0, 1)
        if currevent.key == pygame.K_LEFT and game.snake.direction != (1, 0):
                game.snake.direction = Vector2(-1, 0)
        if currevent.key == pygame.K_RIGHT and game.snake.direction != (-1, 0):
                game.snake.direction = Vector2(1, 0)

    # if game is active
    if game.state == 'RUNNING':
        screen.fill(beige)
        pygame.draw.rect(screen, dark_green,
                         (OFFSET-5, OFFSET -5, cell_size*num_of_cells + 10, cell_size * num_of_cells + 10), 5)
        game.draw()
        title_surface = title_font.render('Pixel Python', True, dark_green)
        screen.blit(title_surface, (OFFSET + 250 , 20))
        score_surface = score_font.render('Score = ' + (str(game.score)), True, dark_green)
        screen.blit(score_surface, (OFFSET-5, OFFSET + cell_size * num_of_cells + 10))

    pygame.display.update()
    clock.tick(60)
