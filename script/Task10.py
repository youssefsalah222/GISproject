import arcpy
arcpy.env.overwriteOutput = True
countries =arcpy.GetParameterAsText(0)
population_of_countries=arcpy.GetParameterAsText(1)
list=[]
with arcpy.da.UpdateCursor(countries,['POP_EST','POP_YEAR',"NAME"])as sc:
    for x in sc:
        if x[1]<2019:
            x[0]=float(population_of_countries)
            list.append(x[2])
            sc.updateRow(x)
arcpy.AddMessage("Done, countries updated")
for country in list:
    arcpy.AddMessage(country)