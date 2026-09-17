import math
import pygame

FOV = math.radians(66)
MAX_DEPTH = 24.0


def cast_and_draw(screen, world, player):
    width, height = screen.get_size()
    half_h = height / 2
    ray_count = width
    ray_angle_step = FOV / ray_count

    # Simple underground palette; no external textures required yet.
    screen.fill((12, 13, 18))
    pygame.draw.rect(screen, (23, 24, 31), (0, half_h, width, half_h))

    start_angle = player.angle - FOV / 2

    for column in range(ray_count):
        ray_angle = start_angle + column * ray_angle_step
        ray_dir_x = math.cos(ray_angle)
        ray_dir_y = math.sin(ray_angle)

        map_x = int(player.x)
        map_y = int(player.y)

        delta_x = abs(1.0 / ray_dir_x) if ray_dir_x != 0 else 1e30
        delta_y = abs(1.0 / ray_dir_y) if ray_dir_y != 0 else 1e30

        if ray_dir_x < 0:
            step_x = -1
            side_x = (player.x - map_x) * delta_x
        else:
            step_x = 1
            side_x = (map_x + 1.0 - player.x) * delta_x

        if ray_dir_y < 0:
            step_y = -1
            side_y = (player.y - map_y) * delta_y
        else:
            step_y = 1
            side_y = (map_y + 1.0 - player.y) * delta_y

        side = 0
        hit = False
        distance = MAX_DEPTH

        for _ in range(128):
            if side_x < side_y:
                side_x += delta_x
                map_x += step_x
                side = 0
            else:
                side_y += delta_y
                map_y += step_y
                side = 1

            if world.is_wall(map_x, map_y):
                hit = True
                distance = side_x - delta_x if side == 0 else side_y - delta_y
                break

            if map_x < 0 or map_y < 0 or map_y >= len(world.map) or map_x >= len(world.map[0]):
                break

        if not hit:
            continue

        # Correct fish-eye distortion.
        corrected = distance * math.cos(ray_angle - player.angle)
        corrected = max(corrected, 0.001)

        wall_height = int(height / corrected)
        top = max(0, int(half_h - wall_height / 2))
        bottom = min(height, int(half_h + wall_height / 2))

        shade = max(35, min(220, int(220 / (1 + corrected * 0.09))))
        if side == 1:
            shade = int(shade * 0.72)

        # Slight variation by map tile makes the prototype easier to read.
        tile = world.tile_at(map_x, map_y)
        if tile == 2:
            base = (90, 70, 110)
        else:
            base = (105, 115, 125)

        color = tuple(max(0, min(255, int(c * shade / 140))) for c in base)
        pygame.draw.line(screen, color, (column, top), (column, bottom))

    # Small center reticle.
    cx, cy = width // 2, height // 2
    pygame.draw.line(screen, (220, 220, 220), (cx - 4, cy), (cx + 4, cy), 1)
    pygame.draw.line(screen, (220, 220, 220), (cx, cy - 4), (cx, cy + 4), 1)
