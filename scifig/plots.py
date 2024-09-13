import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


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

def set_unique_legend(ax, *args, **kwargs):
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), facecolor='white', framealpha=0.7, edgecolor='white')

def number2letter(number, style=1):
    if style ==1 :
        if 1<= number <= 26:
            return chr(number + 64)
        else:
            raise ValueError("Number out of range. Please enter a number between 1 and 26.")
    elif style == 2:
        if 1<= number <= 26:
            return chr(number + 96)
        else:
            raise ValueError("Number out of range. Please enter a number between 1 and 26.")
    else:
        raise ValueError("Style out of range. Please enter a style of 1 or 2.")

def set_label(axs, starting=1, style=1, x=-0.2, y=1.05, **kwargs):
    if style == 1:
        for i, ax in enumerate(axs):
            label = number2letter(i+starting, style=1)
            ax.text(x, y, label, transform=ax.transAxes, size=19, weight='bold', **kwargs)
    elif style == 2:
        for i, ax in enumerate(axs):
            label = '('+number2letter(i+starting, style=2)+')'
            ax.text(x, y, label, transform=ax.transAxes, size=19, weight='bold', **kwargs)
    else:
        raise ValueError("Style out of range. Please enter a style of 1 or 2.")
    
def color_cycle(id):
    colors = {
        1 : '#1f77b4',
        2 : '#ff7f0e',
        3 : '#2ca02c',
        4 : '#d62728',
        5 : '#9467bd',
        6 : '#8c564b',
        7 : '#e377c2',
        8 : '#7f7f7f',
        9 : '#bcbd22',
        10: '#17becf',
    }
    return colors.get(id, '#000000')

def savefig(fig, filename):
    fig.savefig(filename, dpi=600, bbox_inches='tight')