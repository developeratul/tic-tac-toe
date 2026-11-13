#Testing Grounds

import tkinter as tk

root = tk.Tk()
root.title("The Grid Geometry Manager")
root.minsize(200, 200)

position = { "player_x" : [], "player_y" : [] 
            }

def get_position_x(event):
    widget = event.widget
    grid_info = widget.grid_info()
    position["player_x"].append((grid_info['row'],grid_info['column']))
    print(position)

def get_position_y(event):
    widget = event.widget
    grid_info = widget.grid_info()
    position["player_y"].append((grid_info['row'],grid_info['column']))
    print(position)

def build_grid():
    value = int(entry.get())

    for row in range(value):
        for col in range(value):

            button = tk.Button(
                root,
                text=f"Cell ({row + 1}, {col + 1})",
                width=10,
                height=5,
            )
            button.grid(row=row + 1, column=col + 1)
            button.bind('<Button-1>',get_position_x)
            button.bind('<Button-3>',get_position_y)

label = tk.Label(root, text="Enter the number of grids: ")
label.grid(row=0, column=0)

entry = tk.Entry(root)
entry.grid(row=1, column=0)

button = tk.Button(root, text="Build the Grid", command=build_grid)
button.grid(row=2, column=0)


root.mainloop()