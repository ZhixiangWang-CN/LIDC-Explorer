import pylidc as pl
from pylidc.utils import volume_viewer


ann = pl.query(pl.Annotation).first()
vol = ann.scan.to_volume()

padding = 70.0

mask = ann.boolean_mask(pad=padding)
bbox = ann.bbox(pad=padding)

volume_viewer(vol[bbox], mask, ls='-', lw=2, c='r')