import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("YANDEXARIA - Главное меню")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

font = pygame.font.SysFont(None, 55)
button_font = pygame.font.SysFont(None, 40)

title_text = font.render("YANDEXARIA", True, BLACK)

class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.hovered and mouse_pressed[0]

def main_menu():
    button_width, button_height = 300, 60
    multiplayer_button = Button(
        WIDTH // 2 - button_width // 2,
        HEIGHT // 2 - button_height - 20,
        button_width,
        button_height,
        "Многопользовательская игра",
        button_font,
        GREEN,
        GRAY
    )
    singleplayer_button = Button(
        WIDTH // 2 - button_width // 2,
        HEIGHT // 2 + 20,
        button_width,
        button_height,
        "Одиночная игра",
        button_font,
        RED,
        GRAY
    )

    while True:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        multiplayer_button.check_hover(mouse_pos)
        singleplayer_button.check_hover(mouse_pos)

        if multiplayer_button.hovered:
            multiplayer_button.rect.y, singleplayer_button.rect.y = singleplayer_button.rect.y, multiplayer_button.rect.y

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        multiplayer_button.draw(screen)
        singleplayer_button.draw(screen)

        if multiplayer_button.is_clicked(mouse_pos, mouse_pressed):
            return "multiplayer"
        if singleplayer_button.is_clicked(mouse_pos, mouse_pressed):
            return "singleplayer"

        pygame.display.flip()