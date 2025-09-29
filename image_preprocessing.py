# -*- coding: utf-8 -*-
"""
Created on Thu May 22 15:30:25 2025

@author: mirat
"""
import SimpleITK as sitk
import os

def recast_images(input_path,output_path=""):

    # count how many images have been processed
    images_processed = 0

    # create output folder
    if output_path == "":
        output_path = input_path + "16bit"
    print("\nPreparing output folder . . .")
    os.makedirs(output_path)

    # prepare to read images
    reader = sitk.ImageFileReader()
    reader.SetImageIO("TIFFImageIO")

    # prepare filter
    filter = sitk.CastImageFilter()
    filter.SetOutputPixelType(1)
    print(f"Filter output pixel type: {filter.GetOutputPixelType()}")

    # prepare to write images, set output compression type to LZW
    writer = sitk.ImageFileWriter()
    # writer.SetCompressor("LZW")

    # process every image in input folder
    print("Processing images . . .")
    for f in os.listdir(input_path):
        if (f.endswith(".tif") or f.endswith("tiff")):

            # read image
            reader.SetFileName(os.path.join(input_path, f))
            image = reader.Execute()

            # # cast to a different data type
            # image = sitk.Cast(image,sitk.sitkInt32)
            filter.Execute(image)

            # write image
            writer.SetFileName(os.path.join(output_path, f))
            writer.SetImageIO("TIFFImageIO")
            writer.UseCompressionOn()
            writer.SetCompressor("LZW")
            writer.Execute(image)

            # count total images processed
            images_processed += 1
            if (images_processed % 50) == 0:
                print(f"   {images_processed} images processed")
                # disclose size
                print(f"   Size: {image.GetSize()}")
                # disclose pixel type
                print(f"PixelID: {image.GetPixelID()}")
                print(f"PixelID as string: {image.GetPixelIDTypeAsString()}")

    print("Done\n")

def recast_3d(input_path,output_path=""):
    # create output folder
    if output_path == "":
        output_path = input_path + "16bit"
    print("\nPreparing output folder . . .")
    os.makedirs(output_path)

    # prepare to read images
    print("Reading image . . .")
    reader = sitk.ImageSeriesReader()
    reader.SetImageIO("TIFFImageIO")
    series_filenames = sorted([os.path.join(input_path, f) for f in os.listdir(input_path)])
    reader.SetFileNames(series_filenames)
    image = reader.Execute()

    # filter
    print("Rescaling Intensity. . .")
    image = sitk.RescaleIntensity(image, outputMinimum=0, outputMaximum=255)

    # print("Applying filter 2. . .")
    # filter = sitk.ClampImageFilter()
    # print(f"   Lower Bound: {filter.GetLowerBound()}")    
    # print(f"   Upper Bound: {filter.GetUpperBound()}")
    # filter.SetLowerBound(0)
    # filter.SetUpperBound(255)
    # filter.SetOutputPixelType(sitk.sitkUInt8)
    # print(f"Filter output pixel type: {filter.GetOutputPixelType()}")
    # image = filter.Execute(image)

    print("Casting to 8bit. . .")
    filter = sitk.CastImageFilter()
    filter.SetOutputPixelType(sitk.sitkUInt8)
    image = filter.Execute(image)

    # prepare to write images, set output compression type to LZW
    writer = sitk.ImageSeriesWriter()
    writer.SetImageIO(reader.GetImageIO())
    series_filenames = list(['slice_' + str(i).zfill(5) + '.tiff' for i in range(image.GetSize()[2])]) # output filename formatting
    series_filenames = [os.path.join(output_path, f) for f in series_filenames] # creates output paths
    writer.SetFileNames(series_filenames)
    writer.Execute(image)

    # disclose size
    print(f"   Size: {image.GetSize()}")
    # disclose pixel type
    print(f"PixelID: {image.GetPixelID()}")
    print(f"PixelID as string: {image.GetPixelIDTypeAsString()}")

    print("Done\n")    

