import arcade

# DIFFERENT THEMES TO BE USED WITH THE GAME THAT CAN BE CHANGED FOR ACCESSIBILTY:
# Best theme (imoh) is blues
theme={
    "original": {
        "BG": (142, 202, 230), # LIGHT BLUE
        "FRAME_COLOUR" : (182, 213, 227), # LIGHTER BLUE
        "STARTING_CELL_COLOUR" :  (33, 158, 188), # MEDIUM BLUE
        "P1_COLOUR" : arcade.color.BLUE,
        "P2_COLOUR" : arcade.color.RED,
        "TITLE_COLOUR" : (2, 48, 71), # DARK BLUE
        "SUBTITLE_COLOUR" : (33, 158, 188), # MEDIUM BLUE,
        "WINNING_COLOUR" : (0, 255, 0), # GREEN
        "GUI_TITLE" : "Tic-Tac-Toe",
        "GUI_TITLE_FONT_SIZE" : 50,
        "GUI_TITLE_FONT" : "Kenney Blocks",
        "GUI_SUBTITLE_FONT" : "Kenney Blocks",
        "GUI_SUBTITLE_FONT_SIZE" : 25,
    },

    "blues": { # https://coolors.co/palette/e0fbfc-c2dfe3-9db4c0-5c6b73-253237
        "BG": arcade.color_from_hex_string("e0fbfc"), 
        "FRAME_COLOUR" : arcade.color_from_hex_string("c2dfe3"), 
        "STARTING_CELL_COLOUR" :  arcade.color_from_hex_string("9db4c0"), 
        "P1_COLOUR" : arcade.color_from_hex_string("98c1d9"),
        "P2_COLOUR" : arcade.color_from_hex_string("5c6b73"),
        "TITLE_COLOUR" : arcade.color_from_hex_string("253237"), 
        "SUBTITLE_COLOUR" : arcade.color_from_hex_string("5c6b73"), 
        "WINNING_COLOUR" : arcade.color_from_hex_string("ee6c4d"), 
        "GUI_TITLE" : "Tic-Tac-Toe",
        "GUI_TITLE_FONT_SIZE" : 50,
        "GUI_TITLE_FONT" : "Kenney Blocks",
        "GUI_SUBTITLE_FONT" : "Kenney Mini Square",
        "GUI_SUBTITLE_FONT_SIZE" : 25,
    },

    "darkOrange": { # https://coolors.co/palette/fffcf2-ccc5b9-403d39-252422-eb5e28
        "BG": arcade.color_from_hex_string("252422"), 
        "FRAME_COLOUR" : arcade.color_from_hex_string("403D39"), 
        "STARTING_CELL_COLOUR" :  arcade.color_from_hex_string("e9ecef"), 
        "P1_COLOUR" : arcade.color_from_hex_string("847577"),
        "P2_COLOUR" : arcade.color_from_hex_string("CCC5B9"),
        "TITLE_COLOUR" : arcade.color_from_hex_string("FFFCF2"), 
        "SUBTITLE_COLOUR" : arcade.color_from_hex_string("f8f9fa"), 
        "WINNING_COLOUR" : arcade.color_from_hex_string("EB5E28"), 
        "GUI_TITLE" : "Tic-Tac-Toe",
        "GUI_TITLE_FONT_SIZE" : 50,
        "GUI_TITLE_FONT" : "Kenney Blocks",
        "GUI_SUBTITLE_FONT" : "Kenney Blocks",
        "GUI_SUBTITLE_FONT_SIZE" : 25,
    },
}

# Bunch of constants to be passed into the main program

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Aiyush Gupta - Tic Tac Toe"
GUI_TITLE = "Tic-Tac-Toe"
GUI_TITLE_FONT_SIZE = 50
GUI_TITLE_FONT = "Kenney Blocks"
GUI_SUBTITLE_FONT_SIZE = 25

# Player Grid 3X3 with spacing between the cells
ROW_COUNT = 3
COLUMN_COUNT = 3
MARGIN = 10
WIDTH = 100
HEIGHT = 100
LAYER_NAME_GRID = "Grid"

# COLOUR PALLETE -  https://coolors.co/palette/8ecae6-219ebc-023047-ffb703-fb8500

THEME = "blues"

BACKGROUND_COLOR = theme[THEME]["BG"]
FRAME_COLOR = theme[THEME]["FRAME_COLOUR"]
STARTING_CELL_COLOUR = theme[THEME]["STARTING_CELL_COLOUR"]
P1_COLOUR = theme[THEME]["P1_COLOUR"]
P2_COLOUR = theme[THEME]["P2_COLOUR"]
TITLE_COLOUR = theme[THEME]["TITLE_COLOUR"]
SUBTITLE_COLOUR = theme[THEME]["SUBTITLE_COLOUR"]
WINNING_COLOUR = theme[THEME]["WINNING_COLOUR"]