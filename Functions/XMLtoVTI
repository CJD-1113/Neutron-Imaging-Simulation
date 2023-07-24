#Creating file to be displayed in paraview
vox_plot = openmc.Plot()
vox_plot.type = 'voxel'
vox_plot.width = (1500., 1500., 1500.)
vox_plot.pixels = (200, 200, 200)
vox_plot.color_by = 'material'
vox_plot.colors = {castBronze: 'yellow'}#, oxygen: 'red'}  # materials can be coloured using this command
vox_plot.to_vtk(output='cylinder.vti')
