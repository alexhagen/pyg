from colour import Color as c

pu_colors = {'black': '#000000',
             'white': '#ffffff',
             'oldgold': '#a3792c',
             'newgold': '#e3ae24',
             'darkgray': '#746c66',
             'gray': '#a7a9ac',
             'lightgray': '#d1d3d4',
             'lightlightgray': '#e1e3e4',
             'darkgreen': '#3f4b00',
             'green': '#5c8727',
             'teal': '#2eafa4',
             'lightblue': '#7ed0e0',
             'blue': '#7299c6',
             'darkblue': '#5c6f7b',
             'purple': '#b63f97',
             'darkred': '#7e543a',
             'red': '#b95915',
             'orange': '#f8981d',
             'lightyellow': '#d9da56',
             'yellow': '#b8b308',
             'browngray': '#4d4038',
             'tan': '#baa892',
             'brown': '#6b4536'}
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


desat = c(pu_colors["blue"])
desat.saturation = 0.0
desat.luminance = 0.1
flow_cmap = list(desat.range_to(c(pu_colors["blue"]), 256))
desat = c(pu_colors["newgold"])
desat.saturation = 0.0
desat.luminance = 0.1
brand_cmap = list(desat.range_to(c(pu_colors["newgold"]), 256))
desat = c(pu_colors["red"])
desat.saturation = 0.0
desat.luminance = 0.75
flame_cmap = list(desat.range_to(c(pu_colors["red"]), 256))
desat = c(pu_colors["teal"])
desat.saturation = 0.0
desat.luminance = 0.9
teal_cmap = list(desat.range_to(c(pu_colors["teal"]), 256))
desat = c(pu_colors["white"])
bw_cmap = list(desat.range_to(c(pu_colors["black"]), 256))

start_c = c(pu_colors["blue"])
mid_c = c(pu_colors["green"])
pu_jet_cmap = list(start_c.range_to(mid_c, 128)) + list(mid_c.range_to(c(pu_colors["red"]), 128))

start_c = c(pu_colors["darkgray"])
brand_cmap = list(start_c.range_to(c(pu_colors["newgold"]), 256))
