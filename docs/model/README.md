# JARVIS — photo-referenced 3D model

Created by visually reviewing all 34 images in `drive-download-20261004T222625Z-1-001.zip`.

## Open the model

- **JARVIS-viewer.html**: double-click to open the self-contained, offline 3D viewer. Drag to orbit, scroll to zoom, click a part to identify it. Includes top and side views, wiring visibility and wireframe controls.
- **JARVIS.glb**: colored, named component meshes for import into a 3D application. Standard glTF 2.0 binary; metres; Y up.
- **JARVIS.obj + JARVIS.mtl**: alternate mesh format. Keep these files together. Millimetres; Y up.
- **build_model.py**: editable procedural geometry source. Requires Python 3 and NumPy.

## What is represented

Black mounting plate, two rectangular strapped modules, fabric straps and buckles, blue pan and tilt servos, triangular brackets and silver servo arms, tilted camera PCB and cylindrical lens, breadboard with socket pattern and power rails, Nano-shaped controller with USB connector, jumper wires, three-core servo cables, screws, and shortened external leads. There are 57 named component/material meshes and 30,256 triangles.

## Fidelity and scale

This is a manually constructed visual approximation using the photos as reference, not a photogrammetry scan or dimensionally verified CAD design. The mounting plate is provisionally 105 × 245 × 5 mm; the breadboard is provisionally 55 × 83 mm. These dimensions are modeling assumptions. Camera pose varies in the references; the model uses one fixed tilted pose. Wire routes, concealed surfaces, labels, and small electronic details are simplified. The blue servo material approximates the visible color without recreating the internal mechanism or translucent shell. The straps and modules beneath them are approximate.

The model is intended for visualization and further editing. Manufacturing would require physical measurements, tolerances, and dedicated solid geometry. Wire routes do not specify electrical connections.

## Reference photos

All 34 supplied photographs were reviewed to construct the model. Three representative photographs are published in [the repository gallery](https://github.com/kamransalahuddin/JARVIS#the-hardware): the complete device (IMG_4336), camera and servo assembly (IMG_4352), and controller wiring (IMG_4354). The overview is cropped for presentation; the selected photos are resized for GitHub. The full source archive and contact sheets are not included in this public package.

## Rebuild

Run `python3 build_model.py` to regenerate GLB, OBJ, MTL and model-data.json. Then run `python3 assemble_viewer.py` to refresh the self-contained viewer. The bundled Three.js r160 library powers the viewer and is distributed under its MIT license (THREE-LICENSE.txt).
