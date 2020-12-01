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


class View:
    def __init__(self, vc):
        self.vc = vc
        self.root = tk.Tk()
        self.root.title("Cloud Analyzer")
        self.root.iconbitmap(resource_path('resources\cloud_ico.ico'))

        # Control variables
        self.lbl_info_var = tk.StringVar(value='No csv detected')
        self.lbl_n_clouds_var = tk.StringVar(value='File not analyzed')
        self.lbl_export_info_var = tk.StringVar(value='')
        self.ent_check_button_var = tk.IntVar()  # Holds a boolean, returns 0 for False and 1 for True

        # Buttons to be controlled (necessary in init)
        self.__btn_analyze = tk.Button(master=self.root, text="ANALYZE CLOUDS",
                                       command=self.vc.btn_analyze_pressed, state="disabled")
        self.__btn_export_clouds = tk.Button(master=self.root, text="EXPORT CLOUDS CSV",
                                             command=self.vc.btn_export_pressed, state="disabled")

        self.__btn_plot_clouds = tk.Button(master=self.root, text="PLOT CLOUDS DATA",
                                           command=self.vc.btn_plot_clouds_pressed, state="disabled")

        # Create widgets
        self.__load_view()

    def __load_view(self):
        # ---------- CREATING ELEMENTS NOT NECESSARY AS ATTRIBUTES ----------
        # Image
        cloud_image = tk.PhotoImage(file=resource_path('resources\cloud2.png'))
        lbl_image = tk.Label(self.root, image=cloud_image, anchor="center")
        lbl_image.image = cloud_image

        # Separator
        sep_separator1 = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        sep_separator2 = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        sep_separator3 = ttk.Separator(self.root, orient=tk.HORIZONTAL)

        # Load csv button
        btn_load = tk.Button(master=self.root, text="LOAD CSV FILE", command=self.vc.btn_load_pressed)

        # Info label
        lbl_info = tk.Label(self.root, textvariable=self.lbl_info_var)

        # Label to show number of clouds
        lbl_n_clouds = tk.Label(self.root, textvariable=self.lbl_n_clouds_var)

        # Label to show exporting process
        lbl_export_info = tk.Label(self.root, textvariable=self.lbl_export_info_var)

        # ---------- PACK ELEMENTS ----------
        lbl_image.pack(padx=30, pady=10)                                    # Image
        sep_separator1.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)     # Separator
        btn_load.pack(fill=tk.BOTH, padx=10, pady=10)                       # Load button
        lbl_info.pack(fill=tk.BOTH, padx=10, pady=0, expand=False)          # Info label
        sep_separator2.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)     # Separator
        self.__btn_analyze.pack(fill=tk.BOTH, padx=10, pady=10)             # Analyze button (as attribute)
        lbl_n_clouds.pack(fill=tk.BOTH, padx=10, pady=0)                    # Number of clouds label
        sep_separator3.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)     # Separator
        self.__btn_plot_clouds.pack(fill=tk.BOTH, padx=10, pady=10)         # Plot clouds button (as attribute)
        self.__btn_export_clouds.pack(fill=tk.BOTH, padx=10, pady=10)       # Export button (as attribute)
        lbl_export_info.pack(fill=tk.BOTH, padx=10, pady=0)

    def disable_btn_analyze(self):
        self.__btn_analyze.config(state="disabled")

    def enable_btn_analyze(self):
        self.__btn_analyze.config(state="normal")

    def disable_btn_export_clouds(self):
        self.__btn_export_clouds.config(state="disabled")

    def enable_btn_export_clouds(self):
        self.__btn_export_clouds.config(state="normal")

    def disable_btn_plot_clouds(self):
        self.__btn_plot_clouds.config(state="disabled")

    def enable_btn_plot_clouds(self):
        self.__btn_plot_clouds.config(state="normal")

    def csv_error(self):
        mb.showerror("Error", "Invalid csv file.")
