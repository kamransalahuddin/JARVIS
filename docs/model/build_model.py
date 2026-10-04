"""Photo-referenced JARVIS visual replica. Model authoring units: millimetres.
Only Python stdlib + numpy required. GLB exports in metres; OBJ exports in mm.
"""
from pathlib import Path
import json, math, struct, collections
import numpy as np
P=Path(__file__).resolve().parent
materials={
 'chassis':('#171b21',.84,.05),'strap':('#111216',.99,0),'edge':('#292c31',.88,0),
 'blue':('#153b9c',.27,.12),'blue_edge':('#2459c4',.3,.1),'pcb':('#20262b',.7,.05),
 'nano':('#174c65',.65,.08),'cream':('#e9e6d6',.8,0),'hole':('#454743',.95,0),
 'silver':('#b9bdc4',.28,.85),'gold':('#b9a06c',.35,.7),'glass':('#152e40',.12,.5),
 'red':('#b9302c',.6,0),'yellow':('#e2b939',.6,0),'green':('#2f8163',.6,0),
 'purple':('#806aab',.6,0),'orange':('#d88035',.6,0),'brown':('#644635',.7,0),
 'white':('#dfddd1',.65,0),'black':('#222426',.75,0),'led':('#78b777',.3,.1)}
parts=collections.OrderedDict()
def add(name,mat,v,f):
 key=(name,mat)
 if key not in parts:parts[key]=[[],[]]
 vv,ff=parts[key]; off=len(vv);vv.extend(np.asarray(v).tolist());ff.extend((np.asarray(f)+off).tolist())
def box(name,mat,c,s,R=None):
 v=np.array([[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]])*np.array(s)/2
 if R is not None:v=v@R.T
 v+=c
 f=[[0,2,1],[0,3,2],[4,5,6],[4,6,7],[0,1,5],[0,5,4],[3,7,6],[3,6,2],[0,4,7],[0,7,3],[1,2,6],[1,6,5]]
 add(name,mat,v,f)
def tube(name,mat,points,r,segments=10):
 pts=np.array(points,float);v=[]
 for i,p in enumerate(pts):
  tangent=pts[min(i+1,len(pts)-1)]-pts[max(i-1,0)];tangent/=np.linalg.norm(tangent)
  ref=np.array([0.,1,0]) if abs(tangent[1])<.92 else np.array([1.,0,0])
  a=np.cross(tangent,ref);a/=np.linalg.norm(a);b=np.cross(tangent,a)
  for j in range(segments):v.append(p+r*(a*math.cos(j*2*math.pi/segments)+b*math.sin(j*2*math.pi/segments)))
 f=[]
 for i in range(len(pts)-1):
  for j in range(segments):
   a=i*segments+j;b=i*segments+(j+1)%segments;c=b+segments;d=a+segments
   f.extend([[a,b,c],[a,c,d]])
 v.extend([pts[0],pts[-1]])
 for j in range(segments):f.extend([[len(v)-2,(j+1)%segments,j],[len(v)-1,(len(pts)-1)*segments+j,(len(pts)-1)*segments+(j+1)%segments]])
 add(name,mat,v,f)
def cyl(name,mat,c,r,h,axis=(0,1,0),n=32):
 a=np.array(axis,float);a/=np.linalg.norm(a);c=np.array(c);tube(name,mat,[c-a*h/2,c+a*h/2],r,n)
def wire(name,mat,control,r=.7):
 # Catmull-Rom route through observed endpoints and bends.
 p=np.array(control,float);q=np.vstack([p[0],p,p[-1]]);out=[]
 for i in range(1,len(q)-2):
  a,b,c,d=q[i-1:i+3]
  for t in np.linspace(0,1,12,endpoint=False):out.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t))
 out.append(p[-1]);tube(name,mat,out,r)
def screw(c,axis=(0,1,0),r=2.4):
 cyl('Fasteners','silver',c,r,1.25,axis,16)
 c=np.array(c)+np.array(axis)*.68
 if axis==(0,1,0):box('Fasteners','hole',c,(r*1.3,.12,.5));box('Fasteners','hole',c,(.5,.12,r*1.3))
def beam(name,mat,a,b,width,depth):
 a=np.array(a);b=np.array(b);y=b-a;L=np.linalg.norm(y);y=y/L;x=np.array([1.,0,0]);z=np.cross(x,y);R=np.column_stack([x,y,z]);box(name,mat,(a+b)/2,(depth,L,width),R)
