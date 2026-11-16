import tkinter as tk
from enum import Enum

MIN_SIZE = 3
MAX_SIZE = 10
WIN_COLOR = "#2e9e5b"
MIN_ROUNDS = 3
MAX_ROUNDS = 15

root = tk.Tk()
root.title("Tic Tac Toe")
root.minsize(320, 320)


class Player(Enum):
    PLAYER_X = "X"
    PLAYER_Y = "O"


PLAYER_X: Player = Player.PLAYER_X
PLAYER_Y: Player = Player.PLAYER_Y

positions: dict[tuple, tk.StringVar] = {}
grid_buttons: list[tk.Button] = []
current_turn = PLAYER_X
grid_size = 0
game_over = False
total_rounds = 0
current_round = 1
scores = {PLAYER_X: 0, PLAYER_Y: 0}


# ---------------------------------------------------------------- game logic


def evaluate_game(
    player: Player, last_move: tuple
) -> tuple[str | None, list[tuple[int, int]]]:
    """Return (result, winning_cells) after `player` moved.

    result is "win", "draw" or None (game continues).
    """
    row, column = last_move
    n = grid_size
    mark = player.value

    def owned(r: int, c: int) -> bool:
        return positions[(r, c)].get() == mark

    # Only lines passing through the last move can have been completed by it.
    lines = [
        [(row, c) for c in range(n)],
        [(r, column) for r in range(n)],
    ]
    if row == column:
        lines.append([(i, i) for i in range(n)])
    if row + column == n - 1:
        lines.append([(i, n - 1 - i) for i in range(n)])

    for line in lines:
        if all(owned(r, c) for r, c in line):
            return "win", line

    if all(var.get() != "" for var in positions.values()):
        return "draw", []

    return None, []


def show_popup(message: str, button_text: str, action):
    popup = tk.Toplevel(root)
    popup.title("Tic Tac Toe")
    popup.transient(root)
    popup.resizable(False, False)

    tk.Label(popup, text=message, font=("TkDefaultFont", 16, "bold")).pack(
        padx=40, pady=(25, 15)
    )

    def proceed():
        popup.destroy()
        action()

    tk.Button(popup, text=button_text, width=12, command=proceed).pack(pady=(0, 25))

    popup.protocol("WM_DELETE_WINDOW", proceed)
    # Dock the popup at the bottom of the window so the board stays visible.
    popup.update_idletasks()
    x = root.winfo_rootx() + (root.winfo_width() - popup.winfo_width()) // 2
    y = root.winfo_rooty() + root.winfo_height() - popup.winfo_height() - 10
    popup.geometry(f"+{x}+{y}")
    popup.grab_set()


def update_status():
    turn_label.config(
        text=(
            f"Round {current_round}/{total_rounds}   "
            f"X: {scores[PLAYER_X]}  O: {scores[PLAYER_Y]}   "
            f"Turn: {current_turn.value}"
        )
    )


def finish_round(winner: Player | None):
    global current_round
    if winner is not None:
        scores[winner] += 1

    if current_round < total_rounds:
        message = (
            f"{winner.value} won round {current_round}!"
            if winner
            else f"Round {current_round} is a draw!"
        )
        current_round += 1
        show_popup(message, "Next round", start_round)
        return

    x, o = scores[PLAYER_X], scores[PLAYER_Y]
    if x > o:
        message = f"X wins the match! ({x}-{o})"
    elif o > x:
        message = f"O wins the match! ({o}-{x})"
    else:
        message = f"The match is a draw! ({x}-{o})"
    show_popup(message, "Rematch", lambda: start_game(grid_size, total_rounds))


def play(row: int, column: int):
    global current_turn, game_over
    if game_over or positions[(row, column)].get() != "":
        return

    positions[(row, column)].set(current_turn.value)

    result, winning_cells = evaluate_game(current_turn, (row, column))
    if result == "win":
        game_over = True
        for r, c in winning_cells:
            grid_buttons[r * grid_size + c].config(
                bg=WIN_COLOR, activebackground=WIN_COLOR, fg="white"
            )
        winner = current_turn
        root.after(700, lambda: finish_round(winner))
        return
    if result == "draw":
        game_over = True
        root.after(700, lambda: finish_round(None))
        return

    current_turn = PLAYER_Y if current_turn is PLAYER_X else PLAYER_X
    update_status()


# ------------------------------------------------------------------- screens

menu_frame = tk.Frame(root)
pvc_frame = tk.Frame(root)
game_frame = tk.Frame(root)


