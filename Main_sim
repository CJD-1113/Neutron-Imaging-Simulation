%matplotlib inline
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

print(mats)



# GEOMETRY
#Making cylinder
cylinderSurface = openmc.XCylinder(r=1.2)
upperSurface = openmc.XPlane(x0=2)
lowerSurface = openmc.XPlane(x0=1)

cylinderInside = -cylinderSurface & -upperSurface & +lowerSurface

cylinderInside.boundary_type = "transmission"

# Create cells, mapping materials to cells
cylinder = openmc.Cell(name='cylinder')
cylinder.fill = castBronze
cylinder.region = cylinderInside

box = openmc.rectangular_prism(width=10, height=10, boundary_type='vacuum')
air_region = box & +cylinderSurface & +upperSurface & -lowerSurface
air = openmc.Cell(name='air')
air.fill = nitrogen

# Create a geometry and export to XML
root_universe = openmc.Universe(cells=[cylinder, air])
geom = openmc.Geometry(root_universe)                    
geom.export_to_xml()  

root_universe.plot(width=(20,20))
root_universe.plot(width=(20,20), basis='yz')



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




cell_filter = openmc.CellFilter([cylinder])
tally = openmc.Tally(name="Neutron Flux")
tally.filters = [cell_filter]

tally.scores = ["flux"]

tallies = openmc.Tallies([tally])
tallies.export_to_xml()

model=openmc.model.Model(geom, mats, settings, tallies)
openmc.run()
