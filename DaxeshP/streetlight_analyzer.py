import arcpy
import os

streetlight_fc = None
roads_cl_fc = None
road_name_field = None


def _get_unique_values(fc, field_name):
    return set(row[0] for row in arcpy.da.SearchCursor(fc, field_name))


def _get_streetlight_layer(road_name, distance):
    if road_name not in _get_unique_values(roads_cl_fc, road_name_field):
        return None
    
    wc = f"{road_name_field}='{road_name}'"
    road_lyr = arcpy.management.MakeFeatureLayer(roads_cl_fc, 'Selected roads', where_clause=wc)
    streetlight_lyr = arcpy.management.MakeFeatureLayer(streetlight_fc, 'All streetlights')
    
    return arcpy.management.SelectLayerByLocation(streetlight_lyr, 'WITHIN_A_DISTANCE', road_lyr, distance)


def get_streetlight_count(road_name, distance):
    streetlight_layer = _get_streetlight_layer(road_name, distance)
    return int(arcpy.management.GetCount(streetlight_layer)[0]) if streetlight_layer else 0


def save_streetlights(road_name, distance, out_fc):
    streetlight_layer = _get_streetlight_layer(road_name, distance)
    
    if streetlight_layer:
        print(f'Writing selected features to {out_fc}')
        arcpy.management.CopyFeatures(streetlight_layer, out_fc)
    else:
        print(f'{road_name} not found. No features to write to {out_fc}')


def show_road_names(pattern=None):
    road_field = arcpy.AddFieldDelimiters(os.path.dirname(roads_cl_fc), road_name_field)
    where_clause = f"{road_field} LIKE '%{pattern.upper()}%'" if pattern else ''
    
    names = {row[0] for row in arcpy.da.SearchCursor(roads_cl_fc, road_name_field, where_clause=where_clause)}
    
    for name in names:
        print(name)
