import bpy, math, os, random
from mathutils import Vector
OUT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
sc=bpy.context.scene
sc.render.engine='BLENDER_WORKBENCH'
sc.display.shading.light='STUDIO'; sc.display.shading.studiolight_rotate_z=0.4
sc.display.shading.color_type='MATERIAL'; sc.display.shading.show_shadows=True
sc.display.shading.show_cavity=True; sc.display.shading.cavity_type='BOTH'
sc.display.shading.curvature_ridge_factor=1.3; sc.display.shading.curvature_valley_factor=1.1
sc.display.shading.show_specular_highlight=True
sc.display.shading.background_type='WORLD'; sc.world.color=(0.78,0.80,0.82)
sc.render.resolution_x=960; sc.render.resolution_y=540; sc.render.resolution_percentage=100
sc.render.fps=24; sc.frame_start=1; sc.frame_end=360
sc.render.image_settings.file_format='PNG'; sc.render.film_transparent=False

def mat(n,c):
 m=bpy.data.materials.new(n); m.diffuse_color=(*c,1); return m
white=mat('Porcelain',(0.86,.86,.84)); gray=mat('Warm chalk',(.67,.69,.69)); dark=mat('Pale graphite',(.36,.40,.42)); road=mat('Street',(.56,.59,.60))
def finish(o,n,m,parent=None):
 o.name=n; o.data.materials.append(m)
 if parent:o.parent=parent
 return o
def cube(n,p,s,m=white,parent=None,bevel=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p); o=bpy.context.object; o.scale=s
 if bevel:
  bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); mod=o.modifiers.new('Soft edges','BEVEL'); mod.width=bevel; mod.segments=2; o.modifiers.new('Normals','WEIGHTED_NORMAL')
 return finish(o,n,m,parent)
def ball(n,p,s,m=white,parent=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,location=p); o=bpy.context.object; o.scale=s
 for f in o.data.polygons:f.use_smooth=True
 return finish(o,n,m,parent)
def rod(n,a,b,r=.04,m=white,parent=None):
 a,b=Vector(a),Vector(b); bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=r,depth=(b-a).length,location=(a+b)/2); o=bpy.context.object; o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); return finish(o,n,m,parent)
def setrod(o,a,b):
 a,b=Vector(a),Vector(b); o.location=(a+b)/2; o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); o.scale.z=(b-a).length/o.data['length']
 for prop in ['location','rotation_euler','scale']:o.keyframe_insert(prop)
def movingrod(n,r,m):
 o=rod(n,(0,0,0),(0,0,1),r,m,root); o.data['length']=1.; return o
bpy.ops.object.empty_add(); root=bpy.context.object; root.name='Cyclist • animated route'
# Bicycle faces +X, wheel axle along Y.
wheels=[]
for x in [-.82,.82]:
 bpy.ops.object.empty_add(location=(x,0,.57)); hub=bpy.context.object; hub.parent=root; hub.name='Rolling wheel'; wheels.append(hub)
 bpy.ops.mesh.primitive_torus_add(major_radius=.50,minor_radius=.045,major_segments=40,minor_segments=8,location=(0,0,0),rotation=(math.pi/2,0,0)); o=bpy.context.object; o.parent=hub; finish(o,'Whitewall tyre',dark)
 for i in range(12):
  a=i*math.pi/6; rod('Spoke',(0,0,0),(.49*math.cos(a),0,.49*math.sin(a)),.009,gray,hub)
 ball('Axle',(x,0,.57),(.07,.10,.07),gray,root)
A=(-.82,0,.57); B=(-.30,0,1.28); C=(.05,0,.62); D=(.60,0,1.32); E=(.82,0,.57)
for a,b in [(A,B),(B,C),(C,A),(B,D),(D,C),(D,E)]:rod('Bicycle frame',a,b,.036,white,root)
rod('Seat post',B,(-.33,0,1.46),.035,gray,root); cube('Saddle',(-.37,0,1.47),(.33,.23,.07),dark,root,.03)
rod('Stem',D,(.60,0,1.58),.035,gray,root); rod('Handlebar',(.60,-.34,1.58),(.60,.34,1.58),.028,dark,root)
# Stylized adult woman, sculptural white clay.
ball('Jacket torso',(-.13,0,1.88),(.23,.19,.40),white,root).rotation_euler.y=.45
ball('Pelvis',(-.38,0,1.53),(.23,.20,.18),gray,root)
rod('Neck',(.02,0,2.13),(.08,0,2.28),.09,white,root)
ball('Face',(.10,0,2.42),(.18,.155,.23),white,root)
ball('Hair cap',(.04,.01,2.49),(.19,.17,.20),gray,root)
ball('Nose',(.273,0,2.42),(.055,.05,.055),white,root)
rod('Ponytail',(-.10,.04,2.48),(-.42,.07,2.29),.085,gray,root)
for y in [-.17,.17]:
 shoulder=(-.01,y,2.06); elbow=(.28,y*1.5,1.83); hand=(.60,y*1.7,1.58)
 rod('Upper sleeve',shoulder,elbow,.075,white,root); ball('Elbow',elbow,(.076,)*3,white,root); rod('Forearm',elbow,hand,.055,white,root); ball('Hand',hand,(.065,)*3,white,root)
