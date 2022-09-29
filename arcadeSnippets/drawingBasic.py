import arcade

arcade.open_window(600, 600, "Drawing", True)

arcade.set_background_color(arcade.color.BLUE) # arcade.csscolor.NAME, ((189, 55, 180))

# Get ready to draw
arcade.start_render()

# (The drawing code will go here.)
# LEFT, RIGHT, TOP, BOTTOM
# L < R, T > B
arcade.draw_lrtb_rectangle_filled(60, 70, 599, 50, arcade.csscolor.GREEN)

arcade.draw_text("Woahh text",
                 150, 230,
                 arcade.color.WHITE, 24)

# Finish drawing
arcade.finish_render()

arcade.run()