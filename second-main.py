from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import math

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

        self.vertices = []
        self.edges = []
        self.start_vertex = None
        self.edge_mode = "edge"
        self.matrix_weight_mode = "no_weight"
        self.parse_matrix_mode = "adj"

        self.vertex_radius = 18

        self.setupUi()
        self.setupButtons()
        self.show()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1200, 850)
        self.setWindowTitle("Graph Drawer")
        self.centralwidget = QWidget(self)

        self.imageBackground = QImage(QSize(685, 685), QImage.Format_ARGB32)
        self.imageBackground.fill(Qt.transparent)

        self.DisplayAdjMatrixButton = QPushButton(self.centralwidget, text = "Матрица смежности")
        self.DisplayAdjMatrixButton.setGeometry(QRect(50, 750, 210, 35))

        self.DisplayIncMatrixButton = QPushButton(self.centralwidget, text = "Матрица инцидентности")
        self.DisplayIncMatrixButton.setGeometry(QRect(290, 750, 210, 35))

        self.ClearButton = QPushButton(self.centralwidget, text = "Очистить поле")
        self.ClearButton.setGeometry(QRect(530, 750, 140, 35))

        self.ChangeModeButton = QPushButton(self.centralwidget, text = "Конструктор вершин")
        self.ChangeModeButton.setGeometry(QRect(870, 780, 185, 35))

        self.EdgeModeButton = QPushButton(self.centralwidget, text = "Рисование ребер")
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

        self.DrawFrame()

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

    def DrawFrame(self):
        qp = QPainter(self.imageBackground)
        qp.setPen(QPen(QColor(120, 120, 120), 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        qp.drawLine(0, 0, 684, 0)
        qp.drawLine(684, 0, 684, 684)
        qp.drawLine(684, 684, 0, 684)
        qp.drawLine(0, 684, 0, 0)
        qp.end()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def warningPopup(self, title, _text):
        QMessageBox.question(self, title, _text, QMessageBox.Ok, QMessageBox.Ok)

    def mousePressEvent(self, event):
        if (15 < event.x() < 700 and 15 < event.y() < 700):
            
                self.RenderVertex(self.imageBackground, event.x(), event.y(), str(len(self.vertices) + 1))
                self.vertices.append([event.x(), event.y(), 1])
                self.update()

    def RenderVertex(self, image, x, y, index):
        x -= self.vertex_radius
        y -= self.vertex_radius
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
    
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(QPoint(15, 15), self.imageBackground)

    def setupButtons(self):
        self.DisplayAdjMatrixButton.clicked.connect(self.display_adjacency_matrix)
        self.DisplayIncMatrixButton.clicked.connect(self.display_incidence_matrix)
        self.EdgeModeButton.clicked.connect(self.toggle_edge_mode)
        self.ClearButton.clicked.connect(self.clear_graph)
        self.BuildGraphButton.clicked.connect(self.build_graph)
        self.InputMatrixSelectorCombo.currentIndexChanged.connect(self.index_changed)

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

    def toggle_edge_mode(self):
        if self.edge_mode == "edge":
            self.edge_mode_button.config(text="Рисование дуг")
            self.edge_mode = "arc"
            return

        if self.edge_mode == "arc":
            self.edge_mode_button.config(text="Рисование ребер")
            self.edge_mode = "edge"
            return

        vertex_id = self.canvas.create_oval(x - 18, y - 18, x + 18, y + 18, fill="lightblue", outline="lightblue", width=3)
        self.vertices.append(vertex_id)
        vertex_index = len(self.vertices)
        label_id = self.canvas.create_text(x, y, text=str(vertex_index), fill="black", font=("Arial", 12))
        if not self.adjacency_matrix:
            self.adjacency_matrix = [[0]]
        else:
            for row in self.adjacency_matrix:
                row.append(0)
            self.adjacency_matrix.append([0] * len(self.adjacency_matrix[0]))

        if self.start_vertex is not None:
            end_vertex = vertex_id
            self.finish_edge_context(end_vertex)

    def finish_edge_context(self, end_vertex, weight=None):
        x, y = self.canvas.coords(end_vertex)[:2]
        start_x = (self.canvas.coords(self.start_vertex)[0] + self.canvas.coords(self.start_vertex)[2]) / 2
        start_y = (self.canvas.coords(self.start_vertex)[1] + self.canvas.coords(self.start_vertex)[3]) / 2
        end_x = (self.canvas.coords(end_vertex)[0] + self.canvas.coords(end_vertex)[2]) / 2
        end_y = (self.canvas.coords(end_vertex)[1] + self.canvas.coords(end_vertex)[3]) / 2
        vertex_radius = 15
        angle = math.atan2(end_y - start_y, end_x - start_x)
        start_x = start_x + vertex_radius * math.cos(angle)
        start_y = start_y + vertex_radius * math.sin(angle)
        end_x = end_x - vertex_radius * math.cos(angle)
        end_y = end_y - vertex_radius * math.sin(angle)
        weight = self.ask_for_weight()
        if self.edge_mode == "arc":
            if self.start_vertex == end_vertex:
                loop_id = self.canvas.create_arc(x - 18, y - 18, x + 25, y + 25, start=20, extent=240, style=tk.ARC,
                                                 outline="lightblue", width=3)
                self.edges.append(loop_id)
                vertex_index = self.vertices.index(end_vertex)
                text_x = x + -20 * math.cos(math.radians(20))
                text_y = y + -20 * math.sin(math.radians(20))
                if weight is not None:
                    self.canvas.create_text(text_x, text_y, text=weight, fill="black", font=("Arial", 10))
                else:
                    weight = 1
                self.edges.append(loop_id)
                vertex_index = self.vertices.index(end_vertex)
                self.adjacency_matrix[vertex_index][vertex_index] = weight
            else:
                line_id = self.canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST, fill="lightblue", arrowshape=(15, 20, 5), width=3)
                self.edges.append(line_id)
                start_vertex_index = self.vertices.index(self.start_vertex)
                end_vertex_index = self.vertices.index(end_vertex)
                if weight is not None:
                    label_x, label_y = (start_x + end_x) / 2, (start_y + end_y) / 2
                    label = self.canvas.create_text(label_x, label_y, text=str(weight), fill="black", font=("Arial", 10))
                    text_width = self.canvas.bbox(label)[2] - self.canvas.bbox(label)[0]
                    rect_x1, rect_y1, rect_x2, rect_y2 = label_x - text_width / 2 - 5, label_y - 10, label_x + text_width / 2 + 5, label_y + 10
                    rectangle = self.canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill="lightblue", outline="lightblue")
                    self.canvas.tag_lower(rectangle, label)
                else:
                    weight = 1
                self.adjacency_matrix[start_vertex_index][end_vertex_index] = weight
            self.start_vertex = None
            if self.context_menu:
                self.context_menu.destroy()

        elif self.edge_mode == "edge":
            if self.start_vertex == end_vertex:
                loop_id = self.canvas.create_arc(x - 18, y - 18, x + 25, y + 25, start=20, extent=240, style=tk.ARC, outline="lightblue", width=3)
                self.edges.append(loop_id)
                vertex_index = self.vertices.index(end_vertex)
                text_x = x + -20 * math.cos(math.radians(20))
                text_y = y + -20 * math.sin(math.radians(20))
                if weight is not None:
                    self.canvas.create_text(text_x, text_y, text=weight, fill="black", font=("Arial", 10))
                else:
                    weight = 1
                self.edges.append(loop_id)
                vertex_index = self.vertices.index(end_vertex)
                self.adjacency_matrix[vertex_index][vertex_index] = weight
            else:
                line_id = self.canvas.create_line(
                    start_x, start_y, end_x, end_y, fill="lightblue", width=3
                )
                if weight is not None:
                    label_x, label_y = (start_x + end_x) / 2, (start_y + end_y) / 2
                    label = self.canvas.create_text(label_x, label_y, text=str(weight), fill="black", font=("Arial", 10))
                    text_width = self.canvas.bbox(label)[2] - self.canvas.bbox(label)[0]
                    rect_x1, rect_y1, rect_x2, rect_y2 = label_x - text_width / 2 - 5, label_y - 10, label_x + text_width / 2 + 5, label_y + 10
                    rectangle = self.canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill="lightblue", outline="lightblue")
                    self.canvas.tag_lower(rectangle, label)
                else:
                    weight = 1
                start_vertex_index = self.vertices.index(self.start_vertex)
                end_vertex_index = self.vertices.index(end_vertex)
                self.adjacency_matrix[start_vertex_index][end_vertex_index] = weight
                self.adjacency_matrix[end_vertex_index][start_vertex_index] = weight

            self.start_vertex = None
            if self.context_menu:
                self.context_menu.destroy()

    def ask_for_weight(self):
        weight_str, ok = QInputDialog.getText(self,'Weight','Введите вес ребра:')
        if (ok):
            try:
                weight = int(weight_str)
                return weight
            except ValueError:
                return None

    def drag_vertex(self, event):
        x, y = event.x, event.y
        item = self.canvas.find_closest(x, y)

        if item and item[0] in self.vertices:
            vertex_id = item[0]
            text_id = self.get_text_id_for_vertex(vertex_id)
            self.canvas.coords(vertex_id, x - 18, y - 18, x + 18, y + 18)
            self.canvas.coords(text_id, x, y)
            self.redraw_edges()

    def redraw_edges(self):
        for edge_id in self.edges:
            self.canvas.delete(edge_id)
        self.edges = []

        for i, start_vertex in enumerate(self.vertices):
            for j, end_vertex in enumerate(self.vertices):
                if (self.adjacency_matrix[i][j] != 1):
                    continue

                start_x, start_y = self.get_vertex_center(start_vertex)
                end_x, end_y = self.get_vertex_center(end_vertex)
                x, y = self.canvas.coords(end_vertex)[:2]

                vertex_radius = 15
                angle = math.atan2(end_y - start_y, end_x - start_x)
                start_x = start_x + vertex_radius * math.cos(angle)
                start_y = start_y + vertex_radius * math.sin(angle)
                end_x = end_x - vertex_radius * math.cos(angle)
                end_y = end_y - vertex_radius * math.sin(angle)

                if start_vertex == end_vertex:
                    loop_id = self.canvas.create_arc(x - 18, y - 18, x + 25, y + 25, tart=20, extent=240, style=tk.ARC, outline="lightblue", width=3)
                    self.edges.append(loop_id)
                else:
                    if (self.adjacency_matrix[i][j] == self.adjacency_matrix[j][i]):
                        line_id = self.canvas.create_line(start_x, start_y, end_x, end_y, fill="lightblue", width=3)
                    else:
                        line_id = self.canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST, fill="lightblue", width=3)

                    self.edges.append(line_id)

    def clear_graph(self):
        #self.canvas.delete("all")
        self.imageBackground.fill(Qt.transparent)
        self.DrawFrame()
        self.update()
        self.vertices = []
        self.edges = []
        self.start_vertex = None
        self.TextOutput.setText("")

    def display_adjacency_matrix(self):
        if len(self.vertices) == 0:
            self.TextOutput.setText("Пустой граф")
            return
        
        adj_matrix = [[0] * len(self.vertices)] * len(self.vertices)
        for edge in self.edges:
            if edge[3] == 0:
                adj_matrix[edge[0]][edge[1]] = edge[2]
            else:
                adj_matrix[edge[1]][edge[0]] = edge[2]
        
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

        incidence_matrix = [[0] * len(self.edges)] * len(self.vertices)
        for i, edge in enumerate(self.edges):
            if edge[3] == 0:
                incidence_matrix[i][edge[0]] = edge[2]

        max_width = max(len(str(entry)) for row in incidence_matrix for entry in row)
        output_text = ""
        for row in incidence_matrix:
            formatted_row = [f"{entry:>{max_width}}" for entry in row]
            output_text += " ".join(formatted_row) + "\n"
        self.TextOutput.setText(output_text)

    def create_graph(self, vertices_count):
        center_x, center_y = self.imageBackground.size().width() / 2 + 15, self.imageBackground.size().height() / 2 + 15
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
        print(self.vertices)
        print(self.edges)

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