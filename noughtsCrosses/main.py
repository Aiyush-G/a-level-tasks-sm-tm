from pprint import pprint   # Debugging
import arcade
import arcade.gui
import os
from utility import *       # My own library for managing theming
import random               # For the computers turn


class GridCell(arcade.SpriteSolidColor):
    """ Class that represents a single grid cell by tracking its' state, clicked by, colour etc..."""
    def __init__(self, WIDTH, HEIGHT, COLOR, row, column):
        super().__init__(WIDTH, HEIGHT, COLOR)

        """ REFERENCE:
        print("DEBUG")
        self.grid_sprites[0][0].color = arcade.color.BLUE
        print(self.grid_sprites[0][0].color)
        print("END DEBUG")
        """

        self.clickedBy = None               # Clicked By: P1 / P2 / Computer
        self.row = row                      # Any value =< ROW_COUNT
        self.column = column                # Any value =< COLUMN_COUNT
        self.state = "notClicked"           # State: notClicked, occupied
        self.winningCell = False            # Allows the state change to be animated
        self.animationFinished = False      # Helper variable for animations

    def reset(self):
        """ To be called when the grid is redrawn to reset necessary variable values"""
        self.color = self.COLOR
        self.winningCell = False
    
    def isWinningCell(self):
        """ Returns value of variable: Utility function, this could be reimplemented as an anonomous function"""
        if self.winningCell:
            return True
    
    def update_animation(self, delta_time):
        if self.winningCell:
            my_target_color = WINNING_COLOUR # Contains RGB 
            transition_speed = 0.1           # Max value is 1
            current_color = self.color
            
            # Interpolation between the two colours
            # Color = R, G, B
            # Interpolation: transition speed * (end colour - start color)
            colour = (
                current_color[0] + (transition_speed * (my_target_color[0] - current_color[0])), 
                current_color[1] + (transition_speed * (my_target_color[1] - current_color[1])), 
                current_color[2] + (transition_speed * (my_target_color[2] - current_color[2]))) 

            self.color = colour
            


    def occupied(self):
        """ 
        Returns state of cell: helper function
        Print statements here are for debugging
        """
        if self.state == "notClicked": 
            print("Not occupied")
            return False
        else: 
            print("Occupied")
            return True

    def clicked(self):
        """ 
        When a cell is clicked, if it is clicked by player 1 then change to their colour, else, player 2 colour.
        Update who the cell was clicked by
        Update the state of the cell to occupied
        """
        print(f"Row {self.row}, Column {self.column}")

        if gameState.turn == 0: # Player 1
                self.color = P1_COLOUR
                self.clickedBy = 0
        elif gameState.turn == 1: # Player 2
            self.color = P2_COLOUR
            self.clickedBy = 1
        self.state = "occupied"

