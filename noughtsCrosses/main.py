from pprint import pprint # Debugging
import arcade
import arcade.gui
import os
from utility import * # My own library for managing theming
import random # For the computers turn

### TODO:
### Implement Rounds DONE
### Implement Computer vs 1
###### Implement a simulated click
### Implement difficulty


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
        self.state = "notClicked"
        self.winningCell = False
        self.animationFinished = False

    def reset(self):
        self.color = self.COLOR
        self.winningCell = False
    
    def isWinningCell(self):
        if self.winningCell:
            return True
    
    def update_animation(self, delta_time):
        if self.winningCell:
            my_target_color = WINNING_COLOUR # GREEN
            transition_speed = 0.1
            current_color = self.color
            
            colour = (
                current_color[0] + (transition_speed * (my_target_color[0] - current_color[0])), 
                current_color[1] + (transition_speed * (my_target_color[1] - current_color[1])), 
                current_color[2] + (transition_speed * (my_target_color[2] - current_color[2]))) 

            self.color = colour
            


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
                self.color = P1_COLOUR
                self.clickedBy = 0
        elif gameState.turn == 1: # Player 2
            self.color = P2_COLOUR
            self.clickedBy = 1
        self.state = "occupied"

class GameState():
    def __init__(self):
        self.turn = None
        self.debug = True # Console output variable
        self.trackedGridState = None
        self.trackedGridClickedBy = None
        self.won = False
        self.wonBy = False
        self.round = 0
        self.backingTack = arcade.Sound(":resources:music/funkyrobot.mp3")
        self.backingTack.play(loop=True)

        self.p0Score = 0
        self.p1Score = 0

        # GUI
        self.mode = "1v1" # vComputer / 1v1
        self.numberOfRounds = "5" # 3 / 5 / 10
        self.difficulty = "easy" # easy / difficult
    
    def reset(self):
        # Call when going back to the menu alongisde setup
        self.p0Score = 0 
        self.p1Score = 0
    
    # For next round
    def setup(self):
        # AFTER WINNING
        self.won = False # Sets the true when the game has been won
        self.wonBy = False
        self.turn = 0
        
    
    def incrementTurn(self):
        # Swaps player turns from 1 to 2
        self.turn = 0 if self.turn else 1
        if self.debug: print(f"\n Turn: {self.turn}")

