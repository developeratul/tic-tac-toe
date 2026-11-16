import tkinter as tk

root = tk.Tk()
root.title("The Grid Geometry Manager")
root.minsize(200, 200)

PLAYER_X = "X"
PLAYER_Y = "O"

positions: dict[tuple, tk.StringVar] = {}
current_turn = PLAYER_X


def evaluate_game() -> None:
    return


def register_position_x(row: int, column: int):
    positions[(row, column)].set("X")


def register_position_y(row: int, column: int):
    positions[(row, column)].set("O")


def register_position(event: tk.Event[tk.Button]):
    widget = event.widget
    grid_info = widget.grid_info()
    row = grid_info["row"] - 1
    column = grid_info["column"] - 1

    existing_registration_holder = positions[row, column].get()
    already_registered = (
        existing_registration_holder is PLAYER_X
        or existing_registration_holder is PLAYER_Y
    )

    if already_registered:
        return
    else:
        global current_turn
        if current_turn is PLAYER_X:
            register_position_x(row, column)
            current_turn = PLAYER_Y
        else:
            register_position_y(row, column)
            current_turn = PLAYER_X


def register_labels(grid_size: int):
    for row in range(grid_size):
        for column in range(grid_size):
            positions[(row, column)] = tk.StringVar()
            positions[(row, column)].set("")


def build_grid():
    value = int(entry.get())

    register_labels(value)

    for row in range(value):
        for col in range(value):
            button = tk.Button(
                root,
                textvariable=positions[(row, col)],
                width=10,
                height=5,
            )
            button.grid(row=row + 1, column=col + 1)
            button.bind("<Button-1>", register_position)
            button.bind("<Button-3>", register_position)


label = tk.Label(root, text="Enter the number of grids: ")
label.grid(row=0, column=0)

entry = tk.Entry(root)
entry.grid(row=1, column=0)

button = tk.Button(root, text="Build the Grid", command=build_grid)
button.grid(row=2, column=0)


root.mainloop()
