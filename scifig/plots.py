import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from scipy.ndimage import rotate
import matplotlib.image as mimg
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

    plt.rcParams['lines.linewidth'] = 2.0
    plt.rcParams['scatter.marker'] = 'o'
    plt.rcParams['lines.markersize'] = 6

    return fig, axs

def set_grid(ax, *args, **kwargs):
    ax.grid(which='major', ls='--', dashes=(5,5), lw=1, alpha=0.5, *args, **kwargs)

def set_legend(ax, *args, **kwargs):
    ax.legend(facecolor='white', framealpha=0.7, edgecolor='white', *args, **kwargs)

## merge the enties with same name and reorder
#  order is the list of entries you expect, like ['line A', 'line B', 'line C'] 
def merge_legend(ax, order=None, *args, **kwargs):
    handles, labels = ax.get_legend_handles_labels()
    unique = dict(zip(labels, handles))  # Remove duplicate labels
    if order is None:
        ax.legend(unique.values(), unique.keys(), facecolor='white', framealpha=0.7, edgecolor='white', *args, **kwargs)  # Set unique legend
    else:
        ordered_handels = [unique[label] for label in order]
        ordered_labels = [label for label in order]
        ax.legend(ordered_handels, ordered_labels, facecolor='white', framealpha=0.7, edgecolor='white', *args, **kwargs)

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
            label = '(' + number2letter(i+starting, style=2) + ')'
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


def insert_image(ax, image_path, x, y, zoom=1.0, rotation=0):
    """
    Insert an image into a matplotlib axis.
    
    Parameters:
    - ax: The axis to insert the image into.
    - image_path: Path to the image file.
    - x,y: Coordinates in the axis where the image will be placed.
    - rotate: Angle to rotate the image (default is 0).
    - zoom: Zoom factor for the image (default is 1.0).
    """

    img = mimg.imread(image_path)
    img = rotate(img, rotation)  # Rotate the image if needed
    imagebox = OffsetImage(img, zoom=zoom)
    ab = AnnotationBbox(imagebox, (x, y), frameon=False)
    ax.add_artist(ab)


