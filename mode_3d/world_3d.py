class World3D:
    # 0 = empty, 1 = wall, 2 = alternate wall type.
    MAP = [
        "1111111111111111",
        "1000000000000001",
        "1011110111111101",
        "1000010100000101",
        "1111010101110101",
        "1000010001010001",
        "1011111101011111",
        "1000000101000001",
        "1011110101111101",
        "1000010100000001",
        "1011010111111101",
        "1001010000000101",
        "1001000111110101",
        "1000000000010001",
        "1000000000000001",
        "1111111111111111",
    ]

    def __init__(self):
        self.map = [list(row) for row in self.MAP]

    def tile_at(self, x, y):
        if y < 0 or y >= len(self.map) or x < 0 or x >= len(self.map[0]):
            return 1
        value = self.map[y][x]
        return 2 if value == "2" else (1 if value == "1" else 0)

    def is_wall(self, x, y):
        return self.tile_at(x, y) != 0

    def update(self, dt):
        pass

    def draw(self, screen, player):
        from raycasting.raycaster import cast_and_draw
        cast_and_draw(screen, self, player)