class GameState():
    """
    Class that holds the "global" variables that should be shared between the entire application
    Ie. turn, grid etc...
    """
    def __init__(self):
        self.turn = None                    # 0 (Player 1) / 1 (Player 2)
        self.debug = True                   # Console output variable
        self.trackedGridState = None        # Unfortunately a limitation of the library is that there is no way that sprite 
        self.trackedGridClickedBy = None    # groups can be stored in 2D arrays, therefore, a separate array has to be instantiated
        self.won = False
        self.wonBy = False
        self.round = 0
        self.backingTack = arcade.Sound(":resources:music/funkyrobot.mp3")
        self.backingTack.play(loop=True)

        self.p0Score = 0                    # Tracks the player score, 
        self.p1Score = 0                    # Player 1 - Either human or CPU

        # GUI                               MAIN MENU OPTIONS
        self.mode = "1v1"                   # vComputer / 1v1
        self.numberOfRounds = "5"           # 3 / 5 / 10
        self.difficulty = "easy"            # easy / difficult
    
    def reset(self):
        # Obselete function but kept in main code as reference, replaced by setup
        # Call when going back to the menu alongisde setup
        self.p0Score = 0 
        self.p1Score = 0
    
    
    def setup(self):
        """
        When the gameScreen is first shown, reset the variable values. When a completely new game is created, this function
        is called again to reset those values.
        """
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
        self.winTrack = None    # To play when a player has won
        self.clickTrack = None  # To play when a cell has been clicked

        # State Management
        gameState.turn = None
    
    def setup(self):
        """ Game Setup, call function to restart / start (from scratch) the game"""

        # Cameras - each view has a different camera, this means that the screen items are drawn in different orders for z-index.
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)
        
        # Scene init and config
        self.scene = arcade.Scene()

        # Create Sprite Lists
        self.scene.add_sprite_list(LAYER_NAME_GRID, self.grid_sprite_list)

        # Grid sprite list contains an arcade reference to all the cells within the grid so that they can be batch manipulated
        # this was instructed by the docs, however, I believe storing them in a normal 2D array could work better.
        # The grid_sprites was this newer implementation that allowed the sprites to be stored in a 2d array representing their
        # position within the naught and crosses grid. Both were kept for different usage throughout the program, they are both
        # usually reference together.
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
        # Dynamic Creation fo a grid depending upon the number of rows / columns
        
        for row in range(ROW_COUNT):
            self.grid_sprites.append([])
            for column in range(COLUMN_COUNT):
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)                # X and Y coords generated dynamically
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)
                # Create each sprite with a default bg colour
                sprite = GridCell(WIDTH, HEIGHT, STARTING_CELL_COLOUR, row, column)
                sprite.center_x = x
                sprite.center_y = y
                self.scene.add_sprite(LAYER_NAME_GRID, sprite)
                self.grid_sprites[row].append(sprite)
        
        # Positioning
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
        """ Render the screen GUI"""
        # Clear the screen to the background colour
        self.clear()

        # Switch to GUI camera before drawing GUI items
        # 1. Score / Menu / Timer etc...
        self.gui_camera.use()

        """
        GUI ELEMENTS:
        BG / TITLE / ROUND etc..
        """

        # Background to the grid cells
        arcade.draw_rectangle_filled(
            center_x = self.scene[LAYER_NAME_GRID].center[0], 
            center_y = self.scene[LAYER_NAME_GRID].center[1], 
            width = ROW_COUNT*(WIDTH+1.5*MARGIN), 
            height= COLUMN_COUNT*(HEIGHT+1.5*MARGIN), 
            color = FRAME_COLOR # (182, 213, 227) OLD
        )
        
        # Text items, the theme that they are referencing is pulled from utils.py, a basic API has been constructed
        # to provide theming which could be implemented in a later version of naughts and crosses.
        textTitle = arcade.Text(theme[THEME]["GUI_TITLE"],
                         140,
                         SCREEN_HEIGHT - 80,
                         theme[THEME]["TITLE_COLOUR"],
                         theme[THEME]["GUI_TITLE_FONT_SIZE"],
                         font_name = theme[THEME]["GUI_TITLE_FONT"],)
        
        # Player X: Turn
        textPlayer = arcade.Text(f"Player: {gameState.turn + 1}",
                         300,
                         70,
                         theme[THEME]["SUBTITLE_COLOUR"],
                         theme[THEME]["GUI_SUBTITLE_FONT_SIZE"],
                         font_name = theme[THEME]["GUI_SUBTITLE_FONT"])

        # Rounds: 0 --> gameState.numberOfRounds
        textRound = arcade.Text(f"Round {gameState.round}",
                         320,
                         30,
                         theme[THEME]["SUBTITLE_COLOUR"],
                         theme[THEME]["GUI_SUBTITLE_FONT_SIZE"],
                         font_name=theme[THEME]["GUI_SUBTITLE_FONT"])
        
        # Player X Score
        p0Score = arcade.Text(f"P1 Score: {gameState.p0Score}",
                         25,
                         70,
                         theme[THEME]["SUBTITLE_COLOUR"],
                         theme[THEME]["GUI_SUBTITLE_FONT_SIZE"],
                         font_name=theme[THEME]["GUI_SUBTITLE_FONT"])
        
        # Depending on whether the CPU player is enabled the text varies: "CPU" / "P2" + Score: SCORE
        if gameState.mode == "vComputer": player = "CPU"
        else: player = "P2"
        p1Score = arcade.Text(f"{player} Score: {gameState.p1Score}",
                         25,
                         30,
                         theme[THEME]["SUBTITLE_COLOUR"],
                         theme[THEME]["GUI_SUBTITLE_FONT_SIZE"],
                         font_name=theme[THEME]["GUI_SUBTITLE_FONT"])
        
        # Place text in the center of the screen: x start = (screen width / 2) - (content width / 2)
        # Positioning
        textRound.x = (SCREEN_WIDTH / 2) - (textRound.content_width / 2)
        textPlayer.x = (SCREEN_WIDTH / 2) - (textPlayer.content_width / 2)
        textTitle.x = (SCREEN_WIDTH / 2) - (textTitle.content_width / 2)

        # Draw all items
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

    def on_update(self, delta_time):
        """ Movement / Game Logic"""

        # FLAG is used since if all the cells are occupied with no winner then the round needs to be incremented with no 
        # change in score. 
        # BUG -> FEATURE: if the winner makes their winning move in the last possible cell on the grid then they get double
        # points. At first this was a bug, however, it adds more skill to winning the game if you are behind on points. 
        allOccupied = True
        for sprite in self.scene[LAYER_NAME_GRID]:
            sprite.isWinningCell()

            # If the grid is filled but there is no wining state then move onto the next round
            if sprite.state == "notClicked":
                allOccupied = False 
        
        # Move onto next round if grid is full with some cleanup
        if allOccupied:
            self.trackGrid()
            #self.calculateWin()
            arcade.pause(1)
            self.noWinTrack.play()
            self.nextRound()
        
        # Computers turn after the player has "played"
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
            
            # Get a list, of the cells pressed at one time (hopefully just contains one cell)
            # If that cell has not been clicked before, then simulate a click on that cell 
            # and move to the next turn, change its' colour and play a sound.
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
            
            # Updates both references of the grid: 2D & 1D
            self.trackGrid()
            self.calculateWin()

            
        else:
            # If the game has been won then move to next round
            self.nextRound()
    
    def computerTurn(self):
        """ Simulated playing via the computer """
        # Requirements:
        # EASY:
        # Click a random cell
        # Click a cell that isn't already clicked

        # DIFFICULT: 
        # One way to tackle the difficult mode could be to use a minimax function
        # However, that results in an always draw or win for the CPU, therefore, 
        # by implementing common tic-tac-toe strategy with some randomness could make 
        # this more fair.
        # IE. take corners first then random

        # If game isn't won and game mode is easy then just select and click a random cell, loop if the cell is occupied already.
        if not gameState.won:
            chosenCell = False
            if gameState.difficulty == "easy": # Any random cell
                while not chosenCell:
                    # print(self.grid_sprites[0][0].state)
                    randCell = random.choice(self.scene[LAYER_NAME_GRID])
                    if randCell.state == "notClicked":
                        chosenCell = True

            elif gameState.difficulty == "difficult": # Corner cells first
                # Indexes order for self.scene[LAYER_NAME_GRID].state are as follows:
                # 0 1 2
                # 3 4 5 
                # 6 7 8 

                # If two corners are now occupied by CPU:
                # 0, 2 -> Select 1
                # 0, 6 -> Select 3
                # 2, 8 -> Select 5
                # 6, 2 -> Select 4
                # 8,0  -> Select 4


                cornerCellIndexes = [0, 8, 6, 2]
                currIndex = 0
                cornerCellsOccupiedBy = [] # cellIndex, whoBy
                occupyCornerCell, goForWin = True, False
                twoCornerCellsOccupied, twoCells = 0, []

                # Get a list of all the corner cells
                for turn in range(0, len(cornerCellIndexes)):
                    # Not the CPU is clicked by: 1 not 0 
                    cornerCellsOccupiedBy.append([cornerCellIndexes[turn],self.scene[LAYER_NAME_GRID][turn].clickedBy]) # cellIndex, whoBy
                # Check if two corners are occupied by the CPU, if so then it simulates a click of any other unocuppied cell.
                for gridC in cornerCellsOccupiedBy:
                    print(f"GRIDC: {gridC}")
                    if str(gridC[1]) == "1":            # Player 1
                        twoCornerCellsOccupied+= 1
                        twoCells.append(gridC[0])       # Index of the grid
                if twoCornerCellsOccupied == 2: 
                    goForWin = True
                    occupyCornerCell = False

                # If two corner cells occupied by the CPU then go for the winning combination
                if goForWin:
                    print(F"TWO CELLS: {twoCells}")
                    if twoCells == [0,2]: randCell = self.scene[LAYER_NAME_GRID][1]
                    elif twoCells == [0,6]: randCell = self.scene[LAYER_NAME_GRID][3]
                    elif twoCells == [2,8]: randCell = self.scene[LAYER_NAME_GRID][5]
                    elif twoCells == [6,2]: randCell = self.scene[LAYER_NAME_GRID][4]
                    elif twoCells == [8,0]: randCell = self.scene[LAYER_NAME_GRID][4]
                    print(f"INDEX TO BE CLICKED => TWO CORENER CELLS SELECTED: {self.scene[LAYER_NAME_GRID].index(randCell)}")

                    # If the winning cell is occupied then select another random cell
                    if not randCell.state == "notClicked": # AKA ITS OCCUPIED
                        occupyCornerCell = True

                # If cell is occupied then occupyCornerCell = True => it will select any random cell
                # Attempt to occupy any corner cell.
                if occupyCornerCell:
                    while not chosenCell:
                        randCell = self.scene[LAYER_NAME_GRID][cornerCellIndexes[currIndex]]
                        if randCell.state == "notClicked":
                            chosenCell = True
                        else:
                            if (currIndex + 1)> 3:
                                randCell = random.choice(self.scene[LAYER_NAME_GRID])
                                if randCell.state == "notClicked":
                                    chosenCell = True
                            else:
                                currIndex += 1
                                print(f"CurrIndex {currIndex}")
            
            # Click cell, increment turn, track 2D & 1D grid
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
       

        # Tracks who the grid is clicked by
        trackedGridClickedBy = []
        for row in range(ROW_COUNT):
            trackedGridClickedBy.append([])
            for column in range(COLUMN_COUNT):
                trackedGridClickedBy[row].append(self.grid_sprites[row][column].clickedBy)
        
        # Update in global state
        gameState.trackedGridState = trackedGridState
        gameState.trackedGridClickedBy = trackedGridClickedBy

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
        #### IMPLEMENTED WINNING SQUARE ATTRIBUTE TO EACH GRID CELL
        ####
        ####

        ## IMPLEMENTED ROW CHECKING
        gcb = gameState.trackedGridClickedBy

        # Checks each row to see if it is occupied by the same player
        # Calls hasWon when a winning row has been found
        for row in gcb:
            if all(x==row[0] for x in row) and row[0] != None:
                self.hasWon(_type = "row", pos = gcb.index(row), winner = row[0])
             
                # Updates the winning cell property so the cells can be highlighted later
                for index in range(0, ROW_COUNT):
                    self.grid_sprites[gcb.index(row)][index].winningCell = True
                    

        ### IMPLEMENTED COLUMN CHECKING, itterates through each column to check if it is occupied by the same player
        # Calls hasWon function when a winning column found
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
        
        # IMPLEMENTED DIAGONAL CHECKING - NOT DYNAMIC RIGHT NOW AND ONLY WORKS WITH 3X3
        # DIAGONAL L2R
        if gcb[0][0] != None:
            if gcb[0][0] == gcb[1][1] and gcb[0][0] == gcb[2][2]: # Combination of diagonal cells
                
                self.hasWon(_type = "DIAGONAL", pos = "3 X 3 LTR", winner = gcb[0][0])

                # Updates the winning cell property so the cells can be highlighted later
                self.grid_sprites[0][0].winningCell = True
                self.grid_sprites[1][1].winningCell = True
                self.grid_sprites[2][2].winningCell = True
        
        # RTL diagonal checking, hardcoded combinations, however, this could be done dynamically at a later stage.
        if gcb[0][2] != None:
            if gcb[0][2] == gcb[1][1] and gcb[0][2] == gcb[2][0]:
                
                self.hasWon(_type = "DIAGONAL", pos = "3 X 3 RTL", winner = gcb[0][2])
                self.grid_sprites[0][2].winningCell = True
                self.grid_sprites[1][1].winningCell = True
                self.grid_sprites[2][0].winningCell = True

    
    def hasWon(self, _type, pos, winner): # Column, Row, Diagonal / row 1,2,3, etc... / 0,1
        """ When the player has won, reflect this change in the game state alongside the winner, increase their score by 1"""
        print(f"3 in a row on {_type} {pos} by player {winner} aka ({winner+1})")
        gameState.won = True
        gameState.wonBy = winner
        if int(winner) == 0:
            gameState.p0Score+= 1
        elif int(winner) == 1:
            gameState.p1Score += 1

        # Winning sound
        self.winTrack.play()
    
    def nextRound(self):
        """ 
        Increments the game round by 1, if the next game round is greater than the number selected by the player in 
        the starting menu then change the game view to the GameEnd() View
        """
        gameState.round += 1
        print(f"Round: {gameState.round}")
        print(f"Total number of rounds: {gameState.numberOfRounds}")

        if int(gameState.numberOfRounds) < gameState.round:
            print(f"{gameState.numberOfRounds} < {gameState.round}")
            end_view = GameEnd()
            self.window.show_view(end_view)
        else: # If increment to next game then reset the game view and show it to the user
            gameState.setup()
            game_view = GameView()
            self.window.show_view(game_view)

