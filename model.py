import pandas as pd
from utils.derivate_utils import derivate
from utils.filters import smoother
from matplotlib import pyplot as plt
import numpy as np


class FileError(Exception):
    pass


class DayModel:
    # Constructor de la clase. Se le pasa el path del archivo y el tiempo de muestreo
    def __init__(self, vc):
        # ----- INSTANCE VARIABLES -----
        # Controlador
        self.vc = vc

        # Datos en bruto que vienen del csv
        self.__data = None

        # Lista de tuplas. Cada tupla contienen index de inicio y final de nube
        self.__clouds_index_list = None

        # Otras variables necesarias para trabajar con ellas
        self.__irradiance_p = None          # Derivada de la irradiancia
        self.__irradiance_smooth = None     # Irradiancia filtrada
        self.__sample_time_ms = None        # Tiempo de muestreo

    def __reset(self):
        # Resetear todas las variables si se cambia el archivo
        self.__data = None
        self.__clouds_index_list = None
        self.__irradiance_p = None
        self.__irradiance_smooth = None
        self.__sample_time_ms = None

    def load_csv_data(self, filepath):
        self.__reset()
        self.__data = pd.read_csv(filepath)
        if not {'Time', 't', 'G', 'V', 'I', 'f'}.issubset(self.__data.columns):
            raise FileError("csv file invalid. Need {Time, t, G, V, I, f}")
        else:
            # Obtener el tiempo de muestreo del archivo
            self.__sample_time_ms = self.__data['t'][1] - self.__data['t'][0]
            self.__data['t'] = self.__data['t']-self.__data['t'][0]

    # --- BUSCAR NUBES ---
    #   -- Parametros
    #       irradiance_p -> derivada de la irradiancia
    #       derivative_treshold -> Margen de tolerancia del valor de la derivada por debajo de 0 para detección de nube
    #       derivate_interval -> intervalo en ms cada el que se calcula la derivada
    #       samples_between_clouds -> Muestras entre dos nubes consecutivas para que sea considerada una sola
    #
    #   -- Return -> lista de tuplas con inicio y final de cada nube
    def get_clouds_index(self, derivate_interval_ms, irradiance_treshold,  derivative_treshold, time_btw_clouds):
        self.__clouds_index_list = []

        # Se filtra la señal primero. Aquí se podría poner un filtro u otro dependiendo de como se quiera filtrar
        self.__irradiance_smooth = smoother(self.__data['G'])

        if derivate_interval_ms < self.__sample_time_ms:
            derivate_interval_ms = self.__sample_time_ms

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
                        self.__clouds_index_list.append((cloud_start, cloud_end))
                    cloud_start = None
                    cloud_end = None
                    state = 1

        # Devolvermos el numero de nubes que hemos encontrado
        return len(self.__clouds_index_list)

    # --- OBTENER MUESTRAS DE DATOS QUE FORMAN LAS NUBES ---
    #   -- Parametros
    #       NUNGUNO POR AHORA
    #   -- Return ->  Lista de DataFrame de pandas
    def get_clouds_samples(self, filter):
        clouds_index = self.__clouds_index_list  # Variable local para estar mas comodo
        clouds_samples = []

        # Se añade un tiempo por detrás para exportar las muestras. En segundos
        time_pre_post = 20

        samples_pre_post = (time_pre_post * 1000) // self.__sample_time_ms

        if filter:
            # Get keys
            keys = self.__data.keys()
            keys = np.delete(keys.values, [0, 1])

        for cloud_index in clouds_index:

            cloud_ini = cloud_index[0] - samples_pre_post
            if cloud_ini < 0:
                cloud_ini = 0

            cloud_end = cloud_index[1] + samples_pre_post
            if cloud_end >= len(self.__data):
                cloud_end = len(self.__data) - 1

            cloud_sample = self.__data.iloc[cloud_ini:cloud_end].copy()

            if filter:
                # Esto es para filtrar todas las muestras que no sean ni Time ni t
                for key in keys:
                    cloud_sample.loc[:, key] = smoother(cloud_sample.loc[:, key])

            clouds_samples.append(cloud_sample)

        return clouds_samples

    # --- OBTENER INFO DE TODAS LAS NUBES COMO LISTA DE DATAFRAMES DE PANDAS ---
    #   -- Parametros
    #       NUNGUNO POR AHORA
    #   -- Return ->  Lista de DataFrame de pandas
    def get_clouds_info(self, filter):
        cloud_list_info = []

        if filter:
            irradiance = self.__irradiance_smooth
        else:
            irradiance = self.__data['G']

        for i, cloud in enumerate(self.__clouds_index_list):

            irradiance_decrement = irradiance[cloud[0]] - irradiance[cloud[1]]
            cloud_duration = self.__data['t'][cloud[1]] - self.__data['t'][cloud[0]]

            level = pow(irradiance_decrement, 2) / (cloud_duration / 1000)

            cloud_dic = {
                "Cloud": i,
                "Time": self.__data['Time'][cloud[0]],
                "Start at": self.__data['t'][cloud[0]],
                "duration": cloud_duration,
                "sample_time": self.__sample_time_ms,
                "ΔG": irradiance_decrement,
                "dG/dt max": np.amin(self.__irradiance_p[cloud[0]:cloud[1]]),
                "Level": level
            }
            cloud_list_info.append(cloud_dic)
        return pd.DataFrame.from_records(cloud_list_info)

    def plot_clouds(self, filter):
        # Vamos a dibujar todas las nubes que hemos recogido. La longitud de t debe ser igual a la de la derivada
        t = self.__data['t']
        t = t[0:len(self.__irradiance_p)]

        if filter:
            irradiance = self.__irradiance_smooth[0:len(t)]
        else:
            irradiance = self.__data['G'][0:len(t)]

        fig, ax = plt.subplots()
        plt.plot(t, irradiance)
        ax.twinx()
        plt.plot(t, self.__irradiance_p, 'g-')

        for cloud in self.__clouds_index_list:
            plt.fill_between(t, self.__irradiance_p, where=(t >= t[cloud[0]]) & (t <= t[cloud[1]]))

        plt.show()

    def get_sample_time(self):
        return self.__sample_time_ms
