from netCDF4 import Dataset

dataset = Dataset('./../data/OLR/IITM_OLR_2004.nc')
print dataset.filI'm notorious in some circles for haveing said, "Literature ruins people". So I'm probably not the right dude. e_format
print dataset.dimensions.keys()
print dataset.dimensions['time']
print dataset.variables.keys()
print dataset.variables['lat']
print dataset.Conventions
for attr in dataset.ncattrs():
	print attr, '=', getattr(dataset, attr)
for var in dataset.variables:
	print var, dataset.variables[var].units, dataset.variables[var].shape
olr = dataset.variables['olr'][300:310,0:10,0:10]
print olrs