def compress_images(input_path,output_path=""):

    # count how many images have been processed
    images_processed = 0

    # create output folder
    if output_path == "":
        output_path = input_path + "\\compressed"
    print("\nPreparing output folder . . .")
    os.makedirs(output_path)

    # prepare to read images
    reader = sitk.ImageFileReader()
    reader.SetImageIO("TIFFImageIO")

    # prepare to write images, set output compression type to LZW
    writer = sitk.ImageFileWriter()
    # writer.SetCompressor("LZW")

    # process every image in input folder
    print("Processing images . . .")
    for f in os.listdir(input_path):
        if (f.endswith(".tif") or f.endswith("tiff")):

            # read image
            reader.SetFileName(os.path.join(input_path, f))
            image = reader.Execute()

            # write image
            writer.SetFileName(os.path.join(output_path, f))
            writer.SetImageIO("TIFFImageIO")
            writer.UseCompressionOn()
            writer.SetCompressor("LZW")
            writer.Execute(image)

            # count total images processed
            images_processed += 1
            if (images_processed % 50) == 0:
                print(f"   {images_processed} images processed")
    print("Done\n")

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
    # series_filenames = sorted([os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".tif") or f.endswith(".tiff")])
    series_filenames = sorted([os.path.join(input_path, f) for f in os.listdir(input_path) if f.startswith("sub2")])
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

def window_rescale_cast_3d(n,input_path,output_path=""):

    # create output folder
    if output_path == "":
        output_path = input_path + "_messed_with"
    print("\nPreparing output folder . . .")
    os.makedirs(output_path)

    # configure and execute reader
    print("Reading image stack . . .")
    reader = sitk.ImageSeriesReader()
    reader.SetImageIO("TIFFImageIO")
    # series_filenames = sorted([os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".tif") or f.endswith(".tiff")])
    series_filenames = sorted([os.path.join(input_path, f) for f in os.listdir(input_path) if f.startswith(f"sub{n}")])
    # series_filenames = sorted([os.path.join(input_path, f) for f in os.listdir(input_path)])
    reader.SetFileNames(series_filenames)
    image = reader.Execute()
    print(f"   3d Image Size: {image.GetSize()}")

    # windowing filter
    print("Windowing intensity . . .")
    filter = sitk.IntensityWindowingImageFilter()
    filter.SetWindowMinimum(0)
    filter.SetWindowMaximum(0.1)
    filter.SetOutputMinimum(0)
    filter.SetOutputMaximum(255)
    image = filter.Execute(image)

    # rescaling filter
    print("Rescaling intensity, because apparently windowing isn't enough . . .")
    image = sitk.RescaleIntensity(image, outputMinimum=0, outputMaximum=255)

    # print("Applying filter 2. . .")
    # filter = sitk.ClampImageFilter()
    # print(f"   Lower Bound: {filter.GetLowerBound()}")    
    # print(f"   Upper Bound: {filter.GetUpperBound()}")
    # filter.SetLowerBound(0)
    # filter.SetUpperBound(255)
    # filter.SetOutputPixelType(sitk.sitkUInt8)
    # print(f"Filter output pixel type: {filter.GetOutputPixelType()}")
    # image = filter.Execute(image)

    # cast to 8-bit
    print("Casting to 8bit . . .")
    filter = sitk.CastImageFilter()
    filter.SetOutputPixelType(sitk.sitkUInt8)
    image = filter.Execute(image)

    # windowing filter, again
    print("Windowing intensity . . .")
    filter = sitk.IntensityWindowingImageFilter()
    filter.SetWindowMinimum(0)
    filter.SetWindowMaximum(10)
    filter.SetOutputMinimum(0)
    filter.SetOutputMaximum(255)
    image = filter.Execute(image)

    # set up writer
    print("Writing image stack to output folder . . .")
    writer = sitk.ImageSeriesWriter()
    series_filenames = list(['slice_' + str(i).zfill(5) + '.tiff' for i in range(image.GetSize()[2])]) # output filename formatting
    series_filenames = [os.path.join(output_path, f) for f in series_filenames] # creates output paths
    writer.SetFileNames(series_filenames)

    # configure compression
    writer.SetImageIO("TIFFImageIO")
    writer.UseCompressionOn()
    writer.SetCompressor("LZW")

    # execute writer
    writer.Execute(image)
    print("Done\n")

