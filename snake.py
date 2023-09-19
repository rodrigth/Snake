import pygame
import random

# Initialiser pygame
pygame.init()

# Couleurs
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Dimensions de l'écran
WIDTH = 640
HEIGHT = 480
BLOCK_SIZE = 80

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

#Image Palmier

PALMIER_IMAGE = pygame.image.load('palmier.png')
PALMIER_IMAGE = pygame.transform.scale(PALMIER_IMAGE, (BLOCK_SIZE, BLOCK_SIZE))

IMAGE1 = pygame.image.load('Flo_negate.png')
IMAGE1 = pygame.transform.scale(IMAGE1, (BLOCK_SIZE, BLOCK_SIZE))

IMAGE2 = pygame.image.load('theo_negate.png')
IMAGE2 = pygame.transform.scale(IMAGE2, (BLOCK_SIZE, BLOCK_SIZE))

class Snake:
    def __init__(self):
        self.positions = [(5, 5), (4, 5), (3, 5)]
        self.direction = RIGHT
        self.grow = False
    
    def update(self):
        head = self.positions[0]
        new_head = ((head[0] + self.direction[0]) % (WIDTH // BLOCK_SIZE),
                    (head[1] + self.direction[1]) % (HEIGHT // BLOCK_SIZE))
        if new_head in self.positions[1:]:
            return True  # Collision avec soi-même
        self.positions = [new_head] + self.positions[:-1]
        if self.grow:
            self.positions.append(self.positions[-1])
            self.grow = False
        return False
    
    def draw(self, screen):
        for index, position in enumerate(self.positions):
            if index % 2 == 0:
                img = IMAGE1
            else:
                img = IMAGE2
            screen.blit(img, (position[0]*BLOCK_SIZE, position[1]*BLOCK_SIZE))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.direction != DOWN:
                self.direction = UP
            elif event.key == pygame.K_DOWN and self.direction != UP:
                self.direction = DOWN
            elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                self.direction = LEFT
            elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                self.direction = RIGHT

class Palmier:
    def __init__(self):
        self.position = (random.randint(0, (WIDTH // BLOCK_SIZE) - 1),
                         random.randint(0, (HEIGHT // BLOCK_SIZE) - 1))
    
    def draw(self, screen):
        screen.blit(PALMIER_IMAGE, (self.position[0]*BLOCK_SIZE, self.position[1]*BLOCK_SIZE))

class Game:
    def __init__(self):
        self.snake = Snake()
        self.Palmier = Palmier()
        self.score = 0
        self.font = pygame.font.Font(None, 36)
    
    def draw_score(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
    
    def draw_centered_message(self, screen, message):
        text = self.font.render(message, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(text, text_rect)
    
    def start_screen(self, screen):
        screen.fill(BLACK)
        self.draw_centered_message(screen, "Welcome to Snake Game! Press any key to start.")
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.KEYUP:
                    waiting = False
        return True

    def game_over_screen(self, screen):
        screen.fill(BLACK)
        self.draw_centered_message(screen, f"Game Over! Your score: {self.score}. Press any key to restart.")
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.KEYUP:
                    waiting = False
        return True

    def play(self, screen):
        if not self.start_screen(screen):
            return False
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                self.snake.handle_event(event)
            
            if self.snake.update():
                if not self.game_over_screen(screen):
                    return False
                self.snake = Snake()
                self.Palmier = Palmier()
                self.score = 0
                continue
            
            if self.snake.positions[0] == self.Palmier.position:
                self.snake.grow = True
                self.Palmier = Palmier()
                self.score += 1
            
            screen.fill(BLACK)
            self.snake.draw(screen)
            self.Palmier.draw(screen)
            self.draw_score(screen)
            pygame.display.flip()
            pygame.time.Clock().tick(10)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    
    game = Game()
    game.play(screen)

if __name__ == "__main__":
    main()