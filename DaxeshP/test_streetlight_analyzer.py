import arcpy
import streetlight_analyzer as sa

sa.streetlight_fc = r'..\..\..\..\data\Ottawa\Street_Lights\Street_Lights.shp'
sa.roads_cl_fc = r'..\..\..\..\data\Ottawa\Road_Centrelines\Road_Centrelines.shp'
sa.road_name_field = 'ROAD_NAME_'

arcpy.env.overwriteOutput = True

def test_get_unique_values():
    result = sa._get_unique_values(sa.streetlight_fc, 'LIGHT_TYPE')
    assert result, "Unique values should not be empty"

def test_get_streetlight_count():
    assert sa.get_streetlight_count("CARLING AVE", 0.0002) == 849

def test_save_streetlights():
    out_fc = r'..\output\carling_lights.shp'
    sa.save_streetlights("CARLING AVE", 0.0002, out_fc)
    assert arcpy.Exists(out_fc), f"{out_fc} was not created"
    assert int(arcpy.management.GetCount(out_fc)[0]) == 849, f"Expected 849 features, found {arcpy.management.GetCount(out_fc)[0]}"

def test_show_road_names(capsys):
    sa.show_road_names('car')
    captured = capsys.readouterr()
    assert 'CARLING' in captured.out
    assert len(captured.out.split('\n')) == 113
