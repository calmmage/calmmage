import collections


class Labyrinth:
    def __init__(self, rows, cols):
        if rows <= 0 or cols <= 0:
            raise ValueError("Rows and columns must be positive.")
        self.rows = rows
        self.cols = cols

        # Initialize walls:
        # h_walls[r][c] is the wall between (r-1,c) and (r,c)
        # (i.e., the wall above cell (r,c) if r > 0, or below cell (r-1,c))
        # Dimensions: (rows+1) x cols
        self.h_walls = [[False for _ in range(cols)] for _ in range(rows + 1)]

        # v_walls[r][c] is the wall between (r,c-1) and (r,c)
        # (i.e., the wall to the left of cell (r,c) if c > 0, or right of cell (r,c-1))
        # Dimensions: rows x (cols+1)
        self.v_walls = [[False for _ in range(cols + 1)] for _ in range(rows)]

        # Set boundary walls
        for c in range(cols):
            self.h_walls[0][c] = True  # Top boundary
            self.h_walls[rows][c] = True  # Bottom boundary
        for r in range(rows):
            self.v_walls[r][0] = True  # Left boundary
            self.v_walls[r][cols] = True  # Right boundary

    def is_valid_cell(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def toggle_wall(self, r, c, direction):
        """
        Toggles a wall adjacent to cell (r, c).
        'N', 'S', 'E', 'W' specify which wall of cell (r,c) to toggle.
        Example: Toggling 'N' wall of (r,c) is h_walls[r][c].
                 Toggling 'S' wall of (r,c) is h_walls[r+1][c].
                 Toggling 'W' wall of (r,c) is v_walls[r][c].
                 Toggling 'E' wall of (r,c) is v_walls[r][c+1].
        """
        if not self.is_valid_cell(r, c):
            print(f"Error: Cell ({r},{c}) is out of bounds.")
            return False

        direction = direction.upper()
        toggled = False
        if direction == "N":
            if r > 0:  # Can't toggle boundary wall above row 0 from cell 0,0
                self.h_walls[r][c] = not self.h_walls[r][c]
                toggled = True
            else:
                print("Error: Cannot toggle top boundary wall.")
        elif direction == "S":
            if r < self.rows - 1:  # Can't toggle boundary wall below last row
                self.h_walls[r + 1][c] = not self.h_walls[r + 1][c]
                toggled = True
            else:
                print("Error: Cannot toggle bottom boundary wall.")
        elif direction == "W":
            if c > 0:  # Can't toggle boundary wall left of col 0
                self.v_walls[r][c] = not self.v_walls[r][c]
                toggled = True
            else:
                print("Error: Cannot toggle left boundary wall.")
        elif direction == "E":
            if c < self.cols - 1:  # Can't toggle boundary wall right of last col
                self.v_walls[r][c + 1] = not self.v_walls[r][c + 1]
                toggled = True
            else:
                print("Error: Cannot toggle right boundary wall.")
        else:
            print(f"Error: Invalid direction '{direction}'. Use N, S, E, W.")
            return False

        if toggled:
            # print(f"Wall {direction} of cell ({r},{c}) toggled.")
            return True
        return False

    def get_reachable_neighbors(self, r, c):
        neighbors = []
        # Check North
        if r > 0 and not self.h_walls[r][c]:
            neighbors.append((r - 1, c))
        # Check South
        if r < self.rows - 1 and not self.h_walls[r + 1][c]:
            neighbors.append((r + 1, c))
        # Check West
        if c > 0 and not self.v_walls[r][c]:
            neighbors.append((r, c - 1))
        # Check East
        if c < self.cols - 1 and not self.v_walls[r][c + 1]:
            neighbors.append((r, c + 1))
        return neighbors

    def calculate_score(self, start_r, start_c):
        if not self.is_valid_cell(start_r, start_c):
            print(f"Error: Start cell ({start_r},{start_c}) is out of bounds.")
            return 0, set()

        q = collections.deque([(start_r, start_c)])
        visited = {(start_r, start_c)}
        score = 0

        while q:
            r, c = q.popleft()
            score += 1
            # print(f"Visited ({r},{c})") # For debugging

            for nr, nc in self.get_reachable_neighbors(r, c):
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    q.append((nr, nc))

        return score, visited

    def display(self, visited_cells=None):
        if visited_cells is None:
            visited_cells = set()

        for r in range(self.rows):
            # Print horizontal walls for this row (walls above cells in row r)
            line1 = ""
            for c in range(self.cols):
                line1 += "+"
                line1 += "---" if self.h_walls[r][c] else "   "
            line1 += "+"
            print(line1)

            # Print vertical walls and cell contents for this row
            line2 = ""
            for c in range(self.cols):
                line2 += "|" if self.v_walls[r][c] else " "
                cell_char = "*" if (r, c) in visited_cells else " "
                # You could put cell numbers here, or other markers
                line2 += f" {cell_char} "
            line2 += (
                "|" if self.v_walls[r][self.cols] else " "
            )  # Rightmost wall for the row
            print(line2)

        # Print bottom boundary horizontal walls (walls below cells in row rows-1)
        line_bottom = ""
        for c in range(self.cols):
            line_bottom += "+"
            line_bottom += "---" if self.h_walls[self.rows][c] else "   "
        line_bottom += "+"
        print(line_bottom)
        print("-" * (self.cols * 4 + 1))  # Separator


def game_loop():
    while True:
        try:
            rows = int(input("Enter number of rows for the labyrinth (e.g., 5): "))
            cols = int(input("Enter number of columns for the labyrinth (e.g., 5): "))
            if rows > 0 and cols > 0:
                break
            print("Rows and columns must be positive integers.")
        except ValueError:
            print("Invalid input. Please enter numbers.")

    labyrinth = Labyrinth(rows, cols)
    last_path = None

    while True:
        print("\nLabyrinth:")
        labyrinth.display(last_path)
        last_path = None  # Clear path after displaying

        print("\nOptions:")
        print("  W R C DIR - Toggle Wall (e.g., W 1 1 S)")
        print("              (R=row, C=col, DIR=N,S,E,W for wall of cell R,C)")
        print("  S R C     - Score from Start (e.g., S 0 0)")
        print("  Q         - Quit")

        action = input("> ").strip().upper().split()

        if not action:
            continue

        cmd = action[0]

        if cmd == "W":
            if len(action) == 4:
                try:
                    r, c = int(action[1]), int(action[2])
                    direction = action[3]
                    if not labyrinth.is_valid_cell(r, c):
                        print(
                            f"Cell ({r},{c}) is outside the grid (0-{rows-1}, 0-{cols-1})."
                        )
                    elif direction not in ["N", "S", "E", "W"]:
                        print("Invalid direction. Use N, S, E, or W.")
                    else:
                        labyrinth.toggle_wall(r, c, direction)
                except ValueError:
                    print("Invalid row/column number for wall toggle.")
            else:
                print("Usage: W <row> <col> <direction (N/S/E/W)>")

        elif cmd == "S":
            if len(action) == 3:
                try:
                    start_r, start_c = int(action[1]), int(action[2])
                    if not labyrinth.is_valid_cell(start_r, start_c):
                        print(
                            f"Start cell ({start_r},{start_c}) is outside the grid (0-{rows-1}, 0-{cols-1})."
                        )
                    else:
                        score, visited_path = labyrinth.calculate_score(
                            start_r, start_c
                        )
                        print(f"\n--- Score from ({start_r},{start_c}): {score} ---")
                        last_path = visited_path  # Store path for next display
                except ValueError:
                    print("Invalid row/column number for scoring.")
            else:
                print("Usage: S <start_row> <start_col>")

        elif cmd == "Q":
            print("Thanks for playing!")
            break
        else:
            print("Unknown command.")


if __name__ == "__main__":
    game_loop()
