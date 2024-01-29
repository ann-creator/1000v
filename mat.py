import random

import openmc
from openmc.data import NATURAL_ABUNDANCE
import math
from math import pi
import neutronics_material_maker as nmm

# обогащение 3.7
UO2_mat = openmc.Material(material_id=5, name='UO2', temperature=1027)
UO2_mat.add_nuclide('U235', 0.1505368005)
UO2_mat.add_nuclide('U238', 3.868647792)
UO2_mat.add_nuclide('O16', 8.038320323)
UO2_mat.set_density('g/cm3', 10.4)
# обогащение по урану  3.6 и 4% гадолиния
#mixed_with_Gd2O3_mat = openmc.Material(material_id=1, name='mixed_with_Gd2O3_mat', temperature=1027)
#mixed_with_Gd2O3_mat.add_nuclide('U235', 0.1271720456, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('U238', 3.362402709, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('O16', 7.303819959, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd152', 0.0004390424006, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd154', 0.004764567218, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd155', 0.03235536051, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd156', 0.04467730649, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd157', 0.03399398213, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd158', 0.05359985427, percent_type='ao')
#mixed_with_Gd2O3_mat.add_nuclide('Gd160', 0.04660386482, percent_type='ao')
#mixed_with_Gd2O3_mat.set_density('g/cm3', 10.54)

#print(mixed_with_Gd2O3_mat.get_nuclide_atom_densities())
cladding_mat = openmc.Material(material_id=2, name='cladding_mat', temperature=575)
cladding_mat.add_element('Zr', 0.3268433646, percent_type='ao')
cladding_mat.add_element('Nb', 0.003242341431, percent_type='ao')
cladding_mat.add_element('Hf', 0.00005062657141, percent_type='ao')
cladding_mat.set_density('g/cm3', 6.515)
print(cladding_mat.get_nuclide_atom_densities())
water_mat = openmc.Material(material_id=3, name='water_mat', temperature=575)
water_mat.add_element('H', 0.04843, percent_type='ao')
water_mat.add_nuclide('O16', 0.02422, percent_type='ao')
water_mat.add_nuclide('B10', 0.000004794, percent_type='ao')
water_mat.add_nuclide('B11', 0.00001942, percent_type='ao')
water_mat.set_density('g/cm3', 0.7235)
print(water_mat.get_nuclide_atom_densities())

UO2_16_mat = openmc.Material(material_id=6, name='UO2_16', temperature=1027)
UO2_16_mat.add_element('U', 1.0, enrichment=1.6)
UO2_16_mat.add_element('O', 2.0)
UO2_16_mat.set_density('g/cm3', 10.4)

UO2_24_mat = openmc.Material(material_id=4, name='UO2_24', temperature=1027)
UO2_24_mat.add_element('U', 1.0, enrichment=2.4)
UO2_24_mat.add_element('O', 2.0)
UO2_24_mat.set_density('g/cm3', 10.4)

UO2_33_mat = openmc.Material(material_id=7, name='UO2_33', temperature=1027)
UO2_33_mat.add_element('U', 1.0, enrichment=3.3)
UO2_33_mat.add_element('O', 2.0)
UO2_33_mat.set_density('g/cm3', 10.4)

UO2_36_mat = openmc.Material(material_id=8, name='UO2_36', temperature=1027)
UO2_36_mat.add_element('U', 1.0, enrichment=3.6)
UO2_36_mat.add_element('O', 2.0)
UO2_36_mat.set_density('g/cm3', 10.4)

UO2_40_mat = openmc.Material(material_id=9, name='UO2_40', temperature=1027)
UO2_40_mat.add_element('U', 1.0, enrichment=4.0)
UO2_40_mat.add_element('O', 2.0)
UO2_40_mat.set_density('g/cm3', 10.4)


