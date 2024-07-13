import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import open3d as o3d
import convert_model
import analyze_model


def create_gui(root):
    def show_main_menu():
        clear_window()

        tk.Button(root, text="Process 3D Model", command=show_process_model_menu).grid(row=0, column=2, padx=10,
                                                                                       pady=10)
        tk.Button(root, text="Handle Textures", command=handle_textures).grid(row=1, column=2, padx=10, pady=10)
        tk.Button(root, text="Quit", command=root.quit).grid(row=2, column=2, padx=10, pady=10)

    def clear_window():
        for widget in root.winfo_children():
            widget.destroy()

    def show_process_model_menu():
        clear_window()

        tk.Button(root, text="Go Back", command=show_main_menu).grid(row=0, column=1, padx=10, pady=10, sticky='ne')

        tk.Label(root, text="Select 3D Model:").grid(row=1, column=0, padx=10, pady=10)
        input_var = tk.StringVar()
        tk.Entry(root, textvariable=input_var, width=50).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(root, text="Browse", command=lambda: select_input_file(input_var)).grid(row=1, column=2, padx=10,
                                                                                          pady=10)

        tk.Label(root, text="Select Output Format:").grid(row=2, column=0, padx=10, pady=10)
        output_format_var = tk.StringVar()
        output_format_menu = tk.OptionMenu(root, output_format_var, '.obj', '.stl', '.ply', '.fbx', '.gltf', '.glb')
        output_format_menu.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(root, text="Convert and Save",
                  command=lambda: select_output_format(input_var.get(), output_format_var.get())).grid(row=3, column=1,
                                                                                                       padx=10, pady=10)

        details_var = tk.StringVar()
        tk.Label(root, textvariable=details_var, justify=tk.LEFT).grid(row=1, column=3, padx=10, pady=10, sticky='nw')

        # Canvas for 3D preview
        tk.Label(root, text="Preview:").grid(row=4, column=0, padx=10, pady=10)
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111, projection='3d')
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        def select_input_file(input_var):
            file_path = filedialog.askopenfilename(
                filetypes=[("3D Model Files", "*.obj *.stl *.ply *.fbx *.gltf *.glb")])
            if file_path:
                input_var.set(file_path)
                display_model(file_path, ax, canvas)
                display_model_details(file_path, details_var)

        def select_output_format(input_path, output_format):
            if not output_format:
                messagebox.showerror("Error", "Please select an output format.")
                return
            output_path = filedialog.asksaveasfilename(defaultextension=output_format,
                                                       filetypes=[(f"{output_format} file", f"*{output_format}")])
            if output_path:
                success, message = convert_model.convert_3d_model(input_path, output_path)
                if success:
                    messagebox.showinfo("Success", message)
                else:
                    messagebox.showerror("Error", message)

        def display_model(file_path, ax, canvas):
            try:
                mesh = o3d.io.read_triangle_mesh(file_path)
                vertices = np.asarray(mesh.vertices)
                faces = np.asarray(mesh.triangles) if mesh.has_triangles() else []

                ax.clear()

                if len(faces) > 0:
                    poly3d = [[vertices[vertex_index] for vertex_index in face] for face in faces]
                    ax.add_collection3d(Poly3DCollection(poly3d, alpha=.25, linewidths=1, edgecolors='r'))

                ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], color='k', s=1)

                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')

                scale = vertices.flatten()
                ax.auto_scale_xyz(scale, scale, scale)

                canvas.draw()

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while displaying the model: {e}")

        def display_model_details(file_path, details_var):
            success, details = analyze_model.analyze_3d_model(file_path)
            if success:
                details_str = (
                    f"Number of vertices: {details['num_vertices']}\n"
                    f"Number of faces: {details['num_faces']}\n"
                    f"File size: {details['file_size']:.2f} KB"
                )
                details_var.set(details_str)
            else:
                details_var.set(details)

    def handle_textures():
        clear_window()
        tk.Button(root, text="Go Back", command=show_main_menu).grid(row=0, column=2, padx=10, pady=10, sticky='ne')
        # Add texture handling UI here

    show_main_menu()


if __name__ == "__main__":
    root = tk.Tk()
    create_gui(root)
    root.mainloop()
