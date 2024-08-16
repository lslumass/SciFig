import numpy as np
from scipy.interpolate import make_interp_spline
from scipy.stats import gaussian_kde
from MDAnalysis.analysis import pca
import MDAnalysis as mda


def scatter2hist(point_list, num_bin, styles):
    '''
    convert scatters to hist or distribution
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


def pca2d(axs, psf, dcd, sel, num_bin=100, align=False, cmap='GnBu'): 
    u = mda.Universe(psf, dcd)
    atomgroup = u.select_atoms(sel)
    pc = pca.PCA(u, select=sel, align=align).run()
    pc1, pc2 = pc.transform(sel)[:,0], pc.transform(sel)[:,1]
    var1, var2 = pc.cumulated_variance[1], pc.cumulated_variance[1]
    H, xedges, yedges = np.histogram2d(pc1, pc2, bins=num_bin)
    pmf = H / np.sum(H)

    # convert pmf to free energy
    fe = -np.log(pmf)
    fe_min = np.min(fe[np.isfinite(fe)])
    fe -= fe_min

    im = axs.imshow(fe.T, origin='lower', cmap=cmap)
    axs.figure.colorbar(im, ax = axs, label='Free energy (k$_B$T)', fraction=0.046)
    axs.set(xlabel=f'PC1 ({var1*100:.2f}%)', xticks=[], ylabel=f'PC2 ({var2*100:.2f}%)', yticks=[])
    


def block_mean(data, division):
    '''
    calculate the block mean and std of a list of number 
    data: a list of the scatter points along simulation time
    division: how many parts should the data divided, and the first part will be ignored for analysis
                the rest part will be divided into two blocks, and then the standard deviation and average
    '''
    l = len(data)
    start_frame = int(l/division)
    half = start_frame + int((l-start_frame)/2)
    part1 = np.mean(data[start_frame:half])
    part2 = np.mean(data[half:])
    average = np.mean([part1, part2])
    error = np.std([part1, part2])
    return average, error


def remove_zero(xs, ys):
    '''
    remove the zero section at the beginning and ending of one distribution
    xs: data for x-axis
    ys: data for y-axis
    '''
    for idx in range(len(xs)):
        # find the first non-zero point from begging
        if ys[idx] != 0:
            start = idx-5
            break
    for idx in reversed(range(len(xs))):
        # find the last non-zero point at the end
        if ys[idx] != 0:
            end = idx+5
            break
    return(xs[start], xs[end])