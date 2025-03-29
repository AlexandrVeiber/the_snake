import os
import pygame
from random import randint

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки
SPEED = 20

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()

# Путь к файлу рекорда
HIGH_SCORE_FILE = 'high_score.txt'


def load_high_score():
    """Загружает рекорд из файла."""
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'r') as file:
            return int(file.read().strip())
    return 0


def save_high_score(high_score):
    """Сохраняет рекорд в файл."""
    with open(HIGH_SCORE_FILE, 'w') as file:
        file.write(str(high_score))


def display_score(score):
    """Отображает текущий счет на экране."""
    font = pygame.font.SysFont('Arial', 24)
    score_surface = font.render(f'Счет: {score}', True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0)):
        self.position = position
        self.body_color = (0, 0, 0)

    def draw(self):
        """Метод для отрисовки объекта. Должен быть переопределен."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self):
        super().__init__(self.randomize_position())
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Устанавливает случайное положение яблока."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return x, y

    def draw(self):
        """Отрисовывает яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self):
        initial_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(initial_position)
        self.length = 1
        self.positions = [initial_position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)

        if new_head in self.positions[1:]:
            self.reset()
            return

        self.last = self.positions[-1] if len(self.positions) > 1 else None
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.last = None

    def draw(self):
        """Отрисовывает змейку."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(snake, high_score):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score(high_score)
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                save_high_score(high_score)
                pygame.quit()
                raise SystemExit
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            if event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            if event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            if event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры."""
    pygame.init()
    snake = Snake()
    apple = Apple()
    high_score = load_high_score()

    while True:
        clock.tick(SPEED)
        handle_keys(snake, high_score)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple = Apple()
            high_score = max(high_score, snake.length - 1)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        display_score(snake.length - 1)
        pygame.display.set_caption(f'Змейка - Рекорд: {high_score}')
        pygame.display.update()


if __name__ == '__main__':
    main()
