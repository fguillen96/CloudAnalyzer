import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MyFrame(tk.LabelFrame):
    def disable_frame(self):
        def function(frame):
            for child in frame.winfo_children():
                wtype = child.winfo_class()
                if wtype not in ('Frame', 'Labelframe', 'TFrame', 'TLabelframe'):
                    child.configure(state='disable')
                else:
                    function(child)  # Función recursiva

        frame = self
        function(frame)

    def enable_frame(self):
        def function(frame):
            for child in frame.winfo_children():
                wtype = child.winfo_class()
                if wtype not in ('Frame', 'Labelframe', 'TFrame', 'TLabelframe'):
                    child.configure(state='normal')
                else:
                    function(child)  # Función recursiva

        frame = self
        function(frame)


class LoadCsvFrame(MyFrame):
    def __init__(self, master, controller):
        super().__init__(master, labelanchor='nw', text='Loading csv data')
        self.controller = controller

        # Variable de control para usar en etiqueta
        self.lbl_info_var = tk.StringVar(value='No csv detected')

        # Botón para cargar csv
        btn_load = ttk.Button(master=self, text="LOAD CSV FILE", command=self.controller.btn_load_pressed)

        # Etiqueta para mostrar info
        lbl_info = tk.Label(self, textvariable=self.lbl_info_var, wraplength=225)

        # Pack elements
        btn_load.pack(fill=tk.BOTH, padx=10, pady=10)        # Load button
        lbl_info.pack(padx=10, pady=10)                         # Info label


class AnalyzeFrame(MyFrame):
    def __init__(self, master, controller):
        super().__init__(master,  labelanchor='nw', text='Analyzing  Clouds',)
        self.controller = controller
        self.lbl_n_clouds_var = tk.StringVar(value='File not analyzed')
        self.__load_elements()

    def __load_elements(self):
        # Combobox para elegir umbral de irradiancia. Se pone dentro de un frame nuevo
        frame_lbl_irradiance = ttk.LabelFrame(self, labelanchor='nw', text='Irradiance Treshold (W/m2)')
        self.ent_irradiance_treshold = ttk.Combobox(master=frame_lbl_irradiance,
                                                    values=('100', '150', '200', '250',
                                                            '300', '350', '400', '450', '500'))
        self.ent_irradiance_treshold.pack(fill=tk.BOTH, padx=10, pady=10)

        # Combobox para elegir umbral de la derivada. Se pone dentro de un nuevo frame también
        frame_lbl_derivative = ttk.LabelFrame(self, labelanchor='nw', text='Derivative Treshold')
        self.ent_derivative_treshold = ttk.Combobox(master=frame_lbl_derivative,
                                                    values=('-4', '-5', '-6', '-7', '-8', '-9', '-10'))
        self.ent_derivative_treshold.pack(fill=tk.BOTH, padx=10, pady=10)

        frame_lbl_time = ttk.LabelFrame(self, labelanchor='nw', text='Time between clouds (ms)')
        var = tk.IntVar(value=500)
        self.ent_time_btw_clouds = ttk.Spinbox(master=frame_lbl_time, from_=500, to=5000,
                                               textvariable=var, increment=500)
        self.ent_time_btw_clouds.pack(fill=tk.BOTH, padx=10, pady=10)

        # Boton
        btn_analyze = ttk.Button(master=self, text="ANALYZE CLOUDS", command=self.controller.btn_analyze_pressed)

        # Etiqueta que muestra la informacion
        lbl_n_clouds = tk.Label(self, textvariable=self.lbl_n_clouds_var)

        # Pack elements
        frame_lbl_irradiance.pack(fill=tk.BOTH, padx=10, pady=10)
        frame_lbl_derivative.pack(fill=tk.BOTH, padx=10, pady=10)
        frame_lbl_time.pack(fill=tk.BOTH, padx=10, pady=10)
        btn_analyze.pack(fill=tk.BOTH, padx=10, pady=10)             # Analyze button (as attribute)
        lbl_n_clouds.pack(fill=tk.BOTH, padx=10, pady=10)             # Number of clouds label


class DataFrame(MyFrame):
    def __init__(self, master, controller):
        super().__init__(master,  labelanchor='nw', text='Showing Results')
        self.controller = controller
        self.lbl_export_info_var = tk.StringVar(value='')
        self.__load_elements()

    def __load_elements(self):
        # Etiqueta para mostrar info
        lbl_export_info = tk.Label(self, textvariable=self.lbl_export_info_var)

        # Botón exportar
        btn_export_clouds = ttk.Button(master=self, text="EXPORT CLOUDS CSV",
                                       command=self.controller.btn_export_pressed)

        # Botón plot clouds
        btn_plot_clouds = ttk.Button(master=self, text="PLOT CLOUDS", command=self.controller.btn_plot_clouds_pressed)

        # Pack elements
        btn_plot_clouds.pack(fill=tk.BOTH, padx=10, pady=10)         # Plot clouds button (as attribute)
        btn_export_clouds.pack(fill=tk.BOTH, padx=10, pady=10)       # Export button (as attribute)
        lbl_export_info.pack(fill=tk.BOTH, padx=10, pady=10)


class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.title("Cloud Analyzer")
        self.resizable(False, False)
        self.iconbitmap(resource_path('resources/cloud_ico.ico'))

        self.__load_elements()
        self.disable_frames()

    def __load_elements(self):
        # Image
        cloud_image = tk.PhotoImage(file=resource_path('resources/cloud2.png'))
        lbl_image = tk.Label(self, image=cloud_image, anchor="center")
        lbl_image.image = cloud_image

        # Program principal frames
        self.frame_load = LoadCsvFrame(self, self.controller)
        self.frame_analyze = AnalyzeFrame(self, self.controller)
        self.frame_data = DataFrame(self, self.controller)

        # ---------- PACK ELEMENTS ----------
        lbl_image.pack(padx=50, pady=10)                 # Image
        self.frame_load.pack(fill=tk.BOTH, padx=10, pady=10)
        self.frame_analyze.pack(fill=tk.BOTH, padx=10, pady=10)
        self.frame_data.pack(fill=tk.BOTH, padx=10, pady=10)

    def disable_frames(self):
        self.frame_analyze.disable_frame()
        self.frame_data.disable_frame()

    def csv_error(self):
        mb.showerror("Error", "Invalid csv file.")
