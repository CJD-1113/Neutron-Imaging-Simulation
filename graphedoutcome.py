%matplotlib inline
from IPython.display import Image
import numpy as np
import matplotlib.pyplot as plt

import openmc
import os


castBronze = openmc.Material(1, "castBronze")
castBronze.add_element("Cu", 0.89)
castBronze.add_element("Sn", 0.11)
castBronze.temperature = 293 #K
castBronze.set_density("g/cm3", 8.77)

nitrogen = openmc.Material(2, "nitrogen")
nitrogen.set_density("g/cm3", 0.0012506)
nitrogen.add_element('N', 2.0)
nitrogen.temperature = 293 #K

mats = openmc.Materials([castBronze, nitrogen])
mats.export_to_xml()

# GEOMETRY
#Making cylinder surfaces
cylinderSurface = openmc.xCylinder(r=1.2)
upperSurface = openmc.XPlane(x0=2)
lowerSurface = openmc.XPlane(x0=1)

#Converting into region
cylinderInside = -cylinderSurface & -upperSurface & +lowerSurface
cylinderInside.boundary_type = "transmission"

# Create cells, mapping materials to cells
cylinder = openmc.Cell(name='cylinder')
cylinder.fill = castBronze
cylinder.region = cylinderInside

box = openmc.rectangular_prism(width=10, height=10, boundary_type='vacuum')
air_region = ~ cylinderInside & box
air = openmc.Cell(name='air')
air.fill = nitrogen
air.region = air_region


# Create a geometry and export to XML
root_universe = openmc.Universe(cells=[cylinder, air])
geom = openmc.Geometry(root_universe)                    
geom.export_to_xml()  

root_universe.plot(width=(5,5))
root_universe.plot(width=(5,5), basis='yz')

settings = openmc.Settings()
settings.particles = 10000
settings.batches = 10
settings.inactive = 0

source = openmc.Source()
source.space = openmc.stats.Point()
source.angle = openmc.stats.Monodirectional()
settings.source = source
settings.run_mode = 'fixed source'
settings.export_to_xml()

# Instantiate an empty Tallies object
tallies = openmc.Tallies()

# Create mesh which will be used for tally
mesh = openmc.RegularMesh()
mesh.dimension = [10, 10]
mesh.lower_left = [-0.63, -0.63]
mesh.upper_right = [0.63, 0.63]

# Create mesh filter for tally
mesh_filter = openmc.MeshFilter(mesh)

# Create mesh tally to score flux and fission rate
tally = openmc.Tally(name='flux')
tally.filters = [mesh_filter]
tally.scores = ['flux', 'fission']
tallies.append(tally)

# Export to "tallies.xml"
tallies.export_to_xml()

# Run OpenMC!
model=openmc.model.Model(geom, mats, settings, tallies)
openmc.run()

#POST PROCESSING
sp = openmc.StatePoint('statepoint.10.h5')
tally = sp.get_tally(scores=['flux'])
flux = tally.get_slice(scores=['flux'])

print(flux)
flux.std_dev.shape = (10, 10)
flux.mean.shape = (10, 10)
fig = plt.subplot(121)
fig.imshow(flux.mean)
