import pyasge
import math

from bigpowerup import Whiskey
from gamestate import GameState, GameStateID
from map import Map
from projectile import Projectile
from enemy import Enemy
from boss import Boss
from pathfinding import Node
from powerup import PowerUp


class GamePlay(GameState):
    def __init__(self, data):
        super().__init__(data)
        self.id = GameStateID.GAMEPLAY

        # register the key handler for this class
        self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.input)
        self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_MOVE, self.mouseMovement)
        self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.click_event)

        # create a player sprite
        self.sprite = pyasge.Sprite()
        self.sprite.scale = 0.65
        self.sprite.loadTexture("data/images/PNG/Man Blue/manBlue_gun.png")
        self.sprite.x = 512 - self.sprite.width * 0.5
        self.sprite.y = 512 - self.sprite.height * 0.5
        self.sprite.z_order = 4
        self.angle = 0
        self.player_speed = 0

        # bullet properties
        self.projectile_angle = 0
        self.bullet_distance_x = 0
        self.bullet_distance_y = 0
        self.total_bullet_magnitude = 0

        # zombie properties
        self.enemy_distance_x = 0
        self.enemy_distance_y = 0
        self.total_enemy_magnitude = 0
        self.enemy_angle = 0

        # healthbars
        self.healthbar_x = 100
        self.healthbar_y = 100
        self.bosshurt = 0

        self.healthbar2 = pyasge.Sprite()
        self.healthbar2.loadTexture("data/images/PNG/healthbar2.png")
        self.healthbar2.x = self.healthbar_x
        self.healthbar2.y = self.healthbar_y
        self.healthbar2.z_order = 1

        self.healthbar3 = pyasge.Sprite()
        self.healthbar3.loadTexture("data/images/PNG/healthbar3.png")
        self.healthbar3.x = self.healthbar_x
        self.healthbar3.y = self.healthbar_y
        self.healthbar3.z_order = 1

        self.healthbar4 = pyasge.Sprite()
        self.healthbar4.loadTexture("data/images/PNG/healthbar4.png")
        self.healthbar4.x = self.healthbar_x
        self.healthbar4.y = self.healthbar_y
        self.healthbar4.z_order = 1

        self.healthbar5 = pyasge.Sprite()
        self.healthbar5.loadTexture("data/images/PNG/healthbar5.png")
        self.healthbar5.x = self.healthbar_x
        self.healthbar5.y = self.healthbar_y
        self.healthbar5.z_order = 1

        # boss properties
        self.boss_distance_x = 0
        self.boss_distance_y = 0
        self.total_boss_magnitude = 0
        self.x_goal_tile = None
        self.y_goal_tile = None
        self.boss_angle = 0
        self.path_number = 0

        self.boss = None

        self.path = []

        self.map = Map()

        # array properties
        # projectile init
        self.projectiles = []
        self.projectile_count = 10
        self.bullet_speed = 400

        while len(self.projectiles) != self.projectile_count:
            projectile = Projectile()
            self.projectiles.append(projectile)
        self.projectile_count = 0

        self.enemies = []

        # enemy spawner
        while len(self.enemies) != 3:
            enemy = Enemy()
            self.enemies.append(enemy)

        self.boss = None

        # images indicating what control mode you are in
        self.controlmode = pyasge.Sprite()
        self.controlmode.loadTexture("data/images/PNG/controlmode.png")
        self.controlmode.scale = 1
        self.controlmode.x = 170
        self.controlmode.y = 15

        self.mousemode = pyasge.Sprite()
        self.mousemode.loadTexture("data/images/PNG/mousemode.png")
        self.mousemode.scale = 1
        self.mousemode.x = self.controlmode.x
        self.mousemode.y = self.controlmode.y

        # track key states
        self.keys = {
            pyasge.KEYS.KEY_A: False,
            pyasge.KEYS.KEY_D: False,
            pyasge.KEYS.KEY_W: False,
            pyasge.KEYS.KEY_S: False,
            pyasge.KEYS.KEY_EQUAL: False,
            pyasge.KEYS.KEY_MINUS: False,
        }

        # track mouse states
        self.mouse_click = {
            pyasge.MOUSE.MOUSE_BTN1: False
        }

        # If a controller is connected, defaults to controller mode.
        # Elsewhere, Keyboard/mouse activity will switch from controller mode to normal mode, and vice versa.
        if self.data.inputs.getGamePad(0).connected:
            self.controller_active = True
        else:
            self.controller_active = False

        # controller axis state
        self.contr_x = 0
        self.contr_y = 0
        self.contr_x_right = 0
        self.contr_y_right = 0

        # booleans used to determine controller button clicks compared to just being pressed, probably a better way to do this but it works
        self.contr_button_rbump_active = False

        # mode swap timer to prevent the player glitchily using mouse and controller at the same time
        self.swaptimer = 60

        # adding score
        self.score = 0
        self.score_as_str = "0"
        self.score_text = pyasge.Text(self.data.fonts['kenvector'], self.score_as_str)
        self.score_text.position = [200 - self.score_text.width * 0.5, 35]
        self.score_text.z_order = 10
        self.score_text.colour = pyasge.COLOURS.WHITE

        # adding drunk meter
        self.meter = 100
        round(self.meter)
        self.meter_as_str = str(self.meter)
        self.meter_text = pyasge.Text(self.data.fonts['kenvector'], self.meter_as_str)
        self.meter_text.position = [750 - self.meter_text.width * 0.5, 35]
        self.meter_text.z_order = 10
        self.meter_text.colour = pyasge.COLOURS.WHITE

        # add warning text
        self.warning_text = pyasge.Text(self.data.fonts['kenvector'], "Sobering up! Get inside!")
        self.warning_text.position = [400 - self.warning_text.width * 0.5, 325]
        self.warning_text.z_order = 50
        self.warning_text.colour = pyasge.COLOURS.AQUA

        # adding power ups
        self.power_ups = []
        while len(self.power_ups) != 20:
            power_up = PowerUp()
            self.power_ups.append(power_up)

        # assign stronger alcohol
        self.whiskey = []
        while len(self.whiskey) != 4:
            whisk = Whiskey()
            self.whiskey.append(whisk)
            for whisk in self.whiskey:
                whisk.sprite.x += whisk.sprite.width * 0.5

    def input(self, event: pyasge.KeyEvent) -> None:
        if event.action is not pyasge.KEYS.KEY_REPEATED:
            self.keys[event.key] = event.action is pyasge.KEYS.KEY_PRESSED
            self.player_speed = 250
        else:
            self.player_speed = 0

    def click_event(self, event: pyasge.ClickEvent) -> None:
        if event.button is pyasge.MOUSE.MOUSE_BTN1:
            if event.action is pyasge.MOUSE.BUTTON_PRESSED:
                self.mouse_click[event.button] = event.action is pyasge.MOUSE.BUTTON_PRESSED

                # spawn bullet
                self.projectiles[self.projectile_count].visibility = True
                self.projectiles[self.projectile_count].sprite.x = self.sprite.x + self.projectiles[
                    self.projectile_count].sprite.width / 2
                self.projectiles[self.projectile_count].sprite.y = self.sprite.y + self.projectiles[
                    self.projectile_count].sprite.height / 2

                # click position
                self.projectiles[self.projectile_count].destination_x = event.x
                self.projectiles[self.projectile_count].destination_y = event.y

                # bullet rotation
                self.projectile_angle = math.atan2(
                    event.y - (self.projectiles[self.projectile_count].sprite.y - self.projectiles[
                        self.projectile_count].sprite.height / 2),
                    event.x - (self.projectiles[self.projectile_count].sprite.x - self.projectiles[
                        self.projectile_count].sprite.width / 2))
                if self.projectile_count < 9:
                    self.projectile_count += 1
                else:
                    self.projectile_count = 0

    def mouseMovement(self, event: pyasge.MoveEvent):
        # looks at mouse position
        self.angle = math.atan2(event.y - (self.sprite.y - self.sprite.height / 2),
                                event.x - (self.sprite.x - self.sprite.width / 2))
        if self.controller_active:
            if self.swaptimer == 60:
                self.controller_active = False  # makes the game switch into keyboard/mouse mode from controller mode when the mouse is moved
                self.swaptimer = 0

    def update(self, game_time: pyasge.GameTime) -> GameStateID:

        # once again, swaptimer is to stop the player using mouse/controller simultaneously
        if self.swaptimer < 60:
            self.swaptimer = self.swaptimer + 1

        # KEYBOARD INPUTS
        if self.keys[pyasge.KEYS.KEY_W]:
            if not self.controller_active:
                self.sprite.y = self.sprite.y - self.player_speed * game_time.fixed_timestep
            else:
                if self.swaptimer == 60:
                    self.controller_active = False
                    self.swaptimer = 0

        if self.keys[pyasge.KEYS.KEY_S]:
            if not self.controller_active:
                self.sprite.y = self.sprite.y + self.player_speed * game_time.fixed_timestep
            else:
                if self.swaptimer == 60:
                    self.controller_active = False
                    self.swaptimer = 0

        if self.keys[pyasge.KEYS.KEY_A]:
            if not self.controller_active:
                self.sprite.x = self.sprite.x - self.player_speed * game_time.fixed_timestep
            else:
                if self.swaptimer == 60:
                    self.controller_active = False
                    self.swaptimer = 0

        if self.keys[pyasge.KEYS.KEY_D]:
            if not self.controller_active:
                self.sprite.x = self.sprite.x + self.player_speed * game_time.fixed_timestep
            else:
                if self.swaptimer == 60:
                    self.controller_active = False
                    self.swaptimer = 0

        # COLLISION
        # MAP
        x_player_tile = self.map.tile(pyasge.Point2D(self.sprite.x, self.sprite.y))[0]
        y_player_tile = self.map.tile(pyasge.Point2D(self.sprite.x, self.sprite.y))[1]

        x_player_tile_left = self.map.tile(pyasge.Point2D(self.sprite.x - 10, self.sprite.y))[0]
        x_player_tile_right = self.map.tile(pyasge.Point2D(self.sprite.x + self.sprite.width / 2, self.sprite.y))[0]
        y_player_tile_top = self.map.tile(pyasge.Point2D(self.sprite.x, self.sprite.y - 10))[1]
        y_player_tile_bottom = self.map.tile(pyasge.Point2D(self.sprite.x, self.sprite.y + self.sprite.height / 2))[1]

        # RIGHT
        if self.map.costmap[y_player_tile][x_player_tile_right] >= 100:
            if not self.controller_active:
                if self.keys[pyasge.KEYS.KEY_D]:
                    self.sprite.x = self.sprite.x - 250 * game_time.fixed_timestep

            else:
                if self.contr_x > 0.1:
                    self.sprite.x = self.sprite.x - 250 * game_time.fixed_timestep

        # LEFT
        if self.map.costmap[y_player_tile][x_player_tile_left] >= 100:
            if not self.controller_active:
                if self.keys[pyasge.KEYS.KEY_A]:
                    self.sprite.x = self.sprite.x + 250 * game_time.fixed_timestep

            else:
                if self.contr_x < -0.1:
                    self.sprite.x = self.sprite.x + 250 * game_time.fixed_timestep

        # TOP
        if self.map.costmap[y_player_tile_top][x_player_tile] >= 100:
            if not self.controller_active:
                if self.keys[pyasge.KEYS.KEY_W]:
                    self.sprite.y = self.sprite.y + 250 * game_time.fixed_timestep

            else:
                if self.contr_y < -0.1:
                    self.sprite.y = self.sprite.y + 250 * game_time.fixed_timestep

        # BOTTOM
        if self.map.costmap[y_player_tile_bottom][x_player_tile] >= 100:
            if not self.controller_active:
                if self.keys[pyasge.KEYS.KEY_S]:
                    self.sprite.y = self.sprite.y - 250 * game_time.fixed_timestep

            else:
                if self.contr_y > 0.1:
                    self.sprite.y = self.sprite.y - 250 * game_time.fixed_timestep

        # WINDOW X
        if 780 - self.sprite.width / 2 < self.sprite.x or self.sprite.x < self.sprite.width / 2:
            if not self.controller_active:
                if self.keys[pyasge.KEYS.KEY_A]:
                    self.sprite.x = self.sprite.x + 250 * game_time.fixed_timestep
                if self.keys[pyasge.KEYS.KEY_D]:
                    self.sprite.x = self.sprite.x - 250 * game_time.fixed_timestep
            else:
                if self.contr_x > 0.1:
                    self.sprite.x = self.sprite.x - 250 * game_time.fixed_timestep
                if self.contr_x < -0.1:
                    self.sprite.x = self.sprite.x + 250 * game_time.fixed_timestep

        # WINDOW Y
        if 950 - self.sprite.height / 2 < self.sprite.y or self.sprite.y < self.sprite.height / 2:
            if not self.controller_active:
                if self.keys[pyasge.KEYS.KEY_W]:
                    self.sprite.y = self.sprite.y + 250 * game_time.fixed_timestep
                if self.keys[pyasge.KEYS.KEY_S]:
                    self.sprite.y = self.sprite.y - 250 * game_time.fixed_timestep
            else:
                if self.contr_y > 0.1:
                    self.sprite.y = self.sprite.y - 250 * game_time.fixed_timestep
                if self.contr_y < -0.1:
                    self.sprite.y = self.sprite.y + 250 * game_time.fixed_timestep

        # rotates the player sprite to whatever self.angle currently is.
        self.sprite.rotation = self.angle

        # updating health bar
        self.healthbar2.x = self.healthbar_x
        self.healthbar2.y = self.healthbar_y
        self.healthbar3.x = self.healthbar_x
        self.healthbar3.y = self.healthbar_y
        self.healthbar4.x = self.healthbar_x
        self.healthbar4.y = self.healthbar_y
        self.healthbar5.x = self.healthbar_x
        self.healthbar5.y = self.healthbar_y

        # healthbar related things
        if self.boss is not None:
            if self.boss.health == 8 or self.boss.health == 7:
                self.bosshurt = 2
            if self.boss.health == 6 or self.boss.health == 5:
                self.bosshurt = 3
            if self.boss.health == 4 or self.boss.health == 3:
                self.bosshurt = 4
            if self.boss.health == 2 or self.boss.health == 1:
                self.bosshurt = 5

        # controller movement
        if self.data.inputs.getGamePad(0).connected:
            self.contr_x = self.data.inputs.getGamePad(0).x
            self.contr_y = self.data.inputs.getGamePad(0).y
            if self.contr_y < 0.1:
                if self.controller_active:
                    self.sprite.y = self.sprite.y - abs(self.contr_y) * self.player_speed * game_time.fixed_timestep
            if self.contr_y > -0.1:
                if self.controller_active:
                    self.sprite.y = self.sprite.y + abs(self.contr_y) * self.player_speed * game_time.fixed_timestep
            if self.contr_x < 0.1:
                if self.controller_active:
                    self.sprite.x = self.sprite.x - abs(self.contr_x) * self.player_speed * game_time.fixed_timestep
            if self.contr_x > -0.1:
                if self.controller_active:
                    self.sprite.x = self.sprite.x + abs(self.contr_x) * self.player_speed * game_time.fixed_timestep

            # controller aiming
            self.contr_x_right = self.data.inputs.getGamePad(0).x_right_axis
            self.contr_y_right = self.data.inputs.getGamePad(0).y_right_axis

            # switching to controller on stick movement + changing player angle
            if abs(self.contr_x) > 0.1 or abs(self.contr_y) > 0.1:
                if self.controller_active:
                    self.player_speed = 250
                    self.angle = math.atan2(self.contr_y, self.contr_x)  # makes the player look where they're running
                else:
                    if self.swaptimer == 60:
                        self.controller_active = True
                        self.swaptimer = 0
            else:
                if self.controller_active:
                    self.player_speed = 0

            # same as above but for the right stick
            if abs(self.contr_x_right) > 0.1 or abs(self.contr_y_right) > 0.1:
                if self.controller_active:
                    self.angle = math.atan2(self.contr_y_right,
                                            self.contr_x_right)  # makes the player look at what they're aiming at
                else:
                    if self.swaptimer == 60:
                        self.controller_active = True
                        self.swaptimer = 0

            # switching to controller on button activity
            if not self.controller_active:
                if self.data.inputs.getGamePad(0).RIGHT_BUMPER:
                    if self.swaptimer == 60:
                        self.controller_active = True
                        self.swaptimer = 0

            # controller bullets
            if self.controller_active:
                if self.data.inputs.getGamePad(0).RIGHT_BUMPER:
                    self.controller_active = True
                    if not self.contr_button_rbump_active:  # used to stop the player unleashing a machinegun stream of bullets
                        if abs(self.contr_x_right) > 0.8 or abs(
                                self.contr_y_right) > 0.8:  # requires the stick to be far out to fire
                            self.contr_button_rbump_active = True

                            # spawn bullet
                            self.projectiles[self.projectile_count].visibility = True
                            self.projectiles[self.projectile_count].sprite.x = self.sprite.x + self.projectiles[
                                self.projectile_count].sprite.width / 2
                            self.projectiles[self.projectile_count].sprite.y = self.sprite.y + self.projectiles[
                                self.projectile_count].sprite.height / 2

                            # direction to aim
                            self.projectiles[self.projectile_count].destination_x = self.sprite.x + (
                                    self.contr_x_right * 400)
                            self.projectiles[self.projectile_count].destination_y = self.sprite.y + (
                                    self.contr_y_right * 400)

                            # bullet rotation
                            self.projectile_angle = math.atan2(
                                self.contr_y - (self.projectiles[self.projectile_count].sprite.y - self.projectiles[
                                    self.projectile_count].sprite.height / 2),
                                self.contr_x - (self.projectiles[self.projectile_count].sprite.x - self.projectiles[
                                    self.projectile_count].sprite.width / 2))
                            if self.projectile_count < 9:
                                self.projectile_count += 1
                            else:
                                self.projectile_count = 0
                else:
                    self.contr_button_rbump_active = False

        # ENEMY
        self.tree()

        for x in range(len(self.enemies)):
            if not self.enemies[x].visibility:
                del self.enemies[x]
                break

        for enemy in self.enemies:

            # DAMAGE
            if self.sprite.x < enemy.sprite.x + enemy.sprite.width and self.sprite.x + self.sprite.width > enemy.sprite.x and self.sprite.y < enemy.sprite.y + enemy.sprite.height and self.sprite.y + self.sprite.height > enemy.sprite.y:
                self.meter = self.meter - 0.08
                # GRAB
                if self.player_speed == 250:
                    self.player_speed = 0

            # Pathfinding
            enemy_x_tile = self.map.tile(pyasge.Point2D(enemy.sprite.x, enemy.sprite.y))[0]
            enemy_y_tile = self.map.tile(pyasge.Point2D(enemy.sprite.x, enemy.sprite.y))[1]

            x_player_tile = self.map.tile(pyasge.Point2D(self.sprite.x, self.sprite.y))[0]
            y_player_tile = self.map.tile(pyasge.Point2D(self.sprite.x, self.sprite.y))[1]

            if not (y_player_tile == enemy.y_goal_tile and x_player_tile == enemy.x_goal_tile):
                enemy.path = []
                enemy.x_goal_tile = None
                enemy.y_goal_tile = None

            if enemy.x_goal_tile is None and enemy.y_goal_tile is None:
                enemy.x_goal_tile = x_player_tile
                enemy.y_goal_tile = y_player_tile

                enemy_pathfinding = Node(enemy_x_tile, enemy_y_tile, enemy.x_goal_tile, enemy.y_goal_tile)

            if enemy.path:
                if not (enemy.x_goal_tile == enemy.path[0][0] and enemy.y_goal_tile == enemy.path[0][1]):
                    if enemy_x_tile == enemy.path[0][0] and enemy_y_tile == enemy.path[0][1]:
                        del enemy.path[0]

            if not enemy.path:
                enemy_path = enemy_pathfinding.a_star_search((enemy_x_tile, enemy_y_tile),
                                                             (enemy.x_goal_tile, enemy.y_goal_tile))
                enemy.path = enemy_path

            # ENEMY MOVEMENT
            self.enemy_distance_x = self.map.world(enemy.path[0]).x - enemy.sprite.x
            self.enemy_distance_y = self.map.world(enemy.path[0]).y - enemy.sprite.y

            self.total_enemy_magnitude = math.sqrt((self.enemy_distance_x ** 2) + (self.enemy_distance_y ** 2))

            # ENEMY LOOK
            self.enemy_angle = math.atan2(self.sprite.y - (enemy.sprite.y - enemy.sprite.height / 2),
                                          self.sprite.x - (enemy.sprite.x - enemy.sprite.width / 2))

            enemy.sprite.rotation = self.enemy_angle

            if enemy.visibility:
                enemy.sprite.x = enemy.sprite.x + (
                        self.enemy_distance_x / self.total_enemy_magnitude) * enemy.speed / 10
                enemy.sprite.y = enemy.sprite.y + (
                        self.enemy_distance_y / self.total_enemy_magnitude) * enemy.speed / 10
                if enemy.health == 0:
                    enemy.visibility = False
                    self.score += 100
                    break

                for bullet in self.projectiles:
                    if enemy.sprite.x < bullet.sprite.x < enemy.sprite.x + enemy.sprite.width:
                        if enemy.sprite.y < bullet.sprite.y < enemy.sprite.y + enemy.sprite.width:
                            if bullet.visibility:
                                enemy.health += -1
                                bullet.visibility = False


        # shoot bullet
        for projectile in self.projectiles:
            if projectile.visibility:
                self.bullet_distance_x = projectile.destination_x - projectile.sprite.x
                self.bullet_distance_y = projectile.destination_y - projectile.sprite.y

                self.total_bullet_magnitude = math.sqrt((self.bullet_distance_x ** 2) + (self.bullet_distance_y ** 2))

                projectile.sprite.rotation = self.projectile_angle
                if projectile.visibility:
                    projectile.sprite.x = projectile.sprite.x + (
                            self.bullet_distance_x / self.total_bullet_magnitude * 2) * game_time.fixed_timestep * self.bullet_speed
                    projectile.sprite.y = projectile.sprite.y + (
                            self.bullet_distance_y / self.total_bullet_magnitude * 2) * game_time.fixed_timestep * self.bullet_speed

                    if self.total_bullet_magnitude < 20:
                        projectile.visibility = False

        # drunk meter conditions
        round(self.meter)
        self.meter_as_str = str(int(self.meter))
        self.meter_text.string = self.meter_as_str

        if self.meter <= 0:
            return GameStateID.GAME_OVER

        # updating drunk meter so it goes down
        self.meter -= 0.0085

        # add the collision box with the outdoor area so if u outside the meter goes down very quick
        # check if the player position is below y value
        if self.sprite.y > 680:
            self.meter -= 0.085

        # power ups
        for power_up in self.power_ups:
            if self.sprite.x < power_up.sprite.x + (
                    power_up.sprite.width / 2 * 0.15) < self.sprite.x + self.sprite.width:
                if self.sprite.y < power_up.sprite.y + (
                        power_up.sprite.height / 2 * 0.15) < self.sprite.y + self.sprite.height:
                    if power_up.visibility:
                        power_up.visibility = False
                        self.meter += 5


        # collision with whiskey
        for whiskey in self.whiskey:
            if self.sprite.x < whiskey.sprite.x < self.sprite.x + self.sprite.width:
                if self.sprite.y < whiskey.sprite.y < self.sprite.y + self.sprite.height:
                    if whiskey.visibility:
                        whiskey.visibility = False
                        self.meter += 10


        # score and win conditions
        self.score_as_str = str(round(self.score))
        self.score_text.string = self.score_as_str
        if self.score >= 500:  # change to 500
            return GameStateID.WINNER_WINNER
        else:
            return GameStateID.GAMEPLAY

    def render(self, game_time: pyasge.GameTime) -> None:
        self.map.render(self.data.renderer)
        self.data.renderer.render(self.sprite)

        # indicates when in controller mode or mouse mode
        if self.controller_active and self.swaptimer < 60:
            self.data.renderer.render(self.controlmode)
        elif self.controller_active == False and self.swaptimer < 60:
            self.data.renderer.render(self.mousemode)

        # healthbar related things

        if self.bosshurt == 2:
            self.data.renderer.render(self.healthbar2)
        if self.bosshurt == 3:
            self.data.renderer.render(self.healthbar3)
        if self.bosshurt == 4:
            self.data.renderer.render(self.healthbar4)
        if self.bosshurt == 5:
            self.data.renderer.render(self.healthbar5)

        for projectile in self.projectiles:
            if projectile.visibility:
                self.data.renderer.render(projectile.sprite)

        for enemy in self.enemies:
            if enemy.visibility:
                self.data.renderer.render(enemy.sprite)

        if self.boss is not None:
            self.data.renderer.render(self.boss.sprite)

        self.data.renderer.render(self.score_text)

        for power_up in self.power_ups:
            if power_up.visibility:
                self.data.renderer.render(power_up.sprite)

        # whiskey
        for whisk in self.whiskey:
            if whisk.visibility:
                self.data.renderer.render(whisk.sprite)

        self.data.renderer.render(self.meter_text)

        if self.sprite.y > 680:
            self.data.renderer.render(self.warning_text)

    def tree(self):

        if self.boss is not None:
            if self.total_boss_magnitude < 50:
                pass
            for bullet in self.projectiles:
                if self.boss.sprite.x < bullet.sprite.x < self.boss.sprite.x + self.boss.sprite.width:
                    if self.boss.sprite.y < bullet.sprite.y < self.boss.sprite.y + self.boss.sprite.width:
                        if bullet.visibility:
                            self.boss.health += -1
                            bullet.visibility = False

            if self.boss.health == 0:
                self.boss.visibility = False
                self.score += 200

            # healthbar updating

            self.healthbar_x = self.boss.sprite.x - 25
            self.healthbar_y = self.boss.sprite.y - 30

        if not self.enemies:
            if self.boss is None:
                self.spawnBoss()
            if self.boss.health <= 5:
                self.boss.speed = 1.5
                self.moveToBar()
            elif self.boss is not None:
                self.moveToPlayer()
                # take damage
                if self.sprite.x < self.boss.sprite.x + self.boss.sprite.width and self.sprite.x + self.sprite.width > self.boss.sprite.x and self.sprite.y < self.boss.sprite.y + self.boss.sprite.height and self.sprite.y + self.sprite.height > self.boss.sprite.y:
                    self.meter = self.meter - 0.8
                    if self.player_speed == 250:
                        self.player_speed = 0

    def spawnBoss(self):
        self.boss = Boss()
        self.moveToPlayer()

    def moveToBar(self):
        self.path = []

        self.x_goal_tile = 12
        self.y_goal_tile = 3
        x_tile = self.map.tile(pyasge.Point2D(self.boss.sprite.x, self.boss.sprite.y))[0]
        y_tile = self.map.tile(pyasge.Point2D(self.boss.sprite.x, self.boss.sprite.y))[1]

        pathfinding = Node(x_tile, y_tile, self.x_goal_tile, self.y_goal_tile)

        if self.path:
            if not (self.x_goal_tile == self.path[0][0] and self.y_goal_tile == self.path[0][1]):
                if x_tile == self.path[0][0] and y_tile == self.path[0][1]:
                    del self.path[0]

        if not self.path:
            path = pathfinding.a_star_search((x_tile, y_tile),
                                             (self.x_goal_tile, self.y_goal_tile))
            self.path = path

        if x_tile == self.x_goal_tile and y_tile == self.y_goal_tile:
            self.boss.health += 3
            self.moveToPlayer()

        self.boss_distance_x = self.map.world(self.path[0]).x - self.boss.sprite.x
        self.boss_distance_y = self.map.world(self.path[0]).y - self.boss.sprite.y
        self.total_boss_magnitude = math.sqrt((self.boss_distance_x ** 2) + (self.boss_distance_y ** 2))

        if self.boss.visibility:
            self.boss.sprite.x = self.boss.sprite.x + (
                    self.boss_distance_x / self.total_boss_magnitude) * self.boss.speed
            self.boss.sprite.y = self.boss.sprite.y + (
                    self.boss_distance_y / self.total_boss_magnitude) * self.boss.speed

            if self.boss.health == 0:
                self.boss.visibility = False

    def moveToPlayer(self):

        self.boss_angle = math.atan2(self.sprite.y - (self.boss.sprite.y - self.boss.sprite.height / 2),
                                     self.sprite.x - (self.boss.sprite.x - self.boss.sprite.width / 2))

        self.boss.sprite.rotation = self.boss_angle

        # Pathfinding
        x_tile = self.map.tile(pyasge.Point2D(self.boss.sprite.x, self.boss.sprite.y))[0]
        y_tile = self.map.tile(pyasge.Point2D(self.boss.sprite.x, self.boss.sprite.y))[1]

        x_player_tile = self.map.tile(pyasge.Point2D(self.sprite.x, self.sprite.y))[0]
        y_player_tile = self.map.tile(pyasge.Point2D(self.sprite.x, self.sprite.y))[1]

        if not (y_player_tile == self.y_goal_tile and x_player_tile == self.x_goal_tile):
            self.path = []
            self.x_goal_tile = None
            self.y_goal_tile = None

        if self.x_goal_tile is None and self.y_goal_tile is None:
            self.x_goal_tile = x_player_tile
            self.y_goal_tile = y_player_tile

            pathfinding = Node(x_tile, y_tile, self.x_goal_tile, self.y_goal_tile)

        if not self.path:
            path = pathfinding.a_star_search((x_tile, y_tile),
                                             (self.x_goal_tile, self.y_goal_tile))
            self.path = path

        if self.path:
            if not (self.x_goal_tile == self.path[0][0] and self.y_goal_tile == self.path[0][1]):
                if x_tile == self.path[0][0] and y_tile == self.path[0][1]:
                    del self.path[0]

        self.boss_distance_x = self.map.world(self.path[0]).x - self.boss.sprite.x
        self.boss_distance_y = self.map.world(self.path[0]).y - self.boss.sprite.y
        self.total_boss_magnitude = math.sqrt((self.boss_distance_x ** 2) + (self.boss_distance_y ** 2))

        if self.boss.visibility:

            self.boss.sprite.x = self.boss.sprite.x + (
                    self.boss_distance_x / self.total_boss_magnitude) * self.boss.speed
            self.boss.sprite.y = self.boss.sprite.y + (
                    self.boss_distance_y / self.total_boss_magnitude) * self.boss.speed

            if self.boss.health == 0:
                self.boss.visibility = False
