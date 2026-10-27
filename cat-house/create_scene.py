import bpy, math, os
from mathutils import Vector
O='/workspace/work/blender_cat_house';os.makedirs(O,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.unit_settings.system='METRIC';scene.unit_settings.length_unit='MILLIMETERS'
def wood(name,c1,c2):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links
 out=n.new('ShaderNodeOutputMaterial');bs=n.new('ShaderNodeBsdfPrincipled');bs.inputs['Roughness'].default_value=.43;l.new(bs.outputs['BSDF'],out.inputs['Surface'])
 tc=n.new('ShaderNodeTexCoord');mp=n.new('ShaderNodeMapping');mp.inputs['Scale'].default_value=(3,48,5);l.new(tc.outputs['Generated'],mp.inputs['Vector'])
 noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=3;noise.inputs['Detail'].default_value=3;noise.inputs['Roughness'].default_value=.65;l.new(mp.outputs['Vector'],noise.inputs['Vector'])
 ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.18;ramp.color_ramp.elements[0].color=(*c1,1);ramp.color_ramp.elements[1].position=.83;ramp.color_ramp.elements[1].color=(*c2,1);l.new(noise.outputs['Fac'],ramp.inputs['Fac']);l.new(ramp.outputs['Color'],bs.inputs['Base Color'])
 bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.14;bump.inputs['Distance'].default_value=.0003;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],bs.inputs['Normal']);return m
woodmat=wood('Warm natural oak | procedural grain',(.30,.15,.061),(.72,.48,.24))
def material(name,color,rough=.5):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;return m
fabric=material('Sage woven linen',(.34,.42,.31),.93)
n=fabric.node_tree.nodes;l=fabric.node_tree.links;noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=260;bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.22;bump.inputs['Distance'].default_value=.0005;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],n.get('Principled BSDF').inputs['Normal'])
seammat=material('Piping | sage',(.23,.30,.22),.9);groundmat=material('Warm studio backdrop',(.78,.75,.68),.85)
def finish(o,mat,bevel=0):
 o.data.materials.append(mat)
 if bevel:
  mod=o.modifiers.new('Soft sanded edges','BEVEL');mod.width=bevel;mod.segments=6
  norm=o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o
def box(name,loc,dim,mat,bevel=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return finish(o,mat,bevel)
def prism(name,pts,y0,y1,mat):
 verts=[(x,y0,z) for x,z in pts]+[(x,y1,z) for x,z in pts];n=len(pts);faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o)
 # Recalculate normals for bevel and rendering.
 bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT');o.select_set(False)
 return finish(o,mat,.004 if name.startswith('04') else .005)
# Coordinates in metres, floor top at .038 and ridge .560.
T=.018;z0=.038;H=.560;slope=(H-z0)/.3;ih=H-T*math.sqrt(1+slope*slope);ix=(ih-z0)/slope
box('01 | Solid wood floor 600 x 600 x 18 mm',(0,0,.029),(.6,.6,.018),woodmat,.006)
left=[(-.3,z0),(0,H),(0,ih),(-ix,z0)]
prism('02 | Left roof | 18 mm solid wood',left,-.3,.3,woodmat)
prism('03 | Right roof | 18 mm solid wood',[(-x,z) for x,z in reversed(left)],-.3,.3,woodmat)
rear=prism('04 | Rear triangular wall',[(-ix,z0),(ix,z0),(0,ih)],.282,.3,woodmat)
bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=.03,depth=.06,location=(0,.291,.250),rotation=(math.pi/2,0,0));cutter=bpy.context.object
mod=rear.modifiers.new('Ventilation hole diameter 60 mm','BOOLEAN');mod.object=cutter
bpy.context.view_layer.objects.active=rear;bpy.ops.object.modifier_move_up(modifier=mod.name);bpy.ops.object.modifier_move_up(modifier=mod.name);bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
for i,(x,y) in enumerate([(-.25,-.25),(.25,-.25),(-.25,.25),(.25,.25)]):box(f'Foot {i+1} | 40 x 40 x 20 mm',(x,y,.01),(.04,.04,.02),woodmat,.005)
# Removable cushion with rounded corners.
pad=box('Removable sage linen cushion | 450 x 520 x 40 mm',(0,-.015,.058),(.45,.52,.04),fabric)
bevel=pad.modifiers.new('Soft rounded cushion','BEVEL');bevel.width=.018;bevel.segments=7
pad.modifiers.new('Cushion normals','WEIGHTED_NORMAL')
# Closed rounded-rectangle seam on top.
pts=[]
for cx,cy,start in [(.201,.221,0),(-.201,.221,90),(-.201,-.251,180),(.201,-.251,270)]:
 for i in range(13):
  a=math.radians(start+i*90/12);pts.append((cx+.018*math.cos(a),cy+.018*math.sin(a),.075))
curve=bpy.data.curves.new('Cushion piping','CURVE');curve.dimensions='3D';curve.bevel_depth=.0011;curve.bevel_resolution=3;s=curve.splines.new('POLY');s.points.add(len(pts)-1)
for p,co in zip(s.points,pts):p.co=(*co,1)
s.use_cyclic_u=True;o=bpy.data.objects.new('Cushion stitched piping',curve);bpy.context.collection.objects.link(o);o.data.materials.append(seammat)
box('Studio floor',(0,0,-.018),(200,200,.03),groundmat)
def aim(o,point):o.rotation_euler=(Vector(point)-o.location).to_track_quat('-Z','Y').to_euler()
def area(name,loc,power,size,color):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=color;aim(o,(0,0,.2))
area('Large soft key',(-.8,-1.1,1.7),95,1.3,(1,.86,.69));area('Front fill',(.8,-1.4,.8),45,1.1,(.84,.91,1));area('Rim',(.3,.9,1.4),80,1,(1,.92,.79))
bpy.ops.object.camera_add(location=(.88,-1.55,.86));cam=bpy.context.object;cam.name='Presentation camera';aim(cam,(0,0,.25));cam.data.type='ORTHO';cam.data.ortho_scale=.98;scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=False
scene.render.resolution_x=1000;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.world.color=(.23,.23,.23)
scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG';scene.render.filepath=O+'/cat_house_render.png'
# Open in a useful model view.
for ar in bpy.context.screen.areas:
 if ar.type=='VIEW_3D':
  ar.spaces.active.region_3d.view_distance=1.4;ar.spaces.active.region_3d.view_location=(0,0,.26)
bpy.ops.object.select_all(action='DESELECT');bpy.context.view_layer.objects.active=pad
scene['design_notes']='Tent solid wood cat house. Overall 600 x 600 x 560 mm. 18 mm wood. Rounded revision: roof 5 mm, base 6 mm, rear 4 mm, feet 5 mm, 6-segment bevels. Concept model; fasteners not detailed.'
bpy.ops.wm.save_as_mainfile(filepath=O+'/tent_cat_house.blend')
bpy.ops.render.render(write_still=True)
