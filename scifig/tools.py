import numpy as np
from scipy.interpolate import make_interp_spline


def scatter2hist(point_list, num_bin, styles):
    '''
    styles:
        pdf: histogram of probability density function
        pmf: histogram of probability mass function
        l_pdf: linked line of pdf
        l_pmf: linked line of pmf
        s_pdf: smoothed line of pdf
        s_pmf: smoothed line of pmf
    '''
    counts, bins = np.histogram(point_list, num_bin)
    pmf = counts/counts.sum()
    pdf = pmf/np.diff(bins)

    if styles == 'pdf':
        bins = bins[:-1]+0.5*np.diff(bins)
        return bins, pdf
    elif styles == 'pmf':
        bins = bins[:-1]+0.5*np.diff(bins)
        return bins, pmf
    elif styles == 'l_pdf':
        bins = np.insert(bins, 0, 2*bins[0]-bins[1])
        bins = bins+0.5*np.diff(bins)[0]
        pdf = np.insert(pdf, 0, 0)
        pdf = np.append(pdf, 0)
        return bins, pdf
    elif styles == 'l_pmf':
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
