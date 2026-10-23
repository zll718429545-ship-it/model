import bpy, math, random
from mathutils import Vector
random.seed(8)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def mat(n,c,rough=.5,metal=0):
 m=bpy.data.materials.new(n); m.diffuse_color=(*c,1); m.use_nodes=True; p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*c,1); p.inputs['Roughness'].default_value=rough; p.inputs['Metallic'].default_value=metal; return m
def wood(n,c):
 m=mat(n,c); ns=m.node_tree.nodes; lk=m.node_tree.links; p=ns.get('Principled BSDF'); t=ns.new('ShaderNodeTexNoise'); t.inputs['Scale'].default_value=3; t.inputs['Detail'].default_value=3; tex=ns.new('ShaderNodeTexCoord'); mp=ns.new('ShaderNodeVectorMath'); mp.operation='MULTIPLY'; mp.inputs[1].default_value=(1,32,5); lk.new(tex.outputs['Generated'],mp.inputs[0]); lk.new(mp.outputs[0],t.inputs['Vector']); ramp=ns.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position=.18; ramp.color_ramp.elements[0].color=(*(v*.48 for v in c),1); ramp.color_ramp.elements[1].position=.85; ramp.color_ramp.elements[1].color=(*(v*1.3 for v in c),1); lk.new(t.outputs['Fac'],ramp.inputs[0]); lk.new(ramp.outputs[0],p.inputs['Base Color']); b=ns.new('ShaderNodeBump'); b.inputs['Strength'].default_value=.14; b.inputs['Distance'].default_value=.025; lk.new(t.outputs['Fac'],b.inputs['Height']); lk.new(b.outputs[0],p.inputs['Normal']); return m
walnut=wood('Warm walnut • flowing grain',(.29,.125,.052)); oak=wood('Natural oak floor',(.58,.34,.15)); cream=mat('Warm plaster',(.82,.81,.74),.9); white=mat('Ivory',(.88,.86,.76)); black=mat('Soft black',(.025,.028,.025),.3); silver=mat('Brushed silver',(.55,.56,.52),.28,.7); dark=mat('Graphite aluminum',(.105,.11,.105),.3,.65); screen=mat('Dark reflective display',(.055,.063,.061),.2,.25); rug=mat('Woven linen',(.7,.67,.55),1); accent=mat('Rug charcoal motifs',(.19,.22,.18),1)
def cube(n,loc,scale,m,bevel=.015):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.name=n; o.dimensions=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(m)
 if bevel: mod=o.modifiers.new('Soft crafted edges','BEVEL'); mod.width=bevel; mod.segments=3; o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o
def uv(n,loc,scale,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,location=loc); o=bpy.context.object;o.name=n;o.scale=scale;o.data.materials.append(m);bpy.ops.object.shade_smooth();return o
def cyl(n,loc,r,d,m):
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=d,location=loc);o=bpy.context.object;o.name=n;o.data.materials.append(m);o.modifiers.new('Rounded rim','BEVEL').width=.007;o.modifiers.new('Normals','WEIGHTED_NORMAL');return o
def tor(n,loc,major,minor,m,rot=(0,0,0)):
 bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=40,minor_segments=12,location=loc,rotation=rot);o=bpy.context.object;o.name=n;o.data.materials.append(m);return o
# room, individual floor boards
cube('Plaster back wall',(0,1.01,1.8),(8,.12,3.6),cream)
cube('Painted skirting',(0,.92,.085),(8,.045,.17),white,.008)
for j in range(13):
 for i in range(8):
  cube('Oak plank',(-4+i*1.05+(j%2)*.52,-3+j*.32,-.035),(1.045,.315,.065),oak,.003)
cube('Linen area rug',(0,-1.55,.009),(4.5,1.75,.016),rug,.025)
for i in range(12):
 for j in range(5):
  o=cube('Woven diamond',(-2.02+i*.36,-2.25+j*.34,.019),(.095,.095,.002),accent,.001);o.rotation_euler.z=math.pi/4
