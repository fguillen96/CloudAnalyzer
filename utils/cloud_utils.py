import pandas as pd
from utils.derivate_utils import derivate
from utils.filters import smoother
from matplotlib import pyplot as plt
import numpy as np


class FileError(Exception):
    pass


# Esta clase contiene todos los datos recogidos en el csv y metodos para calcular las nubes del dia y tal
class DayData:
    # Constructor de la clase. Se le pasa el path del archivo y el tiempo de muestreo
    def __init__(self, data_path):
        self.__data = pd.read_csv(data_path)
        if not {'Time', 't', 'G', 'T', 'V', 'C', 'F'}.issubset(self.__data.columns):
            raise FileError("csv file invalid")
        else:
            self.__sample_time_ms = self.__data['t'][1] - self.__data['t'][0]
            self.__clouds_index = None  # Lista de nubes donde almacenar los index dentro de los datos
            self.__irradiance_p = None
            self.__irradiance_smooth = None

    def get_raw_data(self):
        return self.__data

    # --- BUSCAR NUBES ---
    #   -- Parametros
    #       irradiance_p -> derivada de la irradiancia
    #       derivative_treshold -> Margen de tolerancia del valor de la derivada por debajo de 0 para detección de nube
    #       derivate_interval -> intervalo en ms cada el que se calcula la derivada
    #       samples_between_clouds -> Muestras entre dos nubes consecutivas para que sea considerada una sola
    #
    #   -- Return -> lista de tuplas con inicio y final de cada nube

    def find_clouds_index(self, derivate_interval_ms, irradiance_treshold,  derivative_treshold, time_btw_clouds):
        self.__clouds_index = []

        # Se filtra la señal primero. Aquí se podría poner un filtro u otro dependiendo de como se quiera filtrar
        self.__irradiance_smooth = smoother(self.__data['G'])

        # Se le pasa a la derivada la señal filtrada, el intervalo cada el que se hace y el tiempo de muestreo
        self.__irradiance_p = derivate(self.__irradiance_smooth, derivate_interval_ms, self.__sample_time_ms)

        # --- DETECCIÓN DE NUBES ---
        cloud_start = None      # Para guardar el index de inicio de nube
        cloud_end = None        # Para guardar el index de final de nube
        sample_counter = 0      # Contador de muestras
        state = 1
        samples_btw_clouds = time_btw_clouds // self.__sample_time_ms

        for i, val in enumerate(self.__irradiance_p):
            sample_counter += 1
            if state == 1:
                if val <= derivative_treshold and cloud_start is None:
                    cloud_start = i
                elif val > (-4) and cloud_start is not None:
                    cloud_end = i
                    state = 2
                    sample_counter = 0

            elif state == 2:
                if sample_counter <= samples_btw_clouds and val <= derivative_treshold:
                    state = 1
                elif sample_counter >= samples_btw_clouds:
                    irradiance_decrement = self.__irradiance_smooth[cloud_start] - self.__irradiance_smooth[cloud_end]
                    if (irradiance_decrement >= irradiance_treshold):
                        self.__clouds_index.append((cloud_start, cloud_end))
                    cloud_start = None
                    cloud_end = None
                    state = 1

        return self.__clouds_index

    # --- OBTENER MUESTRAS DE DATOS QUE FORMAN LAS NUBES ---
    #   -- Parametros
    #       NUNGUNO POR AHORA
    #   -- Return ->  Lista de DataFrame de pandas
    def get_clouds_samples(self):
        clouds_index = self.__clouds_index  # Variable local para estar mas comodo
        clouds_samples = []

        # Get keys
        keys = self.__data.keys()
        keys = np.delete(keys.values, [0, 1])

        for cloud_index in clouds_index:
            cloud_sample = self.__data.iloc[cloud_index[0]:cloud_index[1]].copy()
            for key in keys:
                cloud_sample.loc[:, key] = smoother(cloud_sample.loc[:, key])

            clouds_samples.append(cloud_sample)

        return clouds_samples

    def get_cloud_info(self, cloud):

        cloud = {
            "Time": self.__data['Time'][cloud[0]],
            "ms start": self.__data['t'][cloud[0]],
            "ms total": self.__data['t'][cloud[1]] - self.__data['t'][cloud[0]],
            "ms sampl": self.__sample_time_ms,
            "ΔG": self.__irradiance_smooth[cloud[0]] - self.__irradiance_smooth[cloud[1]],
            "dG/dt mx": np.amin(self.__irradiance_p[cloud[0]:cloud[1]])
        }
        return cloud

    # --- OBTENER INFO DE TODAS LAS NUBES COMO LISTA DE DATAFRAMES DE PANDAS ---
    #   -- Parametros
    #       NUNGUNO POR AHORA
    #   -- Return ->  Lista de DataFrame de pandas
    def get_clouds_info(self):
        cloud_list_info = []
        for i, cloud in enumerate(self.__clouds_index):
            cloud_dic = {"Cloud": i}
            cloud_info = self.get_cloud_info(cloud)
            cloud_dic.update(cloud_info)
            cloud_list_info.append(cloud_dic)
        return pd.DataFrame.from_records(cloud_list_info)

    def plot_clouds(self):
        # Vamos a dibujar todas las nubes que hemos recogido. La longitud de t debe ser igual a la de la derivada
        t = self.__data['t']
        t = t[0:len(self.__irradiance_p)]

        # No sé bien como se comportan estas funciones. Por ahora funcionan bien pero me gustaria estudiarlas
        # todo
        fig, ax = plt.subplots()
        plt.plot(t, self.__irradiance_smooth[0:len(t)])
        ax.twinx()
        plt.plot(t, self.__irradiance_p, 'g-')

        for cloud in self.__clouds_index:
            plt.fill_between(t, self.__irradiance_p, where=(t >= t[cloud[0]]) & (t <= t[cloud[1]]))

        plt.show()

    def sort_clouds_g_decrease(self):
        # Aquí devolvemos una lista de nubes ordenada según la irradiancia
        # Ya se tiene la irradiancia filtrada ¿Hay que coger la fitlrada o la normal?

        # Array de 0 donde guardar los valores de irradiancia
        cloud_g_decrease = np.zeros(len(self.__clouds_index))

        # Se guardan los valores de salto de irradiancia entre nubes (se supone que es siempre positivo así)
        for i, cloud in enumerate(self.__clouds_index):
            cloud_g_decrease[i] = self.__irradiance_smooth[cloud[0]] - self.__irradiance_smooth[cloud[1]]

        # Queremos hacer una lista de nubes ordenada (como la del atributo y devolverla)
        # Para ordenar esa lista según el salto de irradiancia, hacemos lo siguiente
        # 1. Se une la lista de nubes con el valor del salto de irradiancia -> lista = [58, (0,5)]
        zip_list = zip(cloud_g_decrease, self.__clouds_index)

        # 2. Se ordenan ahora según el valor del decremento de la irradiancia (de mayor a menor)
        #       Sorted coge el primer elemento de la lista, en este caso el valor de irradiancia
        sort_list = sorted(zip_list, reverse=True)

        # 3. Creamos una nueva lista ya ordenada sin el valor de irradiancia
        #       Esto es un poco raro, pero es así. El "_,i" significa que cogemos la parte a la derecha de la coma
        clouds_sort_g_decrease = [i for _, i in sort_list]

        return clouds_sort_g_decrease

    def sort_clouds_max_derivative(self):
        # Aquí devolvemos una lista de nubes ordenada según la irradiancia
        # Ya se tiene la irradiancia filtrada ¿Hay que coger la fitlrada o la normal?

        # Array de 0 donde guardar los valores de irradiancia
        cloud_derivative_max = np.zeros(len(self.__clouds_index))

        # Se guardan los valores de salto de irradiancia entre nubes (se supone que es siempre positivo así)
        for i, cloud in enumerate(self.__clouds_index):
            cloud_derivative_max[i] = np.amin(self.__irradiance_p[cloud[0]:cloud[1]])

        # Queremos hacer una lista de nubes ordenada (como la del atributo y devolverla)
        # Para ordenar esa lista según el salto de irradiancia, hacemos lo siguiente
        # 1. Se une la lista de nubes con el valor del salto de irradiancia -> lista = [58, (0,5)]
        zip_list = zip(cloud_derivative_max, self.__clouds_index)

        # 2. Se ordenan ahora según el valor del decremento de la irradiancia (de mayor a menor)
        #       Sorted coge el primer elemento de la lista, en este caso el valor de irradiancia
        sort_list = sorted(zip_list)

        # 3. Creamos una nueva lista ya ordenada sin el valor de irradiancia
        #       Esto es un poco raro, pero es así. El "_,i" significa que cogemos la parte a la derecha de la coma
        clouds_sort_max_derivative = [i for _, i in sort_list]

        return clouds_sort_max_derivative

    def plot_frequency(self, cloud, ini, fin):
        i_ini, i_fin = self.__calculate_interval(cloud, ini, fin)

        # filtrado de la frecuencia en ese tramo
        f_smooth = smoother(self.__data['F'][i_ini:i_fin])
        t = self.__data['t'][i_ini:i_fin]

        plt.plot(t, f_smooth)
        plt.show()

    def plot_voltage(self, cloud, ini, fin):
        i_ini, i_fin = self.__calculate_interval(cloud, ini, fin)

        # filtrado de la frecuencia en ese tramo
        f_smooth = smoother(self.__data['V'][i_ini:i_fin])
        t = self.__data['t'][i_ini:i_fin]

        plt.plot(t, f_smooth)
        plt.show()

    def __calculate_interval(self, cloud, ini, fin):
        ini = (ini * 1000) // self.__sample_time_ms
        fin = (fin * 1000) // self.__sample_time_ms

        i_ini = cloud[0] - ini
        i_fin = cloud[1] + fin

        if i_ini < 0:
            i_ini = 0

        if i_fin > len(self.__data) - 1:
            i_fin = len(self.__data) - 1

        return i_ini, i_fin
