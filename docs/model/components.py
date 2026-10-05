# Replace estimated component stand-ins with source-dimensioned hardware.
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
# Retain custom platform, camera, support bracket, and observed cable routes.
for key in list(parts):
 name,mat=key
 if name.startswith(('Breadboard','Controller','Pan servo','Tilt servo','Servo internal','Servo gear','Tilt motor','Woven fastening','Strap stitching','Strap buckles','Strapped modules','Jumper connectors')):
  del parts[key]
# Four separately molded breadboard strips, exactly 400 sockets.
# Adafruit PID64: 82.6 x55 x9.3 mm. Upper housing top =11.8.
top=11.8
box('Breadboard foam backing','white',(0,3,-76),(55,1,82.6))
for x,w in [(-23,9),(23,9),(-9.5,16),(9.5,16)]:
 box('Breadboard molded housing','cream',(x,7,-76),(w,7,82.6))
# Top is a tiled perforated skin. Each socket has a sloped rim and a recessed well.
def socket_tile(x,z,w=2.54,d=2.54):
 outside=[[-w/2,-d/2],[w/2,-d/2],[w/2,d/2],[-w/2,d/2]]
 rim=[[-.72,-.72],[.72,-.72],[.72,.72],[-.72,.72]]
 hole=[[-.46,-.46],[.46,-.46],[.46,.46],[-.46,.46]]
 v=[[x+a,top,z+b] for a,b in outside]+[[x+a,top,z+b] for a,b in rim]+[[x+a,top-.45,z+b] for a,b in hole]+[[x+a,top-1.5,z+b] for a,b in hole]
 f=[]
 for ring in range(3):
  for i in range(4):
   j=(i+1)%4;a=ring*4+i;b=ring*4+j;c=(ring+1)*4+j;d0=(ring+1)*4+i;f.extend([[a,c,b],[a,d0,c]])
 add('Breadboard socket walls','cream',v,f)
 box('Breadboard recessed contacts','hole',(x,top-1.55,z),(.95,.1,.95))
 # Metallic spring contact deep inside the well, not a flat painted square.
 box('Breadboard spring contacts','silver',(x+.31,top-1.4,z),(.12,.16,.65))
# The opaque lower housing must end below the socket well.
# Replace its geometry with body sections whose roofs are beneath the perforated surface.
for key in list(parts):
 if key[0]=='Breadboard molded housing':del parts[key]
for x,w in [(-23,9),(23,9),(-9.5,16),(9.5,16)]:
 box('Breadboard lower housing','cream',(x,6.65,-76),(w,6.5,82.6))
for side in [-1,1]:
 for col in range(5):
  x=side*(3.81+col*2.54)
  for row in range(30):socket_tile(x,-112.83+row*2.54)
 # Borders and channel lips on each terminal block.
 for x,w in [(side*2.01,1.06),(side*16.16,1.84)]:box('Breadboard top border','cream',(x,11.57,-76),(w,.46,82.6))
 for z in [-115.70,-36.30]:box('Breadboard top border','cream',(side*9.3,11.57,z),(13.65,.46,3.2))
 # Power rails: five groups of five sockets, 25 per rail, 100 total.
 for col in [20.32,22.86]:
  for group in range(5):
   for row in range(5):socket_tile(side*col,-110.29+group*15.24+row*2.54)
 for x,w in [(side*18.7,.7),(side*26.0,3.0)]:box('Breadboard rail borders','cream',(x,11.57,-76),(w,.46,82.6))
 for group in range(4):box('Breadboard rail gaps','cream',(side*21.59,11.57,-97.59+group*15.24),(5.08,.46,2.54))
 for z in [-115.06,-36.94]:box('Breadboard rail borders','cream',(side*21.6,11.57,z),(5.8,.46,4.5))
 # Interlocking pegs in the molding.
 for z in [-103,-77,-51]:box('Breadboard interlocking tabs','cream',(side*27.8,7,z),(1.4,3.4,4))
 for x,mat in [(side*25.5,'red'),(side*18.65,'blue')]:box('Breadboard power markings',mat,(x,11.84,-76),(.28,.04,78))
# Exact board outline and component placement from Arduino Nano V3.3 EAGLE CAD.
root=ET.parse(P/'references/arduino-nano/NanoV3.3.brd')
xoffset=1.27;zstart=-113.83;pcbY=16.0
box('Arduino Nano PCB','nano',(xoffset,pcbY,zstart+43.18/2),(17.78,1.6,43.18))
def nano_point(x,y,height=pcbY+.8):return (xoffset+float(y)-8.89,height,zstart+float(x))
# 2.54mm headers, 15.24mm between rows.
for x in [xoffset-7.62,xoffset+7.62]:
 for row in range(15):
  z=zstart+3.81+row*2.54
  box('Nano pin header insulators','black',(x,13.65,z),(2.45,2.5,2.45))
  box('Nano square pins','silver',(x,13.75,z),(.64,7.5,.64))
  cyl('Nano solder pads','silver',(x,16.87,z),.88,.14,n=16)
