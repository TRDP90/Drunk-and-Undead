import pyasge
import random


class PowerUp:

    def __init__(self) -> None:
        self.sprite = pyasge.Sprite()
        self.image = self.sprite.loadTexture("data/images/PNG/power_up.png")
        self.sprite.scale = 0.15
        self.sprite.x = (random.randint(0, 32 * 30)) - self.sprite.width
        self.sprite.y = (random.randint(0, 32 * 30)) + self.sprite.height
        self.sprite.z_order = 15
        self.visibility = True
