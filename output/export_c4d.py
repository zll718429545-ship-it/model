import bpy
from pathlib import Path
out=Path('/workspace/model/output')
bpy.ops.wm.open_mainfile(filepath=str(out/'warm_study.blend'))
bpy.ops.export_scene.fbx(filepath=str(out/'warm_study_c4d.fbx'),use_selection=False,object_types={'MESH','CAMERA','LIGHT'},apply_unit_scale=True,bake_anim=False,path_mode='AUTO')
print('FBX_EXPORTED', (out/'warm_study_c4d.fbx').stat().st_size)
