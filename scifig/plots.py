import matplotlib as mpl
import matplotlib.pyplot as plt


def general_temp(num_row, num_col, size_x, size_y):
    '''
    create a matplotlib figure;
    plt.subplots(num_row, num_col, figsize=(size_x, size_y))
    '''

    fig, axs = plt.subplots(num_row, num_col, figsize=(size_x, size_y))
    fig.tight_layout(pad=3)
    if num_row*num_col != 1:
        axs = axs.ravel()
        for ax in axs:
            ax.tick_params(axis="both", direction='in', width=2, length=8.0)
            plt.setp(ax.spines.values(), linewidth=2)
    else:
        axs.tick_params(axis="both", direction='in', width=2, length=8.0)
        plt.setp(axs.spines.values(), linewidth=2)

    plt.rcParams['font.family'] = "Arial"
    plt.rcParams['font.size'] = 18    
    mpl.rcParams['mathtext.default'] = 'regular'

    return fig, axs

def set_grid(ax, *args, **kwargs):
    ax.grid(which='major', ls='--', dashes=(5,5), lw=1, alpha=0.5, *args, **kwargs)

def set_legend(ax, *args, **kwargs):
    ax.legend(facecolor='white', framealpha=0.7, edgecolor='white', *args, **kwargs)

def set_label(ax, label, **kwargs):
    ax.text(-0.2, 1.05, label, transform=ax.transAxes, size=19, weight='bold', **kwargs)
