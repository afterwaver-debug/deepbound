import importlib.util
import math
import os
import sys
from pathlib import Path

import pygame

WIDTH, HEIGHT, FPS = 640, 480, 60
pygame.init()
try:
    pygame.mixer.init()
except pygame.error:
    pass

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DEEPBOUND")
clock = pygame.time.Clock()
BASE = Path(__file__).resolve().parent

game_mode = "3D"
cutscene_mode = "2D"


def font(size):
    # Pixel Operator: menus, title, and HUD/UI.
    p = BASE / "assets" / "fonts" / "PixelOperator.ttf"
    if not p.exists():
        p = BASE / "assets" / "fonts" / "font.ttf"
    try:
        return pygame.font.Font(str(p), size) if p.exists() else pygame.font.Font(None, size)
    except pygame.error:
        return pygame.font.Font(None, size)


def dialogue_font(size):
    # Open Sans: dialogue and normal readable story text.
    p = BASE / "assets" / "fonts" / "OpenSans.ttf"
    try:
        return pygame.font.Font(str(p), size) if p.exists() else pygame.font.Font(None, size)
    except pygame.error:
        return pygame.font.Font(None, size)


def load_intro():
    # Load the root intro.py explicitly. This avoids the intro/ package
    # shadowing it when both exist in the project.
    path = BASE / "intro.py"
    spec = importlib.util.spec_from_file_location("deepbound_intro", path)
    if spec is None or spec.loader is None:
        raise ImportError("Could not load intro.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.run_intro


def menu(title, items, selected=0):
    f, small = font(32), font(20)
    while True:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return -1
            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(items)
                elif e.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(items)
                elif e.key in (pygame.K_z, pygame.K_RETURN, pygame.K_SPACE):
                    return selected
                elif e.key == pygame.K_ESCAPE:
                    return len(items) - 1

        screen.fill((0, 0, 0))
        t = font(64).render(title, True, (255, 255, 255))
        screen.blit(t, t.get_rect(center=(320, 110)))

        for i, text in enumerate(items):
            s = f.render(
                text,
                True,
                (255, 255, 255) if i == selected else (150, 150, 150),
            )
            r = s.get_rect(center=(320, 245 + i * 55))
            screen.blit(s, r)
            if i == selected:
                screen.blit(f.render('>', True, (255, 255, 255)), (r.left - 30, r.top))

        pygame.display.flip()


def options():
    global game_mode, cutscene_mode
    selected = 0
    while True:
        choice = menu(
            "OPTIONS",
            [f"GAME MODE: {game_mode}", f"CUTSCENE MODE: {cutscene_mode}", "BACK"],
            selected,
        )
        if choice in (-1, 2):
            return choice
        selected = choice
        if choice == 0:
            game_mode = "2D" if game_mode == "3D" else "3D"
        elif choice == 1:
            cutscene_mode = "3D" if cutscene_mode == "2D" else "2D"


def start_3d_game():
    from mode_3d.player_3d import Player3D
    from mode_3d.world_3d import World3D

    world = World3D()
    player = Player3D(world)
    running = True

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    pygame.mouse.get_rel()  # discard the initial mouse jump

    while running:
        dt = min(clock.tick(FPS) / 1000.0, 0.05)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.event.set_grab(False)
                pygame.mouse.set_visible(True)
                return -1
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
            elif e.type == pygame.MOUSEMOTION:
                player.handle_mouse(e.rel)

        keys = pygame.key.get_pressed()
        player.update(dt, keys)
        world.update(dt)
        world.draw(screen, player)

        # Minimal HUD.
        hud = font(18).render("WASD: Move   Mouse/Arrows: Look   ESC: Menu", True, (220, 220, 220))
        screen.blit(hud, (12, 12))
        pygame.display.flip()

    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)
    pygame.mouse.get_rel()
    return 0


def start_2d_game():
    # 2D renderer is still being built; leave the existing mode as a safe placeholder.
    while True:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return -1
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return 0
        screen.fill((0, 0, 0))
        text = font(28).render("2D MODE", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(WIDTH // 2, 205)))
        sub = font(20).render("2D world coming next...", True, (160, 160, 160))
        screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 250)))
        pygame.display.flip()


def start_game():
    if game_mode == "3D":
        return start_3d_game()
    return start_2d_game()


def main():
    try:
        run_intro = load_intro()
        result = run_intro(screen, clock)
        if result == "quit":
            return
    except Exception as exc:
        print("Intro error:", exc)
        # Keep the game usable even if an intro asset is missing.

    while True:
        choice = menu("DEEPBOUND", ["PLAY", "OPTIONS", "QUIT"])
        if choice in (-1, 2):
            break
        if choice == 1:
            if options() == -1:
                break
        elif choice == 0:
            if start_game() == -1:
                break


if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
