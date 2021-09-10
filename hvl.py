import openmc
import matplotlib.pyplot as plt

lead = openmc.Material(name='lead')
lead.add_element('Pb', 1)
lead.set_density('g/cm3', 11.29)
mats = openmc.Materials([lead])
mats.cross_sections = '/Users/jacktweddle/Documents/STFC/Birmingham Project/OpenMC/endfb80_hdf5/cross_sections.xml'

# Create geometries
height = 1
width = 1
thickness = 0.76

pb_top = openmc.ZPlane(z0=height*0.5)
pb_bottom = openmc.ZPlane(z0=-height*0.5)
pb_front = openmc.XPlane(x0=-thickness*0.5)
pb_back = openmc.XPlane(x0=thickness*0.5)
pb_left = openmc.YPlane(y0=-width*0.5)
pb_right = openmc.YPlane(y0=width*0.5)
lead_region = -pb_top & +pb_bottom & +pb_left & -pb_right & +pb_front & -pb_back
lead_cell = openmc.Cell(region=lead_region)
lead_cell.fill = lead

det_top = openmc.ZPlane(z0=height)
det_bottom = openmc.ZPlane(z0=-height)
det_front = openmc.XPlane(x0=thickness*0.5 + 0.05)
det_back = openmc.XPlane(x0=thickness*0.5 + 0.06)
det_left = openmc.YPlane(y0=-width)
det_right = openmc.YPlane(y0=width)
det_region = -det_top & +det_bottom & +det_left & -det_right & +det_front & -det_back
det_cell = openmc.Cell(region=det_region)

sphere = openmc.Sphere(r=2, boundary_type='vacuum')
sphere_region = -sphere & ~lead_region & ~det_region
sphere_cell = openmc.Cell(region=sphere_region)

universe = openmc.Universe(cells=[lead_cell, det_cell, sphere_cell])
geom = openmc.Geometry(universe)

# 2D graphical representation
colours = {lead_cell: 'red', det_cell: 'grey', sphere_cell: 'blue'}
plt.show(universe.plot(width=(5, 5), basis='yz', colors=colours))
plt.show(universe.plot(width=(5, 5), basis='xy', colors=colours))

# Simulation settings
sett = openmc.Settings()
sett.batches = 10
sett.inactive = 0
sett.particles = 1000000
sett.run_mode = 'fixed source'

# Photon source
source = openmc.Source()
source.space = openmc.stats.Point((-1, 0, 0))
source.angle = openmc.stats.Monodirectional(reference_uvw=[1.0, 0, 0])
source.energy = openmc.stats.Discrete([1E6], 1)
source.particle = 'photon'
sett.source = source

# Tally
photon_particle_filter = openmc.ParticleFilter(['photon'])
cell_filter = openmc.CellFilter(det_cell)

tallies = openmc.Tallies()

s1_tally = openmc.Tally(name='tally_on_detector')
s1_tally.scores = ['flux']
s1_tally.filters = [photon_particle_filter, cell_filter]
tallies.append(s1_tally)

model = openmc.model.Model(geom, mats, sett, tallies)
sp_filename = model.run()
