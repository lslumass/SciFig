import numpy as np
from scipy.interpolate import make_interp_spline


def scatter2hist(point_list, num_bin, styles):
    '''
    styles:
        pdf: histogram of probability density function
        pmf: histogram of probability mass function
        s_pdf: smoothed line of pdf
        s_pmf: smoothed line of pmf
    '''
    counts, bins = np.histogram(point_list, num_bin)
    pmf = counts/counts.sum()
    pdf = pmf/np.diff(bins)

    if styles == 'pdf':
        bins = np.insert(bins, 0, 2*bins[0]-bins[1])
        bins = bins+0.5*np.diff(bins)[0]
        pdf = np.insert(pdf, 0, 0)
        pdf = np.append(pdf, 0)
        return bins, pdf
    elif styles == 'pmf':
        bins = np.insert(bins, 0, 2*bins[0]-bins[1])
        bins = bins+0.5*np.diff(bins)[0]
        pmf = np.insert(pmf, 0, 0)
        pmf = np.append(pmf, 0)
        return bins, pmf
    elif styles == 's_pdf':
        bins = np.insert(bins, 0, 2*bins[0]-bins[1])
        bins = bins+0.5*np.diff(bins)[0]
        pdf = np.insert(pdf, 0, 0)
        pdf = np.append(pdf, 0)
        bins_smooth = np.linspace(bins.min(), bins.max(), num_bin*10)
        spline = make_interp_spline(bins, pdf, k=3)
        pdf_smooth = spline(bins_smooth)
        return bins_smooth, pdf_smooth
    elif styles == 's_pmf':
        bins = np.insert(bins, 0, 2*bins[0]-bins[1])
        bins = bins+0.5*np.diff(bins)[0]
        pmf = np.insert(pmf, 0, 0)
        pmf = np.append(pmf, 0)
        bins_smooth = np.linspace(bins.min(), bins.max(), num_bin*10)
        spline = make_interp_spline(bins, pmf, k=2)
        pmf_smooth = spline(bins_smooth)
        return bins_smooth, pmf_smooth
    else:
        print('styles error')


def block_mean(data, division):
    '''
    data: a list of the scatter points along simulation time
    division: how many parts should the data divided, and the first part will be ignored for analysis
                the rest part will be divided into two blocks, and then the standard deviation and average
    '''
    l = len(data)
    start_frame = int(l/division)
    half = int((l-start_frame)/2)
    part1 = np.mean(data[start_frame:half])
    part2 = np.mean(data[half:])
    average = np.mean([part1, part2])
    error = np.std([part1, part2])
    return average, error
