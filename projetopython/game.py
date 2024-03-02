import pygame
import random

# Inicialize o Pygame
pygame.init()

# Defina as dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Defina cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Defina a velocidade do jogador
PLAYER_SPEED = 5

# Crie a classe Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED

# Inicialize a tela e o relógio
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Game")
clock = pygame.time.Clock()

# Crie os grupos de sprites
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Loop principal do jogo
running = True
while running:
    # Mantenha o loop rodando na velocidade desejada
    clock.tick(60)

    # Processamento de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualize
    all_sprites.update()

    # Renderize
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

# Encerre o Pygame
pygame.quit()

