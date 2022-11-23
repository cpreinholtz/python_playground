#!/usr/bin/env python 
import matplotlib.pyplot as plt

import numpy as np
from skimage import data
#from skimage.viewer import ImageViewer

#row, col, channelrgb

imShape = (255, 255**2, 3)

image = np.zeros(imShape, dtype = 'int16')

image[]







fig = plt.figure()
plot1 = fig.add_subplot(1,1,1)
imgplot = plot1.imshow(image)
plt.show()

#viewer = ImageViewer(image)
#viewer.show()