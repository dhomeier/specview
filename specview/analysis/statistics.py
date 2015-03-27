import numpy as np

from specview.core import SpectrumData


def extract(spectrum_data, x_range):
    ''' Extracts a region from a spectrum.

    Paramaters
    ----------
    spectrum_data: SpectrumData
      Contains the spectrum to be extracted.
    w_range: tuple
      A spectral coordinate range as in (wave1, wave2)

    Returns
    -------
    SpectrumData with extracted region.

    '''
    x = spectrum_data.x.data
    y = spectrum_data.y.data

    slice = (x >= x_range[0]) & (x < x_range[1])

    result = SpectrumData()
    result.set_x(x[slice], unit=spectrum_data.x.unit)
    result.set_y(y[slice], unit=spectrum_data.y.unit)

    return result


def stats(spectrum_data):
    ''' Computes basic statistics for a spectral region
    contained in a SpectrumData instance.

    Paramaters
    ----------
    spectrum_data: SpectrumData
      Typically this is returned by the extract() function

    Returns
    -------
    statistics: dict

    '''
    flux = spectrum_data.y.data
    return {'mean':    np.mean(flux),
            'median':  np.median(flux),
            'stddev':  np.std(flux),
            'total':   np.trapz(flux),
            'npoints': len(flux)
            }


def eq_width(cont1_stats, cont2_stats, line):
    ''' Computes an equivalent width given stats for two continuum
    regions, and a SpectrumData instance with the extracted
    spectral line region.

    This uses for now a very simple continuum subtraction method:
    it just subtracts a constant from the line spectrum, where the
    constant is (continuum1[mean] + continuum2[mean]) / 2.

    Parameters
    ----------
    cont1_stats: dict
      This is returned by the stats() function
    cont2_stats: dict
      This is returned by the stats() function
    line: SpectrumData
      This is returned by the extract() function

    Returns
    -------
    flux, equivalent width: tuple
      tuple with two floats

    '''
    # average of 2 continuum regions.
    avg_cont = (cont1_stats['mean'] + cont2_stats['mean']) / 2.0

    # average dispersion in the line region.
    avg_dx = np.mean(line.x.data[1:] - line.x.data[:-1])

    # flux
    flux = np.sum(line.y.data - avg_cont) * avg_dx

    #  EW = Sum( (Fc-Fl)/Fc * dw
    ew =  np.sum((avg_cont - line.y.data) / avg_cont * avg_dx)

    return flux, ew
