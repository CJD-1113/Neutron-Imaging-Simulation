import openmc

castBronze = openmc.Material(1, "castBronze")
castBronze.add_element("Cu", 0.89)
castBronze.add_element("Sn", 0.11)
castBronze.temperature = 293 #K
castBronze.set_density("g/cm3", 8.77)

mats = openmc.Materials([castBronze])
mats.export_to_xml()

dag_univ = openmc.DAGMCUniverse(filename='dagmc.h5m')
geometry = openmc.Geometry(dag_univ)
geometry.export_to_xml()

point = openmc.stats.Point((0,0,0))
src = openmc.Source(space=point)

settings = openmc.settings
settings.source = src
settings.batches = 120
settings.inactive = 20
settings.particles = 10000
settings.temperature = {"method": "interpolation"}
settings.export_to_xml()

openmc.run()