# Four mounting holes are represented as dark recesses with tin rings.
for x in [xoffset-7.62,xoffset+7.62]:
 for z in [zstart+1.27,zstart+41.91]:
  cyl('Nano mounting ring','silver',(x,16.86,z),1.15,.12,n=24)
  cyl('Nano mounting hole','hole',(x,16.94,z),.9,.08,n=24)
# CAD-derived top-side footprints plus relief geometry.
packages={}
for lib in root.findall('.//board/libraries/library'):
 for pkg in lib.findall('packages/package'):packages[(lib.get('name'),pkg.get('name'))]=pkg
for e in root.findall('.//board/elements/element'):
 rot=e.get('rot','R0');name=e.get('name');package=e.get('package');px=float(e.get('x'));py=float(e.get('y'))
 if rot.startswith('M') or name.startswith('U$') or name in ['FRAME1','J1','J2']:continue
 angle=math.radians(float(rot.replace('R','')));rr=np.array([[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]])
 pkg=packages[(e.get('library'),package)]
 for pad in pkg.findall('smd'):
  xy=np.array([float(pad.get('x')),float(pad.get('y'))])@rr.T+np.array([px,py]);c=nano_point(*xy,pcbY+.91)
  box('Nano SMD solder pads','silver',c,(float(pad.get('dy')), .16,float(pad.get('dx'))))
 if name=='IC3':
  # QFN32 in CAD, rotated 45 degrees as visible in the user's Nano.
  phi=math.radians(45);rot3=np.array([[math.cos(phi),0,-math.sin(phi)],[0,1,0],[math.sin(phi),0,math.cos(phi)]])
  box('Nano ATmega328P','black',nano_point(px,py,17.45),(5,1.2,5),rot3)
 elif name=='J3':
  # Mini-B connector shell: folded walls, open mouth, tongue, five contacts.
  c=np.array(nano_point(2.75,8.89,18.6))
  box('Nano Mini-B USB shell','silver',c+[0,1.55,0],(7.7,.35,5.6))
  for dx in [-3.68,3.68]:box('Nano Mini-B USB shell','silver',c+[dx,0,0],(.35,3.2,5.6))
  box('Nano Mini-B USB interior','black',c+[0,0,-2.63],(7,2.5,.1))
  box('Nano Mini-B USB tongue','cream',c+[0,-.55,-.7],(5.5,.6,3.3))
  for j in range(5):box('Nano USB contacts','gold',c+[-1.6+j*.8,-.14,-1.4],(.35,.15,2.0))
 elif name=='SW1':
  box('Nano reset switch','silver',nano_point(px,py,17.65),(3.5,1.7,6));box('Nano reset actuator','cream',nano_point(px,py,18.8),(2.2,.8,3.4))
 elif name=='Y1':box('Nano crystal','silver',nano_point(px,py,17.45),(3.0,1.2,4.5))
 elif name in ['RX','TX','PWR','L']:
  box('Nano indicator housings','cream',nano_point(px,py,17.25),(1.3,.8,2));box('Nano indicator lenses','led',nano_point(px,py,17.7),(.85,.2,1.25))
 elif name=='J4':
  for dx in [-1.27,1.27]:
   for dz in [-2.54,0,2.54]:
    c=np.array(nano_point(px,py,17.5))+[dx,0,dz];box('Nano ICSP socket','black',c,(2.45,1.5,2.45));box('Nano ICSP pins','gold',c+[0,2.2,0],(.64,4.6,.64))
