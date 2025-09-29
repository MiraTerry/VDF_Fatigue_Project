"""
@author: mirat
"""

import SimpleITK as sitk
import os

def resample_stack(transform_factor, input_path, output_path=""):
    # transform_factor is the factor by which the resolution is increased or decreased (>1 for downsampling)

    # create output folder
    if output_path == "":
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

input_path=""
output_path=""
resample_stack(3, input_path, output_path=output_path)