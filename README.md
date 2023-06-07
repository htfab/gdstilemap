# GDS/OAS tilemap generator

Creates deep zoom image tiles from a Caravel/sky130 chip layout for use with [OpenSeadragon](https://openseadragon.github.io/).

Before running `gdstilemap.py`, change the following configuration variables in the source code:
- `caravel_layout` to the GDS/OAS file to be processed
- `zoom_depth` to the maximum zoom level

## Acknowledgements
- `gdstilemap.py` is based on [gds-plotting-playground](https://colab.research.google.com/gist/proppy/c2d0f0f21a7c57fc905e78d9454b6433/gds-plotting-playground.ipynb)
  by [proppy](https://github.com/proppy)
- `sky130+micross.lyp` is based on [mattvenn/klayout\_properties](https://github.com/mattvenn/klayout_properties)
- `caravel.oas` was converted from [efabless/caravel](https://github.com/efabless/caravel)
- `caravel_bump_bond.oas` was converted from [efabless/caravel\_mpw-one](https://github.com/efabless/caravel_mpw-one)
- `osd/images/*` is based on [tombrossman/openseadragon-svg-icons](https://gitlab.com/tombrossman/openseadragon-svg-icons)
- the rest of `osd` was copied directly from [openseadragon](https://github.com/openseadragon/openseadragon)

