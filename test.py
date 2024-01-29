from core import get_TVS_cell
from mat import water_mat
import openmc



TVS_160 = get_TVS_cell(1.6, 0,1,0,1.6, 1)

TVS_240=get_TVS_cell(2.4, 0, 1, 1,1.6, 1)

top_surf = openmc.ZPlane(z0=186.5)
bottom_surf = openmc.ZPlane(z0=-186.5)
top_surf.boundary_type = 'reflective'
bottom_surf.boundary_type = 'reflective'

#all_water2_cell=openmc.Cell(fill=water_mat)
#water2_universe=openmc.Universe(cells=[all_water2_cell,])
#core_lat=openmc.HexLattice()
#core_lat.center=(0.0, 0.0)
#core_lat.pitch=[23.6]
#core_lat.outer=water2_universe
#core_lat.orientation='y'
#outer_ring=[TVS_240]*6
#inner2_ring=[TVS_160]
#core_lat.universes=[outer_ring, inner2_ring]
#outer2_radius=100
#outer2_surf=openmc.ZCylinder(r=outer2_radius, boundary_type='reflective')
#core_cell=openmc.Cell(fill=core_lat, region=-outer2_surf & +bottom_surf & -top_surf)
#print(core_lat)