import netCDF4
import sys
import numpy
import station


numpy.set_printoptions(threshold=sys.maxsize)
ds = netCDF4.Dataset('all_stations_all2001.netcdf')
clk = station.Station(ds, 39)
gtf = station.Station(ds, 80)
msh = station.Station(ds, 138)
ott = station.Station(ds, 151)

print(clk.vector_correlation(gtf))
print(clk.vector_correlation(msh))
print(clk.vector_correlation(ott))
print(gtf.vector_correlation(msh))
print(gtf.vector_correlation(ott))
print(msh.vector_correlation(ott))
