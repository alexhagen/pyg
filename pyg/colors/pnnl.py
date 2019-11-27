#from colour import Color as _c

try:
    from colour.colour import Color as _c
except ModuleNotFoundError:
    from colour import Color as _c
#from colour.colour import Color as _c
from matplotlib.colors import LinearSegmentedColormap
#import matplotlib.pyplot as plt
from copy import copy, deepcopy
import numpy as np
#from cycler import cycler

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
pnnl_colors.update({'copper40': '#EFC899',
                    'copper50': '#EBBA7F',
                    'copper60': '#E7AD66',
                    'copper70': '#E39F4C',
                    'copper80': '#DF9133',
                    'silver40': '#C0C0C1',
                    'silver50': '#B0B0B2',
                    'silver60': '#A0A1A3',
                    'silver70': '#909193',
                    'silver80': '#818184',
                    'bronze40': '#DBB2A5',
                    'bronze50': '#D29F8E',
                    'bronze60': '#CA8C78',
                    'bronze70': '#C17961',
                    'bronze80': '#B8654B',
                    'gold40': '#FBDD99',
                    'gold50': '#F9D47F',
                    'gold60': '#F8CC66',
                    'gold70': '#F7C34C',
                    'gold80': '#F6BB33',
                    'platinum40': '#E1E1E1',
                    'platinum50': '#D9D9D9',
                    'platinum60': '#D1D1D1',
                    'platinum70': '#CACACA',
                    'platinum80': '#C2C2C2',
                    'onyx40': '#A3A4A5',
                    'onyx50': '#8C8D8F',
                    'onyx60': '#757779',
                    'onyx70': '#5E6062',
                    'onyx80': '#47494C',
                    'emerald40': '#99C9AF',
                    'emerald50': '#7FBB9A',
                    'emerald60': '#66AE86',
                    'emerald70': '#4CA072',
                    'emerald80': '#33935E',
                    'sapphire40': '#99ADD2',
                    'sapphire50': '#7F99C6',
                    'sapphire60': '#6685BB',
                    'sapphire70': '#4C70B0',
                    'sapphire80': '#335CA5',
                    'ruby40': '#E59FAE',
                    'ruby50': '#DE8799',
                    'ruby60': '#D86F85',
                    'ruby70': '#D15771',
                    'ruby80': '#CB3F5D',
                    'mercury40': '#CBD7DD',
                    'mercury50': '#BECCD4',
                    'mercury60': '#B2C2CB',
                    'mercury70': '#A5B8C3',
                    'mercury80': '#98AEBA',
                    'topaz40': '#99CDDD',
                    'topaz50': '#7FC0D5',
                    'topaz60': '#66B3CD',
                    'topaz70': '#4CA7C4',
                    'topaz80': '#339ABC',
                    'amethyst40': '#B9ABCC',
                    'amethyst50': '#A796BF',
                    'amethyst60': '#9681B2',
                    'amethyst70': '#846CA5',
                    'amethyst80': '#735799',
                    'garnet40': '#CF99B9',
                    'garnet50': '#C380A7',
                    'garnet60': '#B76796',
                    'garnet70': '#AB4D84',
                    'garnet80': '#9F3473',
                    'emslgreen40': '#C6D599',
                    'emslgreen50': '#B8CA7F',
                    'emslgreen60': '#AABF66',
                    'emslgreen70': '#9CB54C',
                    'emslgreen80': '#8DAA33'})
c = pnnl_colors

start_c = _c(pnnl_colors["silver"])
brand_cmap = list(start_c.range_to(_c(pnnl_colors["copper"]), 256))
cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in brand_cmap]
brand_cmap_mpl = LinearSegmentedColormap.from_list('brand_cmap', cmap_tuple_list)
brand_cmap = []
end_c = _c(pnnl_colors['copper'])
for s, l in zip(np.linspace(0.0, end_c.saturation, 256),
                np.linspace(0.80, end_c.luminance, 256)):
    __color__ = deepcopy(end_c)
    __color__.saturation = s
    __color__.luminance = l
    brand_cmap.append(deepcopy(__color__))
cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in brand_cmap]
brand_cmap_mpl = LinearSegmentedColormap.from_list('brand_cmap', cmap_tuple_list)

