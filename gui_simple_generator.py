#!/usr/bin/env python3
"""
Interfaz gráfica para el generador de G-code simple (sin variaciones aleatorias)
"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
from simple_image_to_gcode import SimpleGCodeGenerator

class SimpleGCodeGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador G-code Simple (sin variaciones aleatorias)")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.canvas_width = tk.DoubleVar(value=200.0)
        self.canvas_height = tk.DoubleVar(value=200.0)
        self.z_safe = tk.DoubleVar(value=5.0)
        self.z_draw = tk.DoubleVar(value=0.2)
        self.feed_rate = tk.IntVar(value=1000)
        self.travel_speed = tk.IntVar(value=3000)
        self.setup_ui()
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        title_label = ttk.Label(main_frame, text="Generador G-code Simple", font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        files_frame = ttk.LabelFrame(main_frame, text="Archivos", padding="10")
        files_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        files_frame.columnconfigure(1, weight=1)
        ttk.Label(files_frame, text="Imagen de entrada:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        ttk.Entry(files_frame, textvariable=self.input_file, state='readonly').grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=(0, 5))
        ttk.Button(files_frame, text="Buscar...", command=self.browse_input_file).grid(row=0, column=2, pady=(0, 5))
        ttk.Label(files_frame, text="Archivo G-code:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(files_frame, textvariable=self.output_file).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(files_frame, text="Guardar como...", command=self.browse_output_file).grid(row=1, column=2)
        canvas_frame = ttk.LabelFrame(main_frame, text="Dimensiones del Canvas (mm)", padding="10")
        canvas_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        ttk.Label(canvas_frame, text="Ancho:").grid(row=0, column=0, sticky=tk.W)
        ttk.Spinbox(canvas_frame, from_=10, to=1000, textvariable=self.canvas_width, width=10).grid(row=0, column=1, padx=(5, 20))
        ttk.Label(canvas_frame, text="Alto:").grid(row=0, column=2, sticky=tk.W)
        ttk.Spinbox(canvas_frame, from_=10, to=1000, textvariable=self.canvas_height, width=10).grid(row=0, column=3, padx=(5, 0))
        z_frame = ttk.LabelFrame(main_frame, text="Parámetros Z (mm)", padding="10")
        z_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        ttk.Label(z_frame, text="Altura segura:").grid(row=0, column=0, sticky=tk.W)
        ttk.Spinbox(z_frame, from_=0.1, to=50, increment=0.1, textvariable=self.z_safe, width=10, format="%.1f").grid(row=0, column=1, padx=(5, 20))
        ttk.Label(z_frame, text="Altura de dibujo:").grid(row=0, column=2, sticky=tk.W)
        ttk.Spinbox(z_frame, from_=0.0, to=10, increment=0.1, textvariable=self.z_draw, width=10, format="%.1f").grid(row=0, column=3, padx=(5, 0))
        speed_frame = ttk.LabelFrame(main_frame, text="Velocidades (mm/min)", padding="10")
        speed_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        ttk.Label(speed_frame, text="Dibujo:").grid(row=0, column=0, sticky=tk.W)
        ttk.Spinbox(speed_frame, from_=100, to=5000, textvariable=self.feed_rate, width=10).grid(row=0, column=1, padx=(5, 20))
        ttk.Label(speed_frame, text="Desplazamiento:").grid(row=0, column=2, sticky=tk.W)
        ttk.Spinbox(speed_frame, from_=500, to=10000, textvariable=self.travel_speed, width=10).grid(row=0, column=3, padx=(5, 0))
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=3, pady=(20, 0))
        ttk.Button(buttons_frame, text="Generar G-code", command=self.generate_gcode, style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(buttons_frame, text="Salir", command=self.root.quit).pack(side=tk.LEFT)
        log_frame = ttk.LabelFrame(main_frame, text="Estado", padding="10")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(20, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_message("¡Bienvenido al Generador Simple de G-code!\nSelecciona una imagen para comenzar.")
    def browse_input_file(self):
        filetypes = [
            ('Imágenes', '*.png *.jpg *.jpeg *.bmp *.tiff *.gif'),
            ('PNG', '*.png'),
            ('JPEG', '*.jpg *.jpeg'),
            ('Todos los archivos', '*.*')
        ]
        filename = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=filetypes, initialdir=os.getcwd())
        if filename:
            self.input_file.set(filename)
            self.log_message(f"Imagen seleccionada: {os.path.basename(filename)}")
            if not self.output_file.get():
                base_name = os.path.splitext(os.path.basename(filename))[0]
                output_name = f"{base_name}_simple.gcode"
                output_path = os.path.join(os.path.dirname(filename), output_name)
                self.output_file.set(output_path)
    def browse_output_file(self):
        filename = filedialog.asksaveasfilename(title="Guardar G-code como", defaultextension=".gcode", filetypes=[('G-code', '*.gcode *.nc *.tap'), ('Todos los archivos', '*.*')], initialdir=os.getcwd())
        if filename:
            self.output_file.set(filename)
            self.log_message(f"Archivo de salida: {os.path.basename(filename)}")
    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
    def validate_inputs(self):
        if not self.input_file.get():
            messagebox.showerror("Error", "Selecciona una imagen de entrada")
            return False
        if not self.output_file.get():
            messagebox.showerror("Error", "Especifica el archivo de salida")
            return False
        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("Error", "El archivo de imagen no existe")
            return False
        return True
    def generate_gcode_thread(self):
        try:
            generator = SimpleGCodeGenerator(
                canvas_width=self.canvas_width.get(),
                canvas_height=self.canvas_height.get(),
                z_safe=self.z_safe.get(),
                z_draw=self.z_draw.get(),
                feed_rate=self.feed_rate.get(),
                travel_speed=self.travel_speed.get()
            )
            self.log_message("Iniciando procesamiento...")
            self.log_message(f"Imagen: {os.path.basename(self.input_file.get())}")
            self.log_message(f"Canvas: {self.canvas_width.get()}x{self.canvas_height.get()}mm")
            self.log_message("Procesando imagen...")
            generator.process_image_to_gcode(self.input_file.get(), self.output_file.get())
            self.log_message("¡G-code generado exitosamente!")
            self.log_message(f"Archivo guardado: {os.path.basename(self.output_file.get())}")
            messagebox.showinfo("Éxito", f"G-code generado exitosamente!\n\nArchivo: {self.output_file.get()}")
        except Exception as e:
            error_msg = f"Error al generar G-code: {str(e)}"
            self.log_message(error_msg)
            messagebox.showerror("Error", error_msg)
        finally:
            self.generate_button.configure(state='normal', text='Generar G-code')
    def generate_gcode(self):
        if not self.validate_inputs():
            return
        self.generate_button = None
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Frame):
                        for button in child.winfo_children():
                            if isinstance(button, ttk.Button) and "Generar" in button['text']:
                                self.generate_button = button
                                break
        if self.generate_button:
            self.generate_button.configure(state='disabled', text='Procesando...')
        self.clear_log()
        thread = threading.Thread(target=self.generate_gcode_thread)
        thread.daemon = True
        thread.start()
def main():
    root = tk.Tk()
    style = ttk.Style()
    try:
        style.theme_use('winnative')
    except:
        style.theme_use('default')
    app = SimpleGCodeGeneratorGUI(root)
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.mainloop()
if __name__ == "__main__":
    main()
