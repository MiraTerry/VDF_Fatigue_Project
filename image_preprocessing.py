# -*- coding: utf-8 -*-
"""
Created on Thu May 22 15:30:25 2025

@author: mirat
"""
import SimpleITK as sitk
import os

# input_path = "XCT data/Specimen_1/segmented_cleaned_combined"
transform_factor = 1/2  # the factor by which the resolution is increased or decreased (>1 for downsampling)

def resample_stack(input_path,transform_factor):
    # create output folder
    output_path = input_path + "_downsampled"
    print("\nPreparing output folder . . .")
    os.makedirs(output_path)

    print("Reading image stack . . .")
    reader = sitk.ImageSeriesReader()
    reader.SetImageIO("TIFFImageIO")
    series_filenames = sorted([os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".tif") or f.endswith(".tiff")])
    reader.SetFileNames(series_filenames)
    image = reader.Execute()

    print("Resampling . . .")
    resample_filter = sitk.ResampleImageFilter()
    resample_filter.SetReferenceImage(image)
    print(f"   Initial size: {resample_filter.GetSize()}")
    resample_filter.SetOutputSpacing(((1/transform_factor), (1/transform_factor), (1/transform_factor))) # keeps spacing consistent before and after resampling
    resample_filter.SetInterpolator(sitk.sitkNearestNeighbor)
    resample_filter.SetSize((int(image.GetSize()[0] * transform_factor), # multiplies resolution by transform_factor
                            int(image.GetSize()[1] * transform_factor), 
                            int(image.GetSize()[2] * transform_factor)))
    print(f"   Resampled size: {resample_filter.GetSize()}")
    image = resample_filter.Execute(image) # apply filter to 3d image

    print("Writing image stack to output folder . . .")
    writer = sitk.ImageSeriesWriter()
    writer.SetImageIO(reader.GetImageIO())
    series_filenames = list(['slice_' + str(i).zfill(5) + '.tiff' for i in range(image.GetSize()[2])]) # output filename formatting
    series_filenames = [os.path.join(output_path, f) for f in series_filenames] # creates output paths
    writer.SetFileNames(series_filenames)
    writer.Execute(image)
    print("Done\n")

for i in range(1,11):
    print(f"\n\nPROCESSING FOLDER {i}:")
    input_path = "XCT data/Specimen_" + str(i) + "/segmented_cleaned_combined"
    resample_stack(input_path,transform_factor)