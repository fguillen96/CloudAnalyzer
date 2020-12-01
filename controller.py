from view import View
from model import Model
from pandas import ExcelWriter
import pandas as pd
from tkinter.filedialog import askopenfilename, asksaveasfilename
from utils.cloud_utils import FileError


class Controller():
    def __init__(self):
        self.model = Model(self)    # initializes the model
        self.view = View(self)      # initializes the view
        self.view.root.configure()
        self.view.root.mainloop()

    # ---------- EVENT HANDLERS ----------
    # Load button pressed. Open csv file
    def btn_load_pressed(self):
        self.view.disable_btn_analyze()
        self.view.disable_btn_export_clouds()

        filepath = askopenfilename(filetypes=[("Text Files", "*.csv"), ("All Files", "*.*")])
        if not filepath:
            self.view.lbl_info_var.set("No csv selected")
        else:
            self.view.lbl_n_clouds_var.set('File not analyzed')
            self.view.lbl_info_var.set(filepath)
            try:
                self.model.instanciate(filepath)
                self.view.enable_btn_analyze()
            except FileError:
                self.view.csv_error()

    # Analyze button pressed. Get number of clouds
    def btn_analyze_pressed(self):
        self.view.lbl_n_clouds_var.set("Analyzing...")
        self.view.root.update_idletasks()
        self.model.analyze()

    def n_clouds_changed_delegate(self):
        n_clouds = self.model.get_n_clouds()
        self.view.lbl_n_clouds_var.set(str(n_clouds) + " clouds found")
        self.view.enable_btn_export_clouds()
        self.view.enable_btn_plot_clouds()

    def btn_plot_clouds_pressed(self):
        self.model.plot_clouds()

    def btn_export_pressed(self):
        clouds_info = self.model.get_clouds_info()
        clouds_samples = self.model.get_clouds_samples()
        filepath = asksaveasfilename(defaultextension="xlsx",
                                     filetypes=[("Excel files", "*.xlsx"), ("All Files", "*.*")])
        if filepath:
            self.view.lbl_export_info_var.set("Exporting...")
            self.view.root.update_idletasks()
            with ExcelWriter(filepath) as writer:
                clouds_info.to_excel(writer, sheet_name='Main', index=False)
                for i, cloud_sample in enumerate(clouds_samples):
                    cloud_sample.to_excel(writer, sheet_name='Cloud ' + str(i), index=False)
            self.view.lbl_export_info_var.set("Succesfully exported!")
        else:
            self.view.lbl_export_info_var.set("Choose filepath!")
