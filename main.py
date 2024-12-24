import pygame, sys, random
from pygame.math import Vector2


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw(self):
        pos_x = self.pos.x * cell_size
        pos_y = self.pos.y * cell_size
        fruit_rect = pygame.Rect(pos_x, pos_y, cell_size, cell_size)
        screen.blit(self.eat, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        self.eat_img = [
            pygame.image.load('Image/banana.png').convert_alpha(),
            pygame.image.load('Image/cherry.png').convert_alpha(),
            pygame.image.load('Image/green-apple.png').convert_alpha(),
            pygame.image.load('Image/red-grape.png').convert_alpha(),
            pygame.image.load('Image/watermelon.png').convert_alpha(),
            pygame.image.load('Image/strawberry.png').convert_alpha()
        ]
        self.eat = pygame.transform.scale(self.eat_img[random.randint(0, 5)], (cell_size, cell_size))


class SNAKE:
    def __init__(self):
        self.body = [Vector2(10, 10), Vector2(9, 10), Vector2(8, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

        self.head_up = pygame.image.load('Image/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Image/head_down.png').convert_alpha()
        self.head_left = pygame.image.load('Image/head_left.png').convert_alpha()
        self.head_right = pygame.image.load('Image/head_right.png').convert_alpha()

        self.tail_up = pygame.image.load('Image/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Image/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('Image/tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('Image/tail_right.png').convert_alpha()

        self.body_vertical = pygame.image.load('Image/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Image/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Image/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Image/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Image/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Image/body_bl.png').convert_alpha()

    def draw_snake(self):
        self.update_head()
        self.tail_update()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)
                    else:
                        pygame.draw.rect(screen, GREEN_DARK, block_rect)

    def update_head(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up

    def tail_update(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_sound(self):
        self.crunch_sound.set_volume(0.2)
        self.crunch_sound.play()

    def snake_restart(self):
        self.body = [Vector2(10, 10), Vector2(9, 10), Vector2(8, 10)]
        self.direction = Vector2(0, 0)


class MAIN:
    def __init__(self):
        self.fruit = FRUIT()
        self.snake = SNAKE()

    def draw_elements(self):
        self.fruit.draw()
        self.snake.draw_snake()
        self.draw_score()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_sound()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.snake_restart()

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(f'Score: {score_text}',True,YELLOW)
        score_x = 155
        score_y = 60
        score_rect = score_surface.get_rect(center=(score_x,score_y))
        screen.blit(score_surface, score_rect)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 150, 0)
BLUE = (0, 0, 255)
YELLOW = (200, 200, 0)
GREEN_DARK = (0, 100, 0)

pygame.init()
cell_size = 40
cell_number = 30
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

pygame.mixer.music.load('Sound/HT2.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

grass_img = pygame.image.load('Image/Grass.jpg').convert_alpha()
grass_img = pygame.transform.scale(grass_img, (cell_size * cell_number, cell_size * cell_number))
grass_rect = pygame.Rect(0, 0, cell_size * cell_number, cell_size * cell_number)

game_font = pygame.font.Font('Font/papyrus-pixel_1.ttf', 90)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_s:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_a:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_d:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)

    screen.blit(grass_img, grass_rect)
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)