# Generate clean, readable silkscreen using documented labels, with no photo wires baked in.
fontfile=next((str(f) for f in [Path('/System/Library/Fonts/Supplemental/Arial.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),Path('C:/Windows/Fonts/arial.ttf')] if f.exists()),'DejaVuSans.ttf')
font=ImageFont.truetype(fontfile,22)
tex=Image.new('RGB',(540,1296),'#164858');draw=ImageDraw.Draw(tex)
left=['D1','D0','RST','GND','D2','D3','D4','D5','D6','D7','D8','D9','D10','D11','D12']
right=['VIN','GND','RST','5V','A7','A6','A5','A4','A3','A2','A1','A0','REF','3V3','D13']
for row in range(15):
 yy=1296-int((3.81+row*2.54)/43.18*1296)
 draw.text((75,yy),left[row],font=font,fill='#e3e3d2',anchor='lm');draw.text((465,yy),right[row],font=font,fill='#e3e3d2',anchor='rm')
draw.text((270,550),'NANO',font=ImageFont.truetype(fontfile,40),fill='#e3e3d2',anchor='mm')
tex.save(P/'textures/nano-silkscreen.png')
# SG90 body reference: 23 x12.2 x29mm; 32.3mm mounting-ear span.
# Local coordinate system: X long side, Y body height, Z depth.
def servo(label,origin,rot):
 before={k:(len(v[0]),len(v[1])) for k,v in parts.items()}
 body=label+' SG90'
 box(body+' casing','blue',(0,11.5,0),(23,22.5,12.2))
 box(body+' top seam','blue_edge',(0,21.7,0),(23.3,.65,12.5))
 box(body+' bottom cap','blue_edge',(0,1,0),(23.3,2,12.5))
 box(body+' mounting ears','blue_edge',(0,18,0),(32.3,2.5,12.2))
 # Rounded gear tower on the top, spline and center screw.
 cyl(body+' gear tower','blue_edge',(-5.5,24.15,0),5.75,3.7,n=48)
 cyl(body+' gear tower','blue_edge',(1.2,23.3,0),3.35,2,n=32)
 cyl(body+' output spline','cream',(-5.5,27.6,0),2.3,3.0,n=24)
 for k in range(20):
  ang=k*math.pi/10;tube(body+' spline teeth','cream',[(-5.5+2.3*math.cos(ang),26.3,2.3*math.sin(ang)),(-5.5+2.3*math.cos(ang),28.8,2.3*math.sin(ang))],.13,4)
 for x in [-14,14]:
  cyl(body+' ear screw recess','hole',(x,19.31,0),1.05,.12,n=20)
 for x in [-9,9]:
  for z in [-4,4]:cyl(body+' casing screws','silver',(x,22.82,z),.75,.22,n=12)
 box(body+' label','gold',(0,12,6.17),(17,10,.10))
 cyl(body+' internal motor','silver',(4,10,0),4,15,n=32)
 # Transform only the meshes of this newly created servo.
 for (name,mat),data in parts.items():
  if name.startswith(body):data[0]=(np.asarray(data[0])@rot.T+origin).tolist()
servo('Pan',np.array([-5.5,37,-6]),np.diag([1.,-1.,-1.]))
# The second servo drives a horizontal axis inside the pan/tilt cradle.
servo('Tilt',np.array([13,45,4]),np.array([[0,-1,0],[1,0,0],[0,0,1.]]))
# Servo label typography, based on the black/gold label visible in the photos.
label=Image.new('RGB',(680,400),'#141516');d=ImageDraw.Draw(label)
d.rectangle((8,8,671,391),outline='#b5a16c',width=8)
for y,txt,sz in [(65,'Tower Pro',60),(172,'Micro Servo',65),(300,'SG90',110)]:d.text((340,y),txt,font=ImageFont.truetype(fontfile,sz),anchor='mm',fill='#b5a16c')
label.save(P/'textures/sg90-label.png')
# Two soft Velcro straps; no invented separate electronic blocks beneath them.
for z in [52,96]:
 pts=[]
 for t in np.linspace(0,1,45):
  x=-53+106*t;y=4+15*math.sin(math.pi*t)**.6
  pts.append((x,y))
 v=[]
 for x,y in pts:v.extend([[x,y,z-11.5],[x,y,z+11.5],[x,y+1.3,z-11.5],[x,y+1.3,z+11.5]])
 f=[]
 for i in range(len(pts)-1):
  a=4*i;b=a+4;f.extend([[a,b,b+1],[a,b+1,a+1],[a+2,a+3,b+3],[a+2,b+3,b+2],[a,a+2,b+2],[a,b+2,b],[a+1,b+1,b+3],[a+1,b+3,a+3]])
 add('Velcro hook-and-loop straps','strap',v,f)
 for x in [-51,51]:box('Velcro underside returns','strap',(x,-1,z),(4,8,23))
 # Small stitched edge loops along each strap.
 for zz in [z-10.5,z+10.5]:
  for i in range(0,len(pts)-2,2):tube('Velcro edge stitching','edge',[[pts[j][0],pts[j][1]+1.5,zz] for j in [i,i+1]],.1,4)
# Breadboard/DuPont connectors at both ends with crimp windows and strain relief.
for mat,points in routes:
 for end in [0,-1]:
  p0=np.array(points[end],float);p1=np.array(points[1 if end==0 else -2],float);direction=p1-p0;direction/=np.linalg.norm(direction)
  # Board-plug ends stand vertically; camera ends follow the observed cable.
  if p0[1]<25:direction=np.array([0.,1,0])
  ref=np.array([1.,0,0]);xx=np.cross(direction,ref)
  if np.linalg.norm(xx)<.1:xx=np.cross(direction,[0.,0,1])
  xx/=np.linalg.norm(xx);zz=np.cross(xx,direction);rr=np.column_stack([xx,direction,zz]);center=p0+direction*3.2
  box('DuPont connector housings','black',center,(2.54,6.4,2.54),rr)
  box('DuPont crimp inspection window','silver',center+zz*1.29,(1.05,2,.06),rr)
  tube('DuPont strain relief',mat,[p0+direction*6.4,p0+direction*8.7],.85,12)
