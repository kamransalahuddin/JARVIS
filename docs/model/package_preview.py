from pathlib import Path
import json,base64
p=Path(__file__).resolve().parent
vendor=p/'vendor'
def data_js(text):return 'data:text/javascript;base64,'+base64.b64encode(text.encode()).decode()
imports={'three':data_js((vendor/'three.module.js').read_text()),'orbit':data_js((vendor/'OrbitControls.js').read_text()),'bufferutils':data_js((vendor/'BufferGeometryUtils.js').read_text()),'gltf':data_js((vendor/'GLTFLoader.js').read_text().replace('./BufferGeometryUtils.js','bufferutils'))}
imports['rgbe']=data_js((vendor/'RGBELoader.js').read_text())
s=(p/'preview.html').read_text()
a=s.index('<script type="importmap">');b=s.index('</script>',a)
s=s[:a]+'<script type="importmap">'+json.dumps({'imports':imports},separators=(',',':'))+s[b:]
s=s.replace("'./vendor/OrbitControls.js'","'orbit'").replace("'./vendor/GLTFLoader.js'","'gltf'").replace("'./vendor/RGBELoader.js'","'rgbe'")
s=s.replace("'studio.hdr'",json.dumps('data:application/octet-stream;base64,'+base64.b64encode((p/'studio.hdr').read_bytes()).decode()))
encoded='data:model/gltf-binary;base64,'+base64.b64encode((p/'JARVIS.glb').read_bytes()).decode()
s=s.replace("params.get('model')||'JARVIS.glb'",json.dumps(encoded))
(p/'JARVIS-viewer.html').write_text(s)
print('Wrote offline scan viewer')