def break_axis(ax, axis='y', break_ranges=None, 
               height_ratios=None, width_ratios=None):
    """
    Break an existing axis into multiple panels.
    
    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        The axis to break (will be replaced)
    axis : str, default='y'
        Which axis to break ('x' or 'y')
    break_ranges : list of tuples
        Ranges to display, e.g., [(0, 10), (50, 60)] creates a break between 10 and 50
    height_ratios : list, optional
        Height ratios for y-axis breaks (auto-calculated if None)
    width_ratios : list, optional
        Width ratios for x-axis breaks (auto-calculated if None)
    
    Returns:
    --------
    axes : list
        List of new subplot axes that replace the original
    
    Example:
    --------
    # Break existing y-axis
    fig, ax = plt.subplots()
    ax.plot(x, y)
    axes = break_axis(ax, axis='y', break_ranges=[(-5, 5), (45, 55)])
    plt.show()
    """
    
    if break_ranges is None:
        raise ValueError("break_ranges must be specified")
    
    n_panels = len(break_ranges)
    
    # Get the figure and position of the original axis
    fig = ax.figure
    position = ax.get_position()
    
    # Store all plot elements from original axis
    lines = ax.get_lines()
    collections = ax.collections
    patches = ax.patches
    texts = ax.texts
    xlabel = ax.get_xlabel()
    ylabel = ax.get_ylabel()
    title = ax.get_title()
    
    # Remove the original axis
    ax.remove()
    
    if axis == 'y':
        # Create vertically stacked subplots in the original position
        if height_ratios is None:
            height_ratios = [r[1] - r[0] for r in break_ranges]
        
        # Create new subplots in the original axis position
        gs = fig.add_gridspec(n_panels, 1, 
                             left=position.x0, right=position.x1,
                             bottom=position.y0, top=position.y1,
                             height_ratios=height_ratios, hspace=0.05)
        
        axes = [fig.add_subplot(gs[i]) for i in range(n_panels)]
        
        # Copy plot elements to each new axis
        for new_ax, (ymin, ymax) in zip(axes, break_ranges):
            # Copy each line
            for line in lines:
                xdata, ydata = line.get_data()
                new_ax.plot(xdata, ydata, 
                           color=line.get_color(),
                           linestyle=line.get_linestyle(),
                           linewidth=line.get_linewidth(),
                           marker=line.get_marker(),
                           markersize=line.get_markersize(),
                           label=line.get_label())
            
            # Copy collections (scatter, etc.)
            for coll in collections:
                offsets = coll.get_offsets()
                if len(offsets) > 0:
                    new_ax.scatter(offsets[:, 0], offsets[:, 1],
                                  c=coll.get_facecolor(),
                                  s=coll.get_sizes())
            
            new_ax.set_ylim(ymin, ymax)
            new_ax.spines['top'].set_visible(False)
            new_ax.spines['bottom'].set_visible(False)
        
        # Show spines only on outer edges
        axes[0].spines['top'].set_visible(True)
        axes[-1].spines['bottom'].set_visible(True)
        axes[-1].set_xlabel(xlabel)
        axes[len(axes)//2].set_ylabel(ylabel)
        axes[0].set_title(title)
        
        # Add break markers
        d = 0.015
        for i, ax in enumerate(axes):
            if i < len(axes) - 1:  # Bottom of upper panels
                kwargs = dict(transform=ax.transAxes, color='k', clip_on=False, linewidth=1)
                ax.plot((-d, +d), (-d, +d), **kwargs)
                ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)
            if i > 0:  # Top of lower panels
                kwargs = dict(transform=ax.transAxes, color='k', clip_on=False, linewidth=1)
                ax.plot((-d, +d), (1 - d, 1 + d), **kwargs)
                ax.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)
        
        # Only show x-ticks on bottom panel
        for ax in axes[:-1]:
            ax.tick_params(labelbottom=False)
    
    elif axis == 'x':
        # Create horizontally arranged subplots in the original position
        if width_ratios is None:
            width_ratios = [r[1] - r[0] for r in break_ranges]
        
        # Create new subplots in the original axis position
        gs = fig.add_gridspec(1, n_panels,
                             left=position.x0, right=position.x1,
                             bottom=position.y0, top=position.y1,
                             width_ratios=width_ratios, wspace=0.05)
        
        axes = [fig.add_subplot(gs[i]) for i in range(n_panels)]
        
        # Copy plot elements to each new axis
        for new_ax, (xmin, xmax) in zip(axes, break_ranges):
            # Copy each line
            for line in lines:
                xdata, ydata = line.get_data()
                new_ax.plot(xdata, ydata,
                           color=line.get_color(),
                           linestyle=line.get_linestyle(),
                           linewidth=line.get_linewidth(),
                           marker=line.get_marker(),
                           markersize=line.get_markersize(),
                           label=line.get_label())
            
            # Copy collections (scatter, etc.)
            for coll in collections:
                offsets = coll.get_offsets()
                if len(offsets) > 0:
                    new_ax.scatter(offsets[:, 0], offsets[:, 1],
                                  c=coll.get_facecolor(),
                                  s=coll.get_sizes())
            
            new_ax.set_xlim(xmin, xmax)
            new_ax.spines['left'].set_visible(False)
            new_ax.spines['right'].set_visible(False)
        
        # Show spines only on outer edges
        axes[0].spines['left'].set_visible(True)
        axes[-1].spines['right'].set_visible(True)
        axes[0].set_ylabel(ylabel)
        axes[len(axes)//2].set_xlabel(xlabel)
        axes[0].set_title(title)
        
        # Add break markers
        d = 0.015
        for i, ax in enumerate(axes):
            if i < len(axes) - 1:  # Right side of left panels
                kwargs = dict(transform=ax.transAxes, color='k', clip_on=False, linewidth=1)
                ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)
                ax.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)
            if i > 0:  # Left side of right panels
                kwargs = dict(transform=ax.transAxes, color='k', clip_on=False, linewidth=1)
                ax.plot((-d, +d), (-d, +d), **kwargs)
                ax.plot((-d, +d), (1 - d, 1 + d), **kwargs)
        
        # Only show y-ticks on left panel
        for ax in axes[1:]:
            ax.tick_params(labelleft=False)
    
    else:
        raise ValueError("axis must be 'x' or 'y'")
    
    return axes