# desk
cube('Solid walnut desktop',(0,0,1.45),(2.85,.94,.095),walnut,.055)
for x in [-1.08,1.08]:
 cube('Walnut vertical leg',(x,0,.67),(.19,.22,1.26),walnut,.018)
 cube('Rounded sled foot',(x,-.005,.065),(.22,.82,.105),walnut,.05)
 cube('Telescoping black steel',(x,0,1.27),(.12,.16,.28),black)
 cube('Under desktop bracket',(x,0,1.375),(.14,.73,.07),black)
cube('Rear crossbar',(0,.24,1.28),(2.2,.08,.1),black)
for x in [-.64,.39]:
 cube('Slim walnut drawer front',(x,-.37,1.285),(.99,.105,.19),walnut,.01)
 cube('Drawer body',(x,-.08,1.31),(.96,.58,.15),walnut)
# laptop
cube('Laptop base',(.05,.02,1.52),(.65,.43,.025),dark,.018)
cube('Keyboard inset',(.05,.085,1.536),(.56,.2,.006),black,.005)
for row in range(5):
 for col in range(13): cube('Keyboard key',(-.204+col*.042,.015+row*.035,1.542),(.034,.025,.004),dark,.003)
cube('Trackpad',(.05,-.125,1.537),(.23,.1,.003),dark,.008)
o=cube('Laptop lid',(.05,.235,1.79),(.65,.022,.45),dark,.012);o.rotation_euler.x=math.radians(-12)
o=cube('Display glass',(.05,.219,1.79),(.607,.005,.405),screen,.006);o.rotation_euler.x=math.radians(-12)
# lamp
cyl('Lamp foot',(-.96,.10,1.53),.105,.025,black)
uv('Lamp sculpted stem',(-.96,.10,1.65),(.038,.038,.14),black)
lamp=mat('Opal illuminated glass',(.95,.88,.63),.35);p=lamp.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.85,.55,1);p.inputs['Emission Strength'].default_value=.5
uv('Mushroom opal shade',(-.96,.10,1.82),(.18,.18,.115),lamp)
# mug, ribbed ceramic
cyl('Coffee cup',(.55,-.19,1.59),.072,.145,white)
coffee=mat('Coffee',(.065,.027,.009));cyl('Coffee surface',(.55,-.19,1.665),.061,.002,coffee)
tor('Ceramic lip',(.55,-.19,1.665),.066,.006,white)
tor('Cup handle',(.635,-.19,1.595),.043,.012,white,(math.pi/2,0,0))
for k in range(36):
 a=k*math.tau/36;cyl('Cup vertical fluting',(.55+.071*math.cos(a),-.19+.071*math.sin(a),1.59),.002,.125,white)
# book and alarm clock
cube('White art book',(1.02,.17,1.53),(.43,.29,.055),white,.004)
clock=uv('Alarm clock body',(1.03,.19,1.705),(.105,.047,.12),black)
o=cyl('Clock ivory dial',(1.03,.137,1.705),.091,.008,white);o.rotation_euler.x=math.pi/2
tor('Clock chrome bezel',(1.03,.13,1.705),.094,.007,silver,(math.pi/2,0,0))
for k in range(12):
 a=k*math.tau/12;o=cube('Hour marker',(1.03+.075*math.sin(a),.128,1.705+.075*math.cos(a)),(.007,.003,.014),black,.001);o.rotation_euler.y=a
for a,l in [(.3,.056),(-1.1,.043)]:
 o=cube('Clock hand',(1.03+math.sin(a)*l/2,.12,1.705+math.cos(a)*l/2),(.006,.004,l),black,.001);o.rotation_euler.y=a
for x in [.96,1.10]:uv('Alarm bell',(x,.19,1.824),(.047,.04,.025),silver)
tor('Clock top handle',(1.03,.19,1.855),.034,.006,silver,(math.pi/2,0,0))
# bookcase left
cube('Bookcase back',(-2.04,.68,1.34),(.91,.045,2.65),walnut)
for x in [-2.51,-1.57]:cube('Bookcase side',(x,.45,1.36),(.065,.52,2.72),walnut)
for z in [.21,.72,1.24,1.87,2.69]:cube('Bookcase shelf',(-2.04,.43,z),(.94,.57,.055),walnut)
for x in [-2.4,-1.68]:
 for y in [.25,.63]:cyl('Cabinet foot',(x,y,.12),.035,.24,walnut)
