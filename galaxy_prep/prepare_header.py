__author__ = 'Ian Fenech Conti'

import pyfits

def prepare_header(offset_path, dither_path, original_path, save_path):

    """
    @param offset_path: file offset
    @param dither_path: dither offset
    @param original_path: path to original image
    @param save_path: path to save output
    """

    # LOAD THE OFFSET VALUES
    f = open(offset_path, 'r')
    offsets = f.readline().split()
    offsets[0] = float(offsets[0])
    offsets[1] = float(offsets[1])
    f.close()

    # LOAD THE DITHER VALUES
    f = open(dither_path, 'r')
    dither = f.readline().split()
    dither[0] = float(dither[0])
    dither[1] = float(dither[1])
    f.close()

    # LOAD FITS FILE
    hdulist = pyfits.open(original_path)

    # EXTRACT FITS FILE HEADER INFORMATION
    prihdr = hdulist[0].header

    # OVERWRITE EXISTING VALUES
    prihdr.set('CTYPE1', 'RA---TAN')
    prihdr.set('CTYPE2', 'DEC---TAN')

    # APPEND NEW KEYS TO HEADER FOR XYCONVERSIONS
    prihdr.update('EXPTIME', 21600.)
    prihdr.update('PHOTPLAM', 0.000000)
    prihdr.update('PHOTZPT', 0.000000)
    prihdr.update('PHOTFLAM', 0.000000)

    # APPEND ADDITIONAL LENSFIT PARAMATERS
    prihdr.set('RADECSYS', 'FK5     ')

    prihdr.set('CRVAL1', 3.450000000E+01)
    prihdr.set('CRVAL2', -7.000000000E+00)

    # GET THE ORIGINAL CRPIX VALUES AND APPEND DITHER AND OFFSET VALUES
    crpix1 = prihdr['CRPIX1']
    crpix2 = prihdr['CRPIX2']

    prihdr.set('CRPIX1', crpix1 + offsets[0] + dither[0])
    prihdr.set('CRPIX2', crpix2 + offsets[1] + dither[1])

    # GET THE GS_SCALE AND CONVERT TO RA/DEC BASED ON THE PIXEL SCALE
    gs_scale = prihdr['GS_SCALE']
    cd_value = gs_scale/3600

    prihdr.set('CD1_1', -cd_value)
    prihdr.set('CD1_2', 0.0000000000000)
    prihdr.set('CD2_1', 0.0000000000000)
    prihdr.set('CD2_2', +cd_value)

    prihdr.set('PV1_0', 0.0000000000000)
    prihdr.set('PV1_1', 1.0000000000000)
    prihdr.set('PV1_2', 0.0000000000000)
    prihdr.set('PV1_4', 0.0000000000000)
    prihdr.set('PV1_5', 0.0000000000000)
    prihdr.set('PV1_6', 0.0000000000000)
    prihdr.set('PV1_7', 0.0000000000000)
    prihdr.set('PV1_8', 0.0000000000000)
    prihdr.set('PV1_9', 0.0000000000000)
    prihdr.set('PV1_10', 0.0000000000000)

    prihdr.set('PV2_0', 0.0000000000000)
    prihdr.set('PV2_1', 1.0000000000000)
    prihdr.set('PV2_2', 0.0000000000000)
    prihdr.set('PV2_4', 0.0000000000000)
    prihdr.set('PV2_5', 0.0000000000000)
    prihdr.set('PV2_6', 0.0000000000000)
    prihdr.set('PV2_7', 0.0000000000000)
    prihdr.set('PV2_8', 0.0000000000000)
    prihdr.set('PV2_9', 0.0000000000000)
    prihdr.set('PV2_10', 0.0000000000000)

    prihdr.update('CUNIT1', 'deg     ')
    prihdr.update('CUNIT2', 'deg     ')

    # DUMP DATA TO FILE
    hdulist.writeto(save_path)
    hdulist.close()
