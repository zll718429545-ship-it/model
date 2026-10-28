import bpy, math, random, os
from mathutils import Vector
random.seed(42)
OUT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def mat(n,c,r=.5,metal=0):
 m=bpy.data.materials.new(n); m.diffuse_color=(*c,1); m.use_nodes=True; p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*c,1); p.inputs['Roughness'].default_value=r; p.inputs['Metallic'].default_value=metal; return m
def proc(n,c1,c2,scale,stretch,r):
 m=mat(n,c1,r); ns=m.node_tree.nodes; l=m.node_tree.links; p=ns.get('Principled BSDF'); tex=ns.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value=scale; tex.inputs['Detail'].default_value=4; coord=ns.new('ShaderNodeTexCoord'); v=ns.new('ShaderNodeVectorMath'); v.operation='MULTIPLY'; v.inputs[1].default_value=stretch; l.new(coord.outputs['Generated'],v.inputs[0]); l.new(v.outputs[0],tex.inputs['Vector']); ramp=ns.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position=.28; ramp.color_ramp.elements[0].color=(*c1,1); ramp.color_ramp.elements[1].position=.7; ramp.color_ramp.elements[1].color=(*c2,1); l.new(tex.outputs['Fac'],ramp.inputs[0]); l.new(ramp.outputs[0],p.inputs['Base Color']); bump=ns.new('ShaderNodeBump'); bump.inputs['Strength'].default_value=.12; bump.inputs['Distance'].default_value=.025; l.new(tex.outputs['Fac'],bump.inputs['Height']); l.new(bump.outputs[0],p.inputs['Normal']); return m
wall=mat('Warm white plaster',(.79,.78,.73),.85); white=mat('Ivory lacquer',(.83,.82,.77),.35); dark=mat('Dark bronze',(.025,.022,.02),.35,.5); steel=mat('Brushed silver refrigerator',(.42,.43,.42),.3,.65); wood=proc('Oak grain',(.24,.105,.033),(.63,.36,.14),4,(5, .3,3),.36); fabric=proc('Charcoal woven upholstery',(.018,.024,.025),(.075,.083,.08),95,(1,1,1),.9); frame=mat('Mahogany picture frame',(.075,.025,.018),.32); paper=mat('Rice paper',(.73,.69,.55),.9); green=mat('Ink foliage',(.09,.16,.12),.9)
marble=mat('Polished white marble',(.8,.79,.74),.16)
ns=marble.node_tree.nodes; l=marble.node_tree.links; p=ns.get('Principled BSDF'); co=ns.new('ShaderNodeTexNoise'); co.inputs['Scale'].default_value=3.8; co.inputs['Roughness'].default_value=.7; co.inputs['Distortion'].default_value=5; ramp=ns.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position=.47; ramp.color_ramp.elements[0].color=(.08,.085,.08,1); ramp.color_ramp.elements[1].position=.54; ramp.color_ramp.elements[1].color=(.87,.86,.8,1); e=ramp.color_ramp.elements.new(.49); e.color=(.48,.48,.44,1); l.new(co.outputs['Fac'],ramp.inputs[0]); l.new(ramp.outputs[0],p.inputs['Base Color'])
def box(n,loc,size,ma,bev=.015):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.name=n; o.dimensions=size; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(ma)
 if bev: mod=o.modifiers.new('Soft manufactured edges','BEVEL'); mod.width=bev; mod.segments=3; o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL')
 return o
def rod(n,a,b,r,ma):
 d=Vector(b)-Vector(a); bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=d.length,location=(Vector(a)+Vector(b))/2); o=bpy.context.object; o.name=n; o.rotation_euler=d.to_track_quat('Z','Y').to_euler(); o.data.materials.append(ma); return o
# Room: x width, y depth, entrance at y=0
box('Subfloor',(0,3.4,-.09),(3.45,7,.15),wood)
for ix in range(17):
 x=-1.6+ix*.2
 for j in range(6):
  y=j*1.35+(ix%3)*.43-.7; low=max(0,y); high=min(6.8,y+1.34)
  if high>low: box('Individual oak floorboard',(x,(low+high)/2,.005),(.198,high-low,.025),wood,.003)
