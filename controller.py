from view import View
from model import DayModel
from pandas import ExcelWriter
from tkinter.filedialog import askopenfilename, asksaveasfilename
from utils.cloud_utils import FileError
import ntpath


class Controller():
    def __init__(self):
        self.model = DayModel(self)    # initializes the model
        self.view = View(self)      # initializes the view
        self.view.mainloop()

    # ---------- EVENT HANDLERS ----------
    # Load button pressed. Open csv file
    def btn_load_pressed(self):
        filepath = askopenfilename(filetypes=[("Text Files", "*.csv"), ("All Files", "*.*")])
        filepath_error = "\nFile not selected\n"
        self.view.disable_frames()
        if not filepath:
            self.view.frame_load.lbl_info_var.set(filepath_error)
        else:

            try:
                self.model.load_csv_data(filepath)
            except FileError:
                self.view.csv_error()
                self.view.frame_load.lbl_info_var.set(filepath_error)
                return

            self.view.frame_analyze.enable_frame()
            file_name = ntpath.basename(filepath)
            sample_time = self.model.get_sample_time()

            string = "* File: " + file_name + "\n\n* Sample time (ms): " + str(sample_time)
            self.view.frame_load.lbl_info_var.set(string)

    # Analyze button pressed. Get number of clouds
    def btn_analyze_pressed(self):
        try:
            irradiance_treshold = int(self.view.frame_analyze.ent_irradiance_treshold.get())
            derivative_treshold = int(self.view.frame_analyze.ent_derivative_treshold.get())
            time_btw_clouds = int(self.view.frame_analyze.ent_time_btw_clouds.get())
            self.view.frame_analyze.lbl_n_clouds_var.set("Analyzing...")
            self.view.update_idletasks()
            n_clouds = self.model.get_clouds_index(500, irradiance_treshold, derivative_treshold, time_btw_clouds)
        except ValueError:
            self.view.options_error()
            self.view.frame_analyze.lbl_n_clouds_var.set("Error: Select options")
            return

        self.view.frame_analyze.lbl_n_clouds_var.set(str(n_clouds) + " clouds found")
        self.view.frame_data.enable_frame()

    def btn_plot_clouds_pressed(self):
        self.model.plot_clouds(self.view.frame_data.filter_var.get())

    def btn_export_pressed(self):
        clouds_info = self.model.get_clouds_info(self.view.frame_data.filter_var.get())
        clouds_samples = self.model.get_clouds_samples(self.view.frame_data.filter_var.get())
        filepath = asksaveasfilename(defaultextension="xlsx",
                                     filetypes=[("Excel files", "*.xlsx"), ("All Files", "*.*")])
        if filepath:
            self.view.frame_data.lbl_export_info_var.set("Exporting...")
            self.view.update_idletasks()
            with ExcelWriter(filepath) as writer:
                clouds_info.to_excel(writer, sheet_name='Main', index=False)
                for i, cloud_sample in enumerate(clouds_samples):
                    cloud_sample.to_excel(writer, sheet_name='Cloud ' + str(i), index=False)
            self.view.frame_data.lbl_export_info_var.set("Succesfully exported!")
        else:
            self.view.frame_data.lbl_export_info_var.set("Choose filepath!")
