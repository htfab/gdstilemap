#!/usr/bin/env python3

import os, sys, re
from klayout import db, lay

layer_props = 'sky130+micross.lyp'
caravel_layout = 'caravel.oas'
bump_bond_layout = 'caravel_bump_bond.oas'

layers = ('psdm', 'nsdm', 'poly', 'licon1', 'li1', 'mcon', 'met1', 'via', 'met2', 'via2', 'met3', 'via3', 'met4', 'via4', 'met5', 'pad', 'pi1', 'rdl', 'pi2')
datatypes = ('drawing', 'res', 'cut', 'gate', 'short', 'pin')
slices = (('bump', 'pi2'), ('beol5', 'pad'), ('beol4', 'via4'), ('beol3', 'via3'), ('beol2', 'via2'), ('beol1', 'via'), ('feol2', 'mcon'), ('feol1', 'licon1'))

file_template = lambda s, z, x, y: f'{s}_files/{z}/{x}_{y}.png'
tile_size_exp = 9
zoom_depth = 12

def zoom(full_box, subdiv, x, y):
    left = full_box.right*x/subdiv + full_box.left*(1-x/subdiv)
    right = full_box.right*(x+1)/subdiv + full_box.left*(1-(x+1)/subdiv)
    top = full_box.bottom*y/subdiv + full_box.top*(1-y/subdiv)
    bottom = full_box.bottom*(y+1)/subdiv + full_box.top*(1-(y+1)/subdiv)
    return db.DBox(left, bottom, right, top)

def change_slice(lv, slice_layer):
    for l in lv.each_layer():
        m = re.match(r'(.*)\.(.*) - (.*)', l.name)
        l.visible = (m is not None and
                     m.group(1) in layers and
                     m.group(2) in datatypes and
                     layers.index(m.group(1)) <= layers.index(slice_layer))
    lv.update_content()

print('Initializing', file=sys.stderr, flush=True)
lv = lay.LayoutView()

print('Loading design', file=sys.stderr, flush=True)
lv.load_layer_props(layer_props)
lv.load_layout(caravel_layout)
lv.load_layout(bump_bond_layout)
lv.max_hier()
lv.set_config('background-color', '#ffffff')
lv.set_config('grid-visible', 'false')
lv.set_config('text-visible', 'false')
full_box = lv.box()

print('Writing dzi manifests', file=sys.stderr, flush=True)
for slice_name, slice_layer in slices:
    tile_size = 1 << tile_size_exp
    width = height = 1 << zoom_depth
    with open(f'{slice_name}.dzi', 'w') as dzi:
        print('\n'.join(('<?xml version="1.0" encoding="UTF-8"?>',
                        f'<Image xmlns="http://schemas.microsoft.com/deepzoom/2008" Format="png" Overlap="0" TileSize="{tile_size}">',
                        f'  <Size Height="{height}" Width="{width}" />', '</Image>')), file=dzi)

for zoom_level in range(zoom_depth+1):
    extra_zoom = zoom_level - tile_size_exp
    subdiv = 1 << extra_zoom if extra_zoom > 0 else 1
    tile_size = 1 << tile_size_exp if extra_zoom > 0 else 1 << zoom_level
    for slice_name, slice_layer in slices:
        os.makedirs(os.path.dirname(file_template(slice_name, zoom_level, 0, 0)), exist_ok=True)
        change_slice(lv, slice_layer)
        for y in range(subdiv):
            for x in range(subdiv):
                file = file_template(slice_name, zoom_level, x, y)
                box = zoom(full_box, subdiv, x, y)
                print(f'Exporting {file}', file=sys.stderr, flush=True)
                lv.save_image_with_options(file, tile_size, tile_size, 0, 3, 0, box)

