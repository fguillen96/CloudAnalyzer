from view import View
from model import Model
import csv
from tkinter.filedialog import askopenfilename, asksaveasfilename
from utils.cloud_utils import FileError


class Controller():
    def __init__(self):
        self.model = Model(self)    # initializes the model
        self.view = View(self)      # initializes the view
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

    def btn_export_pressed(self):
        cloud_list_info = self.model.get_clouds_info()
        filepath = asksaveasfilename(defaultextension="csv", filetypes=[("csv files", "*.csv"), ("All Files", "*.*")],)
        if filepath:
            with open(filepath, 'a', newline='') as f:
                fieldnames = cloud_list_info[0].keys()
                thewriter = csv.DictWriter(f, fieldnames=fieldnames)
                thewriter.writeheader()
                thewriter.writerows(cloud_list_info)
