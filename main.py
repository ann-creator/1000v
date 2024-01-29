import openmc
import openmc.deplete
import sys
import openmc.model
from openmc import stats
import neutronics_material_maker as nmm
from mat import water_mat, cladding_mat, AbstractUO2
#openmc.config['cross_sections']='/home/ann/PycharmProjects/1000/library/jeff33 (1)/jeff-3.3-hdf5/cross_sections.xml'
openmc.config['cross_sections']='/home/ann/PycharmProjects/1000/library/endfb71/endfb-vii.1-hdf5/cross_sections.xml'

#openmc.config['cross_sections'] = '/home/ann/PycharmProjects/1000/library/endfb80/endfb-viii.0-hdf5/cross_sections.xml'
import matplotlib.pyplot as plt

from params import GeometryParams
from core import UO2_mat1
from test import TVS_240
import numpy as np
if __name__ == "__main__":
    materials = openmc.Materials([water_mat,  cladding_mat, ])
    materials.export_to_xml()
    params = GeometryParams()
    # print(universe.get_all_materials())
    geometry=openmc.Geometry()
    geometry.root_universe=openmc.Universe(0, cells=[TVS_240,])
    settings=openmc.Settings()
    settings.temperature={'method': 'interpolation'}
    uniform_dist = stats.Box([-10, -10, -350 / 2], [10, 10, 350 / 2], only_fissionable=True)
    source = openmc.source.Source(space=uniform_dist)
    source.time = stats.Uniform(0, 1)
    settings.source = source
    flux_tally = openmc.Tally(name='flux')
    flux_tally.scores = ['flux']
    U_tally = openmc.Tally(name='fuel')
    U_tally.scores = ['fission', 'total', 'absorption', 'elastic', 'scatter', 'decay-rate']
    U_tally.nuclides = ['U235', 'U238', 'O16', 'H1']
    settings.batches = 100
    settings.particles = 6000
    settings.inactive = 10
    #power = (3000.0e6)/163  # watts
    #model = openmc.Model(geometry, materials, settings)
    #chain_file = '/home/ann/PycharmProjects/1000/library/chain_endfb71_pwr.xml'
    #operator = openmc.deplete.CoupledOperator(model, chain_file)
    #timesteps = [ (2,'MWd/kg'), (4,'MWd/kg'), (6,'MWd/kg'), (8,'MWd/kg'), (10,'MWd/kg'), (12,'MWd/kg'), (14,'MWd/kg'), (15,'MWd/kg'), (20,'MWd/kg'), (40, 'MWd/kg')]  # days
    #integrator=openmc.deplete.PredictorIntegrator(operator, timesteps,  power_density=108.0e6, timestep_units='MWd/kg')


    #openmc.deplete.CECMIntegrator(op, timesteps, power, timestep_units='d').integrate()
    #results = openmc.deplete.Results("depletion_results.h5")
    #time, keff = results.get_keff()

    #settings.run_mode = 'fixed source'
    #cecm = openmc.deplete.CECMIntegrator(operator, dt, power)
    #cecm.integrate()
    #source.strength = 18e0



    #plots = openmc.Plots(plots)
    colors = {water_mat: (32, 178, 170), cladding_mat: (0, 0, 0), UO2_36_mat: (128, 0, 128), mixed_with_Gd2O3_mat: (255, 0, 255), absorber_mat:(100, 100, 100)}
    color_data = dict(color_by='material', colors=colors)
    width = np.array([params.TVS_edge_length * 5.1, params.TVS_edge_length * 5.1, ])
    scale = 5.1 / 2
    fig, ax = plt.subplots(2, 2)

    geometry.root_universe.plot(width=width / scale, pixels=(1000, 1000), basis='xz', **color_data,
                  origin=(0, 0, GeometryParams.tvel_heigh / 2 - 1), axes=ax[0][0])
    geometry.root_universe.plot(width=width / scale, pixels=(1000, 1000), basis='xz', **color_data, origin=(0, 0, 0), axes=ax[1][1])
    geometry.root_universe.plot(width=width / scale, pixels=(1000, 1000), basis='xz', **color_data,
                  origin=(0, 0, -GeometryParams.tvel_heigh / 2 + 1),
                  axes=ax[0][1])
    geometry.root_universe.plot(width=width / scale, pixels=(1000, 1000), basis='xy', **color_data, origin=(0, 0, 0), axes=ax[1][0])
    plt.savefig('geometry.jpg')

    # ...and by openmc.Plots
    plots = [openmc.Plot(), openmc.Plot(), openmc.Plot(), openmc.Plot(), ]
    for i in range(4):
        plots[i].width = width
        plots[i].pixels = (2000, 2000)
        plots[i].basis = 'xz'
        plots[i].color_by = 'material'
        plots[i].colors = colors
    plots[0].origin = (0, 0, GeometryParams.tvel_heigh / 2 - 1)
    plots[2].origin = (0, 0, -GeometryParams.tvel_heigh / 2 - 1)
    plots[-1].basis = 'xy'

    plots = openmc.Plots(plots)
    tallies_file=openmc.Tallies([flux_tally, U_tally])
    tallies_file.export_to_xml()


    plots.export_to_xml('plots.xml')
    settings.export_to_xml('settings.xml')
    geometry.export_to_xml('geometry.xml')
    #model.export_to_xml('model.xml')
    openmc.plot_geometry()
    openmc.run()
