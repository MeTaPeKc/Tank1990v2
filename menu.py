import pygame
import sys
import os

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Tank1990")

button_color = (255, 255, 255)
hover_color = (200, 200, 200)

# Создайте функцию для создания кнопок
def create_button(text, x, y, width, height, color):
    font = pygame.font.Font(None, 40)
    text = font.render(text, True, (0, 0, 0))
    button = pygame.Surface((width, height))
    button.fill(color)
    button.blit(text, (button.get_width()//2 - text.get_width()//2, button.get_height()//2 - text.get_height()//2))
    screen.blit(button, (x, y))
    return button.get_rect(x=x, y=y, width=width, height=height)

# Создайте кнопки
play_button_rect = create_button("Играть", screen_width//2 - 150, screen_height//2 - 50, 300, 100, button_color)
exit_button_rect = create_button("Выход", screen_width//2 - 150, screen_height//2 + 100, 300, 100, button_color)

# Запустите игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Обработка нажатия на кнопки
            if play_button_rect.collidepoint(pygame.mouse.get_pos()):
                os.system('python main.py') # Открывает файл main.py
            elif exit_button_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.quit()
                sys.exit()

    # Отрисовка кнопок
    if play_button_rect.collidepoint(pygame.mouse.get_pos()):
        create_button("Играть", screen_width//2 - 150, screen_height//2 - 50, 300, 100, hover_color)
    else:
        create_button("Играть", screen_width//2 - 150, screen_height//2 - 50, 300, 100, button_color)

    if exit_button_rect.collidepoint(pygame.mouse.get_pos()):
        create_button("Выход", screen_width//2 - 150, screen_height//2 + 100, 300, 100, hover_color)
    else:
        create_button("Выход", screen_width//2 - 150, screen_height//2 + 100, 300, 100, button_color)

    pygame.display.update()
