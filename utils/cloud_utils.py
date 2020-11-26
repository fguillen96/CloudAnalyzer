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
        self.data = pd.read_csv(data_path)
        if not {'Time', 't', 'G', 'T', 'V', 'C', 'F'}.issubset(self.data.columns):
            raise FileError("csv file invalid")
        else:
            self.sample_time_ms = self.data['t'][1] - self.data['t'][0]
            self.clouds = None  # Lista de nubes donde almacenarlas
            self.__irradiance_p = None
            self.__irradiance_smooth = None

    # --- BUSCAR NUBES ---
    #   -- Parametros
    #       irradiance_p -> derivada de la irradiancia
    #       tolerance -> Margen de tolerancia del valor de la derivada por debajo de 0 para detección de nube
    #       derivate_interval -> intervalo en ms cada el que se calcula la derivada
    #       todo
    #       samples_between_clouds -> Muestras entre dos nubes consecutivas para que sea considerada una sola
    #   
    #   -- Return -> lista de tuplas con inicio y final de cada nube

    def find_clouds_index(self, derivate_interval_ms, tolerance):
        self.clouds = []

        # La tolerancia va en valor absoluto
        tolerance = abs(tolerance)

        # Se filtra la señal primero. Aquí se podría poner un filtro u otro dependiendo de como se quiera filtrar
        self.__irradiance_smooth = smoother(self.data['G'])

        # Se le pasa a la derivada la señal filtrada, el intervalo cada el que se hace y el tiempo de muestreo
        self.__irradiance_p = derivate(self.__irradiance_smooth, derivate_interval_ms, self.sample_time_ms)

        # --- DETECCIÓN DE NUBES ---
        cloud_start = None
        cloud_end = None
        for i, val in enumerate(self.__irradiance_p):
            if val < (0 - tolerance) and cloud_start is None:
                cloud_start = i
            elif val > (0 - tolerance) and cloud_start is not None:
                cloud_end = i  # Creo que no estaría incluído porque ya es mayor que 0, ese punto no se incluye
                # Crear nube
                self.clouds.append((cloud_start, cloud_end))
                cloud_start = None

        return self.clouds

    def sort_clouds_g_decrease(self):
        # Aquí devolvemos una lista de nubes ordenada según la irradiancia
        # Ya se tiene la irradiancia filtrada ¿Hay que coger la fitlrada o la normal?

        # Array de 0 donde guardar los valores de irradiancia
        cloud_g_decrease = np.zeros(len(self.clouds))

        # Se guardan los valores de salto de irradiancia entre nubes (se supone que es siempre positivo así)
        for i, cloud in enumerate(self.clouds):
            cloud_g_decrease[i] = self.__irradiance_smooth[cloud[0]] - self.__irradiance_smooth[cloud[1]]

        # Queremos hacer una lista de nubes ordenada (como la del atributo y devolverla)
        # Para ordenar esa lista según el salto de irradiancia, hacemos lo siguiente
        # 1. Se une la lista de nubes con el valor del salto de irradiancia -> lista = [58, (0,5)]
        zip_list = zip(cloud_g_decrease, self.clouds)

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
        cloud_derivative_max = np.zeros(len(self.clouds))

        # Se guardan los valores de salto de irradiancia entre nubes (se supone que es siempre positivo así)
        for i, cloud in enumerate(self.clouds):
            cloud_derivative_max[i] = np.amin(self.__irradiance_p[cloud[0]:cloud[1]])

        # Queremos hacer una lista de nubes ordenada (como la del atributo y devolverla)
        # Para ordenar esa lista según el salto de irradiancia, hacemos lo siguiente
        # 1. Se une la lista de nubes con el valor del salto de irradiancia -> lista = [58, (0,5)]
        zip_list = zip(cloud_derivative_max, self.clouds)

        # 2. Se ordenan ahora según el valor del decremento de la irradiancia (de mayor a menor)
        #       Sorted coge el primer elemento de la lista, en este caso el valor de irradiancia
        sort_list = sorted(zip_list)

        # 3. Creamos una nueva lista ya ordenada sin el valor de irradiancia
        #       Esto es un poco raro, pero es así. El "_,i" significa que cogemos la parte a la derecha de la coma
        clouds_sort_max_derivative = [i for _, i in sort_list]

        return clouds_sort_max_derivative

    def get_cloud_info(self, cloud):

        cloud = {
            "Time": self.data['Time'][cloud[0]],
            "ms start": self.data['t'][cloud[0]],
            "Duration": self.data['t'][cloud[1]] - self.data['t'][cloud[0]],
            "Irradiance decrease": self.__irradiance_smooth[cloud[0]] - self.__irradiance_smooth[cloud[1]],
            "Max derivative value": np.amin(self.__irradiance_p[cloud[0]:cloud[1]])
        }
        return cloud

    def plot_clouds(self):
        # Vamos a dibujar todas las nubes que hemos recogido. La longitud de t debe ser igual a la de la derivada
        t = self.data['t']
        t = t[0:len(self.__irradiance_p)]

        # No sé bien como se comportan estas funciones. Por ahora funcionan bien pero me gustaria estudiarlas
        # todo
        fig, ax = plt.subplots()
        plt.plot(t, self.data['G'][0:len(t)])
        ax.twinx()
        plt.plot(t, self.__irradiance_p, 'g-')

        for cloud in self.clouds:
            plt.fill_between(t, self.__irradiance_p, where=(t >= t[cloud[0]]) & (t <= t[cloud[1]]))

        plt.show()

    def plot_frequency(self, cloud, ini, fin):
        i_ini, i_fin = self.__calculate_interval(cloud, ini, fin)

        # filtrado de la frecuencia en ese tramo
        f_smooth = smoother(self.data['F'][i_ini:i_fin])
        t = self.data['t'][i_ini:i_fin]

        plt.plot(t, f_smooth)
        plt.show()

    def plot_voltage(self, cloud, ini, fin):
        i_ini, i_fin = self.__calculate_interval(cloud, ini, fin)

        # filtrado de la frecuencia en ese tramo
        f_smooth = smoother(self.data['V'][i_ini:i_fin])
        t = self.data['t'][i_ini:i_fin]

        plt.plot(t, f_smooth)
        plt.show()

    def __get_sample_time(self):
        pass

    def __calculate_interval(self, cloud, ini, fin):
        ini = (ini * 1000) // self.sample_time_ms
        fin = (fin * 1000) // self.sample_time_ms

        i_ini = cloud[0] - ini
        i_fin = cloud[1] + fin

        if i_ini < 0:
            i_ini = 0

        if i_fin > len(self.data) - 1:
            i_fin = len(self.data) - 1

        return i_ini, i_fin
