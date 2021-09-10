import openmc
import matplotlib.pyplot as plt

# Create material
tantalum = openmc.Material(name='tantalum')
tantalum.add_element('Ta', 1)
tantalum.set_density('g/cm3', 16.69)
mats = openmc.Materials([tantalum])
mats.cross_sections = '/Users/jacktweddle/Documents/STFC/Birmingham Project/OpenMC/endfb80_hdf5/cross_sections.xml'

# Create geometries
height = 1
width = 1
thickness = 0.0008

top = openmc.ZPlane(z0=height*0.5)
bottom = openmc.ZPlane(z0=-height*0.5)
right = openmc.XPlane(x0=width*0.5)
left = openmc.XPlane(x0=-width*0.5)
front = openmc.YPlane(y0=thickness*0.5)
back = openmc.YPlane(y0=-thickness*0.5)
tantalum_region = -top & +bottom & +left & -right & -front & +back
tantalum_cell = openmc.Cell(region=tantalum_region)
tantalum_cell.fill = tantalum

sphere1 = openmc.Sphere(r=2)
sphere2 = openmc.Sphere(r=2.1, boundary_type='vacuum')
sphere1_region = -sphere1 & ~tantalum_region
sphere1_cell = openmc.Cell(region=sphere1_region)
sphere2_region = +sphere1 & -sphere2
sphere2_cell = openmc.Cell(region=sphere2_region)

universe = openmc.Universe(cells=[tantalum_cell, sphere1_cell, sphere2_cell])
geom = openmc.Geometry(universe)

# 2D graphical representation
colours = {tantalum_cell: 'red', sphere1_cell: 'grey', sphere2_cell: 'blue'}
'''plt.show(universe.plot(width=(6, 6), basis='xz', colors=colours))
plt.show(universe.plot(width=(6, 6), basis='xy', colors=colours))'''

# Simulation settings
sett = openmc.Settings()
sett.batches = 10
sett.inactive = 0
sett.particles = 10000000
sett.run_mode = 'fixed source'

# Photon source
source = openmc.Source()
source.space = openmc.stats.Point((0, 0, 0))
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Discrete([2E6], 1)
source.particle = 'photon'
sett.source = source

# Tally
photon_particle_filter = openmc.ParticleFilter(['photon'])
surface_filter = openmc.SurfaceFilter(sphere1)

tallies = openmc.Tallies()

s1_tally = openmc.Tally(name='tally_on_sphere_1')
s1_tally.scores = ['current']
s1_tally.filters = [photon_particle_filter, surface_filter]
tallies.append(s1_tally)

model = openmc.model.Model(geom, mats, sett, tallies)
sp_filename = model.run()

