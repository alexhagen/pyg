from networkx.utils import is_string_like
from matplotlib.collections import PathCollection
import numpy as np

def _center_ys(layers, mode='spread'):
    ys = np.zeros((len(layers), np.max(layers)))
    if mode == 'spread':
        for i in range(len(layers)):
            ys[i, :layers[i]] = np.linspace(0., 1., layers[i])
        return ys
    if mode == 'center':
        min_sep = 1.0 / np.max(layers)
        for i in range(len(layers)):
            ys[i, :layers[i]] = np.arange(-min_sep * (layers[i] + 1) / 2.0,
                                          min_sep * (layers[i] + 1) / 2.0,
                                          min_sep)[1:] + 0.5
        return ys
    if mode == 'expcenter':
        max_nodes = np.max(layers)
        min_sep = 1.0 / max_nodes
        for i in range(len(layers)):
            if layers[i] is not None:
                r = np.log(max_nodes) / np.log(layers[i])
                ys[i, :layers[i]] = np.arange(-r * min_sep * (layers[i] + 1) / 2.0,
                                              r * min_sep * (layers[i] + 1) / 2.0,
                                              r * min_sep)[1:] + 0.5
        return ys


def nn_layout(G, layers=None, layer_mode='first_digit', center=None, dim=2,
              seed=None):
    print G._node
    xs = np.linspace(0., 1., len(layers))
    print xs, layers
    pos = np.zeros((len(G), dim))
    ys = _center_ys(layers, mode='expcenter')
    if layer_mode == 'first_digit':
        for i, node in enumerate(G):
            print node
            pos[i, 0] = xs[int(node[:3])]
            pos[i, 1] = ys[int(node[:3]), int(node[3:])]
    elif layer_mode == 'attr':
        for i, node in enumerate(G._node.items()):
            print node
            pos[i, 0] = xs[int(node[1]['layer'])]
            pos[i, 1] = ys[int(node[1]['layer']), int(node[1]['node'])]
    pos = pos.astype(np.float32)
    pos = dict(zip(G, pos))
    return pos

def draw_networkx(G, pos=None, arrows=True, with_labels=True, **kwds):
    node_collection = draw_networkx_nodes(G, pos, **kwds)
    edge_collection = draw_networkx_edges(G, pos, arrows=arrows, **kwds)
    #if with_labels:
    #    draw_networkx_labels(G, pos, **kwds)


def draw_networkx_nodes(G, pos, nodelist=None, node_size=300, node_color='r',
                        node_shape='o', alpha=1.0, cmap=None, vmin=None,
                        vmax=None, ax=None, linewidths=None, edgecolors=None,
                        label=None, **kwds):
    if ax is None:
        ax = plt.gca()

    if nodelist is None:
        nodelist = list(G)

    if not nodelist or len(nodelist) == 0:  # empty nodelist, no drawing
        return None

    try:
        xy = np.asarray([pos[v] for v in nodelist])
    except KeyError as e:
        raise nx.NetworkXError('Node %s has no position.' % e)
    except ValueError:
        raise nx.NetworkXError('Bad value in node positions.')

    if isinstance(alpha, collections.Iterable):
        node_color = apply_alpha(node_color, alpha, nodelist, cmap, vmin, vmax)
        alpha = None
    node_collection = []
    for label, x, y in zip(G, xy[:, 0], xy[:, 1]):
        props = dict(ec='black', lw=0.5, fc='white')
        ann = ax.text(x, y, label, ha='center', va='center', bbox=props)
        node_collection.append(ann)
        # get_bbox_patch
    node_collection = PathCollection(node_collection)
    node_collection.set_zorder(2)
    return node_collection


