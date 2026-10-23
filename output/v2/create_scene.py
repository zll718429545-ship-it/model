import bpy, math, random, os
from pathlib import Path
OUT = Path(__file__).resolve().parent
PREVIEW = os.environ.get("STUDY_PREVIEW") == "1"
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

# Refinement pass: joinery, surface grain, furnishing and photographic framing.
def remove_prefix(*prefixes):
 for o in list(bpy.data.objects):
  if any(o.name.startswith(p) for p in prefixes): bpy.data.objects.remove(o,do_unlink=True)
def material_for(o,m):
 o.data.materials.clear();o.data.materials.append(m)
def timber(n,axis='X',floor=False):
 m=mat(n,(.32,.145,.055) if not floor else (.55,.32,.14),.43)
 ns=m.node_tree.nodes;lk=m.node_tree.links;p=ns.get('Principled BSDF')
 p.inputs['Coat Weight'].default_value=.16;p.inputs['Coat Roughness'].default_value=.36
 tc=ns.new('ShaderNodeTexCoord')
 stretch=ns.new('ShaderNodeVectorMath');stretch.operation='MULTIPLY'
 stretch.inputs[1].default_value={'X':(.65,38,9),'Y':(28,.65,10),'Z':(22,18,.8)}[axis]
 lk.new(tc.outputs['Generated'],stretch.inputs[0])
 noise=ns.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=3.2;noise.inputs['Detail'].default_value=3;noise.inputs['Roughness'].default_value=.72
 lk.new(stretch.outputs['Vector'],noise.inputs['Vector'])
 ramp=ns.new('ShaderNodeValToRGB')
 stops=[(.15,(.085,.029,.009,1)),(.38,(.19,.074,.026,1)),(.57,(.29,.132,.055,1)),(.82,(.40,.215,.103,1))]
 if floor:stops=[(.1,(.30,.151,.057,1)),(.4,(.48,.265,.111,1)),(.65,(.61,.377,.185,1)),(.9,(.72,.48,.255,1))]
 ramp.color_ramp.elements.remove(ramp.color_ramp.elements[1])
 for i,(pos,col) in enumerate(stops):
  e=ramp.color_ramp.elements[0] if i==0 else ramp.color_ramp.elements.new(pos);e.position=pos;e.color=col
 lk.new(noise.outputs['Fac'],ramp.inputs[0]);lk.new(ramp.outputs['Color'],p.inputs['Base Color'])
 bump=ns.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.18;bump.inputs['Distance'].default_value=.0012
 lk.new(noise.outputs['Fac'],bump.inputs['Height']);lk.new(bump.outputs[0],p.inputs['Normal'])
 return m
wood_x=timber('Walnut | longitudinal grain');wood_z=timber('Walnut | upright grain','Z');wood_y=timber('Walnut | sled grain','Y');floor_mat=timber('Oak | satin boards','X',True)
for o in list(bpy.data.objects):
 if o.type!='MESH':continue
 if walnut in o.data.materials[:]:
  material_for(o,wood_z if any(s in o.name for s in ['vertical leg','Bookcase side','Bookcase back','Cabinet foot']) else wood_y if 'sled foot' in o.name else wood_x)
 if 'Oak plank' in o.name: material_for(o,floor_mat)
# Lower the wood sleeves so the black lifting columns are visible.
for o in bpy.data.objects:
 if o.name.startswith('Walnut vertical leg'):o.scale.z*=.81;o.location.z=.57
 if o.name.startswith('Solid walnut desktop'):
  o.scale.z*=.83;o.modifiers.get('Soft crafted edges').width=.028
 if o.name.startswith('Slim walnut drawer front'):
  o.scale.z*=.73;o.location.z=1.30
 if o.name.startswith('Drawer body'):o.scale.z*=.8;o.location.z=1.32
 if o.name.startswith('Rounded sled foot'):o.scale.x*=.86
# Fine joinery grooves, metal trim and lift controls.
for x in [-1.08,1.08]:
 cube('Leg joinery recess',(x+.058,-.112,.57),(.007,.003,.92),black,.001)
 cube('Lifting column collar',(x,0,1.105),(.145,.185,.045),black,.005)
 cube('Metal upper saddle',(x,0,1.36),(.22,.68,.055),black,.01)
