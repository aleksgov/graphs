from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import math
import datetime

class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        self.setStyleSheet("QDialog {background-color: #e8f3fc;}")
        self.setWindowTitle(" ")

        buttonBox.button(QDialogButtonBox.Ok).setText("Принять")
        buttonBox.button(QDialogButtonBox.Cancel).setText("Отмена")
        button_style = (
            "QPushButton { "
            "background-color: #90AFFF; "
            "color: #ffffff; "
            "border-radius: 5px;"
            "font-family: Rubik; "
            "font-size: 11pt; "
            "font-weight: bold;"
            "} " 
            "QPushButton:hover { background-color: #7CA0FF; }"
        )
        buttonBox.setStyleSheet(button_style)
        
        ok_button = buttonBox.button(QDialogButtonBox.Ok)
        ok_button.setCursor(Qt.PointingHandCursor)
        ok_button.setStyleSheet(button_style)
        
        cancel_button = buttonBox.button(QDialogButtonBox.Cancel)
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.setStyleSheet(button_style)
        
        layout = QFormLayout(self)
        label = QLabel("Введите вес:", self)
        label.setStyleSheet("font-family: Rubik; font-size: 11pt; color: #1e3b70;")
        
        self.input = QLineEdit(self)
        self.input.setStyleSheet(
            "border: 4px #90AFFF;"
            "border-radius: 8px;"
            "padding: 2px;"
            "font-family: 'Rubik';"
            "font-size: 11pt;"
            "font-weight: bold;"
            "text-align: center;"
            "background-color: #90AFFF;"
            "color: #ffffff;")

        layout.addRow(label, self.input)

        self.comboBox = QComboBox(self)
        self.comboBox.addItem("Дуга")
        self.comboBox.addItem("Ребро")
        self.comboBox.setStyleSheet("border: 4px #90AFFF;"
            "border-radius: 8px;"
            "padding: 2px; "
            "font-family: 'Rubik';"
            "font-size: 11pt;"
            "font-weight: bold;"
            "text-align: center;"
            "background-color: #90AFFF;"
            "color: #ffffff;")
        layout.addWidget(self.comboBox)
        buttonBox.button(QDialogButtonBox.Ok).setFixedSize(100, 24)
        buttonBox.button(QDialogButtonBox.Cancel).setFixedSize(100, 24)
        buttonBox.move(150, 200)
        layout.addWidget(buttonBox)
        self.comboBox.setCursor(Qt.PointingHandCursor)
        
    def getInputs(self):
        return [self.input.text(), self.comboBox.currentIndex()]


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.vertices = []
        self.edges = []
        self.edge_mode = "edge"
        self.matrix_weight_mode = "no_weight"
        self.parse_matrix_mode = "adj"
        self.add_mode = "edge"
        self.vertex_radius = 18
        self.start_vertex = -1
        self.dragged_vertex_index = -1
        self.cursor_pos = [0, 0]
        self.delete = False
        self.setupUi()
        self.setupButtons()
        self.show()
        self.toggle_add_vertex()

    def setupUi(self):
        self.dialog = InputDialog(self)
        self.setObjectName("MainWindow")
        self.resize(1250, 900)
        self.setWindowTitle("Graph Drawer")
        self.centralwidget = QWidget(self)
        self.setStyleSheet("QMainWindow {background-color: #e8f3fc;}")

        self.DisplayAdjMatrixButton = QPushButton(self.centralwidget, text="Матрица\nсмежности")
        self.DisplayAdjMatrixButton.setGeometry(QRect(160, 810, 180, 64))
        self.set_button_style(self.DisplayAdjMatrixButton, "#90AFFF", "#7CA0FF")
        self.DisplayAdjMatrixButton.setCursor(Qt.PointingHandCursor)

        self.DisplayIncMatrixButton = QPushButton(self.centralwidget, text="Матрица\nинцидентности")
        self.DisplayIncMatrixButton.setGeometry(QRect(400, 810, 180, 64))
        self.set_button_style(self.DisplayIncMatrixButton, "#90AFFF", "#7CA0FF")
        self.DisplayIncMatrixButton.setCursor(Qt.PointingHandCursor)

        self.EdgeModeButton = QPushButton(self.centralwidget, text="Конструктор\nсвязей")
        self.EdgeModeButton.setGeometry(QRect(10, 12, 170, 55))
        self.EdgeModeButton.setCursor(Qt.PointingHandCursor)

        self.VertexModeButton = QPushButton(self.centralwidget, text="Конструктор\nвершин")
        self.VertexModeButton.setGeometry(QRect(207, 12, 170, 55))
        self.VertexModeButton.setCursor(Qt.PointingHandCursor)

        self.DeleteButton = QPushButton(self.centralwidget, text="Удалить\nвершину")
        self.DeleteButton.setGeometry(QRect(403, 12, 170, 55))
        self.DeleteButton.setCursor(Qt.PointingHandCursor)

        self.ClearButton = QPushButton(self.centralwidget, text="Очистить поле")
        self.ClearButton.setGeometry(QRect(600, 12, 170, 55))
        self.set_button_style(self.ClearButton, "#FF7474", "#FF5C5C")
        self.ClearButton.setCursor(Qt.PointingHandCursor)

        self.TextOutput = QTextEdit(self.centralwidget)
        self.TextOutput.setGeometry(QRect(800, 45, 420, 300))
        font = QFont("Rubik", 14)
        self.TextOutput.setFont(font)
        self.TextOutput.setStyleSheet("border: 4px solid #90AFFF; "
                                      "border-radius: 10px; "
                                      "padding: 10px; "
                                      "background-color: #ffffff;")
        self.TextOutput.setWordWrapMode(QTextOption.NoWrap)

        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QRect(800, 450, 420, 220))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnWidth(2, 240)
        table_style = (
            "QTableWidget {"
            "border: 4px solid #90AFFF;"
            "gridline-color: #90AFFF;"
            "border-radius: 10px;"
            "}"
        )
        self.tableWidget.setStyleSheet(table_style)

        self.trash_button = QPushButton(self.centralwidget, text="🗑")
        self.trash_button.setGeometry(QRect(1180, 380, 45, 45))
        button_style = (
            "QPushButton { "
                "border-radius: 10px;"
                "padding: 10px;"
                "font-family: 'Rubik';"
                "font-size: 15pt;"
                "background-color: #ffffff;"
                "} "
            "QPushButton:hover { background-color: #FF7474 }"
        )
        self.trash_button.setStyleSheet(button_style)
        self.trash_button.setCursor(Qt.PointingHandCursor)

        self.InputMatrixSelectorCombo = QComboBox(self.centralwidget)
        self.InputMatrixSelectorCombo.addItems(["   Матрица\n   смежности", "   Матрица\n   инцидентности"])
        self.InputMatrixSelectorCombo.setGeometry(QRect(790, 380, 190, 45))
        self.InputMatrixSelectorCombo.setStyleSheet(
            "border: 4px #90AFFF;"
            "border-radius: 8px;"
            "padding: 2px; font-family: 'Rubik';"
            "font-size: 14pt;"
            "font-weight: bold;"
            "text-align: center;"
            "background-color: #90AFFF;"
            "color: #ffffff;")
        self.InputMatrixSelectorCombo.setCursor(Qt.PointingHandCursor)
        
        self.BuildGraphButton = QPushButton(self.centralwidget, text="Построить граф")
        self.BuildGraphButton.setGeometry(QRect(1000, 380, 165, 45))
        self.BuildGraphButton.setCursor(Qt.PointingHandCursor)
        self.set_button_style(self.BuildGraphButton, "#90AFFF", "#7CA0FF")
        self.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(self)

    def set_button_style(self, button, default_color, pressed_color):
        button_style = f"""
            QPushButton {{
                background-color: {default_color};
                color: #ffffff;
                border-radius: 12px;
                font-family: 'Rubik';
                font-size: 14pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {pressed_color};
            }}
        """
        button.setStyleSheet(button_style)

    def setupButtons(self):
        self.DisplayAdjMatrixButton.clicked.connect(self.display_adjacency_matrix)
        self.DisplayIncMatrixButton.clicked.connect(self.display_incidence_matrix)

        self.EdgeModeButton.clicked.connect(self.toggle_add_edge)
        self.VertexModeButton.clicked.connect(self.toggle_add_vertex)
        self.DeleteButton.clicked.connect(self.toggle_delete_mode)

        self.ClearButton.clicked.connect(self.clear_graph)

        self.InputMatrixSelectorCombo.currentIndexChanged.connect(self.index_changed)
        self.BuildGraphButton.clicked.connect(self.build_graph)
        self.trash_button.clicked.connect(self.trash_matrix)

    def warningPopup(self, title, _text):
        QMessageBox.question(self, title, _text, QMessageBox.Ok, QMessageBox.Ok)

    def trash_matrix(self):
        self.TextOutput.clear()
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        
    def toggle_delete_mode(self):
        self.delete = True
        self.set_button_style(self.DeleteButton, "#FF8383", "#FF5C5C")
        self.set_button_style(self.VertexModeButton, "#90AFFF", "#7CA0FF")
        self.set_button_style(self.EdgeModeButton, "#90AFFF", "#7CA0FF")

    def toggle_add_vertex(self):
        self.delete = False
        self.set_button_style(self.EdgeModeButton, "#90AFFF", "#7CA0FF")
        self.set_button_style(self.DeleteButton, "#90AFFF", "#FF7474")
        self.set_button_style(self.VertexModeButton, "#7DD6DB", "#4BCFD6")
        self.add_mode = "vertex"

    def toggle_add_edge(self):
        self.delete = False
        self.set_button_style(self.VertexModeButton, "#90AFFF", "#7CA0FF")
        self.set_button_style(self.DeleteButton, "#90AFFF", "#FF7474")
        self.set_button_style(self.EdgeModeButton, "#7DD6DB", "#4BCFD6")
        self.add_mode = "edge"

    def mousePressEvent(self, event):
        if (15 + self.vertex_radius < event.x() < 765 - self.vertex_radius and 85 + self.vertex_radius < event.y() < 785 - self.vertex_radius):
            if (self.delete):
                for i, vertex in enumerate(self.vertices):
                    if (abs(vertex[0] - event.x()) < self.vertex_radius and abs(vertex[1] - event.y()) < self.vertex_radius):
                        self.vertices.pop(i)
                        j = 0
                        while j < len(self.edges):
                            if (self.edges[j][0] == i or self.edges[j][1] == i):
                                self.edges.pop(j)
                                continue
                            if (self.edges[j][0] > i):
                                self.edges[j][0] -= 1
                            if (self.edges[j][1] > i):
                                self.edges[j][1] -= 1
                            j += 1
                        break
            elif (self.add_mode == "vertex"):
                i = 0
                while i < len(self.vertices):
                    if (abs(self.vertices[i][0] - event.x()) < self.vertex_radius and abs(self.vertices[i][1] - event.y()) < self.vertex_radius):
                        self.dragged_vertex_index = i
                        break
                    i += 1
                else:
                    # self.DrawVertex(self, event.x(), event.y(), str(len(self.vertices) + 1))
                    self.vertices.append([event.x(), event.y(), 1])
                    self.update()
            elif (self.add_mode == "edge"):
                for i, vertex in enumerate(self.vertices):
                    if (abs(vertex[0] - event.x()) < self.vertex_radius and abs(vertex[1] - event.y()) < self.vertex_radius):
                        self.start_vertex = i

    def mouseMoveEvent(self, event):
        if (15 + self.vertex_radius < event.x() < 765 - self.vertex_radius and 85 + self.vertex_radius < event.y() < 785 - self.vertex_radius):
            if (self.dragged_vertex_index != -1):
                self.vertices[self.dragged_vertex_index][0] = event.x()
                self.vertices[self.dragged_vertex_index][1] = event.y()

            if (self.start_vertex != -1):
                self.cursor_pos = [event.x(), event.y()]

            self.update()
        else:
            self.dragged_vertex_index = -1
            self.start_vertex = -1

    def mouseReleaseEvent(self, event):
        if (self.start_vertex != -1):
            for i, vertex in enumerate(self.vertices):
                if (abs(vertex[0] - event.x()) < self.vertex_radius and abs(vertex[1] - event.y()) < self.vertex_radius):
                    self.end_edge(self.start_vertex, i)

        self.dragged_vertex_index = -1
        self.start_vertex = -1
        self.update()

    def DrawVertices(self):
        for i, vertex in enumerate(self.vertices):
            self.DrawVertex(self, vertex[0], vertex[1], str(i + 1))

    def DrawVertex(self, image, x, y, index):
        painter = QPainter(image)
        pen_and_brush = painter.pen()
        pen_and_brush.setColor(QColor("#81a4ff"))
        pen_and_brush.setWidth(2)
        painter.setPen(pen_and_brush)
        painter.setBrush(QColor("#81a4ff"))
        painter.drawEllipse(QRectF(x - self.vertex_radius, y - self.vertex_radius, self.vertex_radius * 2, self.vertex_radius * 2))
        text_pen = painter.pen()
        text_pen.setColor(QColor(Qt.white))
        painter.setPen(text_pen)
        font = QFont("Rubik", 14)
        painter.setFont(font)
        painter.drawText(QRectF(x - self.vertex_radius, y - self.vertex_radius, self.vertex_radius * 2, self.vertex_radius * 2), Qt.AlignCenter, str(index))

        painter.end()

    def DrawEdges(self):
        for edge in self.edges:
            self.DrawEdge(self, self.vertices[edge[0]][0], self.vertices[edge[0]][1], self.vertices[edge[1]][0], self.vertices[edge[1]][1], edge[2], edge[3])

    def DrawEdge(self, image, x1, y1, x2, y2, weight=-1, type=1):
        painter = QPainter(image)
        pen = QPen(QColor(129, 164, 255), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)

        if (x1 == x2 and y1 == y2):
            painter.drawArc(QRect(x1 - self.vertex_radius * 2, y1 - self.vertex_radius * 2, self.vertex_radius * 2, self.vertex_radius * 2), 0, 270 * 16)

            if weight != -1 and weight != "1":
                brush = painter.brush()
                brush.setColor(QColor(Qt.white))
                brush.setStyle(Qt.SolidPattern)
                painter.setBrush(brush)
                painter.drawRect(x1 - self.vertex_radius * 2 - 10, y1 - self.vertex_radius * 2, 30, 18)

                font = QFont("Rubik", 12)
                painter.setFont(font)
                painter.drawText(QRectF(x1 - self.vertex_radius * 2 - 10, y1 - self.vertex_radius * 2, 30, 18), Qt.AlignCenter, str(weight))
        else:
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

            if (type == 0):
                angle = math.atan2(y2 - y1, x2 - x1)
                x2 = x2 - self.vertex_radius * math.cos(angle)
                y2 = y2 - self.vertex_radius * math.sin(angle)
                arrow_len = 15
                arrow_open_angle = math.pi / 10
                brush = painter.brush()
                brush.setColor(QColor(129,164,255))
                brush.setStyle(Qt.SolidPattern)
                painter.setBrush(brush)
                points = [
                    QPointF(x2, y2),
                    QPointF(x2 - arrow_len * math.cos(angle + arrow_open_angle), y2 - arrow_len * math.sin(angle + arrow_open_angle)),
                    QPointF(x2 - arrow_len * math.cos(angle - arrow_open_angle), y2 - arrow_len * math.sin(angle - arrow_open_angle)),
                ]
                painter.drawConvexPolygon(points)

            if weight != -1 and weight != "1":
                brush = painter.brush()
                brush.setColor(QColor(Qt.white))
                brush.setStyle(Qt.SolidPattern)
                painter.setBrush(brush)
                painter.drawRect(int(x2 - (x2 - x1) / 4 - 15), int(y2 - (y2 - y1) / 4 - 9), 30, 18)
                font = QFont("Rubik", 12)
                painter.setFont(font)
                painter.drawText(QRectF(x2 - (x2 - x1) / 4 - 15, y2 - (y2 - y1) / 4 - 9, 30, 18), Qt.AlignCenter, str(weight))

        painter.end()

    def paintEvent(self, event):
        self.DrawFrame()
        if (self.start_vertex != -1):
            self.DrawEdge(self, self.vertices[self.start_vertex][0], self.vertices[self.start_vertex][1], self.cursor_pos[0], self.cursor_pos[1])
        self.DrawEdges()
        self.DrawVertices()

    def DrawFrame(self):
        painter = QPainter(self)
        pen = QPen(QColor("#a0bbff"), 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(QColor("#ffffff"))
        painter.drawRoundedRect(15, 85, 750, 700, 10, 10)

        painter.end()

    def index_changed(self, s):
        if s == 0:
            self.parse_matrix_mode = "adj"
        if s == 1:
            self.parse_matrix_mode = "inc"

    def build_graph(self):
        if self.parse_matrix_mode == "adj":
            self.parse_adjacency_matrix()
        if self.parse_matrix_mode == "inc":
            self.parse_incidence_matrix()

    def ask_for_weight(self):
        if self.dialog.exec():
            weight, type = self.dialog.getInputs()
            if weight.strip() == "":
                return ["1", type]
            try:
                weight = int(weight)
                return [weight, type]
            except ValueError:
                return [None, -1]
            return [None, -1]

    def end_edge(self, start_vertex, end_vertex):
        weight, type = self.ask_for_weight()
        if weight is not None:
            self.edges.append([start_vertex, end_vertex, weight, type])
        if weight is None and type != -1:
            self.edges.append([start_vertex, end_vertex, weight, type])

    def clear_graph(self):
        self.vertices = []
        self.edges = []
        self.start_vertex = -1
        self.dragged_vertex_index = -1
        self.update()

    def display_adjacency_matrix(self):
        if len(self.vertices) == 0:
            self.TextOutput.setText("Пустой граф")
            return

        adj_matrix = [[0 for i in range(len(self.vertices))] for j in range(len(self.vertices))]
        for edge in self.edges:
            if edge[3] == 1:
                adj_matrix[edge[1]][edge[0]] = edge[2]
            adj_matrix[edge[0]][edge[1]] = edge[2]

        max_width = max(len(str(entry)) for row in adj_matrix for entry in row)
        output_text = ""
        for row in adj_matrix:
            formatted_row = [f"{entry:>{max_width}}  " for entry in row]
            output_text += " ".join(formatted_row) + "\n"
        self.TextOutput.setText(output_text)
        self.tableWidget.clear()
        self.tableWidget.setRowCount(len(adj_matrix))
        self.tableWidget.setColumnCount(len(adj_matrix[0]))
        font = QFont("Rubik\n", 12)

        for i in range(len(adj_matrix)):
            for j in range(len(adj_matrix[i])):
                item = QTableWidgetItem(str(adj_matrix[i][j]))
                item.setFont(font)
                self.tableWidget.setItem(i, j, item)
                
    def display_incidence_matrix(self):
        if len(self.vertices) == 0 or len(self.edges) == 0:
            self.TextOutput.setText("Пустой граф")
            return

        incidence_matrix = [[0 for i in range(len(self.edges))] for j in range(len(self.vertices))]

        for i, edge in enumerate(self.edges):
            if edge[3] == 0:
                incidence_matrix[edge[1]][i] = -int(edge[2]) if isinstance(edge[2], str) else -edge[2]
                incidence_matrix[edge[0]][i] = int(edge[2]) if isinstance(edge[2], str) else edge[2]
            if edge[3] == 1:
                incidence_matrix[edge[1]][i] = int(edge[2]) if isinstance(edge[2], str) else edge[2]
                incidence_matrix[edge[0]][i] = int(edge[2]) if isinstance(edge[2], str) else edge[2]

        max_width = max(len(str(entry)) for row in incidence_matrix for entry in row)
        output_text = ""
        for row in incidence_matrix:
            formatted_row = [f"{entry:>{max_width}}" for entry in row]
            output_text += " ".join(formatted_row) + "\n"
        self.TextOutput.setText(output_text)

    def create_graph(self, vertices_count):
        center_x, center_y = 700 / 2 + 15, 700 / 2 + 15
        radius = center_x / 2
        for i in range(vertices_count):
            self.vertices.append([center_x + radius * math.cos(2 * math.pi / vertices_count * i), center_y + radius * math.sin(2 * math.pi / vertices_count * i), 1])

    def parse_adjacency_matrix(self):
        lines = self.TextOutput.toPlainText().strip().split("\n")

        self.clear_graph()

        if len(lines[0]) == 0:
            self.warningPopup("Ошибка!", "Формат матрицы неверен.")
            return

        try:
            matrix = [list(map(int, line.split())) for line in lines]
        except ValueError:
            self.warningPopup("Ошибка!", "Формат матрицы неверен.")
            return

        if any(len(row) != len(matrix) for row in matrix):
            self.warningPopup("Ошибка!", "Матрица должна быть квадратной.")
            return

        self.create_graph(len(matrix))

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                weight = matrix[i][j]
                if weight > 0:
                    if not [j, i, weight, 0] in self.edges:
                        self.edges.append([i, j, weight, 0])
                    else:
                        for k, edge in enumerate(self.edges):
                            if edge[0] == j and edge[1] == i:
                                self.edges[k][3] = 1

    def parse_incidence_matrix(self):
        lines = self.TextOutput.toPlainText().strip().split("\n")

        self.clear_graph()

        if len(lines[0]) == 0:
            self.warningPopup("Ошибка!", "Формат матрицы неверен")
            return

        try:
            matrix = [list(map(int, line.split())) for line in lines]
        except ValueError:
            self.warningPopup("Ошибка!", "Формат матрицы неверен")
            return

        any_row = matrix[0]
        if any(len(row) != len(any_row) for row in matrix):
            self.warningPopup("Ошибка!", "Матрица должна быть правильных размеров")
            return

        num_vertices, num_edges = len(matrix), len(matrix[0])
        self.create_graph(num_vertices)

        for i in range(num_edges):
            start_vertex = -1
            ended = False
            start_weight = 0
            for j in range(num_vertices):
                if matrix[j][i] != 0:
                    if start_vertex == -1:
                        start_vertex = j
                        start_weight = matrix[j][i]
                    else:
                        if start_weight == matrix[j][i]:
                            self.edges.append([start_vertex, j, start_weight, 1])
                        elif start_weight > 0:
                            self.edges.append([start_vertex, j, start_weight, 0])
                        else:
                            self.edges.append([j, start_vertex, -start_weight, 0])
                        ended = True
            if (not ended):
                self.edges.append([start_vertex, start_vertex, start_weight, 0])


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    sys.exit(app.exec_())
