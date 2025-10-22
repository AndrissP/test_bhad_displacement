import numpy as np
def get_median(histo, Neff, x_range=None):
    ''' Calculate median and median error (assuming Gaussian distribution).
    This is the binned median, not the real data median
    Extrapolation withing bins is performed.
    '''
    
    xvals = histo.axes[0].centers
    if x_range == None:
        xmi, xma = np.searchsorted(xvals, [min(xvals), max(xvals)]) + [0,1]
    elif len(x_range)!=2:
        raise ValueError("x_range should be a list [xmin; xmax] in which to evaluate the median")
    else:
        xmi, xma = np.searchsorted(xvals, x_range) + [0,1]
    bin_edges = histo.axes[0].edges
    yvals = histo.values()

    xvals = xvals[xmi:xma]
    yvals = yvals[xmi:xma]
    bin_edges = bin_edges[xmi:xma+1]

    yvals_cumsum = np.cumsum(yvals)
    N = np.sum(yvals)

    # once adding weights, Neff appears to be ~1/4 - 1/3 of N when not using weights,
    # so changing limits to match the both cases
    # if np.abs(np.sum(yvals)-Neff)/Neff<1e-5:
    #     N_min_limit=200
    # else:
    N_min_limit=1

    if Neff>N_min_limit:
        med_bin = np.nonzero(yvals_cumsum>N/2)[0][0]
        median = bin_edges[med_bin] + (N/2 - yvals_cumsum[med_bin-1])/yvals[med_bin]*(bin_edges[med_bin+1]
                                                                                 - bin_edges[med_bin])
    elif Neff==0:
        median = 0
        mediastd = 0
        return median, mediastd
    else:
        median=0

    # sumN = np.sum(yvals)
    # if sumN>0:
    #     N_eff = np.sum(histo.variances())/sumN
    #     hist_rms = np.sqrt(np.sum(yvals*((histo.mean()-xvals)**2))/sum(yvals))
    #     medianstd = 1.253 * hist_rms/np.sqrt(N_eff)
    # else:
    #     N_eff = 0
    #     medianstd = 0

    hist_mean = np.sum(xvals*yvals)/sum(yvals) 
    hist_rms = np.sqrt(np.sum(yvals*((hist_mean-xvals)**2))/sum(yvals))
    medianstd = 1.253 * hist_rms/np.sqrt(Neff)
    
    return median, medianstd