legs=[]
for y in [-.14,.14]:legs.append([movingrod('Thigh',.095,gray),movingrod('Shin',.065,white),ball('Knee',(0,0,0),(.09,)*3,gray,root),cube('Sneaker',(0,0,0),(.27,.13,.10),white,root,.03),movingrod('Crank',.018,dark)])
# White city blocks, arcades, trees, planters and lane markings.
cube('Ground',(24,0,-.18),(120,70,.3),white)
cube('Road',(24,0,.0),(110,6,.08),road)
for y in [-3.5,3.5]:cube('Raised pavement',(24,y,.10),(110,1,.22),white,.0 if False else None)
random.seed(9)
for x in range(-12,80,5):
 for side in [-1,1]:
  y=side*6.2; h=random.uniform(3.2,7)
  cube('White city block',(x,y,h/2),(3.7,3.5,h),white,bevel=.10)
  for z in [1.1,2.4,3.7,5.0]:
   if z<h-.4:
    for dx in [-1,0,1]:cube('Recess window',(x+dx,y-side*1.77,z),(.53,.035,.64),gray)
  cube('Cornice',(x,y,h),(3.9,3.7,.16),white)
  rod('Tree trunk',(x+2,side*3.7,.2),(x+2,side*3.7,1.8),.08,gray)
  ball('Tree crown',(x+2,side*3.7,2.2),(.65,.65,.85),white)
for x in range(-15,85,3):cube('Lane dash',(x,0,.05),(1.2,.075,.015),white)
# Low bollards create a visible slalom corridor.
for x in range(7,53,6):
 y=-1.25 if (x//6)%2 else 1.25
 rod('Bollard',(x,y,.08),(x,y,.64),.10,white); ball('Bollard cap',(x,y,.64),(.1,.1,.1),white)
bpy.ops.object.camera_add(); cam=bpy.context.object; sc.camera=cam; cam.data.lens=32
for f in range(1,361):
 t=(f-1)/24; x=t*3.5; y=.68*math.sin(t*1.15); heading=math.atan2(.68*1.15*math.cos(t*1.15),3.5)
 root.location=(x,y,0); root.rotation_euler=(.035*math.sin(t*1.15),0,heading)
 root.keyframe_insert('location',frame=f); root.keyframe_insert('rotation_euler',frame=f)
 phase=t*2*math.pi*1.25
 for w in wheels:w.rotation_euler.y=-x/.50; w.keyframe_insert('rotation_euler',frame=f)
 sc.frame_set(f)
 for i,(th,sh,knee,shoe,crank) in enumerate(legs):
  yy=[-.14,.14][i]; a=phase+i*math.pi; foot=Vector((.05+.20*math.cos(a),yy,.65+.20*math.sin(a))); hip=Vector((-.38,yy,1.56))
  mid=(hip+foot)/2; d=(hip-foot).length; bend=math.sqrt(max(.01,.53**2-(d/2)**2)); mid+=Vector((bend,0,0))
  setrod(th,hip,mid); setrod(sh,mid,foot); setrod(crank,(.05,yy,.65),foot)
  knee.location=mid; knee.keyframe_insert('location',frame=f); shoe.location=foot; shoe.keyframe_insert('location',frame=f)
 angle=.20*math.sin(t*.25)
 cam.location=(x+5.6+angle,y-2.8,3.5+.25*math.sin(t*.3)); target=Vector((x+.15,y,1.20)); cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
 cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_euler',frame=f)
for o in bpy.data.objects:
 if o.animation_data and o.animation_data.action:
  for fc in o.animation_data.action.fcurves:
   for k in fc.keyframe_points:k.interpolation='LINEAR'
sc.frame_set(120)
sc.render.filepath=OUT+'/preview.png'; bpy.ops.wm.save_as_mainfile(filepath=OUT+'/white_city_ride.blend'); bpy.ops.render.render(write_still=True)
sc.render.filepath=OUT+'/frames/'; os.makedirs(OUT+'/frames',exist_ok=True)
bpy.ops.render.render(animation=True)
