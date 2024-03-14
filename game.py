import pygame

class Game:
    def __init__(self, player):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.running = True
        self.x = 0
        self.y = 0
        self.player = player
        self.color = (player["color"]["red"], player["color"]["green"], player["color"]["blue"])
        self.font = pygame.font.Font('freesansbold.ttf', 10)
        self.clock = pygame.time.Clock()
        self.speed = 3

    def draw(self):
        self.screen.fill((255,255,255))
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 10)
        text = self.font.render(self.player["username"], True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (self.x, self.y-14)
        self.screen.blit(text, textRect)
        self.move()

    def move(self):
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_LEFT]:
            self.x -= self.speed
        if user_input[pygame.K_RIGHT]:
            self.x += self.speed
        if user_input[pygame.K_UP]:
            self.y -= self.speed
        if user_input[pygame.K_DOWN]:
            self.y += self.speed

    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.draw()
            pygame.display.update()