from pathlib import Path
p=Path(__file__).resolve().parent
s=(p/'viewer-template.html').read_text().replace('__THREE__',(p/'vendor/three.min.js').read_text()).replace('__MODEL__',(p/'model-data.json').read_text())
(p/'JARVIS-viewer.html').write_text(s)
