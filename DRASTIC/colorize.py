'''
Script to generate a png from a raster file.
It can be used from the command line or from an other python script
'''
from os.path import exists
from osgeo import gdal
from osgeo.gdalconst import GA_ReadOnly
from struct import unpack
import Image
import ImageDraw
from sys import argv
from sys import exit

'''
Main function.
Requires the input file, the color file and the otuput file name. The raster band is 1 by default. If nothing is asked, the discrete colroscale image is created.
'''
def raster2png(raster_file, color_file, out_file_name, raster_band=1, discrete=True):
    #Reading the color table
    color_table = readColorTable(color_file)
    #Reading the band
    data_types ={'Byte':'B','UInt16':'H','Int16':'h','UInt32':'I','Int32':'i','Float32':'f','Float64':'d'}
    if exists(raster_file) is False:
            raise Exception('[Errno 2] No such file or directory: \'' + raster_file + '\'')    
    
    dataset = gdal.Open(raster_file, GA_ReadOnly )
    if dataset == None:
        raise Exception("Unable to read the data file")
    band = dataset.GetRasterBand(raster_band)
    values = band.ReadRaster( 0, 0, band.XSize, band.YSize, band.XSize, band.YSize, band.DataType )
    values = unpack(data_types[gdal.GetDataTypeName(band.DataType)]*band.XSize*band.YSize,values)
    
    #Preparing the color table and the output file
    classification_values = color_table.keys()
    classification_values.sort()
    
    base = Image.new( 'RGBA', (band.XSize,band.YSize) )
    base_draw = ImageDraw.Draw(base)
    alpha_mask = Image.new('L', (band.XSize,band.YSize), 255)
    alpha_draw = ImageDraw.Draw(alpha_mask)
    
    #Reading the value and setting the output color for each pixel
    for pos in range(len(values)):
        y = pos/band.XSize
        x = pos - y * band.XSize
        for index in range(len(classification_values)):

            if values[pos] <= classification_values[index] or index == len(classification_values)-1:
                if discrete == True:
                    if index == 0:
                        index = 1
                    elif index == len(classification_values)-1 and values[pos] >= classification_values[index]:
                        index = index + 1
                    color = color_table[classification_values[index-1]]
                    base_draw.point((x,y), (color[0],color[1],color[2]))
                    alpha_draw.point((x,y),color[3])
                else:
                    if index == 0:
                        r = color_table[classification_values[0]][0]
                        g = color_table[classification_values[0]][1]
                        b = color_table[classification_values[0]][2]
                        a = color_table[classification_values[0]][3]
                    elif index == len(classification_values)-1 and values[pos] >= classification_values[index]:
                        r = color_table[classification_values[index]][0]
                        g = color_table[classification_values[index]][1]
                        b = color_table[classification_values[index]][2]
                        a = color_table[classification_values[index]][3]
                    else:
                        r = color_table[classification_values[index-1]][0] + (values[pos] - classification_values[index-1])*(color_table[classification_values[index]][0] - color_table[classification_values[index-1]][0])/(classification_values[index]-classification_values[index-1]) 
                        g = color_table[classification_values[index-1]][1] + (values[pos] - classification_values[index-1])*(color_table[classification_values[index]][1] - color_table[classification_values[index-1]][1])/(classification_values[index]-classification_values[index-1]) 
                        b = color_table[classification_values[index-1]][2] + (values[pos] - classification_values[index-1])*(color_table[classification_values[index]][2] - color_table[classification_values[index-1]][2])/(classification_values[index]-classification_values[index-1]) 
                        a = color_table[classification_values[index-1]][3] + (values[pos] - classification_values[index-1])*(color_table[classification_values[index]][3] - color_table[classification_values[index-1]][3])/(classification_values[index]-classification_values[index-1]) 
                    
                    base_draw.point((x,y), (int(r),int(g),int(b)))
                    alpha_draw.point((x,y),int(a))
                    
                break
    #Adding transparency and saving the output image       
    color_layer = Image.new('RGBA', base.size, (255, 255, 255, 0))
    base = Image.composite(color_layer, base, alpha_mask)
    base.save(out_file_name)
    
    
    
    
    '''
    The method for reading the color file.
    * If alpha is not defined, a 255 value is set.
    '''
def readColorTable(color_file):
    color_table = {}
    if exists(color_file) is False:
        raise Exception("Color file " + color_file + " does not exist")
    
    fp = open(color_file, "r")
    for line in fp:
        if line.find('#') == -1 and line.find('/') == -1:
            entry = line.split()
            if len(entry) == 5:
                alpha = int(entry[4])
            else:
                alpha=0
            color_table[eval(entry[0])]=[int(entry[1]),int(entry[2]),int(entry[3]),alpha]
    fp.close()
    
    return color_table

'''
Usage explanation
'''
def Usage():
    print "Not enough arguments." 
    print "Usage:"
    print argv[0] + ' [-exact_color_entry|-nearest_color_entry] [-band=1] data_file color_file output_file'    
    exit()

'''
Program Mainline
'''
if __name__ == "__main__":
    
    file_name = None
    colorfile_name = None
    out_file_name = None
    discrete = False
    band = 1

    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg == '-exact_color_entry':
            discrete = True
        elif arg == '-band':
            band = argv[i+1]
            i = i + 1
        elif file_name is None:
            file_name = arg
            file_name = file_name.replace("'","")
            file_name = file_name.replace('"','')
        elif colorfile_name is None:
            colorfile_name = arg
            colorfile_name = colorfile_name.replace("'","")
            colorfile_name = colorfile_name.replace('"','')
        elif out_file_name is None:
            out_file_name = arg
            out_file_name = out_file_name.replace("'","")
            out_file_name = out_file_name.replace('"','')
        i = i + 1   

    if len(argv) == 1 or file_name == None or colorfile_name == None or out_file_name == None: 
        Usage()     
    try:
        raster2png(file_name,colorfile_name,out_file_name,band,discrete)
    except Exception, ex:
        print "Error: " + str(ex)