class AbstractUO2():
    def __init__(self, enricment, density=10.4, temp=1027):
        mat = openmc.Material(material_id=random.randint(10,10000), name=f'UO2_{enricment:.1f}', temperature=temp)
        mat.add_element('U', 1.0, enrichment=4.0)
        mat.add_element('O', 2.0)
        mat.set_density('g/cm3', density)
        self.mat = mat


absorber_top_mat = nmm.Material.from_library(name='Boron Carbide (B4C)', temperature=575).openmc_material

absorber_bottom_mat = openmc.Material(name='absorber_bottom', temperature=575)
absorber_bottom_mat.add_element('Dy', 2.0)
absorber_bottom_mat.add_element('O', 3)
absorber_bottom_mat.add_element('Ti', 1)
absorber_bottom_mat.add_element('O', 2)
absorber_bottom_mat.set_density('g/cm3', 5.1)

# water_mat=openmc.Material(name='water')
# water_mat.add_nuclide('H1', 2.*0.999885, percent_type='ao')
# water_mat.add_nuclide('H2', 2.*0.000115, percent_type='ao')
# water_mat.add_nuclide('O16', 0.99757, percent_type='ao')
# water_mat.add_nuclide('O17', 0.00038, percent_type='ao')
# water_mat.add_nuclide('O18', 0.00205, percent_type='ao')
# water_mat.set_density('g/cm3', 0.7235)
# water_mat=openmc.model.borated_water(600, density=0.7235, temperature=575)
# UO2_mat=openmc.Material(name='UO2')
# UO2_mat.add_element('U', 1.0,  enrichment=3.7)
# UO2_mat.add_element('O', 2.0)
# UO2_mat.set_density('g/cm3', 10.4)
# UO2_mat.volume=V
# UO2_mat.temperature=1027
# UO2_mat1=openmc.Material(name='UO21')
# UO2_mat1.add_element('U', 1.0,  enrichment=3.6)
# UO2_mat1.add_element('O', 2.0)
# UO2_mat1.set_density('g/cm3', 10.4)
# UO2_mat1.volume=V
# UO2_mat1.temperature=1027
# UO2_mat.depletable=True
# zirconi_mat=openmc.Material()
# zirconi_mat.add_element('Zr', 0.99)
# zirconi_mat.add_element('Nb', 0.01)
# zirconi_mat.set_density('g/cm3', 6.55)
Gd2O3_mat=openmc.Material()
Gd2O3_mat.add_element('Gd', 2.0, percent_type='ao')
Gd2O3_mat.add_element('O', 3.0, percent_type='ao')
Gd2O3_mat.set_density( 'g/cm3', 7.41)
#mixed_with_Gd2O3_mat=openmc.Material.mix_materials(
#   materials=[
#        mat,
#        Gd2O3_mat,
#    ],
#    fracs=[0.96, 0.04],
#    percent_type='vo')
#mixed_with_Gd2O3_mat.depletable=True
#mixed_with_Gd2O3_mat.volume=R**2*pi*350*18*7
#mixed_with_Gd2O3_mat.temperature=1027
# helium_mat=openmc.Material(name='Helium')
# helium_mat.add_element('He', 1.0)
# helium_mat.set_density('g/cm3', 0.0001785)
# water_mat = nmm.Material.from_library(name='Water, Liquid').openmc_material
# water_mat.temperature=575
# cladding_mat1 = nmm.Material.from_library(name='Zircaloy-2', temperature=575).openmc_material
# Nb_mat=openmc.Material()
# Nb_mat.add_element('Nb', 100 )
# Nb_mat.set_density('g/cm3', 8.57)
# cladding_mat=openmc.Material.mix_materials(
#    materials=[
#        cladding_mat1,
#        Nb_mat,
#    ],
#    fracs=[0.99, 0.01],
#    percent_type='vo'
# )
# cladding_mat.temperature=575


# tube_mat=nmm.Material.from_library(name='SS_316L_N_IG').openmc_material
# tube_mat.temperature=575
