import pyasge
import random


class Enemy:

    def __init__(self) -> None:
        self.sprite = pyasge.Sprite()
        self.image = self.sprite.loadTexture("data/images/PNG/Zombie 1/zoimbie1_hold.png")
        self.sprite.scale = 0.65

        self.sprite.x = (random.randint(50, 32 * 2)) - self.sprite.width
        self.sprite.y = (random.randint(80, 32 * 15)) + self.sprite.height
        self.sprite.z_order = 5
        self.speed = random.randint(5, 15)
        self.visibility = True
        self.health = 3
        self.path = []
        self.x_goal_tile = None
        self.y_goal_tile = None