for x in [-.93,.94]:
 for y in [-.30,.30]:
  cyl('Underside fastener',(x,y,1.39),.013,.012,silver)
control=cube('Desk height controller',(.9,-.355,1.335),(.22,.10,.033),black,.008)
for x in [.85,.9,.95]:cube('Controller key',(x,-.407,1.337),(.025,.003,.012),dark,.002)
# Sculpted lamp with continuous turned profile.
remove_prefix('Lamp foot','Lamp sculpted stem','Mushroom opal shade')
def lathe(name,profile,center,material,segments=96):
 verts=[];faces=[]
 for radius,z in profile:
  for k in range(segments):
   a=k*math.tau/segments;verts.append((center[0]+radius*math.cos(a),center[1]+radius*math.sin(a),center[2]+z))
 for j in range(len(profile)-1):
  for k in range(segments):
   a=j*segments+k;b=j*segments+(k+1)%segments;faces.append((a,b,b+segments,a+segments))
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.data.materials.append(material)
 for f in mesh.polygons:f.use_smooth=True
 return o
lathe('Turned black lamp pedestal',[(0,0),(.096,0),(.105,.009),(.096,.018),(.065,.025),(.039,.047),(.023,.09),(.016,.135),(.018,.175),(.034,.20),(.064,.213),(0,.214)],(-.96,.10,1.495),black)
lathe('Opal dome shade',[(0,0),(.07,0),(.125,.006),(.162,.017),(.176,.032),(.174,.053),(.159,.081),(.136,.11),(.102,.135),(.061,.152),(0,.162)],(-.96,.10,1.708),lamp)
p=lamp.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Strength'].default_value=1.4
# Cup warm glaze and terracotta foot.
ceramic=mat('Fluted warm porcelain',(.62,.50,.31),.27)
for o in bpy.data.objects:
 if o.name.startswith(('Coffee cup','Cup vertical fluting','Ceramic lip','Cup handle')):material_for(o,ceramic)
cyl('Ceramic unglazed foot',(.55,-.19,1.518),.06,.013,mat('Unglazed clay',(.33,.15,.06),.8))
# Correct the laptop screen hinge: the lid leans away from the keyboard.
for o in bpy.data.objects:
 if o.name.startswith(('Laptop lid','Display glass')):o.rotation_euler.x=math.radians(-12)
# Book jackets and page blocks.
pages=mat('Warm paper edges',(.74,.70,.59),.9)
for o in list(bpy.data.objects):
 if o.name.startswith('Book cover'):
  w,d,h=o.dimensions;loc=o.location.copy()
  cube('Book page block',(loc.x,loc.y+.014,loc.z),(max(.01,w-.009),d-.025,h-.012),pages,.002)
  for side in [-1,1]:cube('Printed book board',(loc.x+side*(w/2-.002),loc.y,loc.z),(.004,d,h),o.data.materials[0],.001)
  o.scale.y=.045;o.location.y=.155
# Remove bottles overlapping the books; place them on the shelf below.
for o in bpy.data.objects:
 if o.name.startswith(('Amber glass bottle','Bottle lid','Bottle label')):o.location.z-=.52
# More convincing labels and typography.
def text_obj(name,body,loc,size,material,rotation=(math.pi/2,0,0),align='CENTER'):
 c=bpy.data.curves.new(name,'FONT');c.body=body;c.size=size;c.align_x=align;c.extrude=.0001;c.space_character=1.05
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=rotation;o.data.materials.append(material);return o
text_obj('Art book title','M & C',(1.02,.021,1.516),.029,black)
text_obj('Storage box number','02',(-2.03,.168,.79),.11,black)
for x in [-2.36,-2.2]:text_obj('Bottle label typography','BOTANIC',(x,.246,.839),.012,black)
for o in list(bpy.data.objects):
 if o.name.startswith('Book spine label'):
  text_obj('Spine typography','ART',(o.location.x,.149,o.location.z-.007),.010,black)
# Alarm: foot pegs and a black casing instead of chrome bells.
for x in [.974,1.086]:
 o=cyl('Alarm clock foot',(x,.19,1.57),.012,.045,black);o.rotation_euler.y=(-.25 if x<1.03 else .25)
for o in bpy.data.objects:
 if o.name.startswith('Alarm bell'):material_for(o,black)
