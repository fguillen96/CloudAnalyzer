import numpy as np


def derivate(data, interval_ms, sample_time):
    # Calcular intervalo de muestras cada los que se hace la derivada
    interval_samples = interval_ms // sample_time

    # El array no va a ser un múltiplo de 50, hay que borrar muestras finales para quedarnos con eso.
    n_delete = (len(data) - 1) % interval_samples

    # Sabiendo el numero de muestras a eliminiar, las borramos del array
    data_array = np.delete(data, slice(len(data) - n_delete, len(data)))

    # dx será el incremento del eje x, en este caso el tiempo entre muestras (esto va en segundos)
    dx = interval_ms / 1000

    # Declaración de array de 0 para guardar los valores que se vayan calculando
    yp = np.zeros(len(data_array), dtype=float)

    # Según la definición de derivada
    for i in range(0, len(data_array), interval_samples):
        if i == 0:
            yp[i] = (data_array[i + interval_samples] - data_array[i]) / dx  # Derivada por el principio
        elif i == len(data_array) - 1:
            yp[i] = (data_array[i] - data_array[i - interval_samples]) / dx  # Derivada por el final
        else:
            yp[i] = (data_array[i + interval_samples] - data_array[i - interval_samples]) / (2 * dx)

        # Rellenar con el mismo valor los index intermedios para tener array de misma duracion
        if i < len(data_array) - 1:
            yp[i + 1:i + interval_samples] = yp[i]

    return yp


def derivate_one(data, dx):
    yp = np.zeros(len(data), dtype=float)
    # Según la definición de derivada
    for i in range(0, len(data)):
        if i == 0:
            yp[i] = (data[i + 1] - data[i]) / dx  # Derivada por el principio
        elif i == len(data) - 1:
            yp[i] = (data[i] - data[i - 1]) / dx  # Derivada por el final
        else:
            yp[i] = (data[i + 1] - data[i - 1]) / (2 * dx)

    return yp
