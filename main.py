import os
import random
import pygame
import pygame.freetype
import time

SIZE = width, height = 2560, 1600
screen = pygame.display.set_mode(SIZE)
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Flappy Bird!")
pygame.mouse.set_visible(False)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (42, 104, 166)
FPS = 60


bg = pygame.image.load(os.path.join('assets', '4622710.webp'))
bg = pygame.transform.scale(bg, (1500, 900))

# Text
pygame.freetype.init()
score_label = pygame.freetype.SysFont('menlo', 50, True)
score = pygame.freetype.SysFont('menlo', 50, True)
best_score_label = pygame.freetype.SysFont('menlo', 50, True)
best_score = pygame.freetype.SysFont('menlo', 50, True)
play_again = pygame.freetype.SysFont('menlo', 50, True)
quit = pygame.freetype.SysFont('menlo', 50, True)

# Sounds
pygame.mixer.init()
point_sound = pygame.mixer.Sound(os.path.join('assets', 'point.mp3'))
jump_sound = pygame.mixer.Sound(os.path.join('assets', 'wing.mp3'))
die_sound = pygame.mixer.Sound(os.path.join('assets', 'die.mp3'))


def draw_screen(bird, score):
    screen.blit(bg, (0 , 0))
    if bird.velocity == 15:
        screen.blit(bird.down, (bird.rect.x, bird.rect.y))
    else:
        screen.blit(bird.up, (bird.rect.x, bird.rect.y))
    if bird.active:
        score.render_to(screen, (100, 100), str(bird.count))
    top_pipe_group.draw(screen)
    bottom_pipe_group.draw(screen)
    pygame.display.update()


def lose_screen(score):
    die_sound.play()
    if bird.count > bird.best_score:
        bird.best_score = bird.count

    pygame.draw.rect(screen, (0, 255, 145), pygame.Rect(470, 370, 500, 270))
    score_label.render_to(screen, (520, 400), "Score: ")
    score.render_to(screen, (750, 400), str(bird.count))
    best_score_label.render_to(screen, (520, 450), "Best: ")
    best_score_label.render_to(screen, (750, 450), str(bird.best_score))
    play_again.render_to(screen, (520, 500), 'p - Play Again')
    quit.render_to(screen, (520, 560), 'q - Quit')
    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                if event.key == pygame.K_p:
                    bird.reset()
                    main()

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'bird3.png'))
        self.neutral = pygame.transform.scale(self.image, (100, 100))
        self.up = pygame.transform.rotate(self.neutral, 25)
        self.down = pygame.transform.rotate(self.neutral, -25)
        self.rect = self.image.get_rect()
        self.velocity = 4
        self.count = 0
        self.incrementing = False
        self.rect = self.rect.inflate(-35, -60)
        self.can_jump = True
        self.active = True
        self.best_score = 0

    def reset(self):
        self.count = 0
        self.incrementing = False
        self.can_jump = True
        self.active = True

    def increment(self):
        self.count += 1



bird = Bird()


class TopPipe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'downpipe.png'))
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect = self.rect.inflate(-50, -65)
        self.active = True

    def update(self):
        if self.active:
            self.rect.x -= 6
        if self.rect.x < -400:
            self.kill()
            self.generate()

    def generate(self):
        randint = random.randint(100, 500)
        randint2 = 900 - randint
        new_top_pipe = TopPipe(3200, randint * -1)
        top_pipe_group.add(new_top_pipe)
        new_bottom_pipe = BottomPipe(3200, randint2)
        bottom_pipe_group.add(new_bottom_pipe)

class BottomPipe(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'downpipe.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect = self.rect.inflate(-50, -50)
        self.active = True

    def update(self):
        if self.active:
            self.rect.x -= 6
        if bird.rect.x > self.rect.x and not bird.incrementing:
            bird.increment()
            bird.incrementing = True
            point_sound.play()
        if self.rect.x < -400:
            self.kill()
            bird.incrementing = False


top_pipe_group = pygame.sprite.Group()
bottom_pipe_group = pygame.sprite.Group()


def main():
    clock = pygame.time.Clock()

    top_pipe_group.empty()
    bottom_pipe_group.empty()

    for num in range(6):
        randint = random.randint(100, 500)
        randint2 = 900 - randint
        top_pipe = TopPipe(600 + num * 600, randint * -1)
        bottom_pipe = BottomPipe(600 + num * 600, randint2)
        top_pipe_group.add(top_pipe)
        bottom_pipe_group.add(bottom_pipe)

    bird.rect.x = 0
    bird.rect.y = 400

    jumping = False
    run = True

    while run:
        clock.tick(FPS)
        draw_screen(bird, score)
        bird.rect.y += bird.velocity


        top_pipe_group.update()
        bottom_pipe_group.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and bird.can_jump:
                    jumping = True

        if jumping:
            bird.velocity = -20
            jump_sound.play()
            jumping = False

        if (bird.rect.y < -100
            or pygame.sprite.spritecollideany(bird, top_pipe_group)
            or pygame.sprite.spritecollideany(bird, bottom_pipe_group)):
            bird.can_jump = False
            for bottom_pipe in bottom_pipe_group:
                bottom_pipe.active = False
            for top_pipe in top_pipe_group:
                top_pipe.active = False

        if (bird.rect.y > 900):
            bird.velocity = 0
            run = False
            bird.active = False
            draw_screen(bird, score)
            lose_screen(score)

        bird.velocity += 1
        if bird.velocity >= 15:
            bird.velocity = 15

    pygame.quit()


if __name__ == '__main__':
    main()