class GameEnd(arcade.View):
    def __init__(self):
        super().__init__()
        # Set the camera to the entire screen
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)
    
    def on_draw(self):
        """
        Shows:
        TITLE
        WINNER
        MODE 
        DIFFICULTY
        """
        # On every draw call clear the screen
        self.clear()
        self.gui_camera.use()

        textTitle = arcade.Text("END OF GAME",
            140,
            SCREEN_HEIGHT - 80,
            theme[THEME]["TITLE_COLOUR"],
            theme[THEME]["GUI_TITLE_FONT_SIZE"],
            font_name = theme[THEME]["GUI_TITLE_FONT"])
        
        # P1 End Score
        score1Text = arcade.Text(f"P1 Score: {gameState.p0Score}",
            140,
            (SCREEN_HEIGHT / 2) - 60,
            theme[THEME]["SUBTITLE_COLOUR"],
            theme[THEME]["GUI_SUBTITLE_FONT_SIZE"],
            font_name = theme[THEME]["GUI_SUBTITLE_FONT"])
        
        # P2 End Score
        score2Text = arcade.Text(f"P2 Score: {gameState.p1Score}",
            140,
            (SCREEN_HEIGHT / 2) - 90,
            theme[THEME]["SUBTITLE_COLOUR"],
            theme[THEME]["GUI_SUBTITLE_FONT_SIZE"],
            font_name = theme[THEME]["GUI_SUBTITLE_FONT"])
        
        # Game Mode: 1V1 / 1 vs CPU
        gameModeText = arcade.Text(f"Mode: {gameState.mode}",
            140,
            (SCREEN_HEIGHT / 2) - 120,
            theme[THEME]["SUBTITLE_COLOUR"],
            theme[THEME]["GUI_SUBTITLE_FONT_SIZE"],
            font_name = theme[THEME]["GUI_SUBTITLE_FONT"])
        
        # Positioning
        score1Text.x = (SCREEN_WIDTH / 2) - (score1Text.content_width / 2)
        score2Text.x = (SCREEN_WIDTH / 2) - (score2Text.content_width / 2)
        gameModeText.x = (SCREEN_WIDTH / 2) - (gameModeText.content_width / 2)

        textTitle.x = (SCREEN_WIDTH / 2) - (textTitle.content_width / 2)
        textTitle.y = (SCREEN_HEIGHT / 2)
        
        # Draw all the items
        textTitle.draw()
        score1Text.draw()
        score2Text.draw()
        gameModeText.draw()
    
    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button to quit the application
        """
        arcade.exit()


class MainMenu(arcade.View):
    """ Class that manages the 'menu' view """
    #arcade.set_background_color(BACKGROUND_COLOR)

    def __init__(self):
        super().__init__()

        # Camera for which the GUI will be drawn onto
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
        # Position the rounds
        self.managerRounds = arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-50,
                align_x=-10,
                child=self.v_box_rounds_text)

        # Button for 3 rounds
        self.button_round_3 = arcade.gui.UIFlatButton(
            text="3", width=100, style = buttonStyle
        )

        # Button for 5 rounds
        self.button_round_5 = arcade.gui.UIFlatButton(
            text="5", width=100, style = buttonStyle
        )

        # Button for 10 rounds
        self.button_round_10 = arcade.gui.UIFlatButton(
            text="10", width=100, style = buttonStyle
        )

        ### Choose Difficulty - Easy / Difficult
        self.button_easy = arcade.gui.UIFlatButton(
            text="easy", width=200, style = buttonStyle
        )

        self.button_difficult = arcade.gui.UIFlatButton(
            text="difficult", width=200, style = buttonStyle
        )

        # VBOX Intial  -  Add the mode widgets
        self.v_box.add(self.button_1v1)
        self.v_box.add(self.button_vComputer)


        # Add a hook to run when we click on the button.
        # There must be a more succinct way to do this, however, this is a new library for me :(
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
    
    """There must be a more efficient way to do this
    Each function acts a hook for the callback method and updates the game state based upon the function title.
    Ie. round3 -> gameState.round = 3 
    
    """
    def round3(self, event): 
        # Set 3 Rounds
        gameState.numberOfRounds = 3
        self.chooseDifficulty()
    def round5(self, event): 
        # Set 5 Rounds
        gameState.numberOfRounds = 5
        self.chooseDifficulty()
    def round10(self, event): 
        # Set 10 rounds
        gameState.numberOfRounds = 10
        self.chooseDifficulty()
    
    def choseEasy(self, event):
        # Set easy mode
        gameState.difficulty = "easy"
        self.manager.disable()
        self.goToGame()
    
    def choseDifficult(self, event):
        # Set difficult mode
        gameState.difficulty = "difficult"
        self.manager.disable()
        self.goToGame()
    
    def chooseDifficulty(self):
        # If the mode is against the computer then choose the difficult, if it is 1V1 then difficulty is obselete.
        if gameState.mode =="vComputer":
            self.v_box.clear()
            self.manager.remove(self.managerRounds)
            self.v_box.add(self.button_easy)
            self.v_box.add(self.button_difficult)
        else: 
            self.manager.disable()
            self.goToGame()
    
    def chooseRounds(self):
        # Manager to display the number of rounds buttons: 3 / 5 / 10
        self.v_box.clear()
        self.v_box.vertical = False
        # self.v_box.add(self.ui_text_label)
        self.manager.add(self.managerRounds)
        self.v_box.add(self.button_round_3)
        self.v_box.add(self.button_round_5)
        self.v_box.add(self.button_round_10)
    
    def button_1v1_clicked(self, event):
        # Mode 1V1
        gameState.mode = "1v1"
        self.chooseRounds()
    
    def button_vComputer_clicked(self, event):
        # Mode: against CPU
        gameState.mode = "vComputer"
        self.chooseRounds()
    
    def goToGame(self):
        # Goes to the game view once the menu has finished, print for debug
        print(f"""
        Mode: {gameState.mode}
        Number of rounds: {gameState.numberOfRounds}
        Difficulty: {gameState.difficulty}
        """)
        game_view = GameView()
        self.window.show_view(game_view)

    def setup(self):
        # Change BG colour
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

        # Clear the screen, select the camera surface to draw onto, draw the scene
        self.clear()
        self.gui_camera.use()
        self.manager.draw()
        
        # TITLE: Tic Tac Toe
        textTitle = arcade.Text(theme[THEME]["GUI_TITLE"],
            140,
            SCREEN_HEIGHT - 80,
            theme[THEME]["TITLE_COLOUR"],
            theme[THEME]["GUI_TITLE_FONT_SIZE"],
            font_name = theme[THEME]["GUI_TITLE_FONT"])
        
        # Positioning
        textTitle.x = (SCREEN_WIDTH / 2) - (textTitle.content_width / 2)
        textTitle.y = (SCREEN_HEIGHT / 2)
        textTitle.draw()
                    
# Insantiate the game state class to be shared amongst the classes
gameState = GameState()
gameState.setup()

def main():
    """ Main function """
    # Show the main menu when the game is first started
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    title_view = MainMenu()
    window.show_view(title_view)

    # Run the game
    arcade.run()


if __name__ == "__main__": # If ran from this file itself and not imported - good practice
    main()