import pygame


class GameCell(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surf = pygame.Surface((width, height))
        # fill surf with a white bg and black outline
        self.surf.fill((255, 255, 255), (1, 1, width - 2, height - 2))
        self.rect = self.surf.get_rect(center=(x + width / 2, y + height / 2))


sprites = pygame.sprite.Group()
# make a grid of GameCells 10x10
for i in range(5):
    for j in range(5):
        sprites.add(GameCell(i * 40 + 100, j * 40 + 100, 40, 40))


def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("quantum comouter 👍")
    running = True

    screen.fill((255, 255, 255))

    for entity in sprites:
        screen.blit(entity.surf, entity.rect)

    clock = pygame.time.Clock()

    while running:
        clock.tick(30)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for entity in sprites:
                    if isinstance(entity, GameCell):
                        if entity.rect.collidepoint(pos):
                            entity.surf.fill((0, 0, 0))
                            screen.blit(entity.surf, entity.rect)
                            pygame.display.update()
                            break


if __name__ == "__main__":
    # call the main function
    main()
