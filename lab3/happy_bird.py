import time

import pygame
import random

pygame.init()

width = 750
height = 600
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Happy Eastern Bluebird")

clock = pygame.time.Clock()

sky = pygame.image.load("images/sky.png").convert_alpha()

bird_image = pygame.image.load("images/bird.png").convert_alpha()

lower_pipe_image = pygame.image.load("images/lower_pipe.png").convert_alpha()
upper_pipe_image = pygame.image.load("images/upper_pipe.png").convert_alpha()

bird_max_fall = 20
bird_max_jump = -90
bird_jump = -17

score_font = pygame.font.Font('freesansbold.ttf', 32)


def play_game(pipe_speed, min_space):
    pygame.event.clear()
    score = 0
    done = False

    bird_rect = bird_image.get_rect(center=(50, 100))
    bird_y_speed = 0
    grav_acc = 0

    pipe_pairs = [
        (pygame.image.load("images/lower_pipe.png").convert_alpha().get_rect(topleft=(800, 500)),
         pygame.image.load("images/upper_pipe.png").convert_alpha().get_rect(bottomleft=(800, 150))),
        (pygame.image.load("images/lower_pipe.png").convert_alpha().get_rect(topleft=(1200, 400)),
         pygame.image.load("images/upper_pipe.png").convert_alpha().get_rect(bottomleft=(1200, 50)))
    ]

    screen.blit(sky, (0, 0))
    screen.blit(bird_image, bird_rect)
    pygame.display.flip()

    print("Start the game by pressing space!")
    start = False
    while not start:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                start = True
                break

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LALT:
                time.sleep(10)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_y_speed = bird_jump
                grav_acc = 0

        grav_acc += 1
        bird_rect.y += bird_y_speed
        # bird_y_speed = min(bird_max_fall, bird_y_speed + 1 + min(grav_acc, 25) **  1.3)
        bird_y_speed = min(bird_max_fall, bird_y_speed + 2 + (grav_acc // 10) ** 2)

        if bird_rect.top <= 0 or bird_rect.bottom >= height:
            print("Oh no! The bird is out of the picture!")
            done = True

        for lower_pipe_rect, upper_pipe_rect in pipe_pairs:
            lower_pipe_rect.x -= pipe_speed
            upper_pipe_rect.x -= pipe_speed

            if bird_rect.colliderect(lower_pipe_rect):
                print("Oh no! The bird crashed into the lower pipe!")
                done = True

            if bird_rect.colliderect(upper_pipe_rect):
                print("Oh no! The bird crashed into the lower pipe!")
                done = True

            if lower_pipe_rect.right < 0:
                score += 1
                lower_pipe_rect.left = width + 50
                upper_pipe_rect.left = width + 50
                upper_pipe_height = random.randint(0, lower_pipe_rect.height - min_space // 2)
                upper_pipe_rect.bottom = upper_pipe_height

                lower_pipe_rect.top = max(
                    upper_pipe_height + min_space + random.randint(0, 80),
                    height - lower_pipe_rect.height + 1
                )

        screen.blit(sky, (0, 0))

        screen.blit(bird_image, bird_rect)

        for lower_pipe_rect, upper_pipe_rect in pipe_pairs:
            screen.blit(lower_pipe_image, lower_pipe_rect)
            screen.blit(upper_pipe_image, upper_pipe_rect)

        score_text = score_font.render(str(score), True, (0, 0, 0))
        score_rect = score_text.get_rect()
        score_rect.topleft = (20, 20)
        screen.blit(score_text, score_rect)

        pygame.display.flip()

        clock.tick(30)

    return score


speed = int(input("Speed (recommended=4): "))
space = int(input("Minimum vertical space: "))

print(f"Your score: {play_game(speed, space)}.")

while True:

    inp = input("Type 1 to play with the same settings."
                "Type 2 to play with new settings."
                "Type anything else to quit.\n")

    if inp == "1":
        print(f"Your score: {play_game(speed, space)}.")

    elif inp == "2":
        speed = int(input("Speed (recommended=4): "))
        space = int(input("Minimum vertical space: "))
        print(f"Your score: {play_game(speed, space)}.")

    else:
        break

pygame.quit()
