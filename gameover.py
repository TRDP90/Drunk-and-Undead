import pyasge

from gamestate import GameState
from gamestate import GameStateID
from gamedata import GameData
from gamemenu import GameMenu


class GameOver(GameState):

    def __init__(self, data) -> None:
        super().__init__(data)
        self.id = GameStateID.GAME_OVER
        self.quit = False

        self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_MOVE, self.mouseMovement)
        self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.click_event)

        self.is_game_over = True
        self.ui_text = pyasge.Text(self.data.fonts['kenvector'], "You are sober. GAME OVER!")
        self.ui_text.scale = 1
        self.ui_text.position = [32 * 12.5 - (self.ui_text.width / 2), 400]
        self.ui_text.z_order = 10
        self.ui_text.colour = pyasge.COLOURS.AQUA

        self.return_text = pyasge.Text(self.data.fonts['kenvector'], "RETURN")
        self.return_text.scale = 1.2
        self.return_text.position = pyasge.Point2D(32 * 12.5 - (self.return_text.width / 2), 700)
        self.return_text.z_order = 10
        self.return_text.colour = pyasge.COLOURS.WHITE

        self.clicky_image = pyasge.Sprite()
        self.clicky_image.loadTexture("data/images/PNG/clickyimage.png")
        self.clicky_image.scale = 0.1
        self.clicky_image.x = self.return_text.x + self.return_text.width + 75
        self.clicky_image.y = 640

        self.contr_image = pyasge.Sprite()
        self.contr_image.loadTexture("data/images/PNG/startbutton.png")
        self.contr_image.x = self.return_text.x - 175
        self.contr_image.y = 640

        self.return_select = False
        self.mouse_x = 0
        self.mouse_y = 0

        self.mouse_click = {
            pyasge.MOUSE.MOUSE_BTN1: False
        }

    def input(self, event: pyasge.KeyEvent) -> None:
        """ Handles the user input to select items on the screen"""
        # quit game
        if event.key is pyasge.KEYS.KEY_ESCAPE:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                self.quit = True
                return

    def click_event(self, event: pyasge.ClickEvent) -> None:
        if event.button is pyasge.MOUSE.MOUSE_BTN1:
            if event.action is pyasge.MOUSE.BUTTON_PRESSED:
                self.mouse_click[event.button] = event.action is pyasge.MOUSE.BUTTON_PRESSED
            if event.action is pyasge.MOUSE.BUTTON_RELEASED:
                if self.return_select is True:
                    self.is_game_over = False

    def mouseMovement(self, event: pyasge.MoveEvent):
        self.mouse_x = event.x
        self.mouse_y = event.y

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        """ If return item is selected transition to appropriate state else return GAME_OVER """
        if self.return_text.x <= self.mouse_x <= (self.return_text.x + self.return_text.width):
            if self.return_text.y - 40 <= self.mouse_y <= self.return_text.y:
                self.return_text.colour = pyasge.COLOURS.RED
                self.return_select = True
            else:
                self.return_text.colour = pyasge.COLOURS.WHITE
                self.return_select = False
        else:
            self.return_text.colour = pyasge.COLOURS.WHITE
            self.return_select = False

        # controller
        if self.data.inputs.getGamePad(0).connected:
            if self.data.inputs.getGamePad(0).START:
                self.is_game_over = False

        if self.is_game_over is False:
            return GameStateID.START_MENU
        else:
            return GameStateID.GAME_OVER

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.render(self.ui_text)
        self.data.renderer.render(self.return_text)
        self.data.renderer.render(self.contr_image)
        self.data.renderer.render(self.clicky_image)


