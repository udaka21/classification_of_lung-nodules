"""
==========================================================
Load CT slices and plot axial, sagittal and coronal images
==========================================================

This example illustrates loading multiple files, sorting them by slice
location, building a 3D image and reslicing it in different planes.

.. usage:

   reslice.py <glob>
   where <glob> refers to a set of DICOM image files.

   Example: python reslice.py "*.dcm". The quotes are needed to protect
   the glob from your system and leave it for the script.

.. note:

   Uses numpy and matplotlib.

   Tested using series 2 from here
   http://www.pcir.org/researchers/54879843_20060101.html
"""

import pydicom
import numpy as np
import matplotlib.pyplot as plt
import sys
import glob

# load the DICOM files
filepath="/home/tung/CT_lung/Dataset/SPIE-AAPM Lung CT Challenge/CT-Training-BE010/04-27-2007-8438-CT INFUSED CHEST-568.1/5-HIGH RES-86.27/*.dcm"
#nodule location
node_z=69
node_y=120
node_x=336
#extracted size
x=32
y=32
z=32


files = []
print('glob: {}'.format(filepath))
for fname in glob.glob(filepath, recursive=False):
    print("loading: {}".format(fname))
    files.append(pydicom.dcmread(fname))

print("file count: {}".format(len(files)))

# skip files with no SliceLocation (eg scout views)
slices = []
skipcount = 0
for f in files:
    if hasattr(f, 'SliceLocation'):
        slices.append(f)
    else:
        skipcount = skipcount + 1

print("skipped, no SliceLocation: {}".format(skipcount))

# ensure they are in the correct order
slices = sorted(slices, key=lambda s: s.SliceLocation)

# pixel aspects, assuming all slices are the same
ps = slices[0].PixelSpacing
ss = slices[0].SliceThickness
ax_aspect = ps[1]/ps[0]
sag_aspect = ps[1]/ss
cor_aspect = ss/ps[0]

# create 3D array
img_shape = list(slices[0].pixel_array.shape)
img_shape.append(len(slices))
img3d = np.zeros(img_shape)

# fill 3D array with the images from the files
for i, s in enumerate(slices):
    img2d = s.pixel_array
    img3d[:, :, i] = img2d

#extracting nodules location
node3d=img3d[(node_x-x//2):(node_x+x//2),(node_y-y//2):(node_y+y//2),(node_z-z//2):(node_z+z//2)]
print(node3d.shape)

#plot 3 orthogonal slices
a1 = plt.subplot(2, 3, 1)
plt.imshow(node3d[:, :, node3d.shape[2]//2])
#a1.set_aspect(ax_aspect)

a2 = plt.subplot(2, 3, 2)
plt.imshow(node3d[:, node3d.shape[1]//2, :])
#a2.set_aspect(sag_aspect)

a3 = plt.subplot(2, 3, 3)
plt.imshow(node3d[node3d.shape[0]//2, :, :].T)
#a3.set_aspect(cor_aspect)

#node image
a4 = plt.subplot(2, 3, 4)
plt.imshow(img3d[ :, :,node_z])
a4.set_aspect(ax_aspect)

a5 = plt.subplot(2, 3, 5)
plt.imshow(img3d[ :, node_y,:])
a5.set_aspect(sag_aspect)

a6 = plt.subplot(2, 3, 6)
plt.imshow(img3d[ node_x, :,:].T)
a6.set_aspect(cor_aspect)

plt.show()