def brand_blue(mpl=True, a_low=0.2, a_high=1.0):
    start_c = _c(pnnl_colors["white"])
    brand_blue_cmap = list(start_c.range_to(_c(pnnl_colors["sapphire"]), 256))
    cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in brand_blue_cmap]
    brand_blue_cmap_mpl = LinearSegmentedColormap.from_list('brand_blue_cmap', cmap_tuple_list)
    alphas = np.linspace(a_low, a_high, len(cmap_tuple_list))
    cmap_tuple_list = [(__c.red, __c.green, __c.blue, a) for __c, a in zip(brand_blue_cmap, alphas)]
    return LinearSegmentedColormap.from_list('brand_blue_cmap', cmap_tuple_list)

def brand(mpl=True, a_low=0.2, a_high=1.0):
    start_c = _c(pnnl_colors["white"])
    brand_cmap = list(start_c.range_to(_c(pnnl_colors["copper"]), 256))
    cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in brand_cmap]
    brand_cmap_mpl = LinearSegmentedColormap.from_list('brand_cmap', cmap_tuple_list)
    alphas = np.linspace(a_low, a_high, len(cmap_tuple_list))
    cmap_tuple_list = [(__c.red, __c.green, __c.blue, a) for __c, a in zip(brand_cmap, alphas)]
    return LinearSegmentedColormap.from_list('brand_cmap', cmap_tuple_list)


start_c = _c(pnnl_colors["sapphire"])
mid_c = _c(pnnl_colors['silver'])
end_c = _c(pnnl_colors["gold"])

brand_dark_cmap = list(start_c.range_to(mid_c, 128)) + \
    list(mid_c.range_to(end_c, 128))
cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in brand_dark_cmap]
'''brand_dark_cmap_mpl = LinearSegmentedColormap.from_list('brand_dark_cmap', cmap_tuple_list)
brand_dark_cmap = []
end_c = _c(pnnl_colors['copper'])
for s, l in zip(np.linspace(0.0, end_c.saturation, 256),
                np.linspace(0.5, end_c.luminance, 256)):
    __color__ = deepcopy(end_c)
    __color__.saturation = s
    __color__.luminance = l
    brand_dark_cmap.append(deepcopy(__color__))
cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in brand_dark_cmap]'''
brand_dark_cmap_mpl = LinearSegmentedColormap.from_list('brand_dark_cmap', cmap_tuple_list)

start_c = _c(pnnl_colors["white"])
brandw_cmap = list(start_c.range_to(_c(pnnl_colors["copper"]), 256))
cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in brandw_cmap]
brandw_cmap_mpl = LinearSegmentedColormap.from_list('brandw_cmap', cmap_tuple_list)
brandw_cmap = []
end_c = _c(pnnl_colors['copper'])
for s, l in zip(np.linspace(0.0, end_c.saturation, 256),
                np.linspace(1.0, end_c.luminance, 256)):
    __color__ = deepcopy(end_c)
    __color__.saturation = s
    __color__.luminance = l
    brandw_cmap.append(deepcopy(__color__))
cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in brandw_cmap]
brandw_cmap_mpl = LinearSegmentedColormap.from_list('brandw_cmap', cmap_tuple_list)

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

start_c = _c(pnnl_colors["white"])
start1_c = _c(pnnl_colors['silver'])
mid1_c = _c(pnnl_colors['sapphire'])
mid_c = _c(pnnl_colors["topaz"])
end_c = _c(pnnl_colors['copper'])
N = 8
jet_gray_cmap = list(start_c.range_to(start1_c, N)) + list(mid1_c.range_to(mid_c, 128 - N//2)) + list(mid_c.range_to(end_c, 128 - N//2))
'''first_half = []
for s, l in zip(np.linspace(start_c.saturation, 0.0, 128),
                np.linspace(start_c.luminance, 0.375, 128)):
    __color__ = deepcopy(start_c)
    __color__.saturation = s
    __color__.luminance = l
    first_half.append(deepcopy(__color__))
second_half = []
for s, l in zip(np.linspace(0.0, end_c.saturation, 128),
                np.linspace(0.375, end_c.luminance, 128)):
    __color__ = deepcopy(end_c)
    __color__.saturation = s
    __color__.luminance = l
    second_half.append(deepcopy(__color__))
#first_half = [copy(start_c).set_saturation(num) for num in np.linspace(start_c.saturation, 0.0, 128)]
jet_gray_cmap = first_half + second_half'''
cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in jet_gray_cmap]
jet_cmap_mpl = LinearSegmentedColormap.from_list('jet_cmap', cmap_tuple_list)

c1 = _c(pnnl_colors["onyx"])
n1 = 160
c2 = _c(pnnl_colors['garnet'])
n2 = 16
c25 = _c(pnnl_colors['ruby'])
n25 = 16
c3 = _c(pnnl_colors['bronze'])
n3 = 16
c4 = _c(pnnl_colors["copper"])
n4 = 24
c5 = _c(pnnl_colors['gold'])
n5 = 24
c6 = _c(pnnl_colors['white'])
flame_cmap = list(c1.range_to(c2, n1)) + \
             list(c2.range_to(c25, n2)) + \
             list(c25.range_to(c3, n25)) + \
             list(c3.range_to(c4, n3)) + \
             list(c4.range_to(c5, n4)) + \
             list(c5.range_to(c6, n5)) + \
             list(c6.range_to(c6, 1))

cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in flame_cmap]
flame_cmap_mpl = LinearSegmentedColormap.from_list('flame_cmap', cmap_tuple_list)