def rescale_existing_8bits(n,input_path,output_path=""):

    # create output folder
    if output_path == "":
        output_path = input_path + "_messed_with"
    print("\nPreparing output folder . . .")
    os.makedirs(output_path)

    # configure and execute reader
    print("Reading image stack . . .")
    reader = sitk.ImageSeriesReader()
    reader.SetImageIO("TIFFImageIO")
    # series_filenames = sorted([os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(".tif") or f.endswith(".tiff")])
    series_filenames = sorted([os.path.join(input_path, f) for f in os.listdir(input_path) if f.startswith(f"sub{n}")])
    # series_filenames = sorted([os.path.join(input_path, f) for f in os.listdir(input_path)])
    reader.SetFileNames(series_filenames)
    image = reader.Execute()
    print(f"   3d Image Size: {image.GetSize()}")

    # apply filter
    print("Windowing intensity . . .")
    filter = sitk.IntensityWindowingImageFilter()
    filter.SetWindowMinimum(0)
    filter.SetWindowMaximum(100)
    filter.SetOutputMinimum(0)
    filter.SetOutputMaximum(255)
    image = filter.Execute(image)

    # # filter
    # print("Rescaling Intensity . . .")
    # image = sitk.RescaleIntensity(image, outputMinimum=0, outputMaximum=255)

    # print("Applying filter 2. . .")
    # filter = sitk.ClampImageFilter()
    # print(f"   Lower Bound: {filter.GetLowerBound()}")    
    # print(f"   Upper Bound: {filter.GetUpperBound()}")
    # filter.SetLowerBound(0)
    # filter.SetUpperBound(255)
    # filter.SetOutputPixelType(sitk.sitkUInt8)
    # print(f"Filter output pixel type: {filter.GetOutputPixelType()}")
    # image = filter.Execute(image)

    # print("Casting to 8bit . . .")
    # filter = sitk.CastImageFilter()
    # filter.SetOutputPixelType(sitk.sitkUInt8)
    # image = filter.Execute(image)

    # # # cast to different data type
    # print("Casting to 8-bit . . .")
    # filter = sitk.CastImageFilter()
    # filter.SetOutputPixelType()

    # set up writer
    print("Writing image stack to output folder . . .")
    writer = sitk.ImageSeriesWriter()
    series_filenames = list(['slice_' + str(i).zfill(5) + '.tiff' for i in range(image.GetSize()[2])]) # output filename formatting
    series_filenames = [os.path.join(output_path, f) for f in series_filenames] # creates output paths
    writer.SetFileNames(series_filenames)

    # configure compression
    writer.SetImageIO("TIFFImageIO")
    writer.UseCompressionOn()
    writer.SetCompressor("LZW")

    # execute writer
    writer.Execute(image)
    print("Done\n")

def stupid_combine(input_path, output_path=""):
    # create output folder
    if output_path == "":
        output_path = input_path + "_renamed"
    print("\nPreparing output folder . . .")
    os.makedirs(output_path)

    images_processed = 0
    # process every image in input folder
    for layer in os.listdir(input_path):
        print("LAYER: ", layer)
        layer_path = os.path.join(input_path, layer)
        for f in os.listdir(layer_path):
            if (f.endswith(".tif") or f.endswith("tiff")):
                os.rename(os.path.join(layer_path, f), os.path.join(output_path, f"{layer}_{f}"))
                images_processed += 1
                if (images_processed % 100) == 0:
                    print(f"   {images_processed} images processed")
    print("Done\n")

def stupid_combine_properly(input_path, output_path="", overlapnum=254):
    # create output folder
    if output_path == "":
        output_path = input_path + "_combined_properly"
    print("\nPreparing output folder . . .")
    os.makedirs(output_path)

    layernum = 1
    print("Deleting images from layers . . .")
    for layer in os.listdir(input_path): # loop through layers
        if layernum > 1: # skip first layer
            print(f"LAYER {layernum}: ", layer)
            images_deleted = 0
            for f in os.listdir(os.path.join(input_path, layer)):
                if images_deleted < overlapnum:
                    os.remove(os.path.join(input_path, layer, f))
                    images_deleted += 1
            print(f"   {images_deleted} images deleted from layer {layernum}")
        layernum += 1

    images_processed = 0
    # process every image in input folder
    print("Combining images . . .")
    for layer in os.listdir(input_path):
        print("LAYER: ", layer)
        layer_path = os.path.join(input_path, layer)
        for f in os.listdir(layer_path):
            if (f.endswith(".tif") or f.endswith("tiff")):
                os.rename(os.path.join(layer_path, f), os.path.join(output_path, f"{layer}_{f}"))
                images_processed += 1
                if (images_processed % 100) == 0:
                    print(f"   {images_processed} images moved")

    print("Done\n")

def why_are_you_the_way_you_are():
    print()

