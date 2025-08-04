# app.py
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QListWidget, QListWidgetItem, QLabel
from hex_grid_widget import HexGridWidget
from solver import solve_shapes

class HexSolverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hex Puzzle Solver")
        layout = QVBoxLayout()

        self.hex_widget = HexGridWidget()
        layout.addWidget(self.hex_widget)

        self.shape_list = QListWidget()
        layout.addWidget(self.shape_list)

        self.board_button = QPushButton("Confirm Board")
        self.board_button.clicked.connect(self.confirm_board)
        layout.addWidget(self.board_button)

        self.mode_button = QPushButton("Next Shape")
        self.mode_button.clicked.connect(self.next_shape)
        layout.addWidget(self.mode_button)

        self.solve_button = QPushButton("Solve")
        self.solve_button.clicked.connect(self.solve_puzzle)
        layout.addWidget(self.solve_button)

        self.reset_shapes_button = QPushButton("Reset Shapes Only")
        self.reset_shapes_button.clicked.connect(self.reset_shapes_only)
        layout.addWidget(self.reset_shapes_button)

        self.reset_button = QPushButton("Reset Board & Shapes")
        self.reset_button.clicked.connect(self.reset_all)
        layout.addWidget(self.reset_button)

        self.log_label = QLabel("")
        layout.addWidget(self.log_label)

        self.setLayout(layout)

    def confirm_board(self):
        self.hex_widget.saved_board = set(self.hex_widget.board_cells)
        self.hex_widget.board_confirmed = True
        self.board_button.setEnabled(False)  # Disable the button
        self.hex_widget.mode = "shape"       # Switch to shape mode
        print(f"Board confirmed with {len(self.hex_widget.saved_board)} cells.")
        self.log(f"Board confirmed with {len(self.hex_widget.saved_board)} cells.")
        self.hex_widget.update()

    def next_shape(self):
        # Save current shape from hex widget
        if self.hex_widget.current_shape:
            self.hex_widget.shapes.append(list(self.hex_widget.current_shape))
            self.hex_widget.current_shape.clear()
            self.hex_widget.update()
            self.update_shape_list()
        self.hex_widget.switch_mode()

    def update_shape_list(self):
        self.shape_list.clear()
        for i, shape in enumerate(self.hex_widget.shapes, 1):
            self.shape_list.addItem(f"Shape {i}: {len(shape)} hexes")

    def solve_puzzle(self):
        board, shapes = self.hex_widget.get_board_and_shapes()

        board_cells_count = len(board)
        shapes_cells_count = sum(len(shape) for shape in shapes)

        if shapes_cells_count > board_cells_count:
            print(f"Unsolvable: Shapes cover {shapes_cells_count} cells but board only has {board_cells_count} cells.")
            self.log(f"Unsolvable: Shapes cover {shapes_cells_count} cells but board only has {board_cells_count} cells.")
            return

        solution = solve_shapes(board, shapes)
        if solution:
            self.hex_widget.show_solution(solution)
            self.log("Solution found and displayed.")
        else:
            print("No solution found.")
            self.log("No solution found.")

    def reset_shapes_only(self):
        self.hex_widget.reset_shapes()
        self.shape_list.clear()
        self.log("Shapes reset. Board remains unchanged.")

    def reset_all(self):
        self.hex_widget.reset_all()
        self.shape_list.clear()
        self.board_button.setEnabled(True) 
        self.log("Board and shapes reset.")

    def log(self, text):
        self.log_label.setText(text)

if __name__ == "__main__":
    app = QApplication([])
    window = HexSolverApp()
    window.show()
    app.exec()
