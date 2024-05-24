import matplotlib as mpl
import matplotlib.pyplot as plt


def general_temp(num_row, num_col, size_x, size_y):
    '''
    create a matplotlib figure;
    plt.subplots(num_row, num_col, figsize=(size_x, size_y))
    '''
    mpl.rcParams['mathtext.default'] = 'regular'
    fig, axs = plt.subplots(num_row, num_col, figsize=(size_x, size_y))
    fig.tight_layout(pad=3)
    if num_row*num_col != 1:
        axs = axs.ravel()
        for ax in axs:
            ax.tick_params(axis="both", direction='in', width=2, length=8.0, pad=6)
            plt.setp(ax.spines.values(), linewidth=2)
    else:
        axs.tick_params(axis="both", direction='in', width=2, length=8.0, pad=6)
        plt.setp(axs.spines.values(), linewidth=2)
    plt.rcParams['font.size'] = 18    