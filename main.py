from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import math

from dataclasses import dataclass

class WarningDialog(QDialog):
    def __init__(self, title, text):
        super().__init__()

        self.setWindowTitle(title)
        self.setFixedSize(350, 260)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("QDialog { border: 4px solid #f65656; border-radius: 5px; background: #ffffff;}")

        error_icon = QPixmap('error.png')
        error_label = QLabel(self)
        error_label.setPixmap(error_icon.scaled(60, 60))
        error_label.setAlignment(Qt.AlignCenter)
        error_label.setGeometry(0, 30, 350, 60)

        text_label = QLabel(self)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setGeometry(0, 105, 350, 120)
        text_label.setText(text)
        font = QFont("Rubik", 16)
        text_label.setFont(font)
        text_label.setWordWrap(True)

        close_button = QPushButton("Закрыть", self)
        close_button.setStyleSheet(
            "QPushButton { "
                "background-color: #f65656; "
                "color: #ffffff; "
                "border-radius: 5px;"
                "font-family: Rubik; "
                "font-size: 14pt; "
            "} "
            "QPushButton:hover { "
                "background-color: #FF7474; "
            "} "
        )
        close_button.clicked.connect(self.reject)
        close_button.setGeometry(0, 215, 350, 45)


class InstructionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Instructions")
        self.layout = QVBoxLayout(self)
        self.stack = QStackedWidget(self)
        self.setStyleSheet("QDialog {background-color: #FFFFFF;}")

        instructions_pages = [
            {
                "text": "<h1>Список возможностей приложения:</h1>"
                        "<h2>1. Добавление вершин:</h2>"
                        "<p>• Выберите режим 'Конструктор вершин', нажав ЛКМ на кнопку 'Конструктор вершин'.</p>"
                        "<p>• Щелкните ЛКМ/ПКМ по пустой области в пределах рамки для графа, чтобы добавить новую вершину.</p>"
                        "<p>• Если вершину необходимо переместить, переключитесь в режим 'Конструктор вершин' и <br>перетащите вершину в новое место, зажав ЛКМ/ПКМ на нужную вершину.</p>",
                "gif_paths": ["video1.gif", "video1.2.gif"]
            },
            {
                "text": "<h2>2. Добавление связей:</h2>"
                        "<p>• Выберите режим 'Конструктор связей', нажав ЛКМ на кнопку 'Конструктор связей'.</p>"
                        "<p>• Чтобы создать связь между двумя вершинами, зажмите ЛКМ/ПКМ на одной вершине и проведите связь до другой вершины.</p>"
                        "<p>• При создании связи вам будет предложено ввести вес ребра и тип («Дуга» или «Ребро»).</p>",
                "gif_paths": ["video2.gif"]
            },
            {
                "text": "<h2>3. Удаление вершин:</h2>"
                        "<p>• Выберите режим 'Удалить вершину', нажав ЛКМ на кнопку 'Удалить вершину'.</p>"
                        "<p>• Щелкните ЛКМ/ПКМ по существующей вершине, чтобы удалить её из графа.</p>",
                "gif_paths": ["video3.gif"]
            },
            {
                "text": "<h2>4. Очистка поля:</h2>"
                        "<p>• Нажмите ЛКМ на кнопку 'Очистить поле', чтобы удалить все вершины и рёбра из графа.</p>",
                "gif_paths": ["video4.gif"]
            },
            {
                "text": "<h2>5. Вывод матриц:</h2>"
                        "<p>• Вы можете просмотреть матрицу смежности или матрицу инцидентности, нажав <br>ЛКМ на соответствующую кнопку ('Матрица смежности' или 'Матрица инцидентности').</p>"
                        "<p>• Результат отображается в окне текстового вывода.</p>",
                "gif_paths": ["video5.gif"]
            },
            {
                "text": "<h2>6. Построение графа по матрице:</h2>"
                        "<p>• Выберите тип матрицы ('Матрица смежности' или 'Матрица инцидентности') с помощью выпадающего списка.</p>"
                        "<p>• Введите матрицу в окно текстового вывода.</p>"
                        "<p>• Нажмите ЛКМ на кнопку 'Построить граф' для создания графа на основе введенной матрицы.</p>",
                "gif_paths": ["video6.gif", "video7.gif"]
            },
            {
                "text": "<h2>7. Особенности интерфейса:</h2>"
                        "<p>• Рамка для графа находится в пределах области наибольшей синей рамки. <br>Вершины не могут быть созданы или перемещены за пределы этой области.</p>"
                        "<p>• Цвет вершин - синий, цвет рёбер - светло-синий.</p>"
                        "<p>• Рамка и кнопки имеют стилизованный дизайн для улучшения визуального восприятия.</p>",
                "gif_paths": []
            },
            {
                "text": "<h2>8. Выход из приложения:</h2>"
                        "<p>• Приложение может быть закрыто при нажатии ЛКМ на крестик в верхнем правом углу окна.</p>"
                        "<p>При использовании приложения рекомендуется внимательно следить за сообщениями об ошибках</p>"
                        "<p>и предупреждениями в случае неправильного ввода данных или выполнения операций.</p>",
                "gif_paths": []
            },
        ]

        for page_info in instructions_pages:
            page_widget = QWidget(self)
            page_layout = QVBoxLayout(page_widget)

            text_label = QLabel(page_info["text"], self)
            text_label.setStyleSheet("font-family: Rubik; font-size: 14pt; color: #1e3b70;")
            page_layout.addWidget(text_label)

            gifs_layout = QHBoxLayout()
            for gif_path in page_info["gif_paths"]:
                gif_label = QLabel(self)
                movie = QMovie(gif_path)
                gif_label.setMovie(movie)
                gif_label.setStyleSheet("border: 4px solid #90AFFF; border-radius: 10px; ")
                gif_label.setFixedSize(600, 450)
                movie.start()
                gifs_layout.addWidget(gif_label)

            page_layout.addLayout(gifs_layout)
            self.stack.addWidget(page_widget)

        self.layout.addWidget(self.stack)

        navigation_layout = QHBoxLayout()

        prev_button = QPushButton("<", self)
        prev_button.clicked.connect(self.prev_page)
        prev_button.setStyleSheet(
            "QPushButton { "
            "background-color: #90AFFF; "
            "color: #ffffff; "
            "border-radius: 24px;"
            "font-family: Rubik; "
            "font-size: 20pt; "
            "font-weight: bold;"
            "} "
            "QPushButton:hover { "
            "background-color: #7CA0FF; "
            "}"
        )
        prev_button.setFixedSize(50, 50)
        navigation_layout.addWidget(prev_button)
        prev_button.setCursor(Qt.PointingHandCursor)

        next_button = QPushButton(">", self)
        next_button.clicked.connect(self.next_page)
        next_button.setStyleSheet(
            "QPushButton { "
            "background-color: #90AFFF; "
            "color: #ffffff; "
            "border-radius: 24px;"
            "font-family: Rubik; "
            "font-size: 20pt; "
            "font-weight: bold;"
            "} "
            "QPushButton:hover { "
            "background-color: #7CA0FF; "
            "}"
        )
        next_button.setFixedSize(50, 50)
        navigation_layout.addWidget(next_button)
        next_button.setCursor(Qt.PointingHandCursor)

        self.layout.addLayout(navigation_layout)

        exit_button = QPushButton("Выход", self)
        exit_button.clicked.connect(self.accept)
        exit_button.setStyleSheet(
            "QPushButton { "
            "background-color: #FF7474; "
            "color: #ffffff; "
            "border-radius: 12px;"
            "font-family: Rubik; "
            "font-size: 18pt; "
            "font-weight: bold;"
            "} "
            "QPushButton:hover { background-color: #FF5C5C; }"
        )
        exit_button.setFixedSize(140, 50)
        self.layout.addWidget(exit_button, alignment=Qt.AlignCenter)
        self.finished.connect(self.deleteLater)
        exit_button.setCursor(Qt.PointingHandCursor)

    def next_page(self):
        current_index = self.stack.currentIndex()
        if current_index < self.stack.count() - 1:
            self.stack.setCurrentIndex(current_index + 1)

    def prev_page(self):
        current_index = self.stack.currentIndex()
        if current_index > 0:
            self.stack.setCurrentIndex(current_index - 1)


