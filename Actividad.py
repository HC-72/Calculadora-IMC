import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
from PIL import Image, ImageTk
import pandas as pd
import uuid
import matplotlib.pyplot as plt

class SMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("(SMI)")
        self.root.geometry("950x750")
        self.create_widgets()

    def create_widgets(self):
        # Crear canvas para la imagen de fondo
        self.canvas = tk.Canvas(self.root, width=950, height=750)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Ruta de la imagen de fondo
        image_path = r"C:/Users/isley/Documents/6VSC2/tona/fondo.PNG"

        try:
            # Cargar y mostrar la imagen de fondo
            self.bg_image = Image.open(image_path)
            self.bg_image = self.bg_image.resize((950, 750), Image.LANCZOS)  # Ajusta el tamaño aquí
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen de fondo. Error: {e}")

        # Crear un frame para contener otros widgets
        self.frame = ttk.Frame(self.canvas, padding="20 20 20 20")
        self.frame.place(relwidth=1, relheight=1)

        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", font=("Helvetica", 12))
        style.configure("TButton", font=("Helvetica", 12))
        style.configure("TEntry", padding=5)
        style.configure("TCombobox", padding=5)

        # Crear etiquetas y entradas
        labels = ["Nombre", "Apellido Paterno", "Apellido Materno", "Peso (kg)", "Altura (m)", "Edad", "Sexo"]
        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(self.frame, text=f"{label}:").grid(column=0, row=i, padx=10, pady=5, sticky="W")
            if label == "Sexo":
                self.entries[label] = ttk.Combobox(self.frame, values=["M", "F"], state="readonly")
            else:
                self.entries[label] = ttk.Entry(self.frame)
            self.entries[label].grid(column=1, row=i, padx=10, pady=5)

        # Crear botones
        buttons_frame = ttk.Frame(self.frame)
        buttons_frame.grid(column=0, row=len(labels), columnspan=2, pady=10)

        ttk.Button(buttons_frame, text="Calcular", command=self.calcular_smi).grid(column=0, row=0, padx=5)
        ttk.Button(buttons_frame, text="Guardar CSV", command=self.guardar_resultados_csv).grid(column=1, row=0, padx=5)
        ttk.Button(buttons_frame, text="Guardar Excel", command=self.guardar_resultados_excel).grid(column=2, row=0, padx=5)
        ttk.Button(buttons_frame, text="Guardar PDF", command=self.guardar_resultados_pdf).grid(column=3, row=0, padx=5)
        ttk.Button(buttons_frame, text="Cargar", command=self.cargar_resultados).grid(column=4, row=0, padx=5)
        ttk.Button(buttons_frame, text="Borrar Fila", command=self.borrar_fila).grid(column=5, row=0, padx=5)
        ttk.Button(buttons_frame, text="Modificar Fila", command=self.modificar_fila).grid(column=6, row=0, padx=5)
        ttk.Button(self.frame, text="Limpiar Campos", command=self.limpiar_campos).grid(column=1, row=len(labels) + 1, padx=10, pady=5)

        # Crear tabla de resultados
        columns = ["ID", "Nombre", "Apellido Paterno", "Apellido Materno", "Peso", "Altura", "Edad", "Sexo", "SMI"]
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.grid(column=0, row=len(labels) + 2, columnspan=2, padx=10, pady=5)

    def generate_id(self):
        return str(uuid.uuid4())

    def calcular_smi(self):
        try:
            data = {label: entry.get() for label, entry in self.entries.items()}
            data["Peso"] = float(data["Peso (kg)"])
            data["Altura"] = float(data["Altura (m)"])
            data["Edad"] = int(data["Edad"])
            if data["Peso"] <= 0 or data["Altura"] <= 0 or data["Edad"] <= 0:
                raise ValueError

            data["ID"] = self.generate_id()
            data["SMI"] = data["Peso"] / (data["Altura"] ** 2)
            self.tree.insert("", "end", values=[data[label] for label in ["ID", "Nombre", "Apellido Paterno", "Apellido Materno", "Peso", "Altura", "Edad", "Sexo", "SMI"]])
            messagebox.showinfo("Éxito", "El cálculo del SMI se ha realizado correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos.")

    def limpiar_campos(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def guardar_resultados_csv(self):
        save_path = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if save_path:
            data = [self.tree.item(row_id)['values'] for row_id in self.tree.get_children()]
            df = pd.DataFrame(data, columns=["ID", "Nombre", "Apellido Paterno", "Apellido Materno", "Peso (kg)", "Altura (m)", "Edad", "Sexo", "SMI"])
            df.to_csv(save_path, index=False)
            messagebox.showinfo("Éxito", "Los resultados se han guardado correctamente en CSV.")

    def guardar_resultados_excel(self):
        save_path = asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        if save_path:
            data = [self.tree.item(row_id)['values'] for row_id in self.tree.get_children()]
            df = pd.DataFrame(data, columns=["ID", "Nombre", "Apellido Paterno", "Apellido Materno", "Peso (kg)", "Altura (m)", "Edad", "Sexo", "SMI"])
            df.to_excel(save_path, index=False)
            messagebox.showinfo("Éxito", "Los resultados se han guardado correctamente en Excel.")

    def guardar_resultados_pdf(self):
        save_path = asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if save_path:
            data = [self.tree.item(row_id)['values'] for row_id in self.tree.get_children()]
            df = pd.DataFrame(data, columns=["ID", "Nombre", "Apellido Paterno", "Apellido Materno", "Peso (kg)", "Altura (m)", "Edad", "Sexo", "SMI"])

            # Crear figura y graficar
            fig, ax = plt.subplots()
            ax.axis('tight')
            ax.axis('off')
            the_table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
            
            fig.savefig(save_path, bbox_inches='tight')
            messagebox.showinfo("Éxito", "Los resultados se han guardado correctamente en PDF.")

    def cargar_resultados(self):
        file_path = askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            df = pd.read_csv(file_path)
            for row in df.itertuples(index=False):
                self.tree.insert("", "end", values=row)
            messagebox.showinfo("Éxito", "Los resultados se han cargado correctamente.")

    def borrar_fila(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)

    def modificar_fila(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una fila para modificar.")
            return

        item_values = self.tree.item(selected_item)["values"]
        if not item_values:
            messagebox.showwarning("Advertencia", "No hay datos disponibles para modificar.")
            return

        for i, label in enumerate(["Nombre", "Apellido Paterno", "Apellido Materno", "Peso (kg)", "Altura (m)", "Edad", "Sexo"]):
            if i < len(item_values):
                self.entries[label].delete(0, tk.END)
                self.entries[label].insert(0, item_values[i + 1])  # Saltar el ID (índice 0)
        
        self.entries["Nombre"].focus()

    def guardar_cambios(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una fila para guardar los cambios.")
            return

        data = {label: entry.get() for label, entry in self.entries.items()}
        try:
            data["Peso (kg)"] = float(data["Peso (kg)"])
            data["Altura (m)"] = float(data["Altura (m)"])
            data["Edad"] = int(data["Edad"])
            if data["Peso (kg)"] <= 0 or data["Altura (m)"] <= 0 or data["Edad"] <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores válidos.")
            return

        data["ID"] = self.tree.item(selected_item)["values"][0]  # Mantener el ID original
        data["SMI"] = data["Peso (kg)"] / (data["Altura (m)"] ** 2)
        self.tree.delete(selected_item)
        self.tree.insert("", "end", values=[data[label] for label in ["ID", "Nombre", "Apellido Paterno", "Apellido Materno", "Peso (kg)", "Altura (m)", "Edad", "Sexo", "SMI"]])
        messagebox.showinfo("Éxito", "Los cambios se han guardado correctamente.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SMICalculator(root)
    root.mainloop()

