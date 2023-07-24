%matplotlib inline
import openmc
import os

# Materials
castBronze = openmc.Material(1, "castBronze")
castBronze.add_nuclide("Cu63", 0.615435)
castBronze.add_nuclide("Cu65", 0.274565)
castBronze.add_nuclide("Sn112", 0.001067)
castBronze.add_nuclide("Sn114", 0.000726)
castBronze.add_nuclide("Sn115", 0.000374)
castBronze.add_nuclide("Sn116", 0.015994)
castBronze.add_nuclide("Sn117", 0.008448)
castBronze.add_nuclide("Sn118", 0.026642)
castBronze.add_nuclide("Sn119", 0.009449)
castBronze.add_nuclide("Sn120", 0.035838)
castBronze.add_nuclide("Sn122", 0.005093)
castBronze.add_nuclide("Sn124", 0.006369)
castBronze.temperature = 293 #K
castBronze.set_density("g/cm3", 8.77)


"""oxygen = openmc.Materials(2.0, "oxygen")
oxygen.add_nuclide("0", 2.0)
oxygen.temperature = 293 #K
oxygen.set_density("g/cm3", 8.77)"""
    
mats = openmc.Materials([castBronze])#, oxygen])
mats.export_to_xml()

# GEOMETRY
#Making cylinder
cylinderSurface = openmc.ZCylinder(r=0.1)
upperSurface = openmc.ZPlane(z0=0.5)
lowerSurface = openmc.ZPlane(z0=-0.5)

#Converting into regions
cylinderInside = -cylinderSurface & -upperSurface & +lowerSurface


# Create cells, mapping materials to cells
cylinder = openmc.Cell(name='cylinder')
cylinder.fill = castBronze
cylinder.region = cylinderInside


# Create a geometry and export to XML
root_universe = openmc.Universe(cells=[cylinder])
geom = openmc.Geometry(root_universe)                    
geom.export_to_xml()  

root_universe.plot(width=(2,2))
root_universe.plot(width=(2,2), basis='xz')

"""
#Creating file to be displayed in paraview
vox_plot = openmc.Plot()
vox_plot.type = 'voxel'
vox_plot.width = (1500., 1500., 1500.)
vox_plot.pixels = (200, 200, 200)
vox_plot.color_by = 'material'
vox_plot.colors = {castBronze: 'yellow'}#, oxygen: 'red'}  # materials can be coloured using this command
vox_plot.to_vtk(output='cylinder.vti')
"""
