from scipy.signal import lfilter
from tsmoothie.smoother import ConvolutionSmoother


def irr_filter(data):
    n = 1000  # the larger n is, the smoother curve will be. Esto lo cambiaremos y se pondrá como parámetro
    b = [1.0 / n] * n
    a = 1
    return lfilter(b, a, data)  # <- Esta variable la guardamos bien


def smoother(data):
    # SUAVIZADO SIN USAR FILTROS
    smoother = ConvolutionSmoother(window_len=30, window_type='ones')
    smoother.smooth(data)

    # Generate intervals
    low, up = smoother.get_intervals('sigma_interval', n_sigma=3)  # Esto no se que hace. Próximamente...

    # Se obtienen dos variables que no entiendo bien que cojones son
    return smoother.smooth_data[0]  # <- Aquí es donde está la magia, la otra variable
