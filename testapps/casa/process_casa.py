from casatasks import importuvfits, listobs

# Convert FITS to CASA Measurement Set
importuvfits(fitsfile='observation.fits', vis='obs.ms')

# List information about the observation
listobs(vis='obs.ms')
print("Conversion to obs.ms complete.")

