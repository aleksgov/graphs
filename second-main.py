from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import math

import datetime

class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        layout = QFormLayout(self)
        
        self.input = QLineEdit(self)
        layout.addRow("Ведите вес", self.input)

        self.comboBox = QComboBox()
        self.comboBox.addItem("Дуга")
        self.comboBox.addItem("Ребро")
        layout.addWidget(self.comboBox)
        
        layout.addWidget(buttonBox)
        
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
    
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

        self.setupUi()
        self.setupButtons()
        self.show()

        self.toggle_add_mode()

    def setupUi(self):
        self.dialog = InputDialog(self)

        self.setObjectName("MainWindow")
        self.resize(1200, 850)
        self.setWindowTitle("Graph Drawer")
        self.centralwidget = QWidget(self)

        self.DisplayAdjMatrixButton = QPushButton(self.centralwidget, text = "Матрица смежности")
        self.DisplayAdjMatrixButton.setGeometry(QRect(50, 750, 210, 35))

        self.DisplayIncMatrixButton = QPushButton(self.centralwidget, text = "Матрица инцидентности")
        self.DisplayIncMatrixButton.setGeometry(QRect(290, 750, 210, 35))

        self.ClearButton = QPushButton(self.centralwidget, text = "Очистить поле")
        self.ClearButton.setGeometry(QRect(530, 750, 140, 35))

        self.VertexModeButton = QPushButton(self.centralwidget, text = "Конструктор вершин")
        self.VertexModeButton.setGeometry(QRect(870, 780, 185, 35))

        self.EdgeModeButton = QPushButton(self.centralwidget, text = "Рисование связей")
        self.EdgeModeButton.setGeometry(QRect(870, 730, 185, 35))

        self.TextOutput = QTextEdit(self.centralwidget)
        self.TextOutput.setGeometry(QRect(760, 15, 380, 300))

        self.BuildGraphButton = QPushButton(self.centralwidget, text = "Простроить граф")
        self.BuildGraphButton.setGeometry(QRect(990, 335, 150, 35))

        self.InputMatrixSelectorCombo = QComboBox(self.centralwidget)
        self.InputMatrixSelectorCombo.addItems(["Матрица смежности", "Матрица инцидентности"])
        self.InputMatrixSelectorCombo.setGeometry(QRect(760, 335, 200, 35))

        # css?
        #self.InputMatrixSelectorCombo.setObjectName("Something")

        self.setCentralWidget(self.centralwidget)

        # self.menubar = QMenuBar(self)
        # self.menubar.setGeometry(QRect(0, 0, 1200, 21))
        # self.menubar.setObjectName("menubar")
        # self.setMenuBar(self.menubar)
        # self.statusbar = QStatusBar(self)
        # self.statusbar.setObjectName("statusbar")
        # self.setStatusBar(self.statusbar)
        #self.retranslateUi()

        QMetaObject.connectSlotsByName(self)

    def setupButtons(self):
        self.DisplayAdjMatrixButton.clicked.connect(self.display_adjacency_matrix)
        self.DisplayIncMatrixButton.clicked.connect(self.display_incidence_matrix)

        self.EdgeModeButton.clicked.connect(self.toggle_add_mode)
        self.VertexModeButton.clicked.connect(self.toggle_add_mode)

        self.ClearButton.clicked.connect(self.clear_graph)

        self.InputMatrixSelectorCombo.currentIndexChanged.connect(self.index_changed)
        self.BuildGraphButton.clicked.connect(self.build_graph)

    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    def warningPopup(self, title, _text):
        QMessageBox.question(self, title, _text, QMessageBox.Ok, QMessageBox.Ok)

    def toggle_add_mode(self):
        if (self.add_mode == "vertex"):
            self.EdgeModeButton.setStyleSheet("background-color: yellow")
            self.VertexModeButton.setStyleSheet("background-color: white")
            self.add_mode = "edge"
        elif (self.add_mode == "edge"):
            self.VertexModeButton.setStyleSheet("background-color: yellow")
            self.EdgeModeButton.setStyleSheet("background-color: white")
            self.add_mode = "vertex"

    def mousePressEvent(self, event):
        if (15 < event.x() < 700 and 15 < event.y() < 700):
            if (self.add_mode == "vertex"):
                i = 0
                while i < len(self.vertices):
                    if (abs(self.vertices[i][0] - event.x()) < self.vertex_radius and abs(self.vertices[i][1] - event.y()) < self.vertex_radius):
                        self.dragged_vertex_index = i
                        break
                    i += 1
                else:
                    #self.DrawVertex(self, event.x(), event.y(), str(len(self.vertices) + 1))
                    self.vertices.append([event.x(), event.y(), 1])
                    self.update()
            if (self.add_mode == "edge"):
                for i, vertex in enumerate(self.vertices):
                    if (abs(vertex[0] - event.x()) < self.vertex_radius and abs(vertex[1] - event.y()) < self.vertex_radius):
                        self.start_vertex = i

    def mouseMoveEvent(self, event):
        if (15 < event.x() < 700 and 15 < event.y() < 700):
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

    def DrawFrame(self):
        painter = QPainter(self)
        pen = QPen(QColor(120, 120, 120), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)

        painter.drawLine(15, 15, 700, 15)
        painter.drawLine(700, 15, 700, 700)
        painter.drawLine(700, 700, 15, 700)
        painter.drawLine(15, 700, 15, 15)
        painter.end()

    def DrawVertices(self):
        for i, vertex in enumerate(self.vertices):
            self.DrawVertex(self, vertex[0], vertex[1], str(i + 1))

    def DrawVertex(self, image, x, y, index):
        painter = QPainter(image)

        pen = painter.pen()
        pen.setColor(QColor(Qt.black))
        pen.setWidth(2)
        painter.setPen(pen)

        brush = painter.brush()
        brush.setColor(QColor(Qt.white))
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)

        painter.drawEllipse(QRectF(x - self.vertex_radius, y - self.vertex_radius, self.vertex_radius * 2, self.vertex_radius * 2))

        font = QFont("Arial", 12)
        painter.setFont(font)
        painter.drawText(QRectF(x - self.vertex_radius, y - self.vertex_radius, self.vertex_radius * 2, self.vertex_radius * 2), Qt.AlignCenter, index)

        painter.end()

    def DrawEdges(self):
        for edge in self.edges:
            self.DrawEdge(self, self.vertices[edge[0]][0], self.vertices[edge[0]][1], self.vertices[edge[1]][0], self.vertices[edge[1]][1], edge[2], edge[3])
    
    def DrawEdge(self, image, x1, y1, x2, y2, weight = -1, type = 1):
        painter = QPainter(image)
        pen = QPen(QColor(80, 80, 120), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)

        if (x1 == x2 and y1 == y2):
            painter.drawArc(QRect(x1 - self.vertex_radius * 2, y1 - self.vertex_radius * 2, self.vertex_radius * 2, self.vertex_radius * 2), 0, 270 * 16)

            if weight != -1:
                brush = painter.brush()
                brush.setColor(QColor(Qt.white))
                brush.setStyle(Qt.SolidPattern)
                painter.setBrush(brush)
                painter.drawRect(x1 - self.vertex_radius * 2 - 10, y1 - self.vertex_radius * 2, 30, 18)
                
                font = QFont("Arial", 12)
                painter.setFont(font)
                painter.drawText(QRectF(x1 - self.vertex_radius * 2 - 10, y1 - self.vertex_radius * 2, 30, 18), Qt.AlignCenter, str(weight))
        else:
            painter.drawLine(int(x1),int(y1),int(x2),int(y2))

            if (type == 0):
                angle = math.atan2(y2 - y1, x2 - x1)
                x2 = x2 - self.vertex_radius * math.cos(angle)
                y2 = y2 - self.vertex_radius * math.sin(angle)
                arrow_len = 15
                arrow_open_angle = math.pi / 10
                brush = painter.brush()
                brush.setColor(QColor(80, 80, 120))
                brush.setStyle(Qt.SolidPattern)
                painter.setBrush(brush)
                points = [
                    QPointF(x2, y2),
                    QPointF(x2 - arrow_len * math.cos(angle + arrow_open_angle), y2 - arrow_len * math.sin(angle + arrow_open_angle)),
                    QPointF(x2 - arrow_len * math.cos(angle - arrow_open_angle), y2 - arrow_len * math.sin(angle - arrow_open_angle)),
                ]
                painter.drawConvexPolygon(points)

            if weight != -1:
                brush = painter.brush()
                brush.setColor(QColor(Qt.white))
                brush.setStyle(Qt.SolidPattern)
                painter.setBrush(brush)
                painter.drawRect(x2 - (x2 - x1) / 4 - 15, y2 - (y2 - y1) / 4 - 9, 30, 18)

                font = QFont("Arial", 12)
                painter.setFont(font)
                painter.drawText(QRectF(x2 - (x2 - x1) / 4 - 15, y2 - (y2 - y1) / 4 - 9, 30, 18), Qt.AlignCenter, str(weight))

        painter.end()

    def paintEvent(self, event):
        #painter = QPainter(self)
        self.DrawFrame()
        if (self.start_vertex != -1):
            self.DrawEdge(self, self.vertices[self.start_vertex][0], self.vertices[self.start_vertex][1], self.cursor_pos[0], self.cursor_pos[1])
        self.DrawEdges()
        self.DrawVertices()
        #painter.end()

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
            try:
                weight = int(weight)
                return [weight, type]
            except ValueError:
                return [None, -1]
        return [None, -1]

    def end_edge(self, start_vertex, end_vertex):
        weight, type = self.ask_for_weight()
        if weight != None:
            for i, edge in enumerate(self.edges):
                if (edge[0] == start_vertex and edge[1] == end_vertex) or (edge[1] == start_vertex and edge[0] == end_vertex and edge[3] == 1):
                    reply = QMessageBox.question(self, 'Вопрос', "Вы уверены что хотите перезаписать связь?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.edges[i] = [start_vertex, end_vertex, weight, type]
                        return

            self.edges.append([start_vertex, end_vertex, weight, type])

    def clear_graph(self):
        self.vertices = []
        self.edges = []
        self.start_vertex = -1
        self.dragged_vertex_index = -1
        self.TextOutput.setText("")
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

    def display_incidence_matrix(self):
        if len(self.vertices) == 0 or len(self.edges) == 0:
            self.TextOutput.setText("Пустой граф")
            return

        incidence_matrix = [[0 for i in range(len(self.edges))] for j in range(len(self.vertices))]
        for i, edge in enumerate(self.edges):
            if edge[3] == 0:
                incidence_matrix[edge[1]][i] = -edge[2]
                incidence_matrix[edge[0]][i] = edge[2]
            if edge[3] == 1:
                incidence_matrix[edge[1]][i] = edge[2]
                incidence_matrix[edge[0]][i] = edge[2]

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
            self.warningPopup("Ошибка!", "Формат матрицы неверен")
            return

        try:
            matrix = [list(map(int, line.split())) for line in lines]
        except ValueError:
            self.warningPopup("Ошибка!", "Формат матрицы неверен")
            return

        if any(len(row) != len(matrix) for row in matrix):
            self.warningPopup("Ошибка!", "Матрица должна быть квадратной")
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
            if(not ended):
                self.edges.append([start_vertex, start_vertex, start_weight, 0])

    '''def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Graph Drawer"))
        self.DisplayAdjMatrixButton.setText(_translate("MainWindow", "Матрица смежности"))
        self.DisplayIncMatrixButton.setText(_translate("MainWindow", "Матрица инцидентности"))
        self.ChangeModeButton.setText(_translate("MainWindow", "Конструктор вершин"))
        self.EdgeModeButton.setText(_translate("MainWindow", "Рисование ребер"))
        self.ClearButton.setText(_translate("MainWindow", "Очистить поле"))
        self.BuildGraphButton.setText(_translate("MainWindow", "Простроить граф"))'''


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    sys.exit(app.exec_())