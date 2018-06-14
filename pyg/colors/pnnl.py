from colour import Color as _c
from matplotlib.colors import LinearSegmentedColormap

pnnl_colors = {'black': '#000000',
               'white': '#ffffff',
               'orange': '#d57500',
               'lightblue': '#748EB3',
               'blue': '#3b73af',
               'darkblue': '#0077a4',
               'gray': '#606060',
               'graydark': '#707276',
               'lightgray': '#eeeeee',
               'lightgreen': '#68AE8C',
               'green': '#719500',
               'purple': '#9682B3',
               'teal': '#66B6CD',
               'red': '#D97985'}
c = pnnl_colors

start_c = _c(pnnl_colors["gray"])
brand_cmap = list(start_c.range_to(_c(pnnl_colors["orange"]), 256))
cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in brand_cmap]
brand_cmap_mpl = LinearSegmentedColormap.from_list('brand_cmap', cmap_tuple_list)


from copy import copy, deepcopy
import numpy as np
start_c = _c(pnnl_colors["blue"])
end_c = _c(pnnl_colors['orange'])
first_half = []
for s, l in zip(np.linspace(start_c.saturation, 0.0, 128),
                np.linspace(start_c.luminance, 0.97, 128)):
    __color__ = deepcopy(start_c)
    __color__.saturation = s
    __color__.luminance = l
    first_half.append(deepcopy(__color__))
second_half = []
for s, l in zip(np.linspace(0.0, end_c.saturation, 128),
                np.linspace(0.97, end_c.luminance, 128)):
    __color__ = deepcopy(end_c)
    __color__.saturation = s
    __color__.luminance = l
    second_half.append(deepcopy(__color__))
#first_half = [copy(start_c).set_saturation(num) for num in np.linspace(start_c.saturation, 0.0, 128)]
jet_cmap = first_half + second_half
'''
black = pu_colors['black']
gray = pu_colors['gray']
gray_dark = pu_colors['darkgray']
gray_darker = pu_colors['browngray']
gray_light = pu_colors['tan']
gray_lighter = pu_colors['lightgray']
brand_primary = pu_colors['newgold']
brand_success = pu_colors['green']
brand_info = pu_colors['teal']
brand_warning = pu_colors['yellow']
brand_error = pu_colors['red']
brand_off = pu_colors['purple']


desat = _c(pu_colors["blue"])
desat.saturation = 0.0
desat.luminance = 0.1
flow_cmap = list(desat.range_to(_c(pu_colors["blue"]), 256))
desat = _c(pu_colors["newgold"])
desat.saturation = 0.0
desat.luminance = 0.1
brand_cmap = list(desat.range_to(_c(pu_colors["newgold"]), 256))
desat = _c(pu_colors["red"])
desat.saturation = 0.0
desat.luminance = 0.75
flame_cmap = list(desat.range_to(_c(pu_colors["red"]), 256))
desat = _c(pu_colors["teal"])
desat.saturation = 0.0
desat.luminance = 0.9
teal_cmap = list(desat.range_to(_c(pu_colors["teal"]), 256))
desat = _c(pu_colors["white"])
bw_cmap = list(desat.range_to(_c(pu_colors["black"]), 256))

start_c = _c(pu_colors["blue"])
mid_c = _c(pu_colors["green"])
pu_jet_cmap = list(start_c.range_to(mid_c, 128)) + list(mid_c.range_to(c(pu_colors["red"]), 128))

start_c = _c(pu_colors["darkgray"])
brand_cmap = list(start_c.range_to(_c(pu_colors["newgold"]), 256))
'''
