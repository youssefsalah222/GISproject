import arcpy
ports = arcpy.GetParameterAsText(0)   # GUI Arcmap
website =arcpy.GetParameterAsText(1)
with arcpy.da.UpdateCursor(ports,['website'])as sc:
    for x in sc:
        if x[0]==' ':
            x[0]=website
            sc.updateRow(x)
arcpy.AddMessage("Done , website updated")
