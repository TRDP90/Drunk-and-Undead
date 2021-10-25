import pyasge


class Boss:

    def __init__(self) -> None:
        self.sprite = pyasge.Sprite()
        self.image = self.sprite.loadTexture("data/images/PNG/Robot 1/robot1_hold.png")
        self.sprite.scale = 1

        self.sprite.x = 100
        self.sprite.y = 100
        self.sprite.z_order = 5
        self.speed = 1
        self.visibility = True
        self.health = 10
