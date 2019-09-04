from . import twod
import matplotlib.image as mpimg
import matplotlib.transforms as mptrans
import numpy as np
from matplotlib.patches import Ellipse, Polygon, Circle
from matplotlib.image import BboxImage, AxesImage
from colour import Color
import os
import copyreg
import types

def _pickle_method(method):
    func_name = method.im_func.__name__
    obj = method.im_self
    cls = method.im_class
    return _unpickle_method, (func_name, obj, cls)

def _unpickle_method(func_name, obj, cls):
    for cls in cls.mro():
        try:
            func = cls.__dict__[func_name]
        except KeyError:
            pass
        else:
            break
        return func.__get__(obj, cls)

copyreg.pickle(types.MethodType, _pickle_method, _unpickle_method)

class ann_im(twod.pyg2d):
    def __init__(self, im_filename, proj_matrix=None):
        super(ann_im, self).__init__()
        self.axes_stack = {}
        self.ax.set_axis_off()
        if im_filename is not None:
            img = mpimg.imread(im_filename)
            self.im_filename = im_filename
            self.ax.set_facecolor('white')
            #self.aximg = self.ax.figure.figimage(img, 0.0, 0.0, resize=False)
            ##self.aximg.set_clip_path(False)
            #self.aximg.set_clip_path(None)
            #self.aximg.set_clip_box(None)
            #print(self.aximg.magnification)
            #self.aximg.magnification(2.0)
            ##tform = mptrans.Affine2D().scale(2.0)
            ##self.aximg.set_transform(tform)
            #print(dir(self.aximg))
            #print(img.shape)
            #self.xlim(0, img.shape[1])
            #self.ylim(0, img.shape[0])
            self.ax.imshow(img, interpolation='nearest')
            #self.fig.figimage(img, xo, yo, resize=True, origin='lower')
            if proj_matrix is None:
                self.get_proj_matrix()
            else:
                self.proj_matrix = proj_matrix
        self.axes_stack['main'] = (self.ax, proj_matrix)

    def move_axis(self, ax, bl, tr):
        blx = bl[0]
        bly = bl[1]
        w = tr[0] - blx
        h = tr[1] - bly
        ax.set_position([blx, bly, w, h], which='original')
        return self

    def add_axis(self, im_filename, bl, tr, name='additional_axis'):
        blx = bl[0]
        bly = bl[1]
        w = tr[0] - blx
        h = tr[1] - bly
        ax = self.fig.add_axes([blx, bly, w, h])
        ax.set_axis_off()
        ax.set_facecolor('white')
        img = mpimg.imread(im_filename)
        img2 = np.zeros_like(img)
        ax.imshow(img, interpolation='gaussian')
        pmatrix = self.get_proj_matrix(fname=im_filename)
        self.axes_stack[name] = (ax, pmatrix)
        return self

    def get_proj_matrix(self, fname=None):
        if fname is None:
            fname = self.im_filename
        proj_matrix = \
            os.popen("identify -verbose %s | grep proj_matrix" % fname).read()
        namespace = {}
        exec(proj_matrix.replace(" ", "").replace(":", "="), namespace)
        self.proj_matrix = namespace['proj_matrix']

    def convert_3d_to_2d(self, x, y, z, proj_matrix=None):
        if proj_matrix is None:
            proj_matrix = self.proj_matrix
        arr = np.array([x, y, z, 1.])
        mat = np.array(proj_matrix).T
        mat = mat.astype(float)
        pcam = np.matmul(arr, mat)
        pcam /= pcam[2]
        # print pcam
        x = pcam[0]
        y = pcam[1]
        return x, y

    def add_data_pointer(self, x, y, z, string='', place='down-right', **kwargs):
        if 'axes' in kwargs:
            if isinstance(kwargs['axes'], str):
                axname = kwargs['axes']
                #print axname
                axes = self.axes_stack[axname][0]
                proj_matrix = self.axes_stack[axname][1]
                kwargs['axes'] = axes
        else:
            axes = self.ax
            proj_matrix = self.proj_matrix
        x,y = self.convert_3d_to_2d(x, y, z, proj_matrix=proj_matrix)
        #print x, y, kwargs
        if isinstance(place, tuple):
            place = (x + place[0], y - place[1])
        elif 'up' in place:
            place = place.replace('up','down')
        elif 'down' in place:
            place = place.replace('down', 'up')

        super(ann_im, self).add_data_pointer(x, point=y, string=string,
                                             place=place, **kwargs)
        return self

    def add_2d_data_pointer(self, x, y,  string='', place='down-right',
                            **kwargs):
        if 'axes' in kwargs:
            if isinstance(kwargs['axes'], str):
                axname = kwargs['axes']
                #print axname
                axes = self.axes_stack[axname][0]
                proj_matrix = self.axes_stack[axname][1]
                kwargs['axes'] = axes
        else:
            axes = self.ax
            proj_matrix = self.proj_matrix
        if isinstance(place, tuple):
            place = (x + place[0], y - place[1])
        elif 'up' in place:
            place = place.replace('up','down')
        elif 'down' in place:
            place = place.replace('down', 'up')

        super(ann_im, self).add_data_pointer(x, point=y, string=string,
                                             place=place, **kwargs)
        return self

    def add_arrow(self, x1, x2, y1, y2, z1, z2, **kwargs):
        x1, y1 = self.convert_3d_to_2d(x1, y1, z1)
        x2, y2 = self.convert_3d_to_2d(x2, y2, z2)
        super(ann_im, self).add_arrow(x1, x2, y1, y2, **kwargs)
        return self

    def add_text(self, x, y, z, string=None, **kwargs):
        if 'axes' in kwargs:
            if isinstance(kwargs['axes'], str):
                axname = kwargs['axes']
                #print axname
                axes = self.axes_stack[axname][0]
                proj_matrix = self.axes_stack[axname][1]
                kwargs['axes'] = axes
        else:
            axes = self.ax
            proj_matrix = self.proj_matrix
        x, y = self.convert_3d_to_2d(x, y, z, proj_matrix=proj_matrix)
        super(ann_im, self).add_text(x, y, string=string, **kwargs)
        return self

    def add_xmeasure(self, x1, x2, y1, z1, string=None, place=None, offset=0.01,
                     axes=None, units='', fc='black'):
        if axes is None:
            axes = self.ax
        if string is None:
            string = r"$%.0f\,\mathrm{" % np.sqrt((x2 - x1)**2.0) + units + "}$"
        if place is None:
            place = "up"
        total_width = np.max(axes.get_ylim()) - np.min(axes.get_ylim())
        length = 0.05
        lw = 0.5
        _x1, _y1 = self.convert_3d_to_2d(x1, y1, z1)
        _x2, _y2 = self.convert_3d_to_2d(x2, y1, z1)
        x_mid = (_x2 + _x1) / 2.0
        y_mid = (_y1 + _y2) / 2.0
        h3 = super(ann_im, self).add_arrow(x_mid, _x1, y_mid, _y1, fc=fc,
                            string=self.latex_string(string), axes=axes)
        h4 = super(ann_im, self).add_arrow(x_mid, _x2, y_mid, _y2, fc=fc,
                            string=self.latex_string(string), axes=axes)
        self.allartists.append((h3, h4))
        return self

    def add_ymeasure(self, x1, y1, y2, z1, string=None, place=None, offset=0.01,
                     axes=None, units='', fc='black'):
        if axes is None:
            axes = self.ax
        if string is None:
            string = r"$%.0f\,\mathrm{" % np.sqrt((x2 - x1)**2.0) + units + "}$"
        if place is None:
            place = "up"
        total_width = np.max(axes.get_ylim()) - np.min(axes.get_ylim())
        length = 0.05
        lw = 0.5
        _x1, _y1 = self.convert_3d_to_2d(x1, y1, z1)
        _x2, _y2 = self.convert_3d_to_2d(x1, y2, z1)
        x_mid = (_x2 + _x1) / 2.0
        y_mid = (_y1 + _y2) / 2.0
        h3 = super(ann_im, self).add_arrow(x_mid, _x1, y_mid, _y1, fc=fc,
                            string=self.latex_string(string), axes=axes)
        h4 = super(ann_im, self).add_arrow(x_mid, _x2, y_mid, _y2, fc=fc,
                            string=self.latex_string(string), axes=axes)
        self.allartists.append((h3, h4))
        return self

    def add_zmeasure(self, x1, y1, z1, z2, string=None, place=None, offset=0.01,
                     axes=None, units='', fc='black'):
        if axes is None:
            axes = self.ax
        if string is None:
            string = r"$%.0f\,\mathrm{" % np.sqrt((x2 - x1)**2.0) + units + "}$"
        if place is None:
            place = "up"
        total_width = np.max(axes.get_ylim()) - np.min(axes.get_ylim())
        length = 0.05
        lw = 0.5
        _x1, _y1 = self.convert_3d_to_2d(x1, y1, z1)
        _x2, _y2 = self.convert_3d_to_2d(x1, y1, z2)
        x_mid = (_x2 + _x1) / 2.0
        y_mid = (_y1 + _y2) / 2.0
        h3 = super(ann_im, self).add_arrow(x_mid, _x1, y_mid, _y1, fc=fc,
                            string=self.latex_string(string), axes=axes)
        h4 = super(ann_im, self).add_arrow(x_mid, _x2, y_mid, _y2, fc=fc,
                            string=self.latex_string(string), axes=axes)
        self.allartists.append((h3, h4))
        return self

    def add_legend_entry(self, color=None, alpha=1.0, name=''):
        patch = self.ax.add_patch(Polygon([[0, 0], [0, 0], [0, 0]],
                               facecolor=color, alpha=alpha, label=name))
        self.bars[name] = patch
        return self

    def export(self, *args, **kwargs):
        kwargs['force_pdf'] = True
        super(ann_im, self).export(*args, **kwargs)
