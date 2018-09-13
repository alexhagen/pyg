from colour import Color as _c
from matplotlib.colors import LinearSegmentedColormap
from copy import copy, deepcopy
import numpy as np

pnnl_colors = {'black': '#000000',
               'white': '#ffffff',
               'orange': '#D77600',
               'lightblue': '#748EB3',
               'blue': '#3b73af',
               'darkblue': '#00338E',
               'gray': '#606060',
               'graydark': '#707276',
               'lightgray': '#eeeeee',
               'lightgreen': '#68AE8C',
               'green': '#719500',
               'purple': '#9682B3',
               'teal': '#66B6CD',
               'red': '#BE0F34',
               'copper': '#D77600',
               'silver': '#616265',
               'bronze': '#A63F1E',
               'gold': '#F4AA00',
               'platinum': '#B3B3B3',
               'onyx': '#191C1F',
               'emerald': '#007836',
               'sapphire': '#00338E',
               'ruby': '#BE0F34',
               'mercury': '#7E9AA9',
               'topaz': '#0081AB',
               'amethyst': '#502D7F',
               'garnet': '#870150',
               'emslgreen': '#719500'}
# Now we need to add the tints - note that these may not match exactly the
# tints on reputation.pnl.gov - however they are computed correctly
pnnl_colors.update({'copper40': '#967040',
                    'copper50': '#A17136',
                    'copper60': '#AC722B',
                    'copper70': '#B77320',
                    'copper80': '#C17415',
                    'silver40': '#3B4F8B',
                    'silver50': '#314A94',
                    'silver60': '#28459E',
                    'silver70': '#1E40A8',
                    'silver80': '#143BB2',
                    'bronze40': '#894E3B',
                    'bronze50': '#934931',
                    'bronze60': '#9D4427',
                    'bronze70': '#A73F1D',
                    'bronze80': '#B03A14',
                    'gold40': '#AB8D49',
                    'gold50': '#B7923D',
                    'gold60': '#C39731',
                    'gold70': '#CF9C25',
                    'gold80': '#DCA018',
                    'platinum40': '#D19595',
                    'platinum50': '#D98D8D',
                    'platinum60': '#E18585',
                    'platinum70': '#E87E7E',
                    'platinum80': '#F07676',
                    'onyx40': '#111C27',
                    'onyx50': '#0E1C2A',
                    'onyx60': '#0B1C2D',
                    'onyx70': '#081C30',
                    'onyx80': '#061C32',
                    'emerald40': '#24543A',
                    'emerald50': '#1E5A39',
                    'emerald60': '#186038',
                    'emerald70': '#126638',
                    'emerald80': '#0C6C37',
                    'sapphire40': '#2B3F63',
                    'sapphire50': '#233D6A',
                    'sapphire60': '#1C3B72',
                    'sapphire70': '#153979',
                    'sapphire80': '#0E3780',
                    'ruby40': '#8F3D4F',
                    'ruby50': '#9A3349',
                    'ruby60': '#A42943',
                    'ruby70': '#AE1F3D',
                    'ruby80': '#B81437',
                    'mercury40': '#68A0BE',
                    'mercury50': '#5EA4C9',
                    'mercury60': '#53A7D4',
                    'mercury70': '#48AADF',
                    'mercury80': '#3DADE9',
                    'topaz40': '#336778',
                    'topaz50': '#2B6B80',
                    'topaz60': '#227089',
                    'topaz70': '#1A7491',
                    'topaz80': '#11789A',
                    'amethyst40': '#513478',
                    'amethyst50': '#502B81',
                    'amethyst60': '#4E228A',
                    'amethyst70': '#4D1A92',
                    'amethyst80': '#4C119B',
                    'garnet40': '#5F2949',
                    'garnet50': '#66224A',
                    'garnet60': '#6D1B4B',
                    'garnet70': '#74144D',
                    'garnet80': '#7A0E4E',
                    'emslgreen40': '#5A682D',
                    'emslgreen50': '#5E7025',
                    'emslgreen60': '#62771E',
                    'emslgreen70': '#657F16',
                    'emslgreen80': '#69860F'})
c = pnnl_colors

start_c = _c(pnnl_colors["silver"])
brand_cmap = list(start_c.range_to(_c(pnnl_colors["copper"]), 256))
cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in brand_cmap]
brand_cmap_mpl = LinearSegmentedColormap.from_list('brand_cmap', cmap_tuple_list)
brand_cmap = []
end_c = _c(pnnl_colors['copper'])
for s, l in zip(np.linspace(0.0, end_c.saturation, 256),
                np.linspace(0.97, end_c.luminance, 256)):
    __color__ = deepcopy(end_c)
    __color__.saturation = s
    __color__.luminance = l
    brand_cmap.append(deepcopy(__color__))
cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in brand_cmap]
brand_cmap_mpl = LinearSegmentedColormap.from_list('brand_cmap', cmap_tuple_list)


start_c = _c(pnnl_colors["blue"])
end_c = _c(pnnl_colors['copper'])
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
