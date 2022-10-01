_list = [
    [6, 7, 8],
    [3, 7, 1,],
    [0, 7, 2],
]

# print(_list[1][0])

def _listing(_list):
    for i in _list:
        vals, currColumn = [], _list.index(i)
        for j in range(0,len(i)):
            curr = _list[j][_list.index(i)]
            print(curr)
            vals.append(curr)
        if all(x==vals[0] for x in vals) and vals[0] != None: 
            print(f"Column {currColumn} has 3 in a row")
        vals.clear()

'''
# Switch to GUI camera before drawing GUI items
        # 1. Score / Menu / Timer etc...
        self.gui_camera.use()

        """
        ADD GUI CODE HERE
        """

        arcade.draw_rectangle_filled(
            center_x = self.scene[LAYER_NAME_GRID].center[0], 
            center_y = self.scene[LAYER_NAME_GRID].center[1], 
            width = ROW_COUNT*(WIDTH+1.5*MARGIN), 
            height= COLUMN_COUNT*(HEIGHT+1.5*MARGIN), 
            color = (182, 213, 227)
        )

        arcade.draw_text(GUI_TITLE,
                         140,
                         SCREEN_HEIGHT - 80,
                         DARK_BLUE,
                         GUI_TITLE_FONT_SIZE,
                         font_name=GUI_TITLE_FONT)
        
        arcade.draw_text(f"Player: {gameState.turn + 1}",
                         300,
                         70,
                         MEDIUM_BLUE,
                         GUI_SUBTITLE_FONT_SIZE,
                         font_name=GUI_TITLE_FONT)
        
        arcade.draw_text(f"Round {gameState.round}",
                         320,
                         30,
                         MEDIUM_BLUE,
                         GUI_SUBTITLE_FONT_SIZE,
                         font_name=GUI_TITLE_FONT)
        
        '''
