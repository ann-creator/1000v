import openmc

DAGMC_universe = openmc.DAGMCUniverse(filename='/home/ann/PycharmProjects/python3.9/dagmc.h5m')
cell=openmc.Cell()
cell.fill=DAGMC_universe
universe = openmc.Universe(cells=[cell])
