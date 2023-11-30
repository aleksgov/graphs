import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Граф Editor")

        self.graph = nx.MultiDiGraph()
        self.matrix_type = tk.StringVar(value="adjacency")  # По умолчанию используется матрица смежности

        self.root.attributes('-fullscreen', True)
        self.root.overrideredirect(True)
        self.root.geometry('400x900+900+200')
        self.root.protocol("WM_DELETE_WINDOW", exit)
        self.init_ui()

    def init_ui(self):
        # Создаем элементы интерфейса
        self.exit_button = tk.Button(self.root, text="X", command=exit, background='red')
        self.label = tk.Label(self.root, text="Выберите тип матрицы:")
        self.radio_adjacency = tk.Radiobutton(self.root, text="Матрица смежности", variable=self.matrix_type, value="adjacency")
        self.radio_incidence = tk.Radiobutton(self.root, text="Матрица инцидентности", variable=self.matrix_type, value="incidence")
        self.label_matrix = tk.Label(self.root, text="Введите матрицу:")
        self.text_area = tk.Text(self.root, height=10, width=40)
        self.draw_button = tk.Button(self.root, text="Нарисовать граф", command=self.draw_graph)

        # Увеличиваем размер кнопок
        self.exit_button.config(font=('TkDefaultFont', 12), width=3, height=1)
        self.label.config(font=('TkDefaultFont', 14, 'bold'))
        self.radio_adjacency.config(font=('TkDefaultFont', 12))
        self.radio_incidence.config(font=('TkDefaultFont', 12))
        self.label_matrix.config(font=('TkDefaultFont', 14, 'bold'))
        self.text_area.config(font=('TkDefaultFont', 12))
        self.draw_button.config(font=('TkDefaultFont', 12))

        # Размещаем элементы на экране
        self.exit_button.pack(pady=10, anchor='e')
        self.label.pack(pady=10, )
        self.radio_adjacency.pack(pady=5)
        self.radio_incidence.pack(pady=5)
        self.label_matrix.pack(pady=5)
        self.text_area.pack(pady=5)
        self.draw_button.pack(pady=10)

        self.text_area.bind("<Button-3>", self.show_context_menu)
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Paste", command=self.paste_matrix)

    def draw_graph(self):
        try:
            matrix_text = self.text_area.get("1.0", tk.END)
            if self.matrix_type.get() == "adjacency":
                self.graph = self.parse_adjacency_matrix(matrix_text)
            else:
                self.graph = self.parse_incidence_matrix(matrix_text)
            self.draw_graph_plot()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при чтении матрицы: {str(e)}")

    def parse_adjacency_matrix(self, matrix_text):
        lines = matrix_text.strip().split("\n")
        matrix = [list(map(int, line.split())) for line in lines]
        if any(len(row) != len(matrix) for row in matrix):
            raise ValueError("Матрица должна быть квадратной")

        graph = nx.MultiDiGraph()
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 1:
                    graph.add_edge(i + 1, j + 1)

        return graph


    def parse_incidence_matrix(self, matrix_text):
        lines = matrix_text.strip().split("\n")
        matrix = [list(map(int, line.split())) for line in lines]

        graph = nx.MultiDiGraph()

        num_vertices, num_edges = len(matrix), len(matrix[0])
        for j in range(num_edges):
            connected_vertices = [[i + 1, matrix[i][j]] for i in range(num_vertices) if matrix[i][j] == 1 or matrix[i][j] == -1]
            if len(connected_vertices) == 1:
                graph.add_edge(connected_vertices[0][0], connected_vertices[0][0])
            if len(connected_vertices) == 2:
                if (connected_vertices[0][1] * connected_vertices[1][1] > 0):
                    graph.add_edge(connected_vertices[1][0], connected_vertices[0][0])
                graph.add_edge(connected_vertices[0][0], connected_vertices[1][0])

        return graph

    def draw_graph_plot(self):
        if hasattr(self, "canvas") and self.canvas:
            plt.close()
            self.canvas.get_tk_widget().destroy()

        pos = nx.spring_layout(self.graph)

        self.canvas = FigureCanvasTkAgg(plt.figure())
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.NONE)
        nx.draw_networkx(self.graph, pos, with_labels=True, font_weight='bold', connectionstyle="arc3,rad=0.1", arrows=True)

        self.canvas.draw()

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def paste_matrix(self):
        try:
            matrix_text = self.root.clipboard_get()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, matrix_text)
        except tk.TclError:
            pass 

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
