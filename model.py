from utils.cloud_utils import DayData


class Model():
    def __init__(self, vc):
        self.vc = vc
        self.__data = None
        self.__cloud_list = None
        self.__cloud_list_info = None

    def instanciate(self, filepath):
        self.__data = DayData(filepath)

    # Send data to controller again
    def analyze_clouds(self, irradiance_treshold, derivative_treshold, time_btw_clouds):
        self.__cloud_list = []
        self.__cloud_list = self.__data.find_clouds_index(500, irradiance_treshold,
                                                          derivative_treshold, time_btw_clouds)
        return len(self.__cloud_list)

    def plot_clouds(self):
        self.__data.plot_clouds()

    def get_clouds_info(self):
        return self.__data.get_clouds_info()

    def get_clouds_samples(self):
        return self.__data.get_clouds_samples()