def draw_networkx_edges(G, pos,
                        edgelist=None,
                        width=1.0,
                        edge_color='k',
                        style='solid',
                        alpha=1.0,
                        arrowstyle='-|>',
                        arrowsize=10,
                        edge_cmap=None,
                        edge_vmin=None,
                        edge_vmax=None,
                        ax=None,
                        arrows=True,
                        label=None,
                        node_size=300,
                        nodelist=None,
                        node_shape="o",
                        **kwds):

    if ax is None:
        ax = plt.gca()

    if edgelist is None:
        edgelist = list(G.edges())

    if not edgelist or len(edgelist) == 0:  # no edges!
        return None

    if nodelist is None:
        nodelist = list(G.nodes())

    # set edge positions
    edge_pos = np.asarray([(pos[e[0]], pos[e[1]]) for e in edgelist])

    if not cb.iterable(width):
        lw = (width,)
    else:
        lw = width

    if not is_string_like(edge_color) \
            and cb.iterable(edge_color) \
            and len(edge_color) == len(edge_pos):
        if np.alltrue([is_string_like(c) for c in edge_color]):
            # (should check ALL elements)
            # list of color letters such as ['k','r','k',...]
            edge_colors = tuple([colorConverter.to_rgba(c, alpha)
                                 for c in edge_color])
        elif np.alltrue([not is_string_like(c) for c in edge_color]):
            # If color specs are given as (rgb) or (rgba) tuples, we're OK
            if np.alltrue([cb.iterable(c) and len(c) in (3, 4)
                           for c in edge_color]):
                edge_colors = tuple(edge_color)
            else:
                # numbers (which are going to be mapped with a colormap)
                edge_colors = None
        else:
            raise ValueError('edge_color must contain color names or numbers')
    else:
        if is_string_like(edge_color) or len(edge_color) == 1:
            edge_colors = (colorConverter.to_rgba(edge_color, alpha), )
        else:
            msg = 'edge_color must be a color or list of one color per edge'
            raise ValueError(msg)

    if (not G.is_directed() or not arrows):
        edge_collection = LineCollection(edge_pos,
                                         colors=edge_colors,
                                         linewidths=lw,
                                         antialiaseds=(1,),
                                         linestyle=style,
                                         transOffset=ax.transData,
                                         )

        edge_collection.set_zorder(1)  # edges go behind nodes
        edge_collection.set_label(label)
        ax.add_collection(edge_collection)

        # Note: there was a bug in mpl regarding the handling of alpha values
        # for each line in a LineCollection. It was fixed in matplotlib by
        # r7184 and r7189 (June 6 2009). We should then not set the alpha
        # value globally, since the user can instead provide per-edge alphas
        # now.  Only set it globally if provided as a scalar.
        if cb.is_numlike(alpha):
            edge_collection.set_alpha(alpha)

        if edge_colors is None:
            if edge_cmap is not None:
                assert(isinstance(edge_cmap, Colormap))
            edge_collection.set_array(np.asarray(edge_color))
            edge_collection.set_cmap(edge_cmap)
            if edge_vmin is not None or edge_vmax is not None:
                edge_collection.set_clim(edge_vmin, edge_vmax)
            else:
                edge_collection.autoscale()
        return edge_collection

    arrow_collection = None

    if G.is_directed() and arrows:
        # Note: Waiting for someone to implement arrow to intersection with
        # marker.  Meanwhile, this works well for polygons with more than 4
        # sides and circle.

        def to_marker_edge(marker_size, marker):
            if marker in "s^>v<d":  # `large` markers need extra space
                return np.sqrt(2 * marker_size) / 2
            else:
                return np.sqrt(marker_size) / 2

        # Draw arrows with `matplotlib.patches.FancyarrowPatch`
        arrow_collection = []
        mutation_scale = arrowsize  # scale factor of arrow head
        arrow_colors = edge_colors
        if arrow_colors is None:
            if edge_cmap is not None:
                assert(isinstance(edge_cmap, Colormap))
            else:
                edge_cmap = plt.get_cmap()  # default matplotlib colormap
            if edge_vmin is None:
                edge_vmin = min(edge_color)
            if edge_vmax is None:
                edge_vmax = max(edge_color)
            color_normal = Normalize(vmin=edge_vmin, vmax=edge_vmax)

        for i, (src, dst) in enumerate(edge_pos):
            x1, y1 = src
            x2, y2 = dst
            arrow_color = None
            line_width = None
            shrink_source = 0  # space from source to tail
            shrink_target = 0  # space from  head to target
            if cb.iterable(node_size):  # many node sizes
                src_node, dst_node = edgelist[i]
                index_node = nodelist.index(dst_node)
                marker_size = node_size[index_node]
                shrink_target = to_marker_edge(marker_size, node_shape)
            else:
                shrink_target = to_marker_edge(node_size, node_shape)
            if arrow_colors is None:
                arrow_color = edge_cmap(color_normal(edge_color[i]))
            elif len(arrow_colors) > 1:
                arrow_color = arrow_colors[i]
            else:
                arrow_color = arrow_colors[0]
            if len(lw) > 1:
                line_width = lw[i]
            else:
                line_width = lw[0]
            arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                    arrowstyle=arrowstyle,
                                    shrinkA=shrink_source,
                                    shrinkB=shrink_target,
                                    mutation_scale=mutation_scale,
                                    color=arrow_color,
                                    linewidth=line_width,
                                    zorder=1)  # arrows go behind nodes

            # There seems to be a bug in matplotlib to make collections of
            # FancyArrowPatch instances. Until fixed, the patches are added
            # individually to the axes instance.
            arrow_collection.append(arrow)
            ax.add_patch(arrow)

    # update view
    minx = np.amin(np.ravel(edge_pos[:, :, 0]))
    maxx = np.amax(np.ravel(edge_pos[:, :, 0]))
    miny = np.amin(np.ravel(edge_pos[:, :, 1]))
    maxy = np.amax(np.ravel(edge_pos[:, :, 1]))

    w = maxx - minx
    h = maxy - miny
    padx,  pady = 0.05 * w, 0.05 * h
    corners = (minx - padx, miny - pady), (maxx + padx, maxy + pady)
    ax.update_datalim(corners)
    ax.autoscale_view()

    return arrow_collection


