import openmc
from mat import cladding_mat, water_mat,  absorber_top_mat, AbstractUO2, Gd2O3_mat
from math import sqrt
from config import *

def get_TVS_cell(enr, rods_inserted=False, tvegs=False, outer_ring=False, outer_ring_enr=False, verbose=True):

     #if outer_ring and not outer_ring_enr:
         #raise Exception('Outer ring enrichment must be set')

    top_surf=openmc.ZPlane(z0=186.5)
    bottom_surf=openmc.ZPlane(z0=-186.5)
    top_surf.boundary_type='reflective'
    bottom_surf.boundary_type='reflective'

    if enr:#TODO: add enrs
        UO2_mat1 = AbstractUO2(enr).mat

    if tvegs:
        UO2_mat2 = openmc.Material.mix_materials(
   materials=[
        UO2_mat1,
        Gd2O3_mat,
    ],
    fracs=[0.96, 0.04],
    percent_type='vo')
    else:
        UO2_mat2 = UO2_mat1

    if outer_ring:
        UO2_mat3 = AbstractUO2(outer_ring_enr).mat
    else:
        UO2_mat3=UO2_mat1

    fuel_surf1=openmc.ZCylinder(r=r1_fuel)
    fuel_surf2=openmc.ZCylinder(r=r2_fuel)

    central_surf1=openmc.ZCylinder(r=r1_central)
    central_surf2=openmc.ZCylinder(r=r2_central)

    guide_surf1=openmc.ZCylinder(r=r1_guide)
    guide_surf2=openmc.ZCylinder(r=r2_guide)

    water_surf=openmc.hexagonal_prism(edge_length=1.275/sqrt(3), orientation='y', boundary_type='transmission')

    tvel1_fuel_cell=openmc.Cell(fill=UO2_mat1, region=-fuel_surf1 & +bottom_surf & -top_surf)
    tvel1_cladding_cell=openmc.Cell(fill=cladding_mat, region=+fuel_surf1 & -fuel_surf2 & +bottom_surf & -top_surf)
    tvel1_water_cell=openmc.Cell(fill=water_mat, region=+fuel_surf2 & water_surf & +bottom_surf & -top_surf)

    tvel2_fuel_cell=openmc.Cell(fill=UO2_mat2, region=-fuel_surf1 & +bottom_surf & -top_surf)
    tvel2_cladding_cell=openmc.Cell(fill=cladding_mat, region=+fuel_surf1 & -fuel_surf2 & +bottom_surf & -top_surf)
    tvel2_water_cell=openmc.Cell(fill=water_mat, region=+fuel_surf2 & water_surf & +bottom_surf & -top_surf)

    tvel3_fuel_cell=openmc.Cell(fill=UO2_mat3, region=-fuel_surf1 & +bottom_surf & -top_surf)
    tvel3_cladding_cell=openmc.Cell(fill=cladding_mat, region=+fuel_surf1 & -fuel_surf2 & +bottom_surf & -top_surf)
    tvel3_water_cell=openmc.Cell(fill=water_mat, region=+fuel_surf2 & water_surf & +bottom_surf & -top_surf)

    #TODO Add tvel3

    tvel1_universe=openmc.Universe(cells=[tvel1_fuel_cell, tvel1_cladding_cell, tvel1_water_cell])
    tvel2_universe=openmc.Universe(cells=[tvel2_fuel_cell, tvel2_cladding_cell, tvel2_water_cell])
    tvel3_universe=openmc.Universe(cells=[tvel3_fuel_cell, tvel3_cladding_cell, tvel3_water_cell])

    if rods_inserted:
        guide_mat = water_mat
    else:
        guide_mat = absorber_top_mat

    guide_cell1=openmc.Cell(fill=guide_mat, region=-guide_surf1 & +bottom_surf & -top_surf)
    guide_cell2=openmc.Cell(fill=cladding_mat, region=+guide_surf1 & -guide_surf2 & +bottom_surf & -top_surf)
    guide_water_cell=openmc.Cell(fill=water_mat, region=+guide_surf2 & water_surf & +bottom_surf & -top_surf)

    guide_universe=openmc.Universe(cells=[guide_cell1, guide_cell2, guide_water_cell])

    central_cell1=openmc.Cell(fill=water_mat, region=-central_surf1 & +bottom_surf & -top_surf)
    central_cell2=openmc.Cell(fill=cladding_mat, region=+central_surf1 & -central_surf2 & +bottom_surf & -top_surf)
    central_water_cell=openmc.Cell(fill=water_mat, region= +central_surf2 & water_surf & +bottom_surf & -top_surf)

    central_universe=openmc.Universe(cells=[central_cell1, central_cell2, central_water_cell])

    all_water_cell=openmc.Cell(fill=water_mat)
    water_universe=openmc.Universe(cells=[all_water_cell,])

    lat = openmc.HexLattice()
    lat.center = (0.0, 0.0)
    lat.pitch = [1.275]
    lat.outer = water_universe
    lat.orientation = 'x'

    firts_ring = [tvel3_universe] * 60
    second_ring = [tvel3_universe] + [tvel1_universe] * 8 + [tvel3_universe] + [tvel1_universe] * 8 + [
        tvel3_universe] + [tvel1_universe] * 8 + [tvel3_universe] + [tvel1_universe] * 8 + [tvel3_universe] + [
                      tvel1_universe] * 8 + [tvel3_universe] + [tvel1_universe] * 8

    third_ring = [tvel1_universe] * 4 + [tvel2_universe] + [tvel1_universe] * 7 + [tvel2_universe] + [tvel1_universe] * 7 + [tvel2_universe] + [tvel1_universe] * 7 + [tvel2_universe] + [tvel1_universe] * 7 + [tvel2_universe] + [tvel1_universe] * 7 + [tvel2_universe] + [tvel1_universe] * 3
    four_ring = [tvel1_universe] * 42
    fife_ring = [tvel1_universe] * 3 + [guide_universe] + [tvel1_universe] * 5 + [guide_universe] + [tvel1_universe] * 5 + [guide_universe] + [tvel1_universe] * 5 + [guide_universe] + [tvel1_universe] * 5 + [guide_universe] + [tvel1_universe] * 5 + [guide_universe] + [tvel1_universe] * 2
    six_ring = [guide_universe] + [tvel1_universe] * 4 + [guide_universe] + [tvel1_universe] * 4 + [guide_universe] + [tvel1_universe] * 4 + [guide_universe] + [tvel1_universe] * 4 + [guide_universe] + [tvel1_universe] * 4 + [guide_universe] + [tvel1_universe] * 4
    seven_ring = [tvel1_universe] + [tvel2_universe] + [tvel1_universe] * 3 + [tvel2_universe] + [tvel1_universe] * 3 + [tvel2_universe] + [tvel1_universe] * 3 + [tvel2_universe] + [tvel1_universe] * 3 + [tvel2_universe] + [tvel1_universe] * 3 + [tvel2_universe] + [tvel1_universe] * 2
    eight_ring = [tvel1_universe] * 2 + [guide_universe] + [tvel1_universe] * 2 + [guide_universe] + [
    tvel1_universe] * 2 + [guide_universe] + [tvel1_universe] * 2 + [guide_universe] + [tvel1_universe] * 2 + [guide_universe] + [tvel1_universe] * 2 + [guide_universe]
    nint_ring = [tvel1_universe] * 12
    ten_ring = [tvel1_universe] * 6
    inner_ring = [central_universe]
    lat.universes = [firts_ring, second_ring, third_ring, four_ring, fife_ring, six_ring, seven_ring, eight_ring, nint_ring, ten_ring, inner_ring]
    outer_surf=openmc.hexagonal_prism(edge_length=23.6/sqrt(3), orientation='x',  boundary_type='reflective')
    TVS_cell = openmc.Cell(fill=lat, region=outer_surf & +bottom_surf & -top_surf)
    #TVS_universe=openmc.Universe(cells=[TVS_cell, ])
    if verbose:
        print(lat)
    return TVS_cell