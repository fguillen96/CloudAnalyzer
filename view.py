import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb


class View:
    def __init__(self, vc):
        self.vc = vc
        self.root = tk.Tk()
        self.root.title("Cloud Analyzer")
        self.root.iconbitmap('resources/cloud_ico.ico')

        # Control variables
        self.lbl_info_var = tk.StringVar(value='No csv detected')
        self.lbl_n_clouds_var = tk.StringVar(value='File not analyzed')

        # Buttons to be controlled (necessary in init)
        self.__btn_analyze = tk.Button(master=self.root, text="ANALYZE CLOUDS",
                                       command=self.vc.btn_analyze_pressed, state="disabled")
        self.__btn_export_clouds = tk.Button(master=self.root, text="EXPORT CLOUDS CSV",
                                             command=self.vc.btn_export_pressed, state="disabled")

        # Create widgets
        self.__load_view()

    def __load_view(self):
        # ---------- CREATING ELEMENTS NOT NECESSARY AS ATTRIBUTES ----------
        # Imagen
        cloud_image = tk.PhotoImage(file='resources/cloud2.png')
        lbl_image = tk.Label(self.root, image=cloud_image, anchor="center")
        lbl_image.image = cloud_image

        # Separator
        sep_separator1 = ttk.Separator(self.root, orient=tk.HORIZONTAL)

        # Load csv button
        btn_load = tk.Button(master=self.root, text="LOAD CSV FILE", command=self.vc.btn_load_pressed)

        # Info label
        lbl_info = tk.Label(self.root, textvariable=self.lbl_info_var)

        # Label to show number of clouds
        lbl_n_clouds = tk.Label(self.root, textvariable=self.lbl_n_clouds_var)

        # ---------- PACK ELEMENTS ----------
        lbl_image.pack(padx=30, pady=10)                                # Image
        sep_separator1.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)  # Separator
        btn_load.pack(fill=tk.BOTH, padx=10, pady=10)                   # Load button
        lbl_info.pack(fill=tk.BOTH, padx=10, pady=0, expand=False)      # Info label
        self.__btn_analyze.pack(fill=tk.BOTH, padx=10, pady=10)         # Analyze button (as attribute)
        lbl_n_clouds.pack(fill=tk.BOTH, padx=10, pady=0)                # Number of clouds label
        self.__btn_export_clouds.pack(fill=tk.BOTH, padx=10, pady=10)   # Export button (as attribute)

    def disable_btn_analyze(self):
        self.__btn_analyze.config(state="disabled")

    def enable_btn_analyze(self):
        self.__btn_analyze.config(state="normal")

    def disable_btn_export_clouds(self):
        self.__btn_export_clouds.config(state="disabled")

    def enable_btn_export_clouds(self):
        self.__btn_export_clouds.config(state="normal")

    def csv_error(self):
        mb.showerror("Error", "Invalid csv file.")