def draw_networkx_labels(G, pos,
                         labels=None,
                         font_size=12,
                         font_color='k',
                         font_family='sans-serif',
                         font_weight='normal',
                         alpha=1.0,
                         bbox=None,
                         ax=None,
                         **kwds):

    if ax is None:
        ax = plt.gca()

    if labels is None:
        labels = dict((n, n) for n in G.nodes())

    # set optional alignment
    horizontalalignment = kwds.get('horizontalalignment', 'center')
    verticalalignment = kwds.get('verticalalignment', 'center')

    text_items = {}  # there is no text collection so we'll fake one
    for n, label in labels.items():
        (x, y) = pos[n]
        if not is_string_like(label):
            label = str(label)  # this makes "1" and 1 labeled the same
        t = ax.text(x, y,
                    label,
                    size=font_size,
                    color=font_color,
                    family=font_family,
                    weight=font_weight,
                    alpha=alpha,
                    horizontalalignment=horizontalalignment,
                    verticalalignment=verticalalignment,
                    transform=ax.transData,
                    bbox=bbox,
                    clip_on=True,
                    )
        text_items[n] = t

    return text_items


def draw_networkx_edge_labels(G, pos,
                              edge_labels=None,
                              label_pos=0.5,
                              font_size=10,
                              font_color='k',
                              font_family='sans-serif',
                              font_weight='normal',
                              alpha=1.0,
                              bbox=None,
                              ax=None,
                              rotate=True,
                              **kwds):

    if ax is None:
        ax = plt.gca()
    if edge_labels is None:
        labels = {(u, v): d for u, v, d in G.edges(data=True)}
    else:
        labels = edge_labels
    text_items = {}
    for (n1, n2), label in labels.items():
        (x1, y1) = pos[n1]
        (x2, y2) = pos[n2]
        (x, y) = (x1 * label_pos + x2 * (1.0 - label_pos),
                  y1 * label_pos + y2 * (1.0 - label_pos))

        if rotate:
            # in degrees
            angle = np.arctan2(y2 - y1, x2 - x1) / (2.0 * np.pi) * 360
            # make label orientation "right-side-up"
            if angle > 90:
                angle -= 180
            if angle < - 90:
                angle += 180
            # transform data coordinate angle to screen coordinate angle
            xy = np.array((x, y))
            trans_angle = ax.transData.transform_angles(np.array((angle,)),
                                                        xy.reshape((1, 2)))[0]
        else:
            trans_angle = 0.0
        # use default box of white with white border
        if bbox is None:
            bbox = dict(boxstyle='round',
                        ec=(1.0, 1.0, 1.0),
                        fc=(1.0, 1.0, 1.0),
                        )
        if not is_string_like(label):
            label = str(label)  # this makes "1" and 1 labeled the same

        # set optional alignment
        horizontalalignment = kwds.get('horizontalalignment', 'center')
        verticalalignment = kwds.get('verticalalignment', 'center')

        t = ax.text(x, y,
                    label,
                    size=font_size,
                    color=font_color,
                    family=font_family,
                    weight=font_weight,
                    alpha=alpha,
                    horizontalalignment=horizontalalignment,
                    verticalalignment=verticalalignment,
                    rotation=trans_angle,
                    transform=ax.transData,
                    bbox=bbox,
                    zorder=1,
                    clip_on=True,
                    )
        text_items[(n1, n2)] = t

    return text_items
