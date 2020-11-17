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
import copy

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
            ax1 = self.ax
            ax1.imshow(img, interpolation='nearest', zorder=0)
            ax2 = self.fig.add_axes(self.ax.get_position())
            ax2.set_axis_off()
            ax2.set_facecolor('none')
            ax2.set_xlim(ax1.get_xlim())
            ax2.set_ylim(ax1.get_ylim())
            self.ax = ax2

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
        ax.imshow(img, interpolation='gaussian', zorder=0)
        ax2 = self.fig.add_axes([blx, bly, w, h])
        ax2.set_axis_off()
        ax2.set_facecolor('transparent')
        self.ax = ax2
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
                                             place=place, axes=self.ax, **kwargs)
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
                                             place=place, axes=self.ax, **kwargs)
        return self

    def add_arrow(self, x1, x2, y1, y2, z1, z2, **kwargs):
        x1, y1 = self.convert_3d_to_2d(x1, y1, z1)
        x2, y2 = self.convert_3d_to_2d(x2, y2, z2)
        super(ann_im, self).add_arrow(x1, x2, y1, y2, zorder=100, axes=self.ax, **kwargs)
        return self

    def add_line(self, x1, x2, y1, y2, z1, z2, **kwargs):
        x1, y1 = self.convert_3d_to_2d(x1, y1, z1)
        x2, y2 = self.convert_3d_to_2d(x2, y2, z2)
        #ap = dict(arrowstyle="-", fc=fc, ec=fc, alpha=alpha)
        super(ann_im, self).add_line([x1, x2], [y1, y2], zorder=100, axes=self.ax, **kwargs)
        #super(ann_im, self).add_arrow(x1, x2, y1, y2, **kwargs)
        return self

    def add_angle(self, c=(0.0, 0.0, 0.0), p1=(0.0, 0.0, 1.0), p2=(0.0, 1.0, 0.0), angle0=None, angle1=None, textangle=None,
                  **kwargs):
        c = np.array(c)
        p1 = np.array(p1)
        p2 = np.array(p2)
        v1 = p1 - c
        v2 = p2 - c
        r1 = np.sqrt(np.sum(np.power(v1, 2.0)))
        r2 = np.sqrt(np.sum(np.power(v2, 2.0)))
        # this is a vector normal to the plane
        n = np.cross(v1, v2)
        # now solve for a vector where dot(u, v) = 0 and dot(u, n) = 0
        u = np.cross(n, v1)
        u = r2*u/np.sqrt(np.sum(np.power(u, 2.0)))
        v1 = v1 / np.sqrt(np.sum(np.power(v1, 2.0)))
        u = u / np.sqrt(np.sum(np.power(u, 2.0)))
        # now find the second vector (this one should be 90deg from p1 in the same plane as p1 and p2)
        xc = c[0]
        x1 = v1[0]
        x2 = u[0]
        yc = c[1]
        y1 = v1[1]
        y2 = u[1]
        zc = c[2]
        z1 = v1[2]
        z2 = u[2]
        xs = []
        ys = []
        zs = []
        if angle0 is None:
            angle0 = 0.0
        if angle1 is None:
            angle1 = np.arccos((x1*x2 + y1*y2 + z1*z2) / (r1 + r2))
        for phi in np.linspace(angle0, angle1, 25):
            xi = xc + r1*np.cos(phi)*x1 + r2*np.sin(phi)*x2
            yi = yc + r1*np.cos(phi)*y1 + r2*np.sin(phi)*y2
            zi = zc + r1*np.cos(phi)*z1 + r2*np.sin(phi)*z2
            xs.append(xi)
            ys.append(yi)
            zs.append(zi)
        _xs = []
        _ys = []
        for x, y, z in zip(xs, ys, zs):
            _x, _y = self.convert_3d_to_2d(x, y, z)
            _xs.append(_x)
            _ys.append(_y)
        super(ann_im, self).add_line(_xs, _ys, axes=self.ax, **kwargs)
        return self

    def get_pos_by_angle(self, c=(0.0, 0.0, 0.0), p1=(0.0, 0.0, 1.0), p2=(0.0, 1.0, 0.0), angle=None):
        c = np.array(c)
        p1 = np.array(p1)
        p2 = np.array(p2)
        v1 = p1 - c
        v2 = p2 - c
        r1 = np.sqrt(np.sum(np.power(v1, 2.0)))
        r2 = np.sqrt(np.sum(np.power(v2, 2.0)))
        # this is a vector normal to the plane
        n = np.cross(v1, v2)
        # now solve for a vector where dot(u, v) = 0 and dot(u, n) = 0
        u = np.cross(n, v1)
        u = r2*u/np.sqrt(np.sum(np.power(u, 2.0)))
        v1 = v1 / np.sqrt(np.sum(np.power(v1, 2.0)))
        u = u / np.sqrt(np.sum(np.power(u, 2.0)))
        # now find the second vector (this one should be 90deg from p1 in the same plane as p1 and p2)
        xc = c[0]
        x1 = v1[0]
        x2 = u[0]
        yc = c[1]
        y1 = v1[1]
        y2 = u[1]
        zc = c[2]
        z1 = v1[2]
        z2 = u[2]
        xi = xc + r1*np.cos(angle)*x1 + r2*np.sin(angle)*x2
        yi = yc + r1*np.cos(angle)*y1 + r2*np.sin(angle)*y2
        zi = zc + r1*np.cos(angle)*z1 + r2*np.sin(angle)*z2
        return xi, yi, zi

    def add_anglemeasure(self, c=(0.0, 0.0, 0.0), p1=(0.0, 0.0, 1.0), p2=(0.0, 1.0, 0.0), angle=None, textangle=None, string='', **kwargs):
        kwargs_plot = copy.copy(kwargs)
        if 'color' in kwargs.keys():
            kwargs_plot['linecolor'] = kwargs['color']
            del kwargs_plot['color']
        self.add_line(c[0], p1[0], c[1], p1[1], c[2], p1[2], **kwargs_plot)
        self.add_line(c[0], p2[0], c[1], p2[1], c[2], p2[2], **kwargs_plot)
        if textangle is None:
            textangle = 0.1
        self.add_angle(c=c, p1=p1, p2=p2, angle0=0.0, angle1=(0.5 - textangle)*angle, **kwargs_plot)
        self.add_angle(c=c, p1=p1, p2=p2, angle0=(0.5 + textangle)*angle, angle1=angle, **kwargs_plot)
        textx, texty, textz = self.get_pos_by_angle(c, p1, p2, angle=0.5*angle)
        self.add_text(textx, texty, textz, string=string, **kwargs)
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
        super(ann_im, self).add_text(x, y, string=string, axes=self.ax, **kwargs)
        return self

    def add_xmeasure(self, x1, x2, y1, z1, string=None, place=None, offset=0.01,
                     axes=None, units='', fc='0.3'):
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
                     axes=None, units='', fc='0.3'):
        if axes is None:
            axes = self.ax
        if string is None:
            string = r"$%.0f\,\mathrm{" % np.sqrt((y2 - y1)**2.0) + units + "}$"
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
                     axes=None, units='', fc='0.3'):
        if axes is None:
            axes = self.ax
        if string is None:
            string = r"$%.0f\,\mathrm{" % np.sqrt((z2 - z1)**2.0) + units + "}$"
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
