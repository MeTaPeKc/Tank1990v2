import pygame
import os

# Инициализируем pygame
pygame.init()

# Устанавливаем размеры окна
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption("Tank1990")

# Загружаем изображения для кнопок
play_button_img = pygame.image.load("PNG/button/play_button.png")
map1_button_img = pygame.image.load("PNG/button/map1_button.png")
map2_button_img = pygame.image.load("PNG/button/map2_button.png")

# Создаем функцию для запуска игры
def start_game(map_file):
    os.system("python " + map_file)

# Создаем функцию для создания кнопок
def create_button(img, x, y, action=None):
    button_rect = img.get_rect()
    button_rect.x = x
    button_rect.y = y
    screen.blit(img, button_rect)
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    if button_rect.collidepoint(mouse_pos) and mouse_click[0] == 1:
        if action:
            action()

# Создаем функцию для запуска меню
def menu():
    while True:
        # Отрисовываем фон меню
        screen.fill((0, 0, 0))

        # Создаем кнопки и привязываем функции к их действиям
        create_button(map1_button_img, 300, 200, lambda: start_game("main.py"))
        create_button(map2_button_img, 300, 300, lambda: start_game("main1.py"))

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()

# Запускаем меню
menu()

play_button_img = pygame.image.load("PNG/button/play_button.png")
map1_button_img = pygame.image.load("PNG/button/map1_button.png")
map2_button_img = pygame.image.load("PNG/button/map2_button.png")