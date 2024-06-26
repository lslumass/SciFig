import numpy as np


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
    probs = counts/counts.sum()
    pdf = probs/np.diff(bins)

    if styles == 'pdf':
        return bins[:-1], pdf
    elif styles == 'pmf':
        return bins[:-1], probs
    elif styles == 'l_pdf':
        return bins[:-1]+0.5*np.diff(bins), pdf
    elif styles == 'l_pmf':
        return bins[:-1]+0.5*np.diff(bins), probs
    elif styles == 's_pdf':
        window_size = 5
        cumsum_vec = np.cumsum(np.insert(pdf, 0, 0))
        pdf_smooth = (cumsum_vec[window_size:] - cumsum_vec[:-window_size])/window_size
        bins_smooth = bins[window_size - 1:]
        return bins_smooth, pdf_smooth
    elif styles == 's_pmf':
        window_size = 5
        cumsum_vec = np.cumsum(np.insert(probs, 0, 0))
        probs_smooth = (cumsum_vec[window_size:] - cumsum_vec[:-window_size])/window_size
        bins_smooth = bins[window_size - 1:]
        return bins_smooth, probs_smooth
    else:
        print('styles error')