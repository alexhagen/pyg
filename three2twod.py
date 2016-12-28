import twod
import matplotlib.image as mpimg
import numpy as np
from matplotlib.patches import Ellipse, Polygon, Circle
from colour import Color

class ann_im(twod.pyg2d):
    def __init__(self, im_filename, proj_matrix):
        super(ann_im, self).__init__()
        img = mpimg.imread(im_filename)
        self.ax.set_axis_off()
        self.ax.imshow(img, interpolation='gaussian')
        self.proj_matrix = proj_matrix

    def convert_3d_to_2d(self, x, y, z):
        arr = np.array([x, y, z, 1.])
        mat = np.array(self.proj_matrix).T
        pcam = np.matmul(arr, mat)
        pcam /= pcam[2]
        print pcam
        x = pcam[0]
        y = pcam[1]
        return x, y

    def add_data_pointer(self, x, y, z, string='', place='down-right'):
        x,y = self.convert_3d_to_2d(x, y, z)
        print x,y
        if isinstance(place, tuple):
            place = (x + place[0], y - place[1])
        elif 'up' in place:
            place = place.replace('up','down')
        elif 'down' in place:
            place = place.replace('down', 'up')

        super(ann_im, self).add_data_pointer(x, point=y, string=string,
                                             place=place)

    def add_legend_entry(self, color=None, alpha=1.0, name=''):
        patch = self.ax.add_patch(Polygon([[0, 0], [0, 0], [0, 0]],
                               facecolor=color, alpha=alpha, label=name))
        self.bars[name] = patch
