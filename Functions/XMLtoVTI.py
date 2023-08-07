#Creating file to be displayed in paraview
plot = openmc.Plot()
plot.type = 'voxel'
plot.width = (100., 100., 60.)
plot.pixels = (400, 400, 200)
plot.basis = 'yz'
plot.origin = (5.0, 2.0, 3.0)
plot.color_by = 'material'
plot.colors = {
    airmix: 'blue',
    castBronze: 'black'
}

plots = openmc.Plots()
plots.append(plot)
plots.export_to_xml()
plot.to_vtk(output='cylinder.vti')