cube('Lower cabinet drawer',(-2.04,.40,.43),(.87,.5,.38),walnut)
colors=[white,mat('Book sage',(.35,.40,.31)),mat('Book ochre',(.58,.37,.16)),mat('Book muted red',(.4,.15,.10))]
for base,count in [(1.275,11),(1.905,6)]:
 x=-2.44
 for i in range(count):
  w=random.uniform(.035,.075);h=random.uniform(.27,.41);m=random.choice(colors)
  cube('Book cover',(x+w/2,.29,base+h/2),(w,.26,h),m,.003)
  cube('Book spine label',(x+w/2,.153,base+h*.73),(w*.6,.002,.035),white,.001)
  x+=w+.012
cube('Storage box',(-2.15,.36,.88),(.53,.37,.25),white)
for x in [-2.36,-2.2]:
 cyl('Amber glass bottle',(x,.29,1.365),.041,.16,mat('Amber '+str(x),(.24,.13,.035),.22));cyl('Bottle lid',(x,.29,1.46),.024,.035,black);cyl('Bottle label',(x,.29,1.36),.042,.07,white)
# wall frames with stylized original art
blue=mat('Print dusty blue',(.26,.43,.52));paper=mat('Print paper',(.84,.82,.72));artdark=mat('Bird print background',(.13,.12,.085));bird=mat('Bird ivory',(.7,.68,.56));orange=mat('Beak',(.63,.25,.065))
for x,z,w,h in [(-.80,2.55,.43,.54),(.09,2.28,.46,.56)]:
 cube('Frame backing',(x,.904,z),(w,.04,h),paper)
 for dx in [-w/2,w/2]:cube('Silver picture side',(x+dx,.866,z),(.018,.055,h+.025),silver,.004)
 for dz in [-h/2,h/2]:cube('Silver picture rail',(x,.866,z+dz),(w,.055,.018),silver,.004)
 if x<-.5:
  cube('Landscape print',(x,.875,z),(.24,.008,.3),blue,.001)
  for k in range(18):uv('Cloud brush stroke',(x+random.uniform(-.10,.10),.865,z+random.uniform(-.13,.13)),(random.uniform(.025,.06),.003,.009),white)
 else:
  cube('Bird artwork dark field',(x,.875,z),(.25,.008,.32),artdark,.001)
  o=uv('Bird body',(x,.862,z+.01),(.048,.006,.083),bird);o.rotation_euler.y=.35
  uv('Bird head',(x+.035,.86,z+.09),(.028,.007,.025),bird)
  o=cube('Bird beak',(x+.071,.857,z+.089),(.035,.005,.009),orange,.001);o.rotation_euler.y=.2
  for dx in [-.015,.012]:cube('Bird leg',(x+dx,.858,z-.09),(.004,.003,.07),bird,.001)
# lights
world=bpy.context.scene.world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.78,.81,.86,1);world.node_tree.nodes['Background'].inputs[1].default_value=.35
def area(n,loc,power,size,target,color):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=n;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=color;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
area('Large soft window',(-3,-4,5),500,4,(0,0,1),(1,.9,.74));area('Soft fill',(3,-2,3),110,3,(0,0,1),(1,.97,.90))
bpy.ops.object.camera_add(location=(4,-7,4.1));cam=bpy.context.object;cam.rotation_euler=(Vector((-.38,.12,1.28))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=4.35;bpy.context.scene.camera=cam
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=80;s.cycles.use_denoising=False;s.render.resolution_x=768;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.world.color=(.8,.8,.8);s.view_settings.view_transform='AgX';s.render.image_settings.file_format='PNG';s.render.filepath='/workspace/model/output/study_render.png'
bpy.ops.wm.save_as_mainfile(filepath='/workspace/model/output/warm_study.blend');bpy.ops.render.render(write_still=True)