for k in range(60):
 a=k*math.tau/60
 o=cube('Minute marker',(1.03+.081*math.sin(a),.124,1.705+.081*math.cos(a)),(.0016,.002,.006),black,.0003);o.rotation_euler.y=a
text_obj('Clock maker','QUARTZ',(1.03,.119,1.667),.009,black)
# Woven material at a physically small scale, shared by the dark motifs.
def fabric(material):
 ns=material.node_tree.nodes;lk=material.node_tree.links;p=ns.get('Principled BSDF');tex=ns.new('ShaderNodeTexCoord')
 wave=[]
 for axis in ['X','Y']:
  n=ns.new('ShaderNodeTexWave');n.bands_direction=axis;n.inputs['Scale'].default_value=340;n.inputs['Distortion'].default_value=2.3;lk.new(tex.outputs['Object'],n.inputs['Vector']);wave.append(n)
 mix=ns.new('ShaderNodeMath');mix.operation='MULTIPLY';lk.new(wave[0].outputs['Fac'],mix.inputs[0]);lk.new(wave[1].outputs['Fac'],mix.inputs[1])
 b=ns.new('ShaderNodeBump');b.inputs['Strength'].default_value=.35;b.inputs['Distance'].default_value=.0013;lk.new(mix.outputs[0],b.inputs['Height']);lk.new(b.outputs[0],p.inputs['Normal'])
 p.inputs['Sheen Weight'].default_value=.2
fabric(rug);fabric(accent)
# Carry the carpet through the bottom of the frame.
o=bpy.data.objects.get('Linen area rug');o.scale.y=1.9;o.location.y=-2.30
for i in range(12):
 for j in range(4):
  o=cube('Woven diamond foreground',(-2.02+i*.36,-2.59-j*.34,.019),(.095,.095,.002),accent,.001);o.rotation_euler.z=math.pi/4
# Subtle plaster surface.
p=cream.node_tree.nodes.get('Principled BSDF');ns=cream.node_tree.nodes;lk=cream.node_tree.links
n=ns.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=190;n.inputs['Detail'].default_value=2
b=ns.new('ShaderNodeBump');b.inputs['Strength'].default_value=.12;b.inputs['Distance'].default_value=.001;lk.new(n.outputs['Fac'],b.inputs['Height']);lk.new(b.outputs[0],p.inputs['Normal'])
# Small original botanical and landscape prints, made from layered geometry.
remove_prefix('Cloud brush stroke','Bird body','Bird head','Bird beak','Bird leg')
def art_shape(name,points,y,material):
 mesh=bpy.data.meshes.new(name);mesh.from_pydata([(x,y,z) for x,z in points],[],[tuple(range(len(points)))]);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.data.materials.append(material);return o
def stroke(name,points,r,material):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=16;cu.bevel_depth=r;cu.bevel_resolution=3;sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
 for p,co in zip(sp.bezier_points,points):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 o=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(o);o.data.materials.append(material);return o
# Bird is an egret with a curved neck and layered wing feathers.
bx,bz=.09,2.28
art_shape('Bird • body silhouette',[(bx-.045,bz-.045),(bx-.025,bz+.02),(bx+.003,bz+.056),(bx+.028,bz+.052),(bx+.04,bz+.005),(bx+.013,bz-.048),(bx-.024,bz-.076)],.862,bird)
stroke('Bird • curved neck',[(bx+.014,.855,bz+.018),(bx+.038,.855,bz+.06),(bx+.031,.855,bz+.104),(bx+.053,.855,bz+.116)],.011,bird)
uv('Bird • head',(bx+.053,.85,bz+.114),(.018,.004,.012),bird)
art_shape('Bird • beak',[(bx+.063,bz+.119),(bx+.10,bz+.11),(bx+.063,bz+.11)],.845,orange)
uv('Bird • eye',(bx+.057,.842,bz+.119),(.0025,.001,.0025),black)
feather=mat('Bird print feather shade',(.5,.49,.41),.9)
for i in range(6):
 stroke('Bird • fine wing feather',[(bx+.012+i*.002,.849,bz+.025),(bx-.017+i*.005,.849,bz-.025),(bx-.04+i*.005,.849,bz-.065)],.0012,feather)
