import pygame
import sys
import random

pygame.init()

window_size = (800, 600)
pygame.display.set_caption("Slot Machine")
screen = pygame.display.set_mode(window_size)
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, window_size)

symbols = ["bell.png", "cherry.png", "lemon.png", "7.png"]
static_image_paths = ["Start.png", "machine.png", "stop.png", "spin.png", "win.png"]

static_images = []
for path in static_image_paths:
    try:
        image = pygame.image.load(path)
        static_images.append(image)
    except:
        sys.exit()

start_image = pygame.transform.scale(static_images[0], (100, 100))
machine_image = pygame.transform.scale(static_images[1], (1200, 1400))
stop_image = pygame.transform.scale(static_images[2], (120, 120))
spin_image = pygame.transform.scale(static_images[3], (250, 250))
win_image = pygame.transform.scale(static_images[4], (150,150))

symbol_images = []
for symbol in symbols:
    try:
        image = pygame.transform.scale(pygame.image.load(symbol), (100, 100))
        symbol_images.append(image)
    except:
        sys.exit()

start_position = (660, 450)
stop_position = (650, 300)
machine_position = (-200,-400)
spin_position = (287, 214)
win_position = (335, 0)

reel_positions = [(machine_position[0] + 560, machine_position[1] + 690),
                  (machine_position[0] + 450, machine_position[1] + 690),
                  (machine_position[0] + 660, machine_position[1] + 690)]

animation_started = [False] * len(reel_positions)
spinning = False
stop_count = 0
random_symbols = [None] * len(reel_positions)

won = False
show_image = True
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_position[0] <= event.pos[0] <= start_position[0] + start_image.get_width() and \
               start_position[1] <= event.pos[1] <= start_position[1] + start_image.get_height():
                show_image = False
                spinning = True
                animation_started = [False] * len(reel_positions)
                stop_count = 0
                won = False

            elif stop_position[0] <= event.pos[0] <= stop_position[0] + stop_image.get_width() and \
                 stop_position[1] <= event.pos[1] <= stop_position[1] + stop_image.get_height():
                if spinning:
                    animation_started[stop_count % len(reel_positions)] = True
                    stop_count += 1
                    if stop_count == len(reel_positions):
                        won = all(symbol == random_symbols[0] for symbol in random_symbols)

    screen.blit(background_image, (0, 0))
    screen.blit(machine_image, machine_position)
    screen.blit(start_image, start_position)
    screen.blit(stop_image, stop_position)
    if show_image:
        screen.blit(spin_image,spin_position)

    for i, position in enumerate(reel_positions):
        if spinning and not animation_started[i]:
            random_symbols[i] = random.choice(symbol_images)
            screen.blit(random_symbols[i], position)
        elif animation_started[i]:
            screen.blit(random_symbols[i], position)

    pygame.display.flip()
    pygame.time.delay(50)

    if won:
        screen.blit(win_image, win_position)
        pygame.display.flip()
        pygame.time.delay(3000)
        won = False