def match_histogram_2d(input_path, output_path="", reference_image_path="C:\\Users\\mirat\\VDF_Fatigue_Project\\Fatigue_Samples_XCT_Data\\the_chosen_one.tiff"):
    # create output folder
    if output_path == "":
        output_path = input_path + "_matched"
    print("\nPreparing output folder . . .")
    os.makedirs(output_path)

    # prepare to read images
    reader = sitk.ImageFileReader()
    reader.SetImageIO("TIFFImageIO")

    # prepare to write images, set output compression type to LZW
    writer = sitk.ImageFileWriter()
    writer.SetImageIO("TIFFImageIO")
    writer.UseCompressionOn()
    writer.SetCompressor("LZW")

    # process every image in input folder
    print("Processing images . . .")
    images_processed = 0
    for f in os.listdir(input_path):
        if (f.endswith(".tif") or f.endswith("tiff")):

            # read image
            reader.SetFileName(os.path.join(input_path, f))
            image = reader.Execute()

            # match histogram
            reference_image = sitk.ReadImage(reference_image_path)
            image = sitk.HistogramMatching(image, reference_image)

            # write image
            writer.SetFileName(os.path.join(output_path, f))
            writer.Execute(image)

            # count total images processed
            images_processed += 1
            if (images_processed % 100) == 0:
                print(f"   {images_processed} images processed")

    print("Done\n")

def match_histogram_3d(input_path, output_path="C:\\Users\\mirat\\VDF_Fatigue_Project\\Fatigue_Samples_XCT_Data\\Specimen_5\\processed_together_combined_matched-by-layer", reference_layer_path="C:\\Users\\mirat\\VDF_Fatigue_Project\\Fatigue_Samples_XCT_Data\\Specimen_5\\processed_together\\thresholded_8bit_layer5"):
    
    # create output folder
    if output_path == "":
        output_path = input_path + "_matched"
    print("\nPreparing output folder . . .")
    os.makedirs(output_path)

    # prepare to write images, set output compression type to LZW
    writer = sitk.ImageSeriesWriter()
    writer.SetImageIO("TIFFImageIO")
    writer.UseCompressionOn()
    writer.SetCompressor("LZW")

    # prepare to read images
    reader = sitk.ImageSeriesReader()
    reader.SetImageIO("TIFFImageIO")

    layernum = 1
    for layer in os.listdir(input_path):

        layer_path = os.path.join(input_path, layer)
        print(f"\nLAYER {layernum}:")

        # execute reader
        print("Reading image stack . . .")
        series_filenames = sorted([os.path.join(layer_path, f) for f in os.listdir(layer_path) if f.endswith(".tif") or f.endswith(".tiff")])
        reader.SetFileNames(series_filenames)
        image = reader.Execute()

        # match histogram
        reference_filenames = sorted([os.path.join(layer_path, f) for f in os.listdir(reference_layer_path) if f.endswith(".tif") or f.endswith(".tiff")])
        reader.SetFileNames(reference_filenames)
        reference_image = reader.Execute()
        image = sitk.HistogramMatching(image, reference_image)

        # execute writer
        print("Writing image stack to output folder . . .")
        series_filenames = list(['layer_' + str(layernum) +'_slice_' + str(i).zfill(5) + '.tiff' for i in range(image.GetSize()[2])]) # output filename formatting
        series_filenames = [os.path.join(output_path, f) for f in series_filenames] # creates output paths
        writer.SetFileNames(series_filenames)
        writer.Execute(image)

        layernum += 1

    print("Done\n")

input_path="C:\\Users\\mirat\\VDF_Fatigue_Project\\Fatigue_Samples_XCT_Data\\Specimen_5\\processed_together_combined"
output_path="C:\\Users\\mirat\\VDF_Fatigue_Project\\Fatigue_Samples_XCT_Data\\Specimen_5\\processed_together_combined_matched2"
match_histogram_2d(input_path, output_path=output_path)


# for n in range(6,11):
#     print(f"\nSAMPLE {n}:")
#     input_path = (f"C:\\Users\\mirat\\VDF_Fatigue_Project\\Fatigue_Samples_XCT_Data\\Specimen_{n}\\segmented_cleaned - Copy")
#     output_path = (f"C:\\Users\\mirat\\VDF_Fatigue_Project\\Fatigue_Samples_XCT_Data\\Specimen_{n}\\segmented_cleaned_combined_properly")
#     stupid_combine_properly(input_path, output_path=output_path)