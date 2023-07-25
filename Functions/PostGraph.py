%matplotlib inline
from IPython.display import Image
import numpy as np
import matplotlib.pyplot as plt
import openmc
import os


sp = openmc.StatePoint('statepoint.10.h5')
tally = sp.get_tally(scores=['flux'])

flux = tally.get_slice(scores=['flux'])
#flux.std_dev.shape = (100, 100)
#flux.mean.shape = (100, 100)
fig = plt.subplot(121)
fig.imshow(flux.mean)
