# -*- coding: utf-8 -*-
"""
Created on Thu May 22 15:30:25 2025

@author: mirat
"""

import SimpleITK as sitk

import numpy as np
import os

reader = sitk.ImageSeriesReader()
reader.SetImageIO("TIFFImageIO")

input_path = "XCT data/test_piece"
series_filenames = sorted([os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".tif") or f.endswith(".tiff")])
reader.SetFileNames(series_filenames)
image = reader.Execute()
# hi
resample_filter = sitk.ResampleImageFilter()
# resample_filter.SetReferenceImage(image)
print(f"Size: {resample_filter.GetSize()}")

resample_filter.SetOutputSpacing((2, 2, 2))
resample_filter.SetInterpolator(sitk.sitkNearestNeighbor)
resample_filter.SetSize((int(image.GetSize()[0] / 2), 
                          int(image.GetSize()[1] / 2), 
                          int(image.GetSize()[2] / 2)))
print(f"Size: {resample_filter.GetSize()}")
image = resample_filter.Execute(image)

writer = sitk.ImageSeriesWriter()
writer.SetImageIO(reader.GetImageIO())

output_path = "XCT data/test_piece_output"
series_filenames = list(['slice_' + str(i).zfill(5) + '.tiff' for i in range(image.GetSize()[2])])
series_filenames = [os.path.join(output_path, f) for f in series_filenames]
writer.SetFileNames(series_filenames)
writer.Execute(image)
print("hey go check if that worked")

# TRY THIS ALL ON POWELL; THE ONLY ERROR IS A MEMORY ERROR

"""
reader = sitk.ImageFileReader()
reader.SetImageIO("TIFFImageIO")

image_path = "XCT data/Specimen_1/segmented_cleaned_combined"
series_filenames = sorted([os.path.join(image_path, f) for f in os.listdir(image_path) if f.endswith(".tif") or f.endswith(".tiff")])
for image_file in series_filenames:
    reader.SetFileName(image_file)
    image = reader.Execute()
    resample_filter = sitk.ResampleImageFilter()
    resample_filter.SetReferenceImage(image)
    tellmethings = resample_filter.GetSize()
    print("size before resampling:")
    print(tellmethings)

    resample_filter.SetOutputSpacing((2, 2))
    resample_filter.SetInterpolator(sitk.sitkNearestNeighbor)
    resample_filter.SetSize((int(image.GetSize()[0] / 2), 
                            int(image.GetSize()[1] / 2)))
    tellmethings = resample_filter.GetSize()
    print("size after resampling:")
    print(tellmethings)
"""