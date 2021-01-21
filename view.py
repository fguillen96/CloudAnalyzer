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

        self.ent_time_btw_clouds = ttk.Spinbox(master=frame_lbl_time, from_=500, to=5000, increment=500)
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


class PllotData(MyFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.config(labelanchor='nw', text='Plot some data?', padx=self.element_pad, pady=self.element_pad)
        self.controller = controller
        self.__load_elements()

    def __load_elements(self):
        # Frame para meter todos los checkbox
        frame_lbl_vars = ttk.LabelFrame(self, labelanchor='nw', text='Vars', padding=self.element_pad)

        # Irradiance checkbox and spinbox
        self.irradiance_var = tk.IntVar()

        irradiance_check = ttk.Checkbutton(master=frame_lbl_vars, text="Irradiance", variable=self.irradiance_var)
        self.irradiance_max = tk.Spinbox(master=frame_lbl_vars, increment=100,
                                         textvariable=tk.IntVar(value=1164), width=5, from_=100, to=1164)
        irradiance_check.grid(row=0, column=0, padx=self.element_pad, pady=self.element_pad, sticky=tk.W)
        self.irradiance_max.grid(row=0, column=1, padx=self.element_pad, pady=self.element_pad, sticky=tk.W)

        # Temperature checkbox and spinbox
        self.celltemp_var = tk.IntVar()
        celltemp_check = ttk.Checkbutton(master=frame_lbl_vars, text="Temp", variable=self.celltemp_var)
        self.celltemp_max = tk.Spinbox(master=frame_lbl_vars, increment=10,
                                       textvariable=tk.IntVar(value=100), width=5)
        celltemp_check.grid(row=1, column=0, padx=self.element_pad, pady=self.element_pad, sticky=tk.W)
        self.celltemp_max.grid(row=1, column=1, padx=self.element_pad, pady=self.element_pad, sticky=tk.W)

        # voltage checkbox and spinbox
        self.voltage_var = tk.IntVar()
        voltage_check = ttk.Checkbutton(master=frame_lbl_vars, text="Voltage", variable=self.voltage_var)
        self.voltage_max = tk.Spinbox(master=frame_lbl_vars, increment=10,
                                      textvariable=tk.IntVar(value=500), width=5, from_=100, to=500)

        voltage_check.grid(row=2, column=0, padx=self.element_pad, pady=self.element_pad, sticky=tk.W)
        self.voltage_max.grid(row=2, column=1, padx=self.element_pad, pady=self.element_pad, sticky=tk.W)

        # Checkbutton para I
        self.current_var = tk.IntVar()
        current_check = ttk.Checkbutton(master=frame_lbl_vars, text="Current", variable=self.current_var)
        self.current_max = tk.Spinbox(master=frame_lbl_vars, increment=1,
                                      textvariable=tk.IntVar(value=5), width=5, from_=1, to=100)
        current_check.grid(row=3, column=0, padx=self.element_pad, pady=self.element_pad, sticky=tk.W)
        self.current_max.grid(row=3, column=1, padx=self.element_pad, pady=self.element_pad, sticky=tk.W)

        # Checkbutton para P
        self.power_var = tk.IntVar()
        power_check = ttk.Checkbutton(master=frame_lbl_vars, text="Power", variable=self.power_var)
        self.power_max = tk.Spinbox(master=frame_lbl_vars, increment=10,
                                    textvariable=tk.IntVar(value=1000), width=5, from_=1, to=1000)
       
        power_check.grid(row=4, column=0, padx=self.element_pad, pady=self.element_pad, sticky=tk.W)
        self.power_max.grid(row=4, column=1, padx=self.element_pad, pady=self.element_pad, sticky=tk.W)

        # Checkbutton para F
        self.frequency_var = tk.IntVar()
        frequency_check = ttk.Checkbutton(master=frame_lbl_vars, text="Frequency", variable=self.frequency_var)
        self.frequency_max = tk.Spinbox(master=frame_lbl_vars, increment=5,
                                    textvariable=tk.IntVar(value=50), width=5, from_=1, to=50)
        frequency_check.grid(row=5, column=0, padx=self.element_pad, pady=self.element_pad, sticky=tk.W)
        self.frequency_max.grid(row=5, column=1, padx=self.element_pad, pady=self.element_pad, sticky=tk.W)

        # Pack
        frame_lbl_vars.pack(fill=tk.BOTH, pady=self.element_pad, padx=self.element_pad)

        # Plot button
        btn_plot = ttk.Button(master=self, text="PLOT DATA", command=self.controller.btn_plot_pressed)
        btn_plot.pack(fill=tk.BOTH, padx=self.element_pad, pady=self.element_pad)


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
        self.frame_plot = PllotData(self, self.controller)

        padding = 5
        lbl_image.grid(row=0, column=0, columnspan=3, padx=padding, pady=padding)
        self.frame_load.grid(row=1, column=0, sticky=tk.N+tk.E+tk.S+tk.W, padx=padding, pady=padding)
        self.frame_data.grid(row=2, column=0, sticky=tk.N+tk.E+tk.S+tk.W, padx=padding, pady=padding)
        self.frame_analyze.grid(row=1, column=1, rowspan=2, sticky=tk.N+tk.E+tk.S+tk.W, padx=padding, pady=padding)
        self.frame_plot.grid(row=1, column=2, rowspan=2, sticky=tk.N+tk.E+tk.S+tk.W, padx=padding, pady=padding)

        tk.Label(text='Developed by Fran Guillén').grid(row=3, column=2, sticky=tk.E, padx=padding)

    def disable_frames(self):
        self.frame_analyze.disable_frame()
        self.frame_data.disable_frame()
        self.frame_plot.disable_frame()

    def csv_error(self):
        mb.showerror("Error", "Invalid csv file.\nFile must contain {'Time', 't', 'G', 'T', 'V', 'C', 'f'}")

    def options_error(self):
        mb.showerror("Error", "You must select a value!")

    def callback_error(self, *args):
        # Build the error message
        message = 'Generic error:\n\n'
        message += traceback.format_exc()
        mb.showerror('Error', message)