# Base and two strapped rectangular modules.
box('Mounting plate','chassis',(0,0,0),(105,5,245))
for z in [51,96]:
 box('Strapped modules','chassis',(0,9,z),(77,13,29))
 box('Strapped modules','edge',(0,16,z),(71,1,25))
 # Strap sweeps across the width and around both sides; 19 mm ribbon.
 pts=[(-53,-3),(-54,4),(-46,12),(-38,21),(-25,25),(0,27),(25,25),(38,21),(48,12),(54,3),(52,-4)]
 v=[]
 for x,y in pts:v.extend([[x,y,z-10],[x,y,z+10],[x,y+1.5,z-10],[x,y+1.5,z+10]])
 f=[]
 for i in range(len(pts)-1):
  a=i*4;b=a+4
  f.extend([[a,b,b+1],[a,b+1,a+1],[a+2,a+3,b+3],[a+2,b+3,b+2],[a,a+2,b+2],[a,b+2,b],[a+1,b+1,b+3],[a+1,b+3,a+3]])
 f.extend([[0,1,3],[0,3,2],[40,42,43],[40,43,41]])
 add('Woven fastening straps','strap',v,f)
 # Fine crosswise stitches give the woven fabric a physical texture.
 for zz in np.arange(z-9,z+9,1.3):tube('Strap stitching','edge',[[x,y+1.65,zz] for x,y in pts[2:9]],.12,4)
 box('Strap buckles','black',(-42,10,z),(9,5,24))
# Breadboard at rear. 30 terminal rows and red/blue power rails.
box('Breadboard','cream',(0,6.7,-76),(55,8.4,83))
box('Breadboard center channel','hole',(0,11,-76),(2,0.12,77))
for x in [-25,-19,19,25]:
 box('Breadboard rail lines','red' if x in [-25,19] else 'blue',(x,10.97,-76),(.28,.07,76))
for row in range(30):
 z=-113+row*2.54
 for x in [-23,-21,21,23]+[-15.25+i*2.54 for i in range(5)]+[5.09+i*2.54 for i in range(5)]:
  box('Breadboard sockets','hole',(x,11.02,z),(.85,.09,.85))
# Arduino Nano-shaped controller sits lengthwise on breadboard.
box('Controller board','nano',(0,15,-91),(18,1.5,44))
for x in [-8.2,8.2]:
 box('Controller headers','black',(x,12.5,-91),(2.2,3,39))
 for i in range(15):
  cyl('Controller pins','gold',(x,16,-109+i*2.54),.65,1,(0,1,0),8)
box('Controller electronics','black',(0,16.5,-95),(7.4,1.3,7.4))
for side in [-1,1]:
 for i in range(8):box('Controller solder','silver',(side*4.1,16.3,-98+i*.85),(1,.4,.4))
box('Controller USB socket','silver',(0,17,-112),(7.8,4.5,6))
box('Controller USB socket','hole',(0,17,-115.1),(5,2.4,.15))
box('Controller electronics','silver',(0,16.3,-84),(3,1.2,4.5))
box('Controller electronics','cream',(0,17,-78),(3,1.5,3))
for i in range(7):
 box('Controller electronics','black',(-4+(i%2)*8,16.2,-105+i*4.5),(1.4,1,2))
box('Controller electronics','led',(4,17,-73),(1.2,.8,1.7))
# Base servo and pan-tilt bracket.
box('Pan mount','chassis',(0,5,-6),(44,5,44))
for x in [-17,17]:
 for z in [-22,10]:screw((x,8,z))
cyl('Pan servo','blue_edge',(0,11,-5),7,6)
box('Pan servo','blue',(0,22,-6),(23,23,12))
box('Pan servo','blue_edge',(0,12,-6),(32,2,12))
box('Pan servo label','gold',(0,23,0.1),(17,7,.2))
box('Pan servo label','black',(0,23,0.3),(15,5,.1))
# Two triangular side frames assembled around a genuine triangular opening.
for x in [-16,16]:
 a=(x,15,-23);b=(x,15,16);c=(x,52,8)
 beam('Tilt bracket','chassis',a,b,6,3)
 beam('Tilt bracket','chassis',b,c,6,3)
 beam('Tilt bracket','chassis',c,a,6,3)
 cyl('Tilt bracket','chassis',(x,51,8),6,3,(1,0,0))
 screw((x+(-2 if x<0 else 2),51,8),(1,0,0),2.8)
 # Visible silver servo arm.
 box('Servo arms','silver',(x+(-2 if x<0 else 2),43,8),(1,17,4))
 for yy in [37,40,43,46]:cyl('Servo arm holes','hole',(x+(-2.55 if x<0 else 2.55),yy,8),.55,.2,(1,0,0),8)
