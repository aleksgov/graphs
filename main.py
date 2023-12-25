import tkinter as tk
from tkinter import ttk
import math
class GraphDrawerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Drawer")
        root.geometry("1200x850")

        self.canvas = tk.Canvas(root, bg="white", width=700, height=700)
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        self.vertices = []
        self.edges = []
        self.adjacency_matrix = []

        self.canvas.bind("<Button-1>", self.create_vertex)
        self.canvas.bind("<Button-3>", self.show_context_menu)
        self.canvas.bind("<ButtonRelease-1>", self.finish_edge)

        # B1-Motion is used for dragging vertices
        self.canvas.bind("<B1-Motion>", self.drag_vertex)

        adjacency_button = ttk.Button(root, text="Матрица смежности", command=lambda: (self.display_adjacency_matrix(), self.display_adjacency_matrix_label()))
        adjacency_button.place(x=50, y=750, width=210, height=35)

        incidence_button = ttk.Button(root, text="Матрица инцидентности", command=lambda: (self.display_incidence_matrix(), self.display_incidence_matrix_label()))
        incidence_button.place(x=290, y=750, width=210, height=35)

        clear_button = ttk.Button(root, text="Очистить граф", command=self.clear_graph)
        clear_button.place(x=530, y=750, width=140, height=35)

        mode_button = ttk.Button(root, text="Конструктор вершин", command=self.toggle_mode)
        mode_button.place(x=870, y=750, width=185, height=35)

        self.text_output = tk.Text(root, wrap=tk.WORD, width=40, height=10, font=("Courier", 12))
        self.text_output.place(x=800, y=15, width=300, height=300)

        style = ttk.Style()
        style.configure("TButton", padding=(10, 5), font="Helvetica 12", foreground="black", background="lightblue")

        build_graph_button = ttk.Button(root, text="Построить граф")
        build_graph_button.place(x=880, y=350, width=165, height=35)
        build_graph_button["style"] = "TButton"

        self.text_output.bind("<Button-3>", self.show_text_context_menu)
        self.text_context_menu = tk.Menu(root, tearoff=0)
        self.text_context_menu.add_command(label="Копировать", command=self.copy_text)
        self.text_context_menu.add_command(label="Вставить", command=self.paste_text)

        self.start_vertex = None
        self.context_menu = None
        self.mode = "add"

    def show_text_context_menu(self, event):
        self.text_context_menu.post(event.x_root, event.y_root)

    def copy_text(self):
        selected_text = self.text_output.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.root.clipboard_clear()
        self.root.clipboard_append(selected_text)
        self.root.update()

    def paste_text(self):
        clipboard_data = self.root.clipboard_get()
        self.text_output.insert(tk.INSERT, clipboard_data)
    def toggle_mode(self):
        if self.mode == "add":
            self.mode = "drag"
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Button-3>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.canvas.bind("<B1-Motion>", self.drag_vertex)
        elif self.mode == "drag":
            self.mode = "add"
            self.canvas.bind("<Button-1>", self.create_vertex)
            self.canvas.bind("<Button-3>", self.show_context_menu)
            self.canvas.bind("<ButtonRelease-1>", self.finish_edge)
            self.canvas.unbind("<B1-Motion>")
    def create_vertex(self, event):
        x, y = event.x, event.y
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

    def show_context_menu(self, event):
        x, y = event.x, event.y
        item = self.canvas.find_closest(x, y)

        if item and item[0] in self.vertices:
            self.start_vertex = item[0]

            vertex_index = self.vertices.index(self.start_vertex) + 1

            self.context_menu = tk.Menu(self.root, tearoff=0)
            for vertex in self.vertices:
                dest_vertex_index = self.vertices.index(vertex) + 1
                self.context_menu.add_command(label=f"До {dest_vertex_index}",
                                              command=lambda v=vertex: self.finish_edge_context(v))
            self.context_menu.post(event.x_root, event.y_root)

    def finish_edge_context(self, end_vertex):
        x, y = self.canvas.coords(end_vertex)[:2]
        start_x, start_y = (self.canvas.coords(self.start_vertex)[0] + self.canvas.coords(self.start_vertex)[2]) / 2, \
                           (self.canvas.coords(self.start_vertex)[1] + self.canvas.coords(self.start_vertex)[3]) / 2
        end_x, end_y = (self.canvas.coords(end_vertex)[0] + self.canvas.coords(end_vertex)[2]) / 2, \
                       (self.canvas.coords(end_vertex)[1] + self.canvas.coords(end_vertex)[3]) / 2
        vertex_radius = 15
        angle = math.atan2(end_y - start_y, end_x - start_x)
        start_x = start_x + vertex_radius * math.cos(angle)
        start_y = start_y + vertex_radius * math.sin(angle)
        end_x = end_x - vertex_radius * math.cos(angle)
        end_y = end_y - vertex_radius * math.sin(angle)

        if self.start_vertex == end_vertex:
            loop_id = self.canvas.create_arc(x - 18, y - 18, x + 25, y + 25, start=20, extent=240, style=tk.ARC,
                                             outline="lightblue", width=3)
            self.edges.append(loop_id)
            vertex_index = self.vertices.index(end_vertex)
            self.adjacency_matrix[vertex_index][vertex_index] = 1
        else:
            line_id = self.canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST, fill="lightblue", width=3)
            self.edges.append(line_id)
            start_vertex_index = self.vertices.index(self.start_vertex)
            end_vertex_index = self.vertices.index(end_vertex)
            self.adjacency_matrix[start_vertex_index][end_vertex_index] = 1

        self.start_vertex = None
        if self.context_menu:
            self.context_menu.destroy()

    def finish_edge(self, event):
        if self.context_menu:
            self.context_menu.destroy()

    def drag_vertex(self, event):
        x, y = event.x, event.y
        item = self.canvas.find_closest(x, y)

        if item and item[0] in self.vertices:
            vertex_id = item[0]
            text_id = self.get_text_id_for_vertex(vertex_id)
            self.canvas.coords(vertex_id, x - 18, y - 18, x + 18, y + 18)
            self.canvas.coords(text_id, x, y)

    def get_text_id_for_vertex(self, vertex_id):
        index = self.vertices.index(vertex_id)
        text_id = self.vertices[index] + 1
        return text_id

    def clear_graph(self):
        self.canvas.delete("all")
        self.vertices = []
        self.edges = []
        self.adjacency_matrix = []
        self.start_vertex = None
        self.text_output.delete("1.0", tk.END)

    def display_adjacency_matrix(self):
        self.text_output.delete("1.0", tk.END)

        if self.adjacency_matrix:
            for row in self.adjacency_matrix:
                self.text_output.insert(tk.END, " ".join(map(str, row)) + "\n")
        else:
            self.text_output.insert(tk.END, "Пустой граф")

    def display_adjacency_matrix_label(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()

        if self.adjacency_matrix:
            label_adj_matrix = tk.Label(self.root, text="Матрица смежности", font=("Arial", 14, "bold"))
            label_adj_matrix.place(x=800, y=415)
            row_labels = [str(i) for i in range(1, len(self.adjacency_matrix) + 1)]
            col_labels = [str(i) for i in range(1, len(self.adjacency_matrix[0]) + 1)]

            label_col_num = tk.Label(self.root, text=" ", font=("Arial", 12))
            label_col_num.place(x=800, y=460)

            for i, col_label in enumerate(col_labels):
                label_col = tk.Label(self.root, text=col_label, font=("Arial", 12, "bold"))
                label_col.place(x=830 + i * 30, y=460)

            for i, row in enumerate(self.adjacency_matrix):
                label_row_num = tk.Label(self.root, text=row_labels[i], font=("Arial", 12, "bold"))
                label_row_num.place(x=800, y=490 + i * 30)

                for j, value in enumerate(row):
                    label_value = tk.Label(self.root, text=str(value), font=("Arial", 12))
                    label_value.place(x=830 + j * 30, y=490 + i * 30)

    def display_incidence_matrix_label(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()

        incidence_matrix, edge_vertices = self.get_incidence_matrix()

        if incidence_matrix:
            label_inc_matrix = tk.Label(self.root, text="Матрица инцидентности", font=("Arial", 14, "bold"))
            label_inc_matrix.place(x=800, y=415)

            row_labels = [str(i) for i in range(1, len(incidence_matrix) + 1)]
            col_labels = [f"({edge[0]}, {edge[1]})" for edge in edge_vertices]

            label_col_num = tk.Label(self.root, text=" ", font=("Arial", 12))
            label_col_num.place(x=800, y=460)

            max_label_width = max(len(label) for label in col_labels)

            for i, col_label in enumerate(col_labels):
                label_col = tk.Label(self.root, text=col_label, font=("Arial", 12, "bold"))
                col_x = 820 + i * 60 + (max_label_width - len(col_label)) * 6
                label_col.place(x=col_x, y=460)

            for i, row in enumerate(incidence_matrix):
                label_row_num = tk.Label(self.root, text=row_labels[i], font=("Arial", 12, "bold"))
                label_row_num.place(x=800, y=500 + i * 30, anchor="e")

                for j, value in enumerate(row):
                    label_value = tk.Label(self.root, text=str(value), font=("Arial", 12))
                    col_x = 820 + j * 60 + (max_label_width - len(str(value))) * 3
                    label_value.place(x=col_x, y=500 + i * 30, anchor="w")

        else:
            label_no_inc_matrix = tk.Label(self.root, text="Пустой граф", font=("Arial", 14, "bold"))
            label_no_inc_matrix.place(x=800, y=415)

    def display_incidence_matrix(self):
        self.text_output.delete("1.0", tk.END)

        incidence_matrix, edge_vertices = self.get_incidence_matrix()
        if incidence_matrix:
            max_width = max(len(str(entry)) for row in incidence_matrix for entry in row)
            for i, row in enumerate(incidence_matrix):
                formatted_row = [f"{entry:>{max_width}}" for entry in row]
                self.text_output.insert(tk.END, "  ".join(formatted_row) + "\n")
                self.text_output.tag_configure(f"row_{i}", justify="left")
                self.text_output.tag_add(f"row_{i}", f"{i + 1}.0", f"{i + 1}.end")

        else:
            self.text_output.insert(tk.END, "Пустой граф")

    def get_incidence_matrix(self):
        if not self.adjacency_matrix:
            return None, None

        num_vertices = len(self.adjacency_matrix)
        num_edges = sum(sum(row) for row in self.adjacency_matrix)

        incidence_matrix = [[0] * num_edges for _ in range(num_vertices)]
        edge_vertices = []

        edge_index = 0
        for i in range(num_vertices):
            for j in range(num_vertices):
                if self.adjacency_matrix[i][j] == 1:
                    incidence_matrix[i][edge_index] = 1
                    incidence_matrix[j][edge_index] = -1
                    edge_vertices.append((i + 1, j + 1) if self.adjacency_matrix[j][i] == 0 else (j + 1, i + 1))
                    edge_index += 1

        return incidence_matrix, edge_vertices

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphDrawerApp(root)
    root.mainloop()
