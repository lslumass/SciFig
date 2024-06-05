import numpy as np
from scipy.stats import gaussian_kde


def scatters2dist(point_list, num_bin):
    '''
    convert a list of scatter points into distribution
    input: point_list = [1, 2, 3, 4, ]
            num_bin: the number of total bins
    return: x_grid, kde_values
            plot(x_grid, kde_values)
    '''
    kde = gaussian_kde(point_list)
    x_grid = np.linspace(np.min(point_list)-1, np.max(point_list)+1, num_bin)
    kde_values = kde(x_grid)
    return x_grid, kde_values

