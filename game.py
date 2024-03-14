import json

import pygame
import socket
import threading
class Game:
    def __init__(self, player):
        pygame.init()
        host = "0.0.0.0"
        #68.7.149.165
        port = 8066
        self.screen = pygame.display.set_mode((1200, 800))
        self.running = True
        self.x = 0
        self.y = 0
        self.player = player
        self.color = (player["color"]["red"], player["color"]["green"], player["color"]["blue"])
        self.font = pygame.font.Font('freesansbold.ttf', 10)
        self.clock = pygame.time.Clock()
        self.speed = 3
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))
        self.state = None
        update_thread = threading.Thread(target=self.update)
        update_thread.start()

    def update(self):
        while self.running:
            print("Updating")
            data = self.server.recv(1024).decode("utf-8")
            self.state = json.loads(data)
            print(data)

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
        if user_input[pygame.K_LEFT] and self.x > 10:
            self.x -= self.speed
        if user_input[pygame.K_RIGHT] and self.x < 1200-10:
            self.x += self.speed
        if user_input[pygame.K_UP] and self.y > 10:
            self.y -= self.speed
        if user_input[pygame.K_DOWN] and self.y < 800-10:
            self.y += self.speed
        position = json.dumps({"x": self.x, "y": self.y, "username": self.player["username"]})
        try:
            self.server.send(position.encode("utf-8"))
        except BrokenPipeError as e:
            print(f"Broken pipe error: {e}")
    def run(self):
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.draw()
            pygame.display.update()