box('Tilt servo','blue',(0,47,5),(26,13,23))
box('Tilt servo','blue_edge',(0,52,5),(32,3,23))
# Camera board faces the straps, tilted upward 45 degrees.
a=-math.radians(46);R=np.array([[1,0,0],[0,math.cos(a),-math.sin(a)],[0,math.sin(a),math.cos(a)]]);C=np.array([0,64,12]);axis=R[:,2]
def campt(v):return C+R@np.array(v)
box('Camera mounting cradle','chassis',campt((0,0,-5)),(27,25,8),R)
box('Camera PCB','pcb',C,(32,32,1.5),R)
box('Camera sensor housing','black',campt((0,0,3)),(17,17,5),R)
for x in [-13,13]:
 for y in [-13,13]:
  cyl('Camera mounting rings','gold',campt((x,y,.9)),2,0.3,axis,24)
  cyl('Camera mounting holes','hole',campt((x,y,1.1)),1.2,.2,axis,20)
for c,r,h in [(8,7.4,9),(15,6.7,5),(19,7.8,4),(22,8.3,3)]:cyl('Camera lens','black',campt((0,0,c)),r,h,axis,48)
for t in range(32):
 ang=t*2*math.pi/32
 tube('Lens focus ribs','edge',[campt((7.4*math.cos(ang),7.4*math.sin(ang),5)),campt((7.4*math.cos(ang),7.4*math.sin(ang),12))],.23,5)
for depth in [14,15,16,17]:cyl('Lens focus rings','edge',campt((0,0,depth)),6.9,.35,axis,48)
cyl('Optical glass','glass',campt((0,0,23.6)),6.9,.3,axis,48)
cyl('Lens aperture','black',campt((0,0,23.8)),3.2,.08,axis,40)
for i in range(7):box('Camera PCB components','cream',campt((-11+i*3.4,-11,1.2)),(1.3,2,.5),R)
# Jumper wires. Individual routes approximate the visible bundle; these are not a wiring diagram.
routes=[
 ('red',[(-7,13,-60),(-24,48,-50),(-30,63,-72),(-7,36,-94),(-6,19,-100)]),
 ('yellow',[(4,17,-99),(4,68,-86),(-27,69,-58),(-32,20,-31),(-6,33,-5)]),
 ('green',[(-12,13,-56),(-39,20,-39),(-47,7,-4),(-39,7,26),(0,10,20)]),
 ('purple',[(-15,13,-62),(-34,11,-59),(-40,5,-18),(-19,7,14),(0,11,-2)]),
 ('black',[(8,19,-101),(24,68,-112),(43,45,-81),(18,21,-74)]),
 ('white',[(6,13,-59),(30,36,-59),(43,29,-91),(9,18,-106)]),
 ('brown',[(-6,18,-105),(-36,40,-91),(-39,53,-46),(-8,34,-9)]),
 ('yellow',[(-13,14,-66),(-25,41,-47),(-12,61,-39),(8,17,-94)]),
 ('black',[(12,14,-65),(29,61,-57),(11,73,-43),(-12,38,-20)]),
 ('red',[(1,57,3),(-18,56,-3),(-27,23,-15),(-18,18,-69)]),
 ('green',[(3,57,3),(-14,60,-10),(-22,30,-28),(7,18,-86)]),
 ('white',[(5,57,3),(-10,59,-12),(-19,29,-31),(9,18,-84)])]
for i,(mat,pts) in enumerate(routes):
 wire('Jumper wiring',mat,pts,.65)
 p=pts[0];box('Jumper connectors','black',(p[0],p[1]+2,p[2]),(2.1,6,2.1))
# Orange / red / brown three-core servo bundles.
for k,mat in enumerate(['orange','red','brown']):
 wire('Servo cable bundle',mat,[(12,45,10),(28+k*1.5,30,15),(36+k*1.5,13,-6),(40+k*1.5,7,28),(26+k*1.5,9,45),(23+k*1.5,14,-40),(12+k*1.5,20,-73)],.7)
