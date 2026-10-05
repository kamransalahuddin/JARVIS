from pathlib import Path
import sys,math,json,struct
import numpy as np
from PIL import Image
import trimesh
from trimesh.visual.material import PBRMaterial
from trimesh.visual.texture import TextureVisuals
p=Path(__file__).resolve().parent
scene=trimesh.load_scene(p/'JARVIS.glb',process=False)
textures={f.name:Image.open(f).convert('RGB') for f in (p/'textures').iterdir() if f.suffix in ['.jpg','.png']}
a=-math.radians(46);R=np.array([[1,0,0],[0,math.cos(a),-math.sin(a)],[0,math.sin(a),math.cos(a)]]);C=np.array([0,64,12])
remove=[]
sideparts=[]
for name,mesh in scene.geometry.items():
 if name in ['Arduino Nano PCB','Camera PCB']:
  axis=R[:,2] if name=='Camera PCB' else np.array([0,1,0])
  top=mesh.face_normals@axis>.98
  side=mesh.submesh([~top],append=True)
  side.visual=TextureVisuals(material=PBRMaterial(name=name+' edges',baseColorFactor=[185,180,151,255] if name=='Breadboard' else [5,7,8,255],roughnessFactor=.72,metallicFactor=0))
  sideparts.append((name+' edges',side))
  mesh.update_faces(top)
 v=mesh.vertices*1000; old=mesh.visual.material;oldname=old.name
 factor=old.baseColorFactor if old.baseColorFactor is not None else [255]*4
 mat=PBRMaterial(name=name,baseColorFactor=factor,roughnessFactor=.55,metallicFactor=0)
 uv=np.column_stack([v[:,0]/20,v[:,2]/20]);norm='plastic-normal.png'
 if name=='Camera PCB':
  local=(v-C)@R;uv=np.column_stack([(local[:,0]+16)/32,(local[:,1]+16)/32]);mat.baseColorTexture=textures['camera-board.jpg'];mat.baseColorFactor=[255]*4;mat.roughnessFactor=.5
 elif name=='Arduino Nano PCB':
  uv=np.column_stack([(v[:,0]-1.27+8.89)/17.78,(v[:,2]+113.83)/43.18]);mat.baseColorTexture=textures['nano-silkscreen.png'];mat.baseColorFactor=[255]*4
 elif name.endswith('SG90 label'):
  if name.startswith('Pan'):
   local=(v-np.array([-5.5,37,-6]))@np.diag([1.,-1.,-1.])
  else:
   local=(v-np.array([13,45,4]))@np.array([[0,-1,0],[1,0,0],[0,0,1.]])
  uv=np.column_stack([(local[:,0]+8.5)/17,(local[:,1]-7)/10])
  mat.baseColorTexture=textures['sg90-label.png'];mat.baseColorFactor=[255]*4;norm=None;mat.roughnessFactor=.6
 elif name=='Mounting plate':
  mat.baseColorTexture=textures['plate.jpg'];mat.baseColorFactor=[165,165,165,255];mat.roughnessFactor=.74
 elif name=='Velcro hook-and-loop straps':
  uv=np.column_stack([v[:,0]/8,v[:,2]/8]);mat.baseColorTexture=textures['fabric.jpg'];mat.baseColorFactor=[155,155,155,255];norm='fabric-normal.png';mat.roughnessFactor=1
 elif name=='Strap stitching':
  remove.append(name);continue
 elif oldname in ['chassis','edge','black']:
  mat.roughnessFactor=.64;mat.baseColorFactor=[22,24,27,255]
 elif oldname in ['blue','blue_edge']:
  mat.baseColorFactor=[32,68,148,255];mat.roughnessFactor=.22
 elif oldname=='silver':
  mat.roughnessFactor=.26;mat.metallicFactor=.92;norm='metal-normal.png'
 elif oldname=='gold':
  mat.roughnessFactor=.36;mat.metallicFactor=.72;norm='metal-normal.png'
 elif oldname=='glass':
  mat.baseColorFactor=[25,29,34,255];mat.roughnessFactor=.075;mat.metallicFactor=.35;norm=None
 else:
  mat.roughnessFactor=.44;norm=None
 if norm:mat.normalTexture=textures[norm]
 if mat.baseColorTexture is None:
  c=np.array(mat.baseColorFactor,dtype=float)/255
  c[:3]=np.where(c[:3]<=.04045,c[:3]/12.92,((c[:3]+.055)/1.055)**2.4)
  mat.baseColorFactor=np.round(c*255).astype(np.uint8)
 mesh.visual=TextureVisuals(uv=uv,material=mat)
for name in remove:scene.delete_geometry(name)
for name,m in sideparts:scene.add_geometry(m,geom_name=name,node_name=name)
raw=scene.export(file_type='glb')
# Add glTF transmission for the blue servo shells and refractive lens.
jlen=struct.unpack_from('<I',raw,12)[0];j=json.loads(raw[20:20+jlen]);binary=raw[20+jlen+8:]
for m in j['materials']:
 if 'SG90 casing' in m['name'] and 'screws' not in m['name']:
  m['extensions']={'KHR_materials_transmission':{'transmissionFactor':.16},'KHR_materials_ior':{'ior':1.46}}
 if 'normalTexture' in m:m['normalTexture']['scale']=.23 if 'strap' in m['name'].lower() else .10
j['extensionsUsed']=list(set(j.get('extensionsUsed',[])+['KHR_materials_transmission','KHR_materials_ior']))
enc=json.dumps(j,separators=(',',':')).encode();enc+=b' '*((-len(enc))%4)
(p/'JARVIS.glb').write_bytes(struct.pack('<III',0x46546c67,2,28+len(enc)+len(binary))+struct.pack('<II',len(enc),0x4e4f534a)+enc+struct.pack('<II',len(binary),0x004e4942)+binary)
print('Textured',len(scene.geometry),'meshes; embedded',len(j.get('images',[])),'maps.')
