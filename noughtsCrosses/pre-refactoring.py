from pprint import pprint
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

# Player turn: 0/1


class GameState():
    def __init__(self):
        self.turn = None
        self.debug = True # Console output variable
        self.trackedGridState = None
        self.trackedGridClickedBy = None
        self.won = False
        self.wonBy = False
    
    def setup(self):
        # AFTER WINNING
        self.won = False # Sets the true when the game has been won
        self.wonBy = False
    
    def incrementTurn(self):
        # Swaps player turns from 1 to 2
        self.turn = 0 if self.turn else 1
        if self.debug: print(self.turn)

class GridCell(arcade.SpriteSolidColor):
    def __init__(self, WIDTH, HEIGHT, COLOR, row, column):
        super().__init__(WIDTH, HEIGHT, COLOR)

        """ REFERENCE:
        print("DEBUG")
        self.grid_sprites[0][0].color = arcade.color.BLUE
        print(self.grid_sprites[0][0].color)
        print("END DEBUG")
        """

        self.clickedBy = None
        self.row = row
        self.column = column
        self.clickedBy = None
        self.state = "notClicked"
        self.winningCell = False

    def reset(self):
        self.color = self.COLOR
        self.winningCell = False
        
    def occupied(self):
        if self.state == "notClicked": 
            print("Not occupied")
            return False
        else: 
            print("Occupied")
            return True

    def clicked(self):
        print(f"Row {self.row}, Column {self.column}")
        if gameState.turn == 0: # Player 1
                self.color = arcade.color.BLUE
                self.clickedBy = 0
        elif gameState.turn == 1: # Player 2
            self.color = arcade.color.RED
            self.clickedBy = 1
        self.state = "occupied"
         
        
        
class TicTacToe(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(LIGHT_BLUE)

        # Sprite Lists
        self.grid_sprite_list = arcade.SpriteList()

        # 2D Representation of 1D sprite list
        # [6 7 8]
        # [3 4 5]
        # [0 1 2]   
        self.grid_sprites = []

        gameState.turn = None
             
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
        gameState.turn = 0

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
    
    def trackGrid(self):
        # Tracks the grid state ie. clicked / unclicked
        trackedGridState = []
        for row in range(ROW_COUNT):
            trackedGridState.append([])
            for column in range(COLUMN_COUNT):
                trackedGridState[row].append(self.grid_sprites[row][column].state)
        #trackedGridState.reverse() ############

        # Tracks who the grid is clicked by
        trackedGridClickedBy = []
        for row in range(ROW_COUNT):
            trackedGridClickedBy.append([])
            for column in range(COLUMN_COUNT):
                trackedGridClickedBy[row].append(self.grid_sprites[row][column].clickedBy)
        #trackedGridClickedBy.reverse() #########

        gameState.trackedGridState = trackedGridState
        gameState.trackedGridClickedBy = trackedGridClickedBy

        pprint(gameState.trackedGridState)
        pprint(gameState.trackedGridClickedBy)
    
    def calculateWin(self):
        """
        Method to analyse the current grid configuration to find whether any combinations are winning: 3 (or X) in a row.
        Ie: Where X wins
        COLUMN  COLUMN  COLUMN  ROW     ROW     ROW       DIAGONAL
        X 0 0   0 X 0   0 0 X   X X X   O O O   0 0 0   X 0 0   0 0 X
        X 0 0   0 X 0   0 0 X   O O O   X X X   0 0 0   0 X 0   0 X 0 
        X 0 0   0 X 0   0 0 X   O O O   O O O   X X X   0 0 X   X 0 0 
                                DONE    DONE    DONE

        """
        ####
        #### IMPLEMENT WINNING SQUARE ATTRIBUTE TO EACH GRID CELL
        ####
        ####

        ## IMPLEMENTED ROW CHECKING
        gcb = gameState.trackedGridClickedBy

        for row in gcb:
            if all(x==row[0] for x in row) and row[0] != None:
                #print(f"3 in row on {gcb.index(row)} won by player {row[0]}")
                self.hasWon(_type = "row", pos = gcb.index(row), winner = row[0])
                
                # self.grid_sprites[gcb.index(row)][0].color = arcade.color.GREEN
                # self.grid_sprites[gcb.index(row)][1].color = arcade.color.GREEN
                # self.grid_sprites[gcb.index(row)][2].color = arcade.color.GREEN

                # Updates the winning cell property so the cells can be highlighted later
                for index in range(0, ROW_COUNT):
                    self.grid_sprites[gcb.index(row)][index].winningCell = True
                    

        ### IMPLEMENTED COLUMN CHECKING
        for i in gcb:
            vals, currColumn = [], gcb.index(i)
            for j in range(0,len(i)):
                curr = gcb[j][gcb.index(i)]
                vals.append(curr)
            if all(x==vals[0] for x in vals) and vals[0] != None: 
                print(f"Column {currColumn} has 3 in a row")
                self.hasWon(_type = "column", pos = currColumn, winner = vals[0])

                # Updates the winning cell property so the cells can be highlighted later
                for index in range(0, COLUMN_COUNT):
                    self.grid_sprites[index][currColumn].winningCell = True

            vals.clear() # Clear the temporary list containing column cell values
        
        # IMPLEMENT DIAGONAL CHECKING - NOT DYNAMIC RIGHT NOW AND ONLY WORKS WITH 3X3
        # DIAGONAL L2R
        if gcb[0][0] != None:
            if gcb[0][0] == gcb[1][1] and gcb[0][0] == gcb[2][2]:
                #print("DIAGONAL 3 X 3 LTR")
                self.hasWon(_type = "DIAGONAL", pos = "3 X 3 LTR", winner = gcb[0][0])
        if gcb[0][2] != None:
            if gcb[0][2] == gcb[1][1] and gcb[0][2] == gcb[2][0]:
                #print("DIAGONAL 3 X 3 RTL")
                self.hasWon(_type = "DIAGONAL", pos = "3 X 3 RTL", winner = gcb[0][2])
    
    def hasWon(self, _type, pos, winner): # Column, Row, Diagonal / row 1,2,3, etc... / 0,1
        print(f"3 in a row on {_type} {pos} by player {winner} aka ({winner+1})")
        gameState.won = True
        gameState.wonBy = winner


    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """

        clicked = arcade.get_sprites_at_point((x, y), self.grid_sprite_list)
        if clicked:
            for cell in clicked:     
                # print(f"cell state {cell.state}")
                if cell.state == "notClicked":
                    cell.clicked()
                    gameState.incrementTurn()
                else:
                    print("Cell Occupied")
        self.trackGrid()
        self.calculateWin()
        
gameState = GameState()
gameState.setup()

def main():
    """ Main function """
    game = TicTacToe(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()