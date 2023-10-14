import openmc
import openmc.deplete
import openmc.model
from openmc import stats
import neutronics_material_maker as nmm
from mat import water_mat, UO2_mat, zirconi_mat, helium
openmc.config['cross_sections']='/media/ann/600E180D69017994/jeff-3.3-hdf5/cross_sections.xml'
import matplotlib.pyplot as plt
from geometry import universe
from openmc import interp1d
import numpy as np
if __name__ == "__main__":
    materials = openmc.Materials([UO2_mat, water_mat, zirconi_mat, helium ])
    materials.export_to_xml()

    # print(universe.get_all_materials())
    geometry=openmc.Geometry(universe)
    settings=openmc.Settings()
    uniform_dist = stats.Box([-10, -10, -350 / 2], [10, 10, 350 / 2], only_fissionable=True)
    source = openmc.source.Source(space=uniform_dist)
    source.time = stats.Uniform(0, 1)
    settings.source = source
    flux_tally = openmc.Tally(name='flux')
    flux_tally.scores = ['flux']
    U_tally = openmc.Tally(name='fuel')
    U_tally.scores = ['fission', 'total', 'absorption', 'elastic', 'scatter', 'decay-rate']
    U_tally.nuclides = ['U235', 'U238', 'O16', 'H1']
    settings.batches = 200
    settings.particles = 2000
    settings.inactive = 10
    power = (3000.0e6)/163  # watts
    # timesteps = [86400.0, 259200, 518400, 950400, 1814400, 3110400, 4838400, 7430400, 10886400, 15206400, 21254400, 29030400]  # days
    timesteps = [1, 3, 6, 11, 21, 36, 36, 56, 86, 126, 176, 246, 336]  # days
    model = openmc.Model(geometry, materials, settings)
    chain_file='/media/ann/600E180D69017994/chain_endfb71_pwr.xml'
    op = openmc.deplete.CoupledOperator(model, chain_file)
    openmc.deplete.CECMIntegrator(op, timesteps, power, timestep_units='d').integrate()
    results = openmc.deplete.Results("depletion_results.h5")
    time, keff = results.get_keff()


    #chain_file = "chain_casl.xml"
    #operator = openmc.deplete.CoupledOperator(model, chain_file)
    #dt = [24 * 60 * 60] * 5
    #power = 1e6  # constant power of 1 MW

    #settings.run_mode = 'fixed source'
    #cecm = openmc.deplete.CECMIntegrator(operator, dt, power)
    #cecm.integrate()
    # source.strength = 18e0

    colors = {
        water_mat: (50,50,125),
        UO2_mat: (0,125,0),
        zirconi_mat: (20, 30, 40),
        helium:(100,100,250),
    }
    width=(2, 2)
    plots = [openmc.Plot(), openmc.Plot(), openmc.Plot(), openmc.Plot(), ]
    for i in range(4):
        plots[i].width = width
        plots[i].pixels = (500, 500)
        plots[i].basis = 'xz'
        plots[i].color_by = 'material'
        plots[i].colors = colors
    plots[0].origin = (0, 0, 350 / 2)
    plots[2].origin = (0, 0, 350 +2)
    plots[-1].basis = 'xy'
    plots[-1].origin = (0, 0, 350/2)

    plots = openmc.Plots(plots)
    tallies_file=openmc.Tallies([flux_tally, U_tally])
    tallies_file.export_to_xml()


    plots.export_to_xml('plots.xml')
    settings.export_to_xml('settings.xml')
    geometry.export_to_xml('geometry.xml')
    #model.export_to_xml('model.xml')
    openmc.plot_geometry()
    openmc.run()