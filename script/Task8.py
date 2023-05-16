import arcpy
arcpy.env.overwriteOutput = True
roads = arcpy.GetParameterAsText(0)
countries = arcpy.GetParameterAsText(1)
population = arcpy.GetParameterAsText(2)
outPath = arcpy.GetParameterAsText(3)
arcpy.MakeFeatureLayer_management(roads, 'roads_layer')
with arcpy.da.SearchCursor(countries, ['FID', 'SOVEREIGNT', 'POP_EST', 'CONTINENT', 'INCOME_GRP']) as c:
    for x in c:
        formatted_output_name = x[1].replace('(', '').replace(')', '_')
        if x[3] == 'Africa' and x[2] > float(population):
            arcpy.MakeFeatureLayer_management(countries, 'countries_layer', """ "FID" = {} """.format(x[0]))
            arcpy.SelectLayerByLocation_management('roads_layer', "WITHIN", 'countries_layer')
            income = x[4].replace('.', ' ')
            arcpy.FeatureClassToFeatureClass_conversion('roads_layer', outPath,
                                                        'Roads_in_{}_{}'.format(formatted_output_name, income))
            print('Correct {}_{} '.format(formatted_output_name, income))

        else:
            print('not needed ' + formatted_output_name)

arcpy.AddMessage("Done , Task 8")