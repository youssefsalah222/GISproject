import arcpy
import os
from PIL import ExifTags , Image
arcpy.env.workspace = r'D:\00SalahEssa\D\4th year\GIS\GISproject\data'
arcpy.env.overwriteOutput = True
countries = r'D:\00SalahEssa\D\4th year\GIS\GISproject\data\ne_10m_admin_0_countries.shp'
points = r'D:\00SalahEssa\D\4th year\GIS\GISproject\data\ne_10m_populated_places.shp'
airports = r'D:\00SalahEssa\D\4th year\GIS\GISproject\data\ne_10m_airports.shp'
ports = r'D:\00SalahEssa\D\4th year\GIS\GISproject\data\ne_10m_ports.shp'
roads = r'D:\00SalahEssa\D\4th year\GIS\GISproject\data\ne_10m_roads.shp'
outPath = r'D:\00SalahEssa\D\4th year\GIS\GISproject\output'
#====================================================================
def Task1():
    fl = arcpy.ListFeatureClasses()
    print(fl)
#====================================================================================

def Task2():
    arcpy.MakeFeatureLayer_management(countries, 'countries_layer')
    arcpy.MakeFeatureLayer_management(airports, 'airports_layer', """ type = 'military' """)
    arcpy.SelectLayerByLocation_management('airports_layer', 'WITHIN', 'countries_layer')
    arcpy.FeatureClassToFeatureClass_conversion('airports_layer', outPath, 'military_airports')
    with arcpy.da.SearchCursor(airports, ['name'], """ type = 'military' """) as sc:
        for x in sc:
            print(x[0])
#=====================================================================================

def Task3():
    arcpy.MakeFeatureLayer_management(countries, 'countries_layer')
    arcpy.MakeFeatureLayer_management(roads, 'roads_layer', """ continent = 'Asia' """)
    arcpy.SelectLayerByLocation_management('roads_layer', 'WITHIN', 'countries_layer')
    arcpy.FeatureClassToFeatureClass_conversion('roads_layer', outPath, 'roads_in_asia')
    sf = r'D:\00SalahEssa\D\4th year\GIS\GISproject\output\roads_in_asia.shp'
    roadsNum = arcpy.GetCount_management(sf).getOutput(0)
    print(roadsNum)

#============================================================================================

def Task4():
    countries_list = ['Italy', 'Spain', 'France']
    arcpy.MakeFeatureLayer_management(ports, 'ports_layer')
    for x in countries_list:
        arcpy.MakeFeatureLayer_management(countries, 'countries_layer', """ Name = '{}' """.format(x))
        arcpy.SelectLayerByLocation_management('ports_layer', 'WITHIN', 'countries_layer')
        arcpy.FeatureClassToFeatureClass_conversion('ports_layer', outPath, 'ports_in_{}'.format(x))
#====================================================================================================

def Task5_MultipleSelections():
    arabic_list = ['Palestine', 'Lebanon', 'S. Sudan', 'Somalia', 'Syria', 'Morocco', 'Oman',
                   'United Arab Emirates', 'Libya', 'Tunisia', 'Sudan', 'Djibouti', 'Qatar', 'Saudi Arabia', 'Kuwait',
                   'Algeria', 'Jordan', 'Egypt', 'Yemen', 'Mauritania', 'Comoros', 'Bahrain']
    arcpy.MakeFeatureLayer_management(points, 'points_layer')
    for x in arabic_list:
        arcpy.MakeFeatureLayer_management(countries, 'countries_layer', """ NAME = '{}' """.format(x))
        arcpy.SelectLayerByLocation_management('points_layer', 'WITHIN', 'countries_layer')
        arcpy.FeatureClassToFeatureClass_conversion('points_layer', outPath, 'cities_in_{}'.format(x))
#=====================================================================================================

def Task5_IfCondition():
    arabic_list = ['Palestine', 'Lebanon', 'S. Sudan', 'Somalia', 'Syria', 'Morocco', 'Oman',
                   'United Arab Emirates', 'Libya', 'Tunisia', 'Sudan', 'Djibouti', 'Qatar', 'Saudi Arabia', 'Kuwait',
                   'Algeria', 'Jordan', 'Egypt', 'Yemen', 'Mauritania', 'Comoros', 'Bahrain']
    arcpy.MakeFeatureLayer_management(points, 'points_layer')
    with arcpy.da.SearchCursor(countries, ['NAME']) as sc:
      for x in sc:
        if x[0] in arabic_list:
         arcpy.MakeFeatureLayer_management(countries,'countries_layer', """ "NAME" = '{}' """.format(x[0]))
         arcpy.SelectLayerByLocation_management('points_layer', 'WITHIN', 'countries_layer')
         arcpy.FeatureClassToFeatureClass_conversion('points_layer', outPath, 'second_cities_in_{}'.format(x[0]))
