import pygame
import random
import sys

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
CAR_WIDTH = 80
CAR_HEIGHT = 160
ROAD_WIDTH = 600
FPS = 60
WHITE = (255, 255, 255)

class Car:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - CAR_WIDTH // 2
        self.y = SCREEN_HEIGHT - CAR_HEIGHT - 10
        self.speed_x = 0
        self.speed_y = 0
        self.image = pygame.transform.scale(pygame.image.load('car_nfs.png'), (CAR_WIDTH, CAR_HEIGHT))
        self.rect = pygame.Rect(self.x, self.y, CAR_WIDTH, CAR_HEIGHT)

    def move_left(self):
        if self.x > SCREEN_WIDTH // 4:
            self.speed_x = -5

    def move_right(self):
        if self.x < SCREEN_WIDTH // 2 - CAR_WIDTH:
            self.speed_x = 5

    def stop_x(self):
        self.speed_x = 0

    def update_position(self):
        self.x += self.speed_x
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Road:
    def __init__(self):
        self.y = 0
        self.speed = 5
        self.image = pygame.image.load('road_nfs.jpg')
        self.image = pygame.transform.scale(self.image, (ROAD_WIDTH, SCREEN_HEIGHT))

    def move(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0

    def draw(self):
        screen.blit(self.image, (SCREEN_WIDTH // 4, self.y))
        screen.blit(self.image, (SCREEN_WIDTH // 4, self.y - SCREEN_HEIGHT))


class HurdleManager:
    def __init__(self):
        self.hurdles = []
        self.speed = 5
        self.spawn_delay = 1000  # milliseconds
        self.last_spawn_time = pygame.time.get_ticks()

    def create_hurdle(self):
        now = pygame.time.get_ticks()
        if now - self.last_spawn_time > self.spawn_delay:
            size = random.randint(40, 80)
            x = random.randint(SCREEN_WIDTH // 4, SCREEN_WIDTH // 2 - size)
            y = -size
            self.hurdles.append(pygame.Rect(x, y, size, size))
            self.last_spawn_time = now

    def move_hurdles(self):
        for hurdle in self.hurdles[:]:
            hurdle.y += self.speed
            if hurdle.y > SCREEN_HEIGHT:
                self.hurdles.remove(hurdle)

    def draw(self):
        for hurdle in self.hurdles:
            pygame.draw.rect(screen, (255, 0, 0), hurdle)


class Game:
    def __init__(self):
        self.car = Car()
        self.road = Road()
        self.hurdle_manager = HurdleManager()
        self.score = 0
        self.game_over = False
        self.play_background_music()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if not self.game_over:
            if keys[pygame.K_LEFT]:
                self.car.move_left()
            elif keys[pygame.K_RIGHT]:
                self.car.move_right()
            else:
                self.car.stop_x()

        if self.game_over and keys[pygame.K_r]:
            self.__init__()

    def check_collision(self):
        for hurdle in self.hurdle_manager.hurdles:
            if self.car.rect.colliderect(hurdle):
                self.game_over = True

    def update_score(self):
        if not self.game_over:
            self.score += 1

    def display_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(self.score), True, WHITE)
        screen.blit(score_text, (10, 10))

    def display_game_over(self):
        font = pygame.font.Font(None, 72)
        over_text = font.render("Game Over!", True, (255, 0, 0))
        screen.blit(over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))

        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render("Press R to Restart", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20))

    def run(self):
        clock = pygame.time.Clock()

        while True:
            self.handle_events()

            if not self.game_over:
                self.road.move()
                self.hurdle_manager.create_hurdle()
                self.hurdle_manager.move_hurdles()
                self.car.update_position()
                self.check_collision()
                self.update_score()

            screen.fill((0, 0, 0))
            self.road.draw()
            self.hurdle_manager.draw()
            self.car.draw()
            self.display_score()

            if self.game_over:
                self.display_game_over()

            pygame.display.update()
            clock.tick(FPS)

    def play_background_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load('background_music.wav')
        pygame.mixer.music.play(-1)


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Need for Speed - Car Racing Game")

game = Game()
game.run()