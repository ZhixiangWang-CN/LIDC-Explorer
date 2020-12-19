import pylidc as pl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
ann = pl.query(pl.Annotation).first()
vol = ann.scan.to_volume()
con = ann.contours[3]

# k = con.image_k_position
ii,jj = ann.contours[3].to_matrix(include_k=False).T
min_x,max_x = min(jj),max(jj)
min_y,max_y = min(ii),max(ii)
w = max_x-min_x
h = max_y-min_y
plt.imshow(vol[:,:,46], cmap=plt.cm.gray)
plt.gca().add_patch(Rectangle((min_x,min_y),w,h,linewidth=1,edgecolor='r',facecolor='none'))
plt.plot(jj, ii, '-r', lw=1, label="Nodule Boundary")
plt.legend()
plt.show()