#==============================================================================================================

def Task6():
    with arcpy.da.SearchCursor(airports, ['name', 'location', 'wikipedia'], """ type = 'major' """) as sc:
        for x in sc:
            print (x[0])
            print (x[1])
            print (x[2]) + '\n'

#============================================================================================================

def Task7():
 arcpy.MakeFeatureLayer_management(roads, 'roads_layer')
 with arcpy.da.SearchCursor(countries, ['FID', 'SOVEREIGNT', 'POP_EST', 'CONTINENT', 'INCOME_GRP']) as c:
    for x in c:
        formatted_output_name = x[1].replace('(', '').replace(')', '_')
        if x[3] == 'Africa' and x[2] > 25e6:
            arcpy.MakeFeatureLayer_management(countries, 'countries_layer', """ "FID" = {} """.format(x[0]))
            arcpy.SelectLayerByLocation_management('roads_layer', "WITHIN", 'countries_layer')
            income = x[4].replace('.', ' ')
            arcpy.FeatureClassToFeatureClass_conversion('roads_layer', outPath, 'Roads_in_{}_{}'.format(formatted_output_name, income))
            print('Included {}_{} '.format(formatted_output_name, income))

        else:
            print('not included ' + formatted_output_name)
#============================================================================================================

def Task11():
    field_list = arcpy.ListFields(points)
    for x in field_list:
        print ("Name: " + x.name)
        print("Type: " + x.type)

#============================================================================================================

def Task12():
    field_list = arcpy.ListFields(points)
    ListField = []
    for field in field_list:
        if field.type != 'String':
            ListField.append(field.name)
    for field in ListField:
        with arcpy.da.UpdateCursor(points, [field]) as city_cursor:
            for x in city_cursor:
                if x[0] == 0 or x[0] == None:
                    x[0] = 2
                    city_cursor.updateRow(x)

#============================================================================================================

def Task13():
    img_folder = r"D:\gisimages"
    img_contents = os.listdir(img_folder)
    for img in img_contents:
        print(img)
        full_path = os.path.join(img_folder , img)
        print("Full path is: " + full_path)
#============================================================================================================

def Task14():
    img_folder = r"D:\gisimages"
    img_contents = os.listdir(img_folder)
    for img in img_contents:
        full_path = os.path.join(img_folder, img)
        pillow_img = Image.open(full_path)
        exif = {ExifTags.TAGS[k]: v for k, v in pillow_img._getexif().items() if k in ExifTags.TAGS}
        print (exif)    # info about image

#============================================================================================================

def Task15():
    img_folder = r"D:\gisimages"
    img_contents = os.listdir(img_folder)
    for img in img_contents:
        full_path = os.path.join(img_folder, img)
        pillow_img = Image.open(full_path)
        exif = {ExifTags.TAGS[k]: v for k, v in pillow_img._getexif().items() if k in ExifTags.TAGS}
        try:
            for key in exif['GPSInfo'].keys():
                print ("This is coded value {}".format(key))
                decoded_value = ExifTags.GPSTAGS.get(key)
                print ("This is its associated label {}".format(decoded_value))
        except:
            print("This image has no GPS Info in it {}".format(full_path))
            pass

#============================================================================================================

def Task16():
    img_folder = r"D:\gisimages"
    img_contents = os.listdir(img_folder)
    for img in img_contents:
        full_path = os.path.join(img_folder, img)
        pillow_img = Image.open(full_path)
        exif = {ExifTags.TAGS[k]: v for k, v in pillow_img._getexif().items() if k in ExifTags.TAGS}
        gps_all = {}
        try:
            for key in exif['GPSInfo'].keys():
                decoded_value = ExifTags.GPSTAGS.get(key)
                gps_all[decoded_value] = exif['GPSInfo'][key]

            long_ref = gps_all.get('GPSLongitudeRef')
            long = gps_all.get('GPSLongitude')
            lat_ref = gps_all.get('GPSLatitudeRef')
            lat = gps_all.get('GPSLatitude')

            print long_ref , "    " , long
            print lat_ref, "    ", lat
        except:
            print("This image has no GPS Info in it {}".format(full_path))
            pass
#============================================================================================================
# Task16()