flame_rev_cmap = flame_cmap[-1:0:-1]
cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in flame_rev_cmap]
flame_rev_cmap_mpl = LinearSegmentedColormap.from_list('flame_rev_cmap', cmap_tuple_list)

c1 = _c(pnnl_colors["onyx"])
n1 = 16
c2 = _c(pnnl_colors['garnet'])
n2 = 64
c25 = _c(pnnl_colors['ruby'])
n25 = 32
c3 = _c(pnnl_colors['bronze'])
n3 = 32
c4 = _c(pnnl_colors["copper"])
n4 = 32
c5 = _c(pnnl_colors['gold'])
n5 = 32
c6 = _c(pnnl_colors['white'])
flame_lowcon_cmap = list(c1.range_to(c2, n1)) + \
             list(c2.range_to(c25, n2)) + \
             list(c25.range_to(c3, n25)) + \
             list(c3.range_to(c4, n3)) + \
             list(c4.range_to(c5, n4)) + \
             list(c5.range_to(c6, n5)) + \
             list(c6.range_to(c6, 1))

cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in flame_lowcon_cmap]
flame_lowcon_cmap_mpl = LinearSegmentedColormap.from_list('flame_lowcon_cmap', cmap_tuple_list)

flame_lowcon_rev_cmap = flame_lowcon_cmap[-1:0:-1]
cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in flame_lowcon_rev_cmap]
flame_lowcon_rev_cmap_mpl = LinearSegmentedColormap.from_list('flame_lowcon_rev_cmap', cmap_tuple_list)


c1 = _c(pnnl_colors["white"])
n1 = 256
c2 = _c(pnnl_colors['platinum40'])
gray_cmap = list(c1.range_to(c2, n1))
cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in gray_cmap]
gray_cmap_mpl = LinearSegmentedColormap.from_list('gray_cmap', cmap_tuple_list)

c1 = _c(pnnl_colors["silver40"])
n1 = 128
c2 = _c(pnnl_colors['platinum40'])
n2 = 128
c3 = _c(pnnl_colors['silver40'])
mid_cmap = list(c1.range_to(c2, n1)) + list(c2.range_to(c3, n2))
cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in mid_cmap]
mid_cmap_mpl = LinearSegmentedColormap.from_list('mid_cmap', cmap_tuple_list)

c1 = _c(pnnl_colors["white"])
n1 = 256
c2 = _c(pnnl_colors['bronze'])
bronze_cmap = list(c1.range_to(c2, n1))
cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in bronze_cmap]
bronze_cmap_mpl = LinearSegmentedColormap.from_list('bronze_cmap', cmap_tuple_list)

c1 = _c(pnnl_colors["white"])
n1 = 256
c2 = _c(pnnl_colors['gold'])
gold_cmap = list(c1.range_to(c2, n1))
cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in gold_cmap]
gold_cmap_mpl = LinearSegmentedColormap.from_list('gold_cmap', cmap_tuple_list)

def from_to(c1, c2, name='new_cmap'):
    c1 = _c(pnnl_colors[c1])
    n1 = 256
    c2 = _c(pnnl_colors[c2])
    _cmap = list(c1.range_to(c2, n1))
    cmap_tuple_list = [(__c.red, __c.green, __c.blue) for __c in _cmap]
    _cmap_mpl = LinearSegmentedColormap.from_list(name, cmap_tuple_list)
    return _cmap_mpl