class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        button_style = (
            "QPushButton { "
                "background-color: #90AFFF; "
                "color: #ffffff; "
                "border-radius: 5px;"
                "font-size: 11pt; "
                "font-weight: bold;"
            "} "
            "QPushButton:hover { "
                "background-color: #7CA0FF; "
            "}"
        )
        input_style = (
            "border: 4px #90AFFF;"
            "border-radius: 8px;"
            "padding: 2px;"
            "font-size: 11pt;"
            "font-weight: bold;"
            "text-align: center;"
            "background-color: #90AFFF;"
            "color: #ffffff;"
        )
        self.setWindowTitle(" ")
        layout = QFormLayout(self)
        self.setStyleSheet("InputDialog {background-color: #e8f3fc; font-family: Rubik; }")


        label = QLabel("Введите вес:", self)
        label.setStyleSheet("font-size: 11pt; color: #1e3b70;")
        self.input = QLineEdit(self)
        self.input.setStyleSheet(input_style)
        layout.addRow(label, self.input)


        self.comboBox = QComboBox(self)
        self.comboBox.addItem("Дуга")
        self.comboBox.addItem("Ребро")
        self.comboBox.setStyleSheet(input_style)
        self.comboBox.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.comboBox)


        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        ok_button = buttonBox.button(QDialogButtonBox.Ok)
        ok_button.setText("Принять")
        ok_button.setStyleSheet(button_style)
        ok_button.setCursor(Qt.PointingHandCursor)
        ok_button.setFixedSize(100, 24)

        cancel_button = buttonBox.button(QDialogButtonBox.Cancel)
        cancel_button.setText("Отмена")
        cancel_button.setStyleSheet(button_style)
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.setFixedSize(100, 24)

        buttonBox.move(150, 200)
        layout.addWidget(buttonBox)

    def getInputs(self):
        result = [self.input.text(), self.comboBox.currentIndex()]
        self.input.setText("")
        return result


class Delegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        if (((1 + index.row()) % 1 == 0) and (1 + index.column()) % 1 == 0):
            painter.setPen(QPen(QColor("#90AFFF"), 2))
            painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())
            painter.drawLine(option.rect.topRight(), option.rect.bottomRight())


@dataclass
class Edge:
    start_index: int
    end_index: int
    weight: int
    type: int           #0 - oriented, 1 - non-oriented


@dataclass
class Vertex:
    x : int
    y : int
    weight : int


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.drawing_board_size = QRectF(15, 85, 750, 700)
        self.vertices = []
        self.edges = []
        self.matrix_weight_mode = "no_weight"
        self.parse_matrix_mode = "adj"
        self.add_mode = "edge"
        self.vertex_radius = 18
        self.start_vertex = -1
        self.dragged_vertex_index = -1
        self.cursor_pos = [0, 0]
        self.delete = False
        self.setupUi()
        self.setupButtonsConnections()
        self.toggle_add_vertex()
        self.setMinimumSize(960, 720)
        self.resize(1250, 900)
        self.show()

    def setupUi(self):
        self.dialog = InputDialog(self)
        self.setObjectName("MainWindow")
        self.setWindowTitle("Graph Drawer")
        self.centralwidget = QWidget(self)
        self.setStyleSheet("QMainWindow {background-color: #e8f3fc;}")

        self.DisplayAdjMatrixButton = QPushButton(self.centralwidget, text="Матрица\nсмежности")
        self.set_button_style(self.DisplayAdjMatrixButton, "#90AFFF", "#7CA0FF", "#a0bbff")

        self.DisplayIncMatrixButton = QPushButton(self.centralwidget, text="Матрица\nинцидентности")
        self.set_button_style(self.DisplayIncMatrixButton, "#90AFFF", "#7CA0FF", "#a0bbff")

        self.EdgeModeButton = QPushButton(self.centralwidget, text="Конструктор\nсвязей")

        self.VertexModeButton = QPushButton(self.centralwidget, text="Конструктор\nвершин")

        self.DeleteButton = QPushButton(self.centralwidget, text="Удалить\nвершину")
        self.set_button_style(self.DeleteButton, "#ff9d9d", "#ff7474", "#ff7474")

        self.ClearButton = QPushButton(self.centralwidget, text="Очистить поле")
        self.set_button_style(self.ClearButton, "#FF7474", "#FF5C5C", "#FF7474")

        self.TextOutput = QTextEdit(self.centralwidget)
        font = QFont("Rubik", 14)
        self.TextOutput.setFont(font)
        self.TextOutput.setStyleSheet("border: 4px solid #90AFFF; "
                                      "border-radius: 10px; "
                                      "padding: 10px; "
                                      "background-color: #ffffff;")
        self.TextOutput.setWordWrapMode(QTextOption.NoWrap)

        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnWidth(2, 240)
        table_style = """
            QTableView {
            }
            QTableView QTableCornerButton::section {
                background: red;
                border: 2px outset red;
            }
            QTableView::indicator:unchecked {
                background-color: #FF0000;
            }
            QTableView {
                background-color: #e8f3fc;
                border: 4px solid #90AFFF;
                border-radius: 10px;
                padding: 10px;
                gridline-color: #90AFFF;
                selection-background-color: #c0dcf4;
            }"""
        self.tableWidget.setStyleSheet(table_style)
        delegate = Delegate(self.tableWidget)
        self.tableWidget.setItemDelegate(delegate)
        self.tableWidget.setShowGrid(0)

        self.trashButton = QPushButton(QIcon('trashbin_button.png'), '', self.centralwidget)
        self.trashButton.setIconSize(QSize(30, 30))
        self.set_button_style(self.trashButton, "#90AFFF", "#7CA0FF", "#a0bbff")

        self.guideButton = QPushButton(QIcon('info_button.png'), '', self.centralwidget)
        self.guideButton.setIconSize(QSize(25, 25))
        button_style = (
            "QPushButton { "
            "border-radius: 22px;"
            "padding: 10px;"
            "font-family: 'Rubik';"
            "font-size: 28pt;"
            "background-color: #90AFFF;"
            "color: #ffffff;"
            "} "
            "QPushButton:hover { background-color: #81a4ff }"
            "QPushButton:pressed { background-color: #a0bbff }"
        )
        self.guideButton.setCursor(Qt.PointingHandCursor)
        self.guideButton.setStyleSheet(button_style)

        self.InputMatrixSelectorCombo = QComboBox(self.centralwidget)
        self.InputMatrixSelectorCombo.addItems(["   Матрица\n   смежности", "   Матрица\n   инцидентности"])
        self.InputMatrixSelectorCombo.setCursor(Qt.PointingHandCursor)
        self.InputMatrixSelectorCombo.setStyleSheet(
            "border: 4px #90AFFF;"
            "border-radius: 8px;"
            "padding: 2px; font-family: 'Rubik';"
            "font-size: 14pt;"
            "font-weight: bold;"
            "text-align: center;"
            "background-color: #90AFFF;"
            "color: #ffffff;")
        self.BuildGraphButton = QPushButton(self.centralwidget, text="Построить граф")
        self.set_button_style(self.BuildGraphButton, "#90AFFF", "#7CA0FF", "#a0bbff")
        self.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(self)

    def setupGeometry(self, width, height):
        window_border = 20
        columns_padding = 30

        width -= window_border * 2 + columns_padding
        height -= window_border * 2

        left_column_width = int(width / 7 * 4)
        left_column_lines_padding = 20

        top_buttons_padding = 20
        top_butons_width = int((left_column_width - top_buttons_padding * 3) / 4)
        top_buttons_height = 55

        bottom_buttons_padding = 40
        bottom_buttons_width = min(180, int((left_column_width - bottom_buttons_padding) / 2))
        bottom_buttons_height = 64

        right_column_lines_padding = 35
        right_column_width = width - left_column_width

        text_output_height = int(height / 3)
        table_widget_height = int(height / 4)

        trash_button_size = 45
        
        right_buttons_padding = 15
        right_buttons_width = int((right_column_width - trash_button_size - right_buttons_padding * 2) / 2)

        self.drawing_board_size = QRectF(window_border, window_border + top_buttons_height + left_column_lines_padding, left_column_width, height - top_buttons_height - bottom_buttons_height - left_column_lines_padding * 2)
        self.DisplayAdjMatrixButton.setGeometry(QRect(window_border + int(left_column_width / 2) - int(bottom_buttons_padding / 2) - bottom_buttons_width, window_border + height - bottom_buttons_height, bottom_buttons_width, bottom_buttons_height))
        self.DisplayIncMatrixButton.setGeometry(QRect(window_border + int(left_column_width / 2) + int(bottom_buttons_padding / 2), window_border + height - bottom_buttons_height, bottom_buttons_width, bottom_buttons_height))
        self.EdgeModeButton.setGeometry(QRect(window_border, window_border, top_butons_width, top_buttons_height))
        self.VertexModeButton.setGeometry(QRect(window_border + (top_butons_width + top_buttons_padding), window_border, top_butons_width, top_buttons_height))
        self.DeleteButton.setGeometry(QRect(window_border + (top_butons_width + top_buttons_padding) * 2, window_border, top_butons_width, top_buttons_height))
        self.ClearButton.setGeometry(QRect(window_border + (top_butons_width + top_buttons_padding) * 3, window_border, top_butons_width, top_buttons_height))
        self.TextOutput.setGeometry(QRect(window_border + left_column_width + columns_padding, window_border, right_column_width, text_output_height))
        self.tableWidget.setGeometry(QRect(window_border + left_column_width + columns_padding, window_border + text_output_height + right_column_lines_padding * 2 + trash_button_size, right_column_width, table_widget_height))
        self.InputMatrixSelectorCombo.setGeometry(QRect(window_border + left_column_width + columns_padding, window_border + text_output_height + right_column_lines_padding, right_buttons_width, trash_button_size))
        self.BuildGraphButton.setGeometry(QRect(window_border + left_column_width + columns_padding + right_buttons_padding + right_buttons_width, window_border + text_output_height + right_column_lines_padding, right_buttons_width, trash_button_size))
        self.trashButton.setGeometry(QRect(window_border + left_column_width + columns_padding + right_buttons_padding * 2 + right_buttons_width * 2, window_border + text_output_height + right_column_lines_padding, trash_button_size, trash_button_size))
        self.guideButton.setGeometry(QRect(window_border + width + columns_padding - trash_button_size, window_border + height - trash_button_size, trash_button_size, trash_button_size))

    def clipVertices(self):
        for vertex in self.vertices:
            vertex[0] = min(max(self.drawing_board_size.x() + self.vertex_radius, vertex[0]), self.drawing_board_size.x() + self.drawing_board_size.width() - self.vertex_radius)
            vertex[1] = min(max(self.drawing_board_size.y() + self.vertex_radius, vertex[1]), self.drawing_board_size.y() + self.drawing_board_size.height() - self.vertex_radius)

    def warningPopup(self, title, _text):
        dialog = WarningDialog(title, _text)
        dialog.exec_()

    def set_button_style(self, button, default_color, hover_color, pressed_color):
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
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {pressed_color};
            }}
        """
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet(button_style)

    def setupButtonsConnections(self):
        self.DisplayAdjMatrixButton.clicked.connect(self.display_adjacency_matrix)
        self.DisplayIncMatrixButton.clicked.connect(self.display_incidence_matrix)

        self.EdgeModeButton.clicked.connect(self.toggle_add_edge)
        self.VertexModeButton.clicked.connect(self.toggle_add_vertex)
        self.DeleteButton.clicked.connect(self.toggle_delete_mode)

        self.ClearButton.clicked.connect(self.clear_graph)

        self.InputMatrixSelectorCombo.currentIndexChanged.connect(self.index_changed)
        self.BuildGraphButton.clicked.connect(self.build_graph)
        self.trashButton.clicked.connect(self.trash_matrix)

        self.guideButton.clicked.connect(self.show_instructions)

    def show_instructions(self):
        instructions_dialog = InstructionsDialog(self)
        instructions_dialog.exec_()

    def trash_matrix(self):
        self.TextOutput.clear()
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)

    def toggle_delete_mode(self):
        self.delete = True
        self.set_button_style(self.DeleteButton, "#FF8383", "#FF5C5C", "#FF5C5C")
        self.set_button_style(self.VertexModeButton, "#90AFFF", "#7CA0FF", "#7CA0FF")
        self.set_button_style(self.EdgeModeButton, "#90AFFF", "#7CA0FF", "#7CA0FF")

    def toggle_add_vertex(self):
        self.delete = False
        self.set_button_style(self.EdgeModeButton, "#90AFFF", "#7CA0FF", "#7CA0FF")
        self.set_button_style(self.DeleteButton, "#90AFFF", "#FF7474", "#FF7474")
        self.set_button_style(self.VertexModeButton, "#7DD6DB", "#4BCFD6", "#4BCFD6")
        self.add_mode = "vertex"

    def toggle_add_edge(self):
        self.delete = False
        self.set_button_style(self.VertexModeButton, "#90AFFF", "#7CA0FF", "#7CA0FF")
        self.set_button_style(self.DeleteButton, "#90AFFF", "#FF7474", "#FF7474")
        self.set_button_style(self.EdgeModeButton, "#7DD6DB", "#4BCFD6", "#4BCFD6")
        self.add_mode = "edge"

    def index_changed(self, index):
        if index == 0:
            self.parse_matrix_mode = "adj"
        if index == 1:
            self.parse_matrix_mode = "inc"

    def mousePressEvent(self, event):
        if (self.drawing_board_size.x() + self.vertex_radius < event.x() < self.drawing_board_size.x() + self.drawing_board_size.width() - self.vertex_radius and \
            self.drawing_board_size.y() + self.vertex_radius < event.y() < self.drawing_board_size.y() + self.drawing_board_size.height() - self.vertex_radius):
            if (self.delete):
                for i, vertex in enumerate(self.vertices):
                    if (abs(vertex[0] - event.x()) < self.vertex_radius and abs(vertex[1] - event.y()) < self.vertex_radius):
                        self.vertices.pop(i)
                        j = 0
                        while j < len(self.edges):
                            if (self.edges[j].start_index == i or self.edges[j].end_index == i):
                                self.edges.pop(j)
                                continue
                            if (self.edges[j].start_index > i):
                                self.edges[j].start_index -= 1
                            if (self.edges[j].end_index > i):
                                self.edges[j].end_index -= 1
                            j += 1
                        break

            elif (self.add_mode == "vertex"):
                for i in range(len(self.vertices)):
                    if (abs(self.vertices[i][0] - event.x()) < self.vertex_radius and abs(self.vertices[i][1] - event.y()) < self.vertex_radius):
                        self.dragged_vertex_index = i
                        break
                else:
                    self.vertices.append([event.x(), event.y(), 1])
                    self.update()

            elif (self.add_mode == "edge"):
                for i, vertex in enumerate(self.vertices):
                    if (abs(vertex[0] - event.x()) < self.vertex_radius and abs(vertex[1] - event.y()) < self.vertex_radius):
                        self.start_vertex = i

    def mouseMoveEvent(self, event):
        if (self.drawing_board_size.x() + self.vertex_radius < event.x() < self.drawing_board_size.x() + self.drawing_board_size.width() - self.vertex_radius and \
            self.drawing_board_size.y() + self.vertex_radius < event.y() < self.drawing_board_size.y() + self.drawing_board_size.height() - self.vertex_radius):
            if (self.dragged_vertex_index != -1):
                self.vertices[self.dragged_vertex_index][0] = event.x()
                self.vertices[self.dragged_vertex_index][1] = event.y()

            if (self.start_vertex != -1):
                self.cursor_pos = [event.x(), event.y()]

            self.update()
        else:
            self.dragged_vertex_index = -1
            self.start_vertex = -1

    def ask_for_weight(self):
            weight = -1
            while int(weight) < 0:
                if self.dialog.exec():
                    weight, type = self.dialog.getInputs()
                    try:
                        if weight.strip() == "":
                            return ["1", type]
                        weight = int(weight)
                        if weight < 0:
                            self.warningPopup(" ", "<h3>&nbsp;Предупреждение!</h3>\n&nbsp;&nbsp;Вес должен быть положительным.<br><br>")
                            continue
                        return [weight, type]
                    except ValueError:
                        weight = -1
                        self.warningPopup(" ", "<h3>&nbsp;Ошибка!</h3>\n&nbsp;&nbsp;Вес должен быть целым числом.<br><br>")
                else:
                    return [None, -1]

    def mouseReleaseEvent(self, event):
        if (self.start_vertex != -1):
            for i, vertex in enumerate(self.vertices):
                if (abs(vertex[0] - event.x()) < self.vertex_radius and abs(vertex[1] - event.y()) < self.vertex_radius):

                    result = self.ask_for_weight()

                    if result is None:  break

                    weight, type = result
                    if weight is None:  break

                    self.end_edge(self.start_vertex, i, weight, type)

        self.dragged_vertex_index = -1
        self.start_vertex = -1
        self.update()

    def resizeEvent(self, event):
        width, height = event.size().width(), event.size().height()
        self.setupGeometry(width, height)
        self.clipVertices()

    def paintEvent(self, event):
        self.DrawFrame()
        if (self.start_vertex != -1):
            self.DrawEdge(self, self.vertices[self.start_vertex][0], self.vertices[self.start_vertex][1], self.cursor_pos[0], self.cursor_pos[1])
        self.DrawEdges()
        self.DrawVertices()

    def DrawVertices(self):
        for i, vertex in enumerate(self.vertices):
            self.DrawVertex(self, vertex[0], vertex[1], str(i + 1))

    def DrawVertex(self, object, x, y, index):
        painter = QPainter(object)

        painter.setPen(QPen(QColor("#81a4ff"), 2))
        painter.setBrush(QColor("#81a4ff"))

        painter.drawEllipse(QRectF(x - self.vertex_radius, y - self.vertex_radius, self.vertex_radius * 2, self.vertex_radius * 2))
        painter.setPen(QColor(Qt.white))

        painter.setFont(QFont("Rubik", 14))
        painter.drawText(QRectF(x - self.vertex_radius, y - self.vertex_radius, self.vertex_radius * 2, self.vertex_radius * 2), Qt.AlignCenter, str(index))

        painter.end()

    def DrawEdges(self):
        for edge in self.edges:
            self.DrawEdge(self, self.vertices[edge.start_index][0], self.vertices[edge.start_index][1], self.vertices[edge.end_index][0], self.vertices[edge.end_index][1], edge.weight, edge.type)

    def DrawEdge(self, object, x1, y1, x2, y2, weight = -1, type = 1):
        painter = QPainter(object)
        painter.setPen(QPen(QColor("#5A88FF"), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        text_x, text_y = x2, y2

        if (x1 == x2 and y1 == y2):
            painter.drawArc(QRect(int(x1) - self.vertex_radius * 2, int(y1) - self.vertex_radius * 2, self.vertex_radius * 2, self.vertex_radius * 2), 0, 270 * 16)
            text_x = int(x1) - self.vertex_radius * 2
            text_y = int(y1) - self.vertex_radius * 2

        else:
            if (type == 0):
                # ================= bezier curve ==================
                angle1 = math.atan2(y2 - y1, x2 - x1)

                x2 = x2 - self.vertex_radius * math.cos(angle1)
                y2 = y2 - self.vertex_radius * math.sin(angle1)

                length = int(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))
                points = [QPoint(int(length / 3), 30), QPoint(int(length / 3 * 2), 30), QPoint(length, 0)]
                for i in range(3):
                    x = x1 + points[i].x() * math.cos(angle1) - points[i].y() * math.sin(angle1)
                    y = y1 + points[i].x() * math.sin(angle1) + points[i].y() * math.cos(angle1)
                    points[i] = QPoint(int(x), int(y))
                path = QPainterPath(QPoint(int(x1 + self.vertex_radius * math.cos(angle1)),
                                           int(y1 + self.vertex_radius * math.sin(angle1))))
                path.cubicTo(points[0], points[1], points[2])
                painter.drawPath(path)

                # ===================== arrow =====================
                angle2 = math.atan2(y2 - points[1].y(), x2 - points[1].x())
                arrow_len = 15
                arrow_open_angle = math.pi / 10
                brush = painter.brush()
                brush.setColor(QColor("#5A88FF"))
                brush.setStyle(Qt.SolidPattern)
                painter.setBrush(brush)
                arrow_points = [
                    QPointF(x2, y2),
                    QPointF(x2 - arrow_len * math.cos(angle2 + arrow_open_angle),
                            y2 - arrow_len * math.sin(angle2 + arrow_open_angle)),
                    QPointF(x2 - arrow_len * math.cos(angle2 - arrow_open_angle),
                            y2 - arrow_len * math.sin(angle2 - arrow_open_angle)),
                ]
                painter.drawConvexPolygon(arrow_points)

                text_x = points[1].x()
                text_y = points[1].y()

            if (type == 1):
                painter.drawLine(int(x1), int(y1), int(x2), int(y2))
                text_x = int(x2) - (x2 - x1) // 4
                text_y = int(y2) - (y2 - y1) // 4

        if (weight != -1 and weight != "1"):
            font = QFont("Rubik", 12)
            font_metrics = QFontMetrics(font)
            width = max(30, int(font_metrics.width(str(weight))))
            height = int(font_metrics.height())

            brush = painter.brush()
            brush.setColor(QColor(Qt.white))
            brush.setStyle(Qt.SolidPattern)
            painter.setBrush(brush)
            painter.setFont(font)
            painter.drawRect(text_x - width // 2 - 2, text_y - height // 2 - 2, width + 4, height + 4)
            painter.drawText(QRectF(text_x - width // 2, text_y - height // 2, width, height), Qt.AlignCenter, str(weight))

        painter.end()

    def DrawFrame(self):
        painter = QPainter(self)
        pen = QPen(QColor("#90AFFF"), 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(QColor("#ffffff"))
        painter.drawRoundedRect(self.drawing_board_size, 10, 10)
        painter.end()

    def build_graph(self):
        if self.parse_matrix_mode == "adj":
            self.parse_adjacency_matrix()
        if self.parse_matrix_mode == "inc":
            self.parse_incidence_matrix()

    def end_edge(self, start_vertex, end_vertex, weight, type):
        i = 0
        while i < len(self.edges):
            edge = self.edges[i]
            if (type == edge.type):
                if (edge.start_index == start_vertex and edge.end_index == end_vertex):
                    self.edges.pop(i)
                    continue

                if (type == 1):
                    if (edge.start_index == end_vertex and edge.end_index == start_vertex):
                        self.edges.pop(i)
                        continue

            if (type != edge.type):
                if (edge.start_index == start_vertex and edge.end_index == end_vertex) or \
                        (edge.start_index == end_vertex and edge.end_index == start_vertex):
                    self.edges.pop(i)
                    continue

            i += 1

        self.edges.append(Edge(start_vertex, end_vertex, weight, type))

        self.update()

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
            if edge.type == 1:
                adj_matrix[edge.end_index][edge.start_index] = edge.weight
            adj_matrix[edge.start_index][edge.end_index] = edge.weight

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

        inc_matrix = [[0 for i in range(len(self.edges))] for j in range(len(self.vertices))]

        for i, edge in enumerate(self.edges):
            if edge.type == 0:
                inc_matrix[edge.end_index][i] = -int(edge.weight) if isinstance(edge.weight, str) else -edge.weight
                inc_matrix[edge.start_index][i] = int(edge.weight) if isinstance(edge.weight, str) else edge.weight
            if edge.type == 1:
                inc_matrix[edge.end_index][i] = int(edge.weight) if isinstance(edge.weight, str) else edge.weight
                inc_matrix[edge.start_index][i] = int(edge.weight) if isinstance(edge.weight, str) else edge.weight

        max_width = max(len(str(entry)) for row in inc_matrix for entry in row)
        output_text = ""
        for row in inc_matrix:
            formatted_row = [f"{entry:>{max_width}}" for entry in row]
            output_text += " ".join(formatted_row) + "\n"
        self.TextOutput.setText(output_text)

        self.tableWidget.clear()
        self.tableWidget.setRowCount(len(inc_matrix))
        self.tableWidget.setColumnCount(len(inc_matrix[0]))
        self.tableWidget.setHorizontalHeaderLabels([f"{edge.start_index + 1}-{edge.end_index + 1}" for edge in self.edges])
        font = QFont("Rubik", 12)

        for i in range(len(inc_matrix)):
            for j in range(len(inc_matrix[i])):
                item = QTableWidgetItem(str(inc_matrix[i][j]))
                item.setFont(font)
                self.tableWidget.setItem(i, j, item)

    def create_graph(self, vertices_count):
        center_x, center_y = self.drawing_board_size.width() / 2 + self.drawing_board_size.x(), self.drawing_board_size.height() / 2 + self.drawing_board_size.y()
        radius = min(center_x / 7 * 6 - self.drawing_board_size.x(), center_y / 7 * 6 - self.drawing_board_size.y())
        for i in range(vertices_count):
            self.vertices.append([center_x + radius * math.cos(2 * math.pi / vertices_count * i), center_y + radius * math.sin(2 * math.pi / vertices_count * i), 1])

    def parse_adjacency_matrix(self):
        lines = self.TextOutput.toPlainText().strip().split("\n")

        self.clear_graph()

        if len(lines[0]) == 0:
            self.warningPopup(" ", "<h3>&nbsp;Ошибка!</h3>\n&nbsp;&nbsp;Формат матрицы неверен.<br><br>")
            return

        try:
            matrix = [list(map(int, line.split())) for line in lines]
        except ValueError:
            self.warningPopup(" ", "<h3>&nbsp;Ошибка!</h3>\n&nbsp;&nbsp;Формат матрицы неверен.<br><br>")
            return

        if any(len(row) != len(matrix) for row in matrix):
            self.warningPopup(" ", "<h3>&nbsp;Ошибка!</h3>\n&nbsp;&nbsp;Матрица должна быть квадратной.<br><br>")
            return

        self.create_graph(len(matrix))

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                weight = matrix[i][j]
                if weight > 0:
                    if not Edge(j, i, weight, 0) in self.edges:
                        self.end_edge(i, j, weight, 0)
                    else:
                        self.edges[self.edges.index(Edge(j, i, weight, 0))].type = 1

    def parse_incidence_matrix(self):
        lines = self.TextOutput.toPlainText().strip().split("\n")

        self.clear_graph()

        if len(lines[0]) == 0:
            self.warningPopup(" ", "<h3>&nbsp;Ошибка!</h3>\n&nbsp;&nbsp;Формат матрицы неверен.<br><br>")
            return

        try:
            matrix = [list(map(int, line.split())) for line in lines]
        except ValueError:
            self.warningPopup(" ", "<h3>&nbsp;Ошибка!</h3>\n&nbsp;&nbsp;Формат матрицы неверен.<br><br>")
            return

        any_row = matrix[0]
        if any(len(row) != len(any_row) for row in matrix):
            self.warningPopup(" ",
                              "<h3>&nbsp;Ошибка!</h3>\n&nbsp;&nbsp;Матрица должна быть требуемых размеров.<br><br>")
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
                            self.end_edge(start_vertex, j, start_weight, 1)
                        elif start_weight > 0:
                            self.end_edge(start_vertex, j, start_weight, 0)
                        else:
                            self.end_edge(j, start_vertex, -start_weight, 0)
                        ended = True
            if (not ended):
                self.end_edge(start_vertex, start_vertex, start_weight, 0)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.setWindowIcon(QIcon('icon.ico'))
    sys.exit(app.exec_())