for dx in [-.012,.009]:
 stroke('Bird • slender leg',[(bx+dx,.85,bz-.058),(bx+dx+.003,.85,bz-.108),(bx+dx-.006,.85,bz-.132)],.0018,feather)
 stroke('Bird • foot',[(bx+dx-.015,.85,bz-.133),(bx+dx-.006,.85,bz-.132),(bx+dx+.006,.85,bz-.133)],.001,feather)
# Layered blue alpine print.
for j,(zc,color) in enumerate([(2.59,(.52,.63,.66)),(2.54,(.35,.50,.58)),(2.48,(.19,.36,.46))]):
 m=mat('Landscape ink '+str(j),color,1);points=[(-.918,2.401)]
 for k in range(15):points.append((-.918+k*.236/14,zc+random.uniform(-.035,.045)))
 points.append((-.682,2.401));art_shape('Landscape • mountain ridge',points,.864-j*.002,m)
for k in range(22):
 x=random.uniform(-.909,-.704);z=random.uniform(2.43,2.61)
 art_shape('Landscape • pale brush stroke',[(x,z),(x+.015,z+.003),(x+.024,z+.006),(x+.012,z+.008)],.854,white)

for o in bpy.data.objects:
 if o.name.startswith(('Turned black lamp','Opal dome')):o.location.x+=.24
 if o.name.startswith(('Frame backing','Silver picture','Landscape','Bird','Print')):o.location.z+=.20
 if o.name.startswith(('Bookcase','Lower cabinet','Cabinet foot','Book cover','Book spine','Book page','Printed book','Spine typography','Storage box','Storage box number','Amber glass','Bottle')):
  o.location.z*=1.12;o.scale.z*=1.12
# Soft window illumination, kept separate from the objects for editing.
world=bpy.context.scene.world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.78,.82,.9,1);world.node_tree.nodes['Background'].inputs[1].default_value=.28
def area(n,loc,power,size,target,color):
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=n;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=color;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
area('Window • soft daylight',(-3.8,-3.6,4.8),650,3.4,(-.3,0,1),(1,.93,.83))
area('Room • reflected fill',(3,-2,3),75,4,(0,0,1),(1,.97,.92))
bpy.ops.object.camera_add(location=(3.77,-8.5,4.25));cam=bpy.context.object;cam.name='Camera • reference composition';cam.rotation_euler=(Vector((-.07,.05,1.43))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=4.55;bpy.context.scene.camera=cam
# Organize the outliner into editable scene components.
collections={n:bpy.data.collections.new(n) for n in ['01 Architecture','02 Walnut desk','03 Bookcase','04 Desktop objects','05 Framed prints','06 Lighting & camera']}
for c in collections.values():bpy.context.scene.collection.children.link(c)
for o in list(bpy.data.objects):
 n=o.name
 if o.type in {'CAMERA','LIGHT'}:key='06 Lighting & camera'
 elif any(k in n for k in ['Plaster','skirting','Oak plank','Linen','Woven']):key='01 Architecture'
 elif any(k in n for k in ['Frame','picture','print','Bird','Cloud','Landscape']):key='05 Framed prints'
 elif o.location.x<-1.5:key='03 Bookcase'
 elif any(k in n for k in ['desktop','leg','foot','Telescoping','crossbar','drawer','Drawer','Leg joinery','Lifting','Metal upper','Underside','Desk height','Controller','sled']) and o.location.z<1.5:key='02 Walnut desk'
 else:key='04 Desktop objects'
 for c in list(o.users_collection):c.objects.unlink(o)
 collections[key].objects.link(o)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=24 if PREVIEW else 64;s.cycles.use_denoising=False;s.cycles.max_bounces=8
s.render.resolution_x=480 if PREVIEW else 960;s.render.resolution_y=640 if PREVIEW else 1280;s.render.resolution_percentage=100
s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=.25
s.render.image_settings.file_format='PNG';s.render.filepath=str(OUT/('preview.png' if PREVIEW else 'study_render.png'));s.render.film_transparent=False
s['About']='Warm walnut study, reconstructed from reference; fully editable procedural materials.'
s['Version']='2.0';s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
# Save with a useful camera view for interactive opening.
for screen_data in bpy.data.screens:
 for a in screen_data.areas:
  if a.type=='VIEW_3D':a.spaces.active.region_3d.view_perspective='CAMERA'
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'warm_study.blend'))
bpy.ops.render.render(write_still=True)