box('Left wall',(-1.78,3.4,1.45),(.16,6.8,2.9),wall)
box('Back wall',(0,6.9,1.45),(3.7,.16,2.9),wall)
# right doorway 3.0 to 4.15
for y,dy in [(1.5,3),(5.5,2.7)]: box('Right wall',(1.78,y,1.45),(.16,dy,2.9),wall)
box('Doorway lintel',(1.78,3.57,2.62),(.16,1.15,.56),wall)
box('Ceiling',(0,3.4,2.99),(3.65,7,.16),wall)
for x in [-1.68,1.68]:
 box('Oak skirting',(x,3.4,.065),(.035,6.8,.13),wood,.005)
 for z,w in [(2.83,.06),(2.88,.1),(2.92,.14)]: box('Crown molding',(x,3.4,z),(w,6.8,.045),white,.008)
box('Back skirting',(0,6.79,.065),(3.4,.03,.13),wood)
# refrigerator left
box('Fridge body',(-1.27,3.6,1.02),(.68,.67,2.04),dark,.035)
for z,h in [(.45,.83),(1.47,1.13)]: box('Silver refrigerator door',(-1.27,3.245,z),(.665,.055,h),steel,.025)
box('Fridge door divider',(-1.27,3.205,.9),(.65,.02,.018),dark,.003)
box('Fridge energy label',(-1.04,3.207,1.9),(.075,.003,.12),white,.002)
# wardrobe end right
box('Wardrobe carcass',(.98,6.47,1.34),(1.27,.6,2.68),white,.02)
for x in [.66,1.3]:
 for z,h in [(.61,1.17),(1.93,1.43)]: box('Wardrobe inset door',(x,6.15,z),(.625,.035,h),white,.006)
 for z in [1.06,1.38]: rod('Wardrobe metal pull',(x+(.25 if x<1 else -.25),6.11,z-.055),(x+(.25 if x<1 else -.25),6.11,z+.055),.009,steel)
# sofa left back
for y in [4.7,5.95]:
 for x in [-1.49,-.85]: box('Sofa pale wood legs',(x,y,.22),(.055,.065,.44),white)
box('Sofa seat frame',(-1.18,5.32,.4),(.8,1.5,.09),white)
box('Sofa charcoal seat',(-1.17,5.32,.49),(.69,1.36,.16),fabric,.06)
box('Sofa back cushion',(-1.48,5.32,.79),(.16,1.4,.64),fabric,.07)
for y in [4.6,6.04]: box('Sofa arm',(-1.16,y,.68),(.82,.065,.08),white)
# coffee table
box('Coffee table top',(-.35,5.35,.47),(.62,1.05,.065),wood,.025)
box('Coffee table apron',(-.35,5.35,.34),(.57,.95,.24),wood)
for x in [-.59,-.11]:
 for y in [4.95,5.75]: box('Coffee table leg',(x,y,.19),(.045,.045,.38),wood)
box('Remote on coffee table',(-.29,5.15,.515),(.07,.2,.018),dark,.01)
# wall TV on right
box('TV wall bracket',(1.65,5.68,1.18),(.08,.24,.28),dark)
box('Television slim body',(1.58,5.68,1.23),(.07,.93,.62),dark,.025)
box('Television screen',(1.535,5.68,1.23),(.006,.86,.55),mat('TV glass',(.025,.035,.04),.12),.005)
rod('TV cable',(1.65,5.68,.98),(1.65,5.68,.28),.006,dark)
# dining table in foreground right
box('Dining oak apron',(.98,1.67,.72),(1.02,1.92,.15),wood)
box('Marble dining tabletop',(.98,1.67,.83),(1.15,2.08,.065),marble,.075)
for x in [.51,1.45]:
 for y in [.81,2.53]: box('Dining table oak legs',(x,y,.38),(.075,.075,.76),wood,.012)
def chair(n,x,y,ang):
 parent=bpy.data.objects.new(n,None); bpy.context.collection.objects.link(parent)
 parts=[]
 parts.append(box(n+' seat',(0,0,.46),(.48,.46,.12),fabric,.055))
 parts.append(box(n+' upholstered back',(0,.2,.83),(.49,.095,.68),fabric,.075))
 for xx in [-.18,.18]:
  for yy in [-.16,.16]: parts.append(rod(n+' leg',(xx,yy,.43),(xx*1.1,yy*1.1,.035),.018,dark))
 for p in parts: p.parent=parent
 parent.location=(x,y,0); parent.rotation_euler.z=ang
