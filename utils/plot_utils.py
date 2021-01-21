from matplotlib import pyplot as plt


# Para dibujar a partir de un diccionario con la variable y sus datos
def plot_pv_params(time, params):
    fig, ax = plt.subplots()  # Create a figure and an axes.
    for param, data in params.items():
        y = (data[1] * 100) / data[0]
        ax.plot(time, y, label=param)  # Plot some data on the axes.

    ax.set_xlabel('time')  # Add an x-label to the axes.
    ax.set_ylabel('%')  # Add a y-label to the axes.
    ax.set_title("Simple Plot")  # Add a title to the axes.
    ax.legend()  # Add a legend.
    plt.show()