class GameView(arcade.View):
    """
    Main application class
    """

    def __init__(self):
        super().__init__()

        # Set the path to start with this program
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Scene Object 
        # Tool to manage a number of different SpriteLists by assigning each one a name, 
        # and maintaining a draw order.

        self.scene = None
        self.grid_sprite_list = None
        self.grid_sprites = None

        # Audio
        #self.backingTrack = None
        self.winTrack = None
        self.clickTrack = None

        # State Management
        gameState.turn = None
    
    def setup(self):
        """ Game Setup, call function to restart / start (from scratch) the game"""

        # Cameras
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        
        # Scene init and config
        self.scene = arcade.Scene()

        # Create Sprite Lists
        self.scene.add_sprite_list(LAYER_NAME_GRID, self.grid_sprite_list)

        self.grid_sprite_list = arcade.SpriteList()
        self.grid_sprites = []
        gameState.turn = 0
        
        # Audio
        self.winTrack = arcade.Sound(":resources:sounds/upgrade2.wav")
        self.clickTrack = arcade.Sound(":resources:sounds/hit4.wav")
        self.noWinTrack = arcade.Sound(":resources:sounds/lose2.wav")

        
        # Grid Creation
        # Stores grid in grid_spire_list and grid_sprites (as representational 2D array)
        # Cells stored as Sprites
        for row in range(ROW_COUNT):
            self.grid_sprites.append([])
            for column in range(COLUMN_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                # Create each sprite with a default bg colour
                #sprite = arcade.SpriteSolidColor(WIDTH, HEIGHT, MEDIUM_BLUE)
                sprite = GridCell(WIDTH, HEIGHT, STARTING_CELL_COLOUR, row, column)
                sprite.center_x = x
                sprite.center_y = y
                #self.grid_sprite_list.append(sprite)
                self.scene.add_sprite(LAYER_NAME_GRID, sprite)
                self.grid_sprites[row].append(sprite)
        
        self.scene[LAYER_NAME_GRID].move(
            (SCREEN_WIDTH // 2) - (COLUMN_COUNT*(WIDTH+MARGIN)) // 2, 
            (SCREEN_HEIGHT // 2) - (ROW_COUNT*(HEIGHT+MARGIN)) // 2
        )
        
        

        # -- Other Stuff
        # Set bg colour
        arcade.set_background_color(BACKGROUND_COLOR)

    def on_show_view(self):
        """Function ran when the view changed to 'Game View' """
        self.setup()
    
    def on_draw(self):
        """ Render the screen"""
        # Clear the screen to the background colour
        self.clear()

        # Switch to GUI camera before drawing GUI items
        # 1. Score / Menu / Timer etc...
        self.gui_camera.use()

        """
        GUI ELEMENTS:
        BG / TITLE / ROUND etc..
        """

        arcade.draw_rectangle_filled(
            center_x = self.scene[LAYER_NAME_GRID].center[0], 
            center_y = self.scene[LAYER_NAME_GRID].center[1], 
            width = ROW_COUNT*(WIDTH+1.5*MARGIN), 
            height= COLUMN_COUNT*(HEIGHT+1.5*MARGIN), 
            color = FRAME_COLOR # (182, 213, 227) OLD
        )
        
        textTitle = arcade.Text(theme[THEME]["GUI_TITLE"],
                         140,
                         SCREEN_HEIGHT - 80,
                         theme[THEME]["TITLE_COLOUR"],
                         theme[THEME]["GUI_TITLE_FONT_SIZE"],
                         font_name = theme[THEME]["GUI_TITLE_FONT"],)
        
        textPlayer = arcade.Text(f"Player: {gameState.turn + 1}",
                         300,
                         70,
                         theme[THEME]["SUBTITLE_COLOUR"],
                         theme[THEME]["GUI_SUBTITLE_FONT_SIZE"],
                         font_name = theme[THEME]["GUI_SUBTITLE_FONT"])

        textRound = arcade.Text(f"Round {gameState.round}",
                         320,
                         30,
                         theme[THEME]["SUBTITLE_COLOUR"],
                         theme[THEME]["GUI_SUBTITLE_FONT_SIZE"],
                         font_name=theme[THEME]["GUI_SUBTITLE_FONT"])
        
        p0Score = arcade.Text(f"P1 Score: {gameState.p0Score}",
                         25,
                         70,
                         theme[THEME]["SUBTITLE_COLOUR"],
                         theme[THEME]["GUI_SUBTITLE_FONT_SIZE"],
                         font_name=theme[THEME]["GUI_SUBTITLE_FONT"])
        
        if gameState.mode == "vComputer": player = "CPU"
        else: player = "P2"
        p1Score = arcade.Text(f"{player} Score: {gameState.p1Score}",
                         25,
                         30,
                         theme[THEME]["SUBTITLE_COLOUR"],
                         theme[THEME]["GUI_SUBTITLE_FONT_SIZE"],
                         font_name=theme[THEME]["GUI_SUBTITLE_FONT"])
        
        # Place text in the center of the screen: x start = (screen width / 2) - (content width / 2)
        textRound.x = (SCREEN_WIDTH / 2) - (textRound.content_width / 2)
        textPlayer.x = (SCREEN_WIDTH / 2) - (textPlayer.content_width / 2)
        textTitle.x = (SCREEN_WIDTH / 2) - (textTitle.content_width / 2)

        textRound.draw()
        textPlayer.draw()
        textTitle.draw()

        p0Score.draw()
        p1Score.draw()

        # Activate Camera (to be used for screen effects)
        self.camera.use()

        # Draw Scene
        self.scene.draw()
        # self.grid_sprite_list.draw()

        
        """
        ADD GUI CODE HERE
        """
    
    def on_update(self, delta_time):
        """ Movement / Game Logic"""
        allOccupied = True
        for sprite in self.scene[LAYER_NAME_GRID]:
            sprite.isWinningCell()

            # If the grid is filled but there is no wining state then move onto the next round
            if sprite.state == "notClicked":
                allOccupied = False 
        if allOccupied:
            self.trackGrid()
            #self.calculateWin()
            arcade.pause(1)
            self.noWinTrack.play()
            self.nextRound()
        
        if gameState.mode == "vComputer":
            if gameState.turn == 1:
                self.computerTurn()

        # Update Animations
        self.scene.update_animation(
            delta_time, 
            [LAYER_NAME_GRID]
        )

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """

        # If the game has been won by someone then go to the next round
        if not gameState.won:
    
            clicked = arcade.get_sprites_at_point((x, y), self.scene[LAYER_NAME_GRID])
            if clicked:
                for cell in clicked:     
                    print(f"cell state {cell.state}")
                    if cell.state == "notClicked":
                        self.clickTrack.play()
                        cell.clicked()
                        gameState.incrementTurn()
                    else:
                        print("Cell Occupied")
            self.trackGrid()
            self.calculateWin()

            
        else:
            self.nextRound()
    
    def computerTurn(self):
        """ Simulated playing via the computer """
        # Requirements:
        # Click a random cell
        # Click a cell that isn't already clicked

        # One way to tackle the difficult mode could be to use a minimax function
        if not gameState.won:
            chosenCell = False
            while not chosenCell:
                # print(self.grid_sprites[0][0].state)
                randCell = random.choice(self.scene[LAYER_NAME_GRID])
                if randCell.state == "notClicked":
                    chosenCell = True
            
            randCell.clicked()
            gameState.incrementTurn()

            self.trackGrid()
            self.calculateWin()
            

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
        
        #print("\n")
        #gameState.trackedGridState.reverse()
        #pprint(gameState.trackedGridState)
        #print("\n")

        # DEBUG PRETTY PRINT
        #pprint(gameState.trackedGridState)
        #pprint(gameState.trackedGridClickedBy)
    
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

                # Updates the winning cell property so the cells can be highlighted later
                self.grid_sprites[0][0].winningCell = True
                self.grid_sprites[1][1].winningCell = True
                self.grid_sprites[2][2].winningCell = True
        
        
        if gcb[0][2] != None:
            if gcb[0][2] == gcb[1][1] and gcb[0][2] == gcb[2][0]:
                #print("DIAGONAL 3 X 3 RTL")
                self.hasWon(_type = "DIAGONAL", pos = "3 X 3 RTL", winner = gcb[0][2])
                self.grid_sprites[0][2].winningCell = True
                self.grid_sprites[1][1].winningCell = True
                self.grid_sprites[2][0].winningCell = True

    
    def hasWon(self, _type, pos, winner): # Column, Row, Diagonal / row 1,2,3, etc... / 0,1
        print(f"3 in a row on {_type} {pos} by player {winner} aka ({winner+1})")
        gameState.won = True
        gameState.wonBy = winner
        if int(winner) == 0:
            gameState.p0Score+= 1
        elif int(winner) == 1:
            gameState.p1Score += 1

        self.winTrack.play()
    
    def nextRound(self):
        gameState.round += 1
        print(f"Round: {gameState.round}")
        print(f"Total number of rounds: {gameState.numberOfRounds}")

        if int(gameState.numberOfRounds) < gameState.round:
            print(f"{gameState.numberOfRounds} < {gameState.round}")
            end_view = GameEnd()
            self.window.show_view(end_view)
        else:
            gameState.setup()
            game_view = GameView()
            self.window.show_view(game_view)

class GameEnd(arcade.View):
    def __init__(self):
        super().__init__()
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)
    
    def on_draw(self):
        """
        TITLE
        WINNER
        MODE 
        DIFFICULTY
        """

        self.clear()
        self.gui_camera.use()

        textTitle = arcade.Text("END OF GAME",
            140,
            SCREEN_HEIGHT - 80,
            theme[THEME]["TITLE_COLOUR"],
            theme[THEME]["GUI_TITLE_FONT_SIZE"],
            font_name = theme[THEME]["GUI_TITLE_FONT"])
        
        textTitle.x = (SCREEN_WIDTH / 2) - (textTitle.content_width / 2)
        textTitle.y = (SCREEN_HEIGHT / 2)
        textTitle.draw()

class MainMenu(arcade.View):
    """ Class that manages the 'menu' view """
    #arcade.set_background_color(BACKGROUND_COLOR)

    def __init__(self):
        super().__init__()

        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        # Create and enable the UIManager
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Create a box group to align the 'AI / 1V1' button in the center
        self.v_box = arcade.gui.UIBoxLayout(
            space_between= 10,
        )
        self.v_box_rounds_text = arcade.gui.UIBoxLayout(
            space_between=10,
        )
        

        # Style for button
        buttonStyle = {
            "bg_color": WINNING_COLOUR,
            "bg_color_pressed": TITLE_COLOUR,
            "font_color_pressed": BACKGROUND_COLOR,
            "border_color_pressed": BACKGROUND_COLOR,
            "font_name": "Kenney Pixel Square",
            "font_size": 20,
        }
        # Create a button. We'll click on this to open our window.
        # Add it v_box for positioning.

        ### Choose Opponent
        self.button_1v1 = arcade.gui.UIFlatButton(
            text="1 vs 1", width=300, style=buttonStyle
        )
        self.button_vComputer = arcade.gui.UIFlatButton(
            text="1 vs Computer", width=300, style = buttonStyle
        )

        ### Choose Number of Rounds
        self.ui_text_label = arcade.gui.UITextArea(
            text="Rounds:",
            width=300,
            height=40,
            font_size=20,
            font_name="Kenney Pixel Square",
            text_color=TITLE_COLOUR
            )
        self.v_box_rounds_text.add(self.ui_text_label)

        self.managerRounds = arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-50,
                align_x=-10,
                child=self.v_box_rounds_text)

        self.button_round_3 = arcade.gui.UIFlatButton(
            text="3", width=100, style = buttonStyle
        )

        self.button_round_5 = arcade.gui.UIFlatButton(
            text="5", width=100, style = buttonStyle
        )

        self.button_round_10 = arcade.gui.UIFlatButton(
            text="10", width=100, style = buttonStyle
        )

        ### Choose Difficulty
        self.button_easy = arcade.gui.UIFlatButton(
            text="easy", width=200, style = buttonStyle
        )

        self.button_difficult = arcade.gui.UIFlatButton(
            text="difficult", width=200, style = buttonStyle
        )

        # VBOX Intial 
        self.v_box.add(self.button_1v1)
        self.v_box.add(self.button_vComputer)


        # Add a hook to run when we click on the button.
        self.button_1v1.on_click = self.button_1v1_clicked
        self.button_vComputer.on_click = self.button_vComputer_clicked

        self.button_round_3.on_click = self.round3
        self.button_round_5.on_click = self.round5
        self.button_round_10.on_click = self.round10

        self.button_easy.on_click = self.choseEasy
        self.button_difficult.on_click = self.choseDifficult

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-120,
                child=self.v_box)
        )
    
    # There must be a more efficient way to do this ... :(
    def round3(self, event): 
        gameState.numberOfRounds = 3
        self.chooseDifficulty()
    def round5(self, event): 
        gameState.numberOfRounds = 5
        self.chooseDifficulty()
    def round10(self, event): 
        gameState.numberOfRounds = 10
        self.chooseDifficulty()
    
    def choseEasy(self, event):
        gameState.difficulty = "easy"
        self.manager.disable()
        self.goToGame()
    
    def choseDifficult(self, event):
        gameState.difficulty = "difficult"
        self.manager.disable()
        self.goToGame()
    
    def chooseDifficulty(self):
        if gameState.mode =="vComputer":
            self.v_box.clear()
            self.manager.remove(self.managerRounds)
            self.v_box.add(self.button_easy)
            self.v_box.add(self.button_difficult)
        else: 
            self.manager.disable()
            self.goToGame()
    
    def chooseRounds(self):
        self.v_box.clear()
        self.v_box.vertical = False
        # self.v_box.add(self.ui_text_label)
        self.manager.add(self.managerRounds)
        self.v_box.add(self.button_round_3)
        self.v_box.add(self.button_round_5)
        self.v_box.add(self.button_round_10)
    
    def button_1v1_clicked(self, event):
        gameState.mode = "1v1"
        self.chooseRounds()
    
    def button_vComputer_clicked(self, event):
        gameState.mode = "vComputer"
        self.chooseRounds()
    
    def goToGame(self):
        print(f"""
        Mode: {gameState.mode}
        Number of rounds: {gameState.numberOfRounds}
        Difficulty: {gameState.difficulty}
        """)
        game_view = GameView()
        self.window.show_view(game_view)

    def setup(self):
        print("setup")
        arcade.set_background_color(BACKGROUND_COLOR)
    
    def on_show_view(self):
        self.setup()

    def on_draw(self):
        """
        TITLE
        buttons: ONE PLAYER / TWO PLAYER
        buttons: Rounds: 1 / 2 / 3
        IF ONE PLAYER:
            buttons: DIFFICULTY: EASY / HARD
            buttons: PLAYER_ORDER: COMPUTER / PERSON IS P1
        """

        self.clear()
        self.gui_camera.use()
        self.manager.draw()
        

        textTitle = arcade.Text(theme[THEME]["GUI_TITLE"],
            140,
            SCREEN_HEIGHT - 80,
            theme[THEME]["TITLE_COLOUR"],
            theme[THEME]["GUI_TITLE_FONT_SIZE"],
            font_name = theme[THEME]["GUI_TITLE_FONT"])
        
        textTitle.x = (SCREEN_WIDTH / 2) - (textTitle.content_width / 2)
        textTitle.y = (SCREEN_HEIGHT / 2)
        textTitle.draw()
                    

gameState = GameState()
gameState.setup()

def main():
    """ Main function """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    
    title_view = MainMenu()
    window.show_view(title_view)

    #game_view = GameView()
    #window.show_view(game_view)
    #game = TicTacToe(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    #game.setup()
    arcade.run()


if __name__ == "__main__":
    main()