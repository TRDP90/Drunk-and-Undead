import pyasge


class Whiskey:

    def __init__(self) -> None:
        self.sprite = pyasge.Sprite()
        self.image = self.sprite.loadTexture("data/images/PNG/whiskey.png")
        self.sprite.scale = 0.19
        self.sprite.x = 350 - self.sprite.width
        self.sprite.y = 305 - self.sprite.height
        self.sprite.z_order = 4
        self.visibility = True
