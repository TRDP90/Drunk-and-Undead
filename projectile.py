import pyasge


class Projectile:

    def __init__(self) -> None:
        self.sprite = pyasge.Sprite()
        self.image = self.sprite.loadTexture("data/images/PNG/Tanks/PNG/Default size/tank_bullet1.png")
        self.sprite.scale = 0.65
        self.sprite.x = 512 - self.sprite.width * 0.5
        self.sprite.y = 512 - self.sprite.height * 0.5
        self.destination_x = None
        self.destination_y = None
        self.visibility = False
        self.sprite.z_order = 5
