import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import traceback
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
    element_pad = 5

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
        super().__init__(master)
        self.config(labelanchor='nw', text='Loading csv data', padx=self.element_pad, pady=self.element_pad)
        self.controller = controller

        # Variable de control para usar en etiqueta
        self.lbl_info_var = tk.StringVar(value="\nNo csv file selected\n")
        self. __load_elements()

    def __load_elements(self):
        # Botón para cargar csv
        btn_load = ttk.Button(master=self, text="LOAD CSV FILE", command=self.controller.btn_load_pressed)
        btn_load.pack(fill=tk.BOTH, padx=self.element_pad, pady=self.element_pad)

        # ----- FRAME PARA MOSTRAR INFO CSV -----
        frame_csv_info = ttk.LabelFrame(self, labelanchor='nw', text='File info', padding=self.element_pad)
        frame_csv_info.pack(fill=tk.BOTH, padx=self.element_pad, pady=self.element_pad)

        lbl_info = tk.Label(frame_csv_info, textvariable=self.lbl_info_var, width=20, anchor=tk.W, justify=tk.LEFT)
        lbl_info.pack(fill=tk.BOTH)


class AnalyzeFrame(MyFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.config(labelanchor='nw', text='Analyzing  Clouds', padx=self.element_pad, pady=self.element_pad)
        self.controller = controller
        self.lbl_n_clouds_var = tk.StringVar(value='File not analyzed')
        self.__load_elements()

    def __load_elements(self):
        # Combobox para elegir umbral de irradiancia. Se pone dentro de un frame nuevo
        frame_lbl_irradiance = ttk.LabelFrame(self, labelanchor='nw',
                                              text='Irradiance Treshold (W/m2)', padding=self.element_pad)
        self.ent_irradiance_treshold = ttk.Combobox(master=frame_lbl_irradiance,
                                                    values=('100', '150', '200', '250',
                                                            '300', '350', '400', '450', '500'))
        self.ent_irradiance_treshold.pack(fill=tk.BOTH, padx=self.element_pad, pady=self.element_pad)

        # Combobox para elegir umbral de la derivada. Se pone dentro de un nuevo frame también
        frame_lbl_derivative = ttk.LabelFrame(self, labelanchor='nw', text='Derivative Treshold', padding=5)
        self.ent_derivative_treshold = ttk.Combobox(master=frame_lbl_derivative,
                                                    values=('-4', '-5', '-6', '-7', '-8', '-9', '-10'))
        self.ent_derivative_treshold.pack(fill=tk.BOTH, padx=self.element_pad, pady=self.element_pad)

        frame_lbl_time = ttk.LabelFrame(self, labelanchor='nw', text='Time between clouds (ms)',
                                        padding=self.element_pad)
        var = tk.IntVar(value=500)
        self.ent_time_btw_clouds = ttk.Spinbox(master=frame_lbl_time, from_=500, to=5000,
                                               textvariable=var, increment=500)
        self.ent_time_btw_clouds.pack(fill=tk.BOTH, padx=self.element_pad, pady=self.element_pad)

        # Boton
        btn_analyze = ttk.Button(master=self, text="ANALYZE CLOUDS", command=self.controller.btn_analyze_pressed)

        # Etiqueta que muestra la informacion
        lbl_n_clouds = tk.Label(self, textvariable=self.lbl_n_clouds_var)

        # Pack elements
        frame_lbl_irradiance.pack(fill=tk.BOTH, pady=self.element_pad, padx=self.element_pad)
        frame_lbl_derivative.pack(fill=tk.BOTH, pady=self.element_pad, padx=self.element_pad)
        frame_lbl_time.pack(fill=tk.BOTH, pady=self.element_pad, padx=self.element_pad)
        btn_analyze.pack(fill=tk.BOTH, pady=self.element_pad, padx=self.element_pad)
        lbl_n_clouds.pack(fill=tk.BOTH, pady=self.element_pad, padx=self.element_pad)


class DataFrame(MyFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.config(labelanchor='nw', text='Showing Results', padx=self.element_pad, pady=self.element_pad)
        self.controller = controller
        self.__load_elements()

    def __load_elements(self):
        # Checkbutton para filtrado o no
        self.filter_var = tk.IntVar()
        filter_check = ttk.Checkbutton(master=self, text="Filter data", variable=self.filter_var)
        filter_check.pack(fill=tk.BOTH, padx=self.element_pad, pady=self.element_pad)

        # Botón plot clouds
        btn_plot_clouds = ttk.Button(master=self, text="PLOT CLOUDS", command=self.controller.btn_plot_clouds_pressed)
        btn_plot_clouds.pack(fill=tk.BOTH,  pady=self.element_pad, padx=self.element_pad)

        # Botón exportar
        btn_export_clouds = ttk.Button(master=self, text="EXPORT CLOUDS CSV",
                                       command=self.controller.btn_export_pressed)
        btn_export_clouds.pack(fill=tk.BOTH, pady=self.element_pad, padx=self.element_pad)

        # Etiqueta para mostrar info
        self.lbl_export_info_var = tk.StringVar(value='Data not exported')
        lbl_export_info = tk.Label(self, textvariable=self.lbl_export_info_var)
        lbl_export_info.pack(fill=tk.BOTH, pady=self.element_pad, padx=self.element_pad)


class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        tk.Tk.report_callback_exception = self.callback_error

        self.config(padx=10, pady=10)
        self.title("Clouds Analyzer")
        self.resizable(False, False)
        self.iconbitmap(resource_path('resources/cloud_ico.ico'))

        self.__load_elements()
        self.disable_frames()

    def __load_elements(self):
        # Image
        cloud_image = tk.PhotoImage(file=resource_path('resources/header.png'))
        lbl_image = tk.Label(self, image=cloud_image, anchor="center")
        lbl_image.image = cloud_image

        # Program principal frames
        self.frame_load = LoadCsvFrame(self, self.controller)
        self.frame_analyze = AnalyzeFrame(self, self.controller)
        self.frame_data = DataFrame(self, self.controller)

        padding = 5
        lbl_image.grid(row=0, column=0, columnspan=2, padx=padding, pady=padding)
        self.frame_load.grid(row=1, column=0, sticky=tk.N+tk.E+tk.S+tk.W, padx=padding, pady=padding)
        self.frame_data.grid(row=2, column=0, sticky=tk.N+tk.E+tk.S+tk.W, padx=padding, pady=padding)
        self.frame_analyze.grid(row=1, column=1, rowspan=2, sticky=tk.N+tk.E+tk.S+tk.W, padx=padding, pady=padding)

        tk.Label(text='Developed by Fran Guillén').grid(row=3, column=1, sticky=tk.E, padx=padding)

    def disable_frames(self):
        self.frame_analyze.disable_frame()
        self.frame_data.disable_frame()

    def csv_error(self):
        mb.showerror("Error", "Invalid csv file.\nFile must contain {'Time', 't', 'G', 'T', 'V', 'C', 'f'}")

    def options_error(self):
        mb.showerror("Error", "You must select a value!")
    
    def callback_error(self, *args):
        # Build the error message
        message = 'Generic error:\n\n'
        message += traceback.format_exc()
        mb.showerror('Error', message)

    
