from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QMouseEvent
from PyQt6.QtCore import Qt, QPointF
import math

class HexGridWidget(QWidget):
    def __init__(self, radius=5):
        super().__init__()
        self.radius = radius
        self.hex_size = 30
        self.board_cells = set()
        self.current_shape = set()
        self.shapes = []
        self.mode = "board"  # or "shape"
        self.saved_board = set()
        self.board_confirmed = False

        self.setMinimumSize(600, 600)

    def axial_to_pixel(self, q, r):
        x = self.hex_size * (3/2 * q)
        y = self.hex_size * (math.sqrt(3) * (r + q / 2))
        return QPointF(x + self.width()/2, y + self.height()/2)

    def pixel_to_axial(self, x, y):
        x -= self.width()/2
        y -= self.height()/2
        q = (2/3 * x) / self.hex_size
        r = (-1/3 * x + math.sqrt(3)/3 * y) / self.hex_size
        return self.hex_round(q, r)

    def hex_round(self, q, r):
        x = q
        z = r
        y = -x - z
        rx = round(x)
        ry = round(y)
        rz = round(z)

        x_diff = abs(rx - x)
        y_diff = abs(ry - y)
        z_diff = abs(rz - z)

        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry - rz
        elif y_diff > z_diff:
            ry = -rx - rz
        else:
            rz = -rx - ry

        return int(rx), int(rz)

    def paintEvent(self, event):
        painter = QPainter(self)
        for q in range(-self.radius, self.radius+1):
            for r in range(-self.radius, self.radius+1):
                if -q - r >= -self.radius and -q - r <= self.radius:
                    self.draw_hex(painter, q, r)

    def draw_hex(self, painter, q, r):
        center = self.axial_to_pixel(q, r)
        corners = [self.hex_corner(center, i) for i in range(6)]

        # Default color
        color = QColor(255, 255, 255)

        # Highest priority: solution overrides all
        for (cell, sol_color) in getattr(self, 'solution_cells', []):
            if (q, r) == cell:
                color = sol_color
                break
        else:
            # Next: shape drawing takes priority
            if (q, r) in self.current_shape:
                color = QColor(180, 230, 255)
            # Then: board display
            elif getattr(self, 'board_confirmed', False) and (q, r) in getattr(self, 'saved_board', set()):
                color = QColor(220, 220, 220)
            elif not getattr(self, 'board_confirmed', False) and (q, r) in self.board_cells:
                color = QColor(200, 200, 200)

        painter.setBrush(color)
        painter.setPen(QPen(Qt.GlobalColor.black))
        painter.drawPolygon(*corners)

    def hex_corner(self, center, i):
        angle_deg = 60 * i
        angle_rad = math.radians(angle_deg)
        return QPointF(
            center.x() + self.hex_size * math.cos(angle_rad),
            center.y() + self.hex_size * math.sin(angle_rad)
        )

    def mousePressEvent(self, event: QMouseEvent):
        x = event.position().x()
        y = event.position().y()
        q, r = self.pixel_to_axial(x, y)

        if self.mode == "board":
            if getattr(self, "board_confirmed", False):
                return  # ignore clicks on board if confirmed
            if (q, r) in self.board_cells:
                self.board_cells.remove((q, r))
            else:
                self.board_cells.add((q, r))
        elif self.mode == "shape":
            if (q, r) in self.current_shape:
                self.current_shape.remove((q, r))
            else:
                self.current_shape.add((q, r))
        self.update()

    def get_board_and_shapes(self):
        shapes = [list(shape) for shape in self.shapes]
        if self.current_shape:
            shapes.append(list(self.current_shape))
        return set(self.saved_board), shapes

    def show_solution(self, solution):
        self.solution_cells = []
        colors = [QColor.fromHsv(i * 40 % 360, 255, 220) for i in range(len(solution))]

        for i, (shape, anchor) in enumerate(solution):
            aq, ar = anchor
            color = colors[i]
            for dq, dr in shape:
                cell = (aq + dq, ar + dr)
                self.solution_cells.append((cell, color))

        self.update()

    def switch_mode(self):
        if self.mode == "board":
            self.mode = "shape"
        elif self.current_shape:
            self.shapes.append(list(self.current_shape))
            self.current_shape.clear()
        self.update()

    def reset_shapes(self):
        self.shapes.clear()
        self.current_shape.clear()
        self.solution_cells = []
        self.update()

    def reset_all(self):
        self.board_cells.clear()
        self.saved_board.clear()
        self.board_confirmed = False
        self.shapes.clear()
        self.current_shape.clear()
        self.solution_cells = []
        self.mode = "board"
        self.update()
