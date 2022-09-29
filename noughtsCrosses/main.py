import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Aiyush Gupta - Tic Tac Toe"

# Player Grid 3X3 with spacing between the cells
ROW_COUNT = 3
COLUMN_COUNT = 3
MARGIN = 10
WIDTH = 100
HEIGHT = 100

# COLOUR PALLETE -  https://coolors.co/palette/8ecae6-219ebc-023047-ffb703-fb8500
LIGHT_BLUE = (142, 202, 230)
MEDIUM_BLUE = (33, 158, 188)
DARK_BLUE = (2, 48, 71)
YELLOW = (255, 183, 3)
ORANGE = (255, 183, 3)

class GridCell(arcade.SpriteSolidColor):
    def __init__(self, WIDTH, HEIGHT, COLOR, row, column):
        super().__init__(WIDTH, HEIGHT, COLOR)

        self.clickedBy = None
        self.row = row
        self.column = column
        self.clickedBy = None
        self.state = "notClicked"
        self.turn = None # Player that clicked cell 1 / 2 etc...
    
    def reset(self):
        self.color = self.COLOR
    
    def clicked(self):
        if self.state == "notClicked":
            if self.turn == 1:
                self.color = arcade.color.BLUE
            elif self.turn == 2:
                self.color = arcade.color.RED
        
    def updateTurn(self, turn):
        self.turn = turn

class TicTacToe(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(LIGHT_BLUE)

        # Sprite Lists
        self.grid_sprite_list = arcade.SpriteList()
        self.turn = None

        # 2D Representation of 1D sprite list
        # [6 7 8]
        # [3 4 5]
        # [0 1 2]   
        self.grid_sprites = []
             

        # Draw UI
        self.drawGrid()

        # print(f"Grid sprites: {self.grid_sprites}")
    
    def drawGrid(self):
        # Cells as sprites
        for row in range(ROW_COUNT):
            self.grid_sprites.append([])
            for column in range(COLUMN_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                # Create each sprite with a default bg colour
                #sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, MEDIUM_BLUE)
                sprite = GridCell(WIDTH, HEIGHT, MEDIUM_BLUE, row, column)
                sprite.center_x = x
                sprite.center_y = y
                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)
        
        self.grid_sprite_list.move(
            (SCREEN_WIDTH // 2) - (COLUMN_COUNT*(WIDTH+MARGIN)) // 2, 
            (SCREEN_HEIGHT // 2) - (ROW_COUNT*(HEIGHT+MARGIN)) // 2
        )

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        self.turn = 1

    def on_draw(self):
        """
        Render the screen.
        """

        # Clears the screen to the background colour and removes what was last drawn
        self.clear()

        # Calls draw on sprite lists
        self.grid_sprite_list.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """

        clicked = arcade.get_sprites_at_point((x, y), self.grid_sprite_list)
        if clicked:
            for cell in clicked: 
                cell.updateTurn(self.turn)
                cell.clicked()
                self.turn += 1
                #############
                ############# FIX TURN SYSTEM
                ############
            print(f"turn: {self.turn}")

def main():
    """ Main function """
    game = TicTacToe(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()