chair('Near dining chair',.98,.33,math.pi)
chair('Far dining chair',.98,2.94,0)
chair('Side dining chair',.16,1.72,math.pi/2)
# control panels on left
box('Intercom backing',(-1.675,2.48,1.47),(.045,.21,.2),white)
box('Intercom screen',(-1.646,2.48,1.49),(.007,.16,.115),dark)
for y in [.85,2.1]:
 box('Wall light switch',(-1.675,y,1.25),(.03,.105,.105),white)
 box('Switch rocker',(-1.655,y,1.25),(.012,.07,.065),white)
# pictures procedural ink landscape relief, left wall
for cy,cz,w,h in [(1.9,2.12,1.28,.65),(4.28,2.12,.48,.63)]:
 box('Dark wood picture frame',(-1.66,cy,cz),(.055,w,h),frame,.009)
 box('Landscape paper',(-1.625,cy,cz),(.008,w-.08,h-.08),paper,.001)
 for k in range(45):
  yy=cy+random.uniform(-w*.42,w*.42); zz=cz+random.uniform(-h*.36,h*.23)
  o=box('Ink landscape brushstroke',(-1.616,yy,zz),(.006,random.uniform(.02,.12),random.uniform(.006,.035)),green,.003); o.rotation_euler.x=random.uniform(-.7,.7)
# left entrance frame visible
for y in [.03]:
 box('Entrance dark jamb',(-1.65,y,1.2),(.12,.13,2.4),frame)
# ceiling square cluster
em=mat('LED diffuser',(1,1,.94),.25); p=em.node_tree.nodes.get('Principled BSDF'); p.inputs['Emission Color'].default_value=(1,1,.94,1); p.inputs['Emission Strength'].default_value=3
for x,y in [(-.22,4.65),(.22,4.65),(-.22,5.08),(.22,5.08),(0,4.86)]:
 box('Ceiling light black housing',(x,y,2.83),(.44,.44,.12),dark,.045); box('Square luminous diffuser',(x,y,2.758),(.4,.4,.025),em,.04)
for x in [-.3,0,.3]:
 rod('Entry pendant cable',(x,1.1,2.92),(x,1.1,2.68),.009,dark)
 bpy.ops.mesh.primitive_cone_add(vertices=48,radius1=.17,radius2=.07,depth=.24,location=(x,1.1,2.58)); bpy.context.object.name='Black entry pendant shade'; bpy.context.object.data.materials.append(dark)
 rod('Pendant luminous disk',(x,1.1,2.455),(x,1.1,2.46),.155,em)
def area(n,loc,target,power,size,color):
 bpy.ops.object.light_add(type='AREA',location=loc); o=bpy.context.object; o.name=n; o.data.energy=power; o.data.shape='DISK'; o.data.size=size; o.data.color=color; o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
area('Daylight from right doorway',(2.7,3.6,2),(0,3,1),480,2.5,(1,.94,.84))
area('Ceiling bounce',(0,4.85,2.67),(0,4.8,0),160,1.8,(1,.95,.88))
area('Entry soft daylight',(-.4,-1,2.1),(0,3,1),260,3,(.87,.93,1))
bpy.ops.object.camera_add(location=(-.48,-.3,1.62)); cam=bpy.context.object; cam.name='Photo matching entrance camera'; cam.rotation_euler=(Vector((.04,4.7,1.36))-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.lens=20; bpy.context.scene.camera=cam
sc=bpy.context.scene; sc.render.engine='CYCLES'; sc.cycles.samples=48; sc.cycles.use_denoising=False; sc.render.resolution_x=1200; sc.render.resolution_y=900; sc.render.resolution_percentage=100; sc.world.color=(.22,.22,.22); sc.view_settings.view_transform='AgX'; sc.render.image_settings.file_format='PNG'; sc.render.filepath=OUT+'/preview.png'
sc['reference_note']='Approximate reconstruction from one supplied photograph. Dimensions inferred; artwork represented procedurally.'
bpy.ops.wm.save_as_mainfile(compress=True,filepath=OUT+'/photo_apartment.blend'); bpy.ops.render.render(write_still=True)