def show(frame: tk.Frame):
    for f in (menu_frame, pvc_frame, game_frame):
        f.pack_forget()
    frame.pack(expand=True, padx=20, pady=20)


def start_game(size: int, rounds: int):
    global grid_size, total_rounds, current_round

    grid_size = size
    total_rounds = rounds
    current_round = 1
    scores[PLAYER_X] = 0
    scores[PLAYER_Y] = 0
    start_round()
    show(game_frame)


def start_round():
    global current_turn, game_over
    size = grid_size

    for widget in grid_buttons:
        widget.destroy()
    grid_buttons.clear()
    positions.clear()

    current_turn = PLAYER_X
    game_over = False
    update_status()

    for row in range(size):
        for col in range(size):
            positions[(row, col)] = tk.StringVar(value="")
            button = tk.Button(
                board_frame,
                textvariable=positions[(row, col)],
                width=6,
                height=3,
                font=("TkDefaultFont", 14, "bold"),
                command=lambda r=row, c=col: play(r, c),
            )
            button.grid(row=row, column=col)
            grid_buttons.append(button)


# Menu screen
tk.Label(menu_frame, text="Tic Tac Toe", font=("TkDefaultFont", 22, "bold")).pack(
    pady=(0, 20)
)

mode_var = tk.StringVar(value="")
tk.Label(menu_frame, text="Game mode").pack(anchor="w")
tk.Radiobutton(
    menu_frame, text="PvP (Player vs Player)", variable=mode_var, value="pvp"
).pack(anchor="w")
tk.Radiobutton(
    menu_frame, text="PvC (Player vs Computer)", variable=mode_var, value="pvc"
).pack(anchor="w")

size_var = tk.StringVar(value="")
tk.Label(menu_frame, text=f"Board size ({MIN_SIZE}-{MAX_SIZE})").pack(
    anchor="w", pady=(15, 0)
)
tk.Spinbox(
    menu_frame, from_=MIN_SIZE, to=MAX_SIZE, textvariable=size_var, width=6
).pack(anchor="w")

rounds_var = tk.StringVar(value="")
tk.Label(menu_frame, text=f"Rounds ({MIN_ROUNDS}-{MAX_ROUNDS})").pack(
    anchor="w", pady=(15, 0)
)
tk.Spinbox(
    menu_frame, from_=MIN_ROUNDS, to=MAX_ROUNDS, textvariable=rounds_var, width=6
).pack(anchor="w")

start_button = tk.Button(menu_frame, text="Start", state="disabled")
start_button.pack(pady=20)


def selected_size() -> int | None:
    value = size_var.get().strip()
    if value.isdigit() and MIN_SIZE <= int(value) <= MAX_SIZE:
        return int(value)
    return None


def selected_rounds() -> int | None:
    value = rounds_var.get().strip()
    if value.isdigit() and MIN_ROUNDS <= int(value) <= MAX_ROUNDS:
        return int(value)
    return None


def update_start_state(*_):
    ready = (
        mode_var.get() != ""
        and selected_size() is not None
        and selected_rounds() is not None
    )
    start_button.config(state="normal" if ready else "disabled")


def on_start():
    size = selected_size()
    rounds = selected_rounds()
    if size is None or rounds is None:
        return
    if mode_var.get() == "pvp":
        start_game(size, rounds)
    else:
        show(pvc_frame)


mode_var.trace_add("write", update_start_state)
size_var.trace_add("write", update_start_state)
rounds_var.trace_add("write", update_start_state)
start_button.config(command=on_start)

# PvC "not ready" screen
tk.Label(
    pvc_frame, text="PvC isn't ready yet", font=("TkDefaultFont", 16, "bold")
).pack(pady=(0, 15))
tk.Button(
    pvc_frame,
    text="Play PvP instead",
    command=lambda: (
        mode_var.set("pvp"),
        start_game(selected_size() or MIN_SIZE, selected_rounds() or MIN_ROUNDS),
    ),
).pack()
tk.Button(pvc_frame, text="Back", command=lambda: show(menu_frame)).pack(pady=(8, 0))

# Game screen
turn_label = tk.Label(game_frame, text="", font=("TkDefaultFont", 12))
turn_label.pack(pady=(0, 10))
board_frame = tk.Frame(game_frame)
board_frame.pack()
tk.Button(game_frame, text="Menu", command=lambda: show(menu_frame)).pack(pady=(10, 0))

show(menu_frame)
root.mainloop()
