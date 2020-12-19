import numpy as np
import pylidc as pl
from utils import normalize, get_pixels_from_hu, get_intersection, get_union
import matplotlib.pyplot as plt
import os
import nrrd

from matplotlib.patches import Rectangle
scans = pl.query(pl.Scan)
for scan in scans:

    print(scan)
    print("Patient: ", scan.patient_id)

    # Get scan volume from DICOM Images
    try:
        np_vol = get_pixels_from_hu(scan.load_all_dicom_images())
    except:
        # Skip scan since we only look at selected subset of LIDC
        print("Skipped Scan!")
        continue
    root_path = './lung/'
    erased_path = root_path +'erased/'
    label_path = root_path +'label/'
    if not os.path.exists(erased_path):
        os.makedirs(erased_path)
    if not os.path.exists(label_path):
        os.makedirs(label_path)
    # Create empty volumes to hold annotations from all 4 annotatorsf
    mask_ann = [np.zeros(np_vol.shape, dtype=np.bool).T for i in range(4)]

    # Cluster object from pylidc to obtain nodules
    cluster = scan.cluster_annotations()
    print("-" * 50)
    print("Number of Nodules: ", len(cluster))

    nodule_i = 0
    # For each nodule in the scan
    for nodule in cluster:
        print("\n\n")
        print("Annotations per nodule: ", len(nodule))
        # Obtain only 4 annotations of the nodule
        if len(nodule) > 4:
            continue
        ann=nodule[0]
        # anns = nodule.ann
        # ann_idxs = nodule.ann_inx
        # Get each annotation one by one for each nodule
        # for ann_idx, ann in enumerate(nodule):
        #     print("\n")
        #     print("Annotation: {}".format(ann_idx))
        print("Nodule Diameter: ", ann.diameter)
        vol = ann.scan.to_volume()
        slice =ann.contour_slice_indices
        # print("slice",slice)
        mid_slice = (slice.min()+slice.max())//2
        num_slice = len(slice)
        nodule_contours = ann.contours
        num_contours = len(nodule_contours)
        mid_contours = num_contours//2
        malignancy_type = ann.malignancy

        if num_slice>=3:
            left_slice =  (slice.min()+mid_slice)//2
            right_slice = (slice.max() + mid_slice) // 2
            left_contours = mid_contours//2
            right_contours = (mid_contours+num_contours)//2
            # print("malignancy_type",malignancy_type)
            slice_list= [left_slice,mid_slice,right_slice]
            contours_list=[left_contours,mid_contours,right_contours]
        else:
            slice_list = [mid_slice]
            contours_list=[mid_contours]
        for i in range(len(slice_list)):
            image = vol[:,:,slice_list[i]]
            con = ann.contours[contours_list[i]]
            ii, jj = con.to_matrix(include_k=False).T
            min_x, max_x = min(jj), max(jj)
            min_y, max_y = min(ii), max(ii)
            w = max_x - min_x
            h = max_y - min_y
            roi = [min_x,min_y,w,h]
            # print(roi)
            erased_image=image.copy()
            erased_image[min_y:max_y,min_x:max_x]=-500
            id = str(scan.patient_id).split('-')[-1]

            roi_s = '_'.join([str(x) for x in roi])
            name = str(id)+'_'+str(nodule_i)+'_'+str(slice_list[i])+'_'+roi_s+'_'+str(malignancy_type)+'.nrrd'

            save_erased_name = erased_path+name
            save_label_name = label_path+name
            print("saving....",save_erased_name)
            print("patient_id,nodule,slice,roi,malignancy")
            nrrd.write(save_erased_name, erased_image)
            nrrd.write(save_label_name, image)
            # plt.imshow(erased_image, cmap=plt.cm.gray)
            # plt.gca().add_patch(Rectangle((min_x,min_y), w, h, linewidth=1, edgecolor='r', facecolor='none'))
            # plt.show()



