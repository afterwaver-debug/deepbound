import math
import pygame


class Player3D:
    def __init__(self, world, x=2.5, y=2.5, angle=0.0):
        self.world = world
        self.x = x
        self.y = y
        self.angle = angle
        self.move_speed = 3.0
        self.turn_speed = 2.2
        self.mouse_sensitivity = 0.0028
        self.radius = 0.20

    def _blocked(self, x, y):
        # Circle-ish collision using four checks around the player.
        r = self.radius
        checks = ((x-r, y-r), (x+r, y-r), (x-r, y+r), (x+r, y+r))
        return any(self.world.is_wall(int(px), int(py)) for px, py in checks)

    def move(self, dx, dy):
        nx = self.x + dx
        ny = self.y + dy
        if not self._blocked(nx, self.y):
            self.x = nx
        if not self._blocked(self.x, ny):
            self.y = ny

    def update(self, dt, keys):
        forward = 0
        strafe = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            forward += 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            forward -= 1
        if keys[pygame.K_d]:
            strafe += 1
        if keys[pygame.K_a]:
            strafe -= 1

        if forward or strafe:
            length = math.hypot(forward, strafe)
            forward /= length
            strafe /= length
            speed = self.move_speed * dt
            dx = math.cos(self.angle) * forward * speed
            dy = math.sin(self.angle) * forward * speed
            dx += math.cos(self.angle + math.pi / 2) * strafe * speed
            dy += math.sin(self.angle + math.pi / 2) * strafe * speed
            self.move(dx, dy)

        if keys[pygame.K_LEFT]:
            self.angle -= self.turn_speed * dt
        if keys[pygame.K_RIGHT]:
            self.angle += self.turn_speed * dt

    def handle_mouse(self, rel):
        self.angle += rel[0] * self.mouse_sensitivity
