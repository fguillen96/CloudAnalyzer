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
    def analyze(self):
        self.__cloud_list = []
        self.__cloud_list = self.__data.find_clouds(500, 4)
        self.vc.n_clouds_changed_delegate()

    def get_clouds_info(self):
        self.__cloud_list_info = []
        for cloud in self.__cloud_list:
            self.__cloud_list_info.append(self.__data.get_cloud_info(cloud))
        return self.__cloud_list_info

    # Setters and getters
    def get_n_clouds(self):
        return len(self.__cloud_list)