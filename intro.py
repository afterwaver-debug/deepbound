import pygame
from pathlib import Path

WIDTH, HEIGHT, FPS = 640, 480, 60
BASE = Path(__file__).resolve().parent
INTRO_DIR = BASE / 'assets' / 'intro'
FONT_DIR = BASE / 'assets' / 'fonts'

SCENES = [
    ('scene1.png', 'Long ago, people spoke of a place beneath the surface.'),
    ('scene2.png', 'They called it the Deep.'),
    ('scene3.png', 'No one knew who built it... or what waited below.'),
    ('scene4.png', 'One day, you found an entrance.'),
    ('scene5.png', 'You stepped forward.'),
    ('scene6.png', 'The ground disappeared beneath your feet.'),
    ('scene7.png', 'You fell. And fell. And fell...'),
    ('scene8.png', 'When you opened your eyes, the surface was gone.'),
    ('scene9.png', 'Somewhere in the darkness, something moved.'),
    ('scene10.png', 'There was only one way forward.'),
]


def font(size):
    # Dialogue uses Open Sans; fall back safely if the font has not been added yet.
    p = FONT_DIR / 'OpenSans.ttf'
    if not p.exists():
        p = FONT_DIR / 'font.ttf'
    try:
        return pygame.font.Font(str(p), size) if p.exists() else pygame.font.Font(None, size)
    except pygame.error:
        return pygame.font.Font(None, size)


def load_image(name):
    p = INTRO_DIR / name
    if not p.exists():
        return None
    try:
        return pygame.transform.smoothscale(pygame.image.load(str(p)).convert(), (WIDTH, HEIGHT))
    except pygame.error:
        return None


def run_intro(screen, clock):
    text_font = font(25)
    index, chars, timer = 0, 0, 0
    image = load_image(SCENES[0][0])
    fade = 0
    fading = False
    fade_out = True
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))

    while True:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'menu'
                if event.key in (pygame.K_z, pygame.K_RETURN, pygame.K_SPACE) and not fading:
                    full = SCENES[index][1]
                    if chars < len(full):
                        chars = len(full)
                    elif index < len(SCENES) - 1:
                        index += 1
                        chars = 0
                        timer = 0
                        image = load_image(SCENES[index][0])
                        fading, fade_out, fade = True, True, 0
                    else:
                        return 'menu'

        full = SCENES[index][1]
        if not fading and chars < len(full):
            timer += dt
            while timer >= 1000 / 32 and chars < len(full):
                timer -= 1000 / 32
                chars += 1

        if fading:
            fade_speed = 255 / 450

            if fade_out:
                # Fade to black
                fade += dt * fade_speed

                if fade >= 255:
                    fade = 255
                    fade_out = False

                    # Load the NEW scene only after reaching black
                    image = load_image(SCENES[index][0])

            else:
                # Fade back in from black
                fade -= dt * fade_speed

                if fade <= 0:
                    fade = 0
                    fading = False
                    
        screen.fill((0, 0, 0))
        if image:
            screen.blit(image, (0, 0))
        box = pygame.Rect(30, HEIGHT - 135, WIDTH - 60, 105)
        pygame.draw.rect(screen, (0, 0, 0), box)
        pygame.draw.rect(screen, (255, 255, 255), box, 3)
        shown = full[:chars]
        words, lines, line = shown.split(), [], ''
        for word in words:
            test = f'{line} {word}'.strip()
            if text_font.size(test)[0] <= box.width - 30:
                line = test
            else:
                lines.append(line); line = word
        if line: lines.append(line)
        for i, ln in enumerate(lines):
            screen.blit(text_font.render(ln, True, (255,255,255)), (box.x+15, box.y+13+i*32))
        if chars >= len(full) and not fading:
            pygame.draw.polygon(screen, (255,255,255), [(box.right-25,box.bottom-20),(box.right-10,box.bottom-20),(box.right-17,box.bottom-8)])
        if fading:
            fade_surface.set_alpha(max(0, min(255, int(fade))))
            screen.blit(fade_surface, (0,0))
        pygame.display.flip()
