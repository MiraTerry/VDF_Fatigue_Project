# -*- coding: utf-8 -*-
"""
Created on Thu May 22 15:30:25 2025

@author: mirat
"""

import SimpleITK as sitk

import numpy as np
import os
# import matplotlib.pyplot as plt

# from downloaddata import fetch_data as fdata/

# OUTPUT_DIR = "output"

# image_viewer = sitk.ImageViewer()

# reader = sitk.ImageSeriesReader()
# reader.SetImageIO("TIFFImageIO")

# image_path = "C:\\Users\\mirat\\VDF_Fatigue_Project\\Fatigue_Samples_XCT_Data\\Specimen_1\\Specimen_1\\segmented_cleaned_combined\\segmented_cleaned_combined"
# image_files = sorted([os.path.join(image_path, f) for f in os.listdir(image_path) if f.endswith(".tif") or f.endswith(".tiff")])
# reader.SetFileNames(image_files)
# image = reader.Execute()
# # hi
# resampled_image = sitk.ResampleImageFilter()
# resampled_image.SetReferenceImage(image)
# print(f"Size: {resampled_image.GetSize()}")

# resampled_image.SetOutputSpacing((2, 2, 2))
# resampled_image.SetInterpolator(sitk.sitkNearestNeighbor)
# resampled_image.SetSize((int(image.GetSize()[0] / 2), 
#                           int(image.GetSize()[1] / 2), 
#                           int(image.GetSize()[2] / 2)))
# print(f"Size: {resampled_image.GetSize()}")

# TRY THIS ALL ON POWELL; THE ONLY ERROR IS A MEMORY ERROR

# """
reader = sitk.ImageFileReader()
reader.SetImageIO("TIFFImageIO")

image_path = "C:\\Users\\mirat\\VDF_Fatigue_Project\\Fatigue_Samples_XCT_Data\\Specimen_1\\Specimen_1\\segmented_cleaned_combined\\segmented_cleaned_combined"
image_files = sorted([os.path.join(image_path, f) for f in os.listdir(image_path) if f.endswith(".tif") or f.endswith(".tiff")])
for image_file in image_files:
    reader.SetFileName(image_file)
    image = reader.Execute()
    resampled_image = sitk.ResampleImageFilter()
    resampled_image.SetReferenceImage(image)
    tellmethings = resampled_image.GetSize()
    print("size before resampling:")
    print(tellmethings)

    resampled_image.SetOutputSpacing((2, 2))
    resampled_image.SetInterpolator(sitk.sitkNearestNeighbor)
    resampled_image.SetSize((int(image.GetSize()[0] / 2), 
                            int(image.GetSize()[1] / 2)))
    tellmethings = resampled_image.GetSize()
    print("size after resampling:")
    print(tellmethings)
# """