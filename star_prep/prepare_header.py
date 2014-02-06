__author__ = 'Ian Fenech Conti'

import pyfits

# LOAD FITS FILE
hdulist = pyfits.open('/home/ian/Documents/GREAT03/0/starfield_image-000-0.fits')

# EXTRACT FITS FILE HEADER INFORMATION
prihdr = hdulist[0].header

# OVERWRITE EXISTING VALUES
prihdr.set('CTYPE1', 'RA---TAN')
prihdr.set('CTYPE2', 'DEC--TAN')

# APPEND NEW KEYS TO HEADER FOR XYCONVERSIONS
prihdr.update('EXPTIME', 21600.)
prihdr.update('PHOTPLAM', 0.000000)
prihdr.update('PHOTZPT', 0.000000)
prihdr.update('PHOTFLAM', 0.000000)

# APPEND ADDITIONAL LENSFIT PARAMATERS
prihdr.set('RADECSYS', 'FK5     ')

prihdr.set('CRVAL1', 0)
prihdr.set('CRVAL2', 0)

# GET THE ORIGINAL CRPIX VALUES AND APPEND DITHER AND OFFSET VALUES
crpix1 = prihdr['CRPIX1']
crpix2 = prihdr['CRPIX2']

prihdr.set('CRPIX1', crpix1)
prihdr.set('CRPIX2', crpix2)

prihdr.set('EQUINOX', 2000.0000)

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
hdulist.writeto('/home/ian/Documents/GREAT03/0/out/starfield_crop_whole.fits')
hdulist.close()