# Main power and USB leads, shortened to keep the hardware easy to inspect.
box('USB cable','white',(0,17,-121),(8,5,13))
wire('USB cable','white',[(0,17,-126),(1,16,-137),(18,5,-145),(42,-11,-140),(57,-20,-117)],1.9)
box('Power cable','black',(25,12,99),(7,6,20))
wire('Power cable','black',[(25,12,106),(37,12,122),(48,2,138),(49,-17,140),(43,-31,131)],2)
wire('Power cable','black',[(-13,11,0),(-22,6,4),(-38,0,0),(-56,-20,4),(-51,-32,29)],1.8)
# Export each named assembly/material as an independently editable mesh.
meshes=[]
for (name,mat),(v,f) in parts.items():
 v=np.array(v,np.float32);f=np.array(f,np.uint32)
 tri=v[f];norm=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-10)
 # Per-face normals preserve hard mechanical edges and make exports deterministic.
 flat=tri.reshape(-1,3);norm=np.repeat(norm,3,axis=0)
 meshes.append(dict(name=name,material=mat,positions=flat.reshape(-1).round(5).tolist(),normals=norm.reshape(-1).round(5).tolist()))
(P/'model-data.json').write_text(json.dumps({'materials':materials,'meshes':meshes},separators=(',',':')))
# glTF binary, metre units, Y up.
gltf={'asset':{'version':'2.0','generator':'JARVIS photo-reference model builder','extras':{'reference_images':34,'scale':'Estimated from photos; not measured'}},'scene':0,'scenes':[{'nodes':[]}],'nodes':[],'meshes':[],'materials':[],'buffers':[{'byteLength':0}],'bufferViews':[],'accessors':[]}
matids={}
for name,(col,rough,metal) in materials.items():
 matids[name]=len(gltf['materials']);rgb=[int(col[i:i+2],16)/255 for i in (1,3,5)]
 gltf['materials'].append({'name':name,'pbrMetallicRoughness':{'baseColorFactor':rgb+[1],'metallicFactor':metal,'roughnessFactor':rough},'doubleSided':True})
binary=bytearray()
def accessor(vals,position=False):
 arr=np.array(vals,dtype='<f4').reshape(-1,3)
 if position:arr/=1000
 start=len(binary);binary.extend(arr.tobytes());vi=len(gltf['bufferViews']);gltf['bufferViews'].append({'buffer':0,'byteOffset':start,'byteLength':arr.nbytes,'target':34962})
 ac={'bufferView':vi,'componentType':5126,'count':len(arr),'type':'VEC3'}
 if position:ac.update(min=arr.min(axis=0).tolist(),max=arr.max(axis=0).tolist())
 ai=len(gltf['accessors']);gltf['accessors'].append(ac);return ai
for m in meshes:
 pi=accessor(m['positions'],True);ni=accessor(m['normals']);idx=len(gltf['meshes'])
 gltf['meshes'].append({'name':m['name'],'primitives':[{'attributes':{'POSITION':pi,'NORMAL':ni},'material':matids[m['material']]}]})
 gltf['nodes'].append({'name':m['name']+' / '+m['material'],'mesh':idx});gltf['scenes'][0]['nodes'].append(idx)
gltf['buffers'][0]['byteLength']=len(binary)
j=json.dumps(gltf,separators=(',',':')).encode();j+=b' '*((-len(j))%4);binary+=b'\0'*((-len(binary))%4)
(P/'JARVIS.glb').write_bytes(struct.pack('<III',0x46546c67,2,12+8+len(j)+8+len(binary))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(binary),0x004e4942)+binary)
with (P/'JARVIS.obj').open('w') as o:
 o.write('# JARVIS visual replica. Millimetres, Y up; scale is approximate.\nmtllib JARVIS.mtl\n');offset=1
 for (name,mat),(v,f) in parts.items():
  o.write('o '+name.replace(' ','_')+'_'+mat+'\nusemtl '+mat+'\n')
  for p in v:o.write('v %.5f %.5f %.5f\n'%tuple(p))
  for face in f:o.write('f '+' '.join(str(x+offset) for x in face)+'\n')
  offset+=len(v)
with (P/'JARVIS.mtl').open('w') as o:
 for name,(col,rough,metal) in materials.items():
  rgb=[int(col[i:i+2],16)/255 for i in (1,3,5)];o.write('newmtl '+name+'\nKd '+' '.join(map(str,rgb))+'\nKs .25 .25 .25\nNs '+str((1-rough)*150)+'\n\n')
print(f'Created {len(meshes)} component/material meshes; {sum(len(m["positions"])//9 for m in meshes):,} triangles.')
