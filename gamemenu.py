import pyasge

from gamestate import GameState
from gamestate import GameStateID


class GameMenu(GameState):

    def __init__(self, data) -> None:
        super().__init__(data)
        self.id = GameStateID.START_MENU
        self.quit = False

        self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_MOVE, self.mouseMovement)
        self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.click_event)

        self.is_menu = True
        self.ui_text = pyasge.Text(self.data.fonts['kenvector'], "GAME MENU")
        self.ui_text.scale = 1
        self.ui_text.position = [32 * 12 - (self.ui_text.width / 2), 300]
        self.ui_text.z_order = 10
        self.ui_text.colour = pyasge.COLOURS.AQUA

        self.play_text = pyasge.Text(self.data.fonts['kenvector'], "PLAY WITH MOUSE")
        self.play_text.scale = 1
        self.play_text.position = pyasge.Point2D(32 * 12 - (self.play_text.width / 2 - 73), 500)
        self.play_text.z_order = 10
        self.play_text.colour = pyasge.COLOURS.WHITE

        self.play_text_contr = pyasge.Text(self.data.fonts['kenvector'], "PLAY WITH\nCONTROLLER")
        self.play_text_contr.scale = 1
        self.play_text_contr.position = pyasge.Point2D(32 * 12.5 - (self.play_text_contr.width / 2), 700)
        self.play_text_contr.z_order = 10
        self.play_text_contr.colour = pyasge.COLOURS.WHITE

        self.clicky_image = pyasge.Sprite()
        self.clicky_image.loadTexture("data/images/PNG/clickyimage.png")
        self.clicky_image.scale = 0.1
        self.clicky_image.x = self.play_text.width - self.play_text.width + 75
        self.clicky_image.y = 430

        self.contr_image = pyasge.Sprite()
        self.contr_image.loadTexture("data/images/PNG/Xbox_button_A.png")
        self.contr_image.scale = 0.1
        self.contr_image.x = self.play_text.width - self.play_text.width + 75
        self.contr_image.y = 660

        self.play_select = False
        self.quit_select = False
        self.mouse_x = 0
        self.mouse_y = 0

        # track mouse states
        self.mouse_click = {
            pyasge.MOUSE.MOUSE_BTN1: False
        }

    def input(self, event: pyasge.KeyEvent) -> None:
        """ Handles the user input to select menu items """
        # exit menu
        if event.key is pyasge.KEYS.KEY_ESCAPE:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                self.quit = True
                return

    def click_event(self, event: pyasge.ClickEvent) -> None:
        if event.button is pyasge.MOUSE.MOUSE_BTN1:
            if event.action is pyasge.MOUSE.BUTTON_PRESSED:
                self.mouse_click[event.button] = event.action is pyasge.MOUSE.BUTTON_PRESSED
            if event.action is pyasge.MOUSE.BUTTON_RELEASED:
                if self.play_select is True:
                    self.is_menu = False

    def mouseMovement(self, event: pyasge.MoveEvent):
        self.mouse_x = event.x
        self.mouse_y = event.y

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        """ If menu item is selected transition to appropriate state else return START_MENU """

        if self.play_text.x <= self.mouse_x <= (self.play_text.x + self.play_text.width):
            if self.play_text.y - 40 <= self.mouse_y <= self.play_text.y:
                self.play_text.colour = pyasge.COLOURS.RED
                self.play_select = True
            else:
                self.play_text.colour = pyasge.COLOURS.WHITE
                self.play_select = False
        else:
            self.play_text.colour = pyasge.COLOURS.WHITE
            self.play_select = False

        if self.data.inputs.getGamePad(0).connected:
            if self.data.inputs.getGamePad(0).A:
                self.is_menu = False

        if self.is_menu is False:
            return GameStateID.GAMEPLAY
        else:
            return GameStateID.START_MENU

    def render(self, game_time: pyasge.GameTime) -> None:
        """ Use pygame to draw the menu """
        self.data.renderer.render(self.ui_text)
        self.data.renderer.render(self.play_text)
        self.data.renderer.render(self.play_text_contr)
        self.data.renderer.render(self.contr_image)
        self.data.renderer.render(self.clicky_image)

        pass
