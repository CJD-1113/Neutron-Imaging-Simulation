%matplotlib inline
import openmc
import os
import math


castBronze = openmc.Material(1, "castBronze")
castBronze.add_element("Cu", 0.89)
castBronze.add_element("Sn", 0.11)
castBronze.temperature = 293 #K
castBronze.set_density("g/cm3", 8.77)

nitrogen = openmc.Material(2, "nitrogen")
nitrogen.set_density("g/cm3", 0.0012506)
nitrogen.add_element('N', 2.0)
nitrogen.temperature = 293 #K

oxygen = openmc.Material(3, "oxygen")
oxygen.set_density("g/cm3", 0.001429)
oxygen.add_element('O', 2.0)
oxygen.temperature = 293 #K

argon = openmc.Material(4, "argon")
argon.set_density("g/cm3", 0.0017837)
argon.add_element('Ar', 1.0)
argon.temperature = 293 #K

CO2 = openmc.Material(5, "CO2")
CO2.set_density("g/cm3", 0.001976)
CO2.add_element('C', 1.0)
CO2.add_element('O', 2)
CO2.temperature = 293 #K

airmix = openmc.Material.mix_materials([nitrogen, oxygen, argon, CO2], [0.7808, 0.2095, 0.0093, 0.0004], 'ao')
mats = openmc.Materials([castBronze, nitrogen, oxygen, argon, CO2, airmix])
print(mats)
mats.export_to_xml()





# GEOMETRY
#Making cylinder
cylinderSurface = openmc.ZCylinder(r=1.2, boundary_type='transmission')
upperSurface = openmc.ZPlane(z0=21, boundary_type='transmission')
lowerSurface = openmc.ZPlane(z0=20, boundary_type='transmission')

cylinderInside = -cylinderSurface & -upperSurface & +lowerSurface



# Create cells, mapping materials to cells
cylinder = openmc.Cell(name='cylinder')
cylinder.fill = castBronze
cylinder.region = cylinderInside

box = openmc.rectangular_prism(width=60, height=60, boundary_type='vacuum')
air_region = ~ cylinderInside & box
air = openmc.Cell(name='air')
air.fill = airmix
air.region = air_region

# Create a geometry and export to XML
root_universe = openmc.Universe(cells=[cylinder, air])
geom = openmc.Geometry(root_universe)                    
geom.export_to_xml()  

root_universe.plot(width=(60,60))
root_universe.plot(width=(60,60), basis='yz')




settings = openmc.Settings()
settings.particles = 10000
settings.batches = 10
settings.inactive = 0

# source = openmc.Source()
#  source.space = openmc.stats.Box((-0.0000000001, -2, -2), (0, 2, 2))
pi = math.pi
r = openmc.stats.PowerLaw(0.0, 2, 1.0)
phi = openmc.stats.Uniform(0.0, 2*pi)
z = openmc.stats.Discrete([1.0], [0.0])
spatial_dist = openmc.stats.CylindricalIndependent(r, phi, z)
source = openmc.Source(space=spatial_dist)


source.angle = openmc.stats.Monodirectional([0, 0, 1])
source.strength = 1
settings.source = source

settings.run_mode = 'fixed source'

settings.export_to_xml()




cell_filter = openmc.CellFilter([cylinder])
# energy_filter = openmc.EnergyFilter([0.01, 0.3])
tally = openmc.Tally(name="Neutron Flux")
tally.filters = [cell_filter]

tally.scores = ["flux"]

tallies = openmc.Tallies([tally])
tallies.export_to_xml()

model=openmc.model.Model(geom, mats, settings, tallies)
openmc.run()
