# JARVIS component-reference reconstruction

Component-reference edition of the JARVIS model, based on the prototype photographs.

Open JARVIS-viewer.html in a modern browser. The HTML embeds its model, textures, lighting environment, and viewer libraries and works offline. JARVIS.glb is the textured portable 3D model, in metres. Reset view, Electronics close-up, Servo close-up, orbit, zoom, wireframe, and surface texture controls are included.

## What changed

- SG90-style blue servo housings with mounting ears, seams, round gear towers, splines, screws, labels, and internal motor geometry.
- Standard half-size breadboard with 400 individual recessed sockets, metal contacts, central channel, separate power rails, rail markings, and interlocking tabs.
- Classic Arduino Nano footprint and component locations read from Arduino's EAGLE CAD, including 2.54 mm headers, solder pads, ATmega package, Mini-B connector, reset button, LEDs, crystal, and ICSP header.
- DuPont-style jumper connector housings and strain relief at cable ends.
- Curved hook-and-loop straps with fabric material, replacing the prior generic front blocks.
- The camera PCB retains a texture rectified from the supplied photographs.

## Sources and precision

- [TowerPro SG90 specifications](https://towerpro.com.tw/product/sg90-7/): nominal servo envelope 23 × 12.2 × 29 mm. Used as a matching component reference; the photographs do not establish the manufacturer or exact clone revision.
- [Arduino Nano](https://docs.arduino.cc/hardware/nano) and its official CAD download: board outline and top component positions from Nano V3.3 EAGLE files. The CAD outline is 43.18 × 17.78 mm; the product nominal length includes the connector. Individual connector and component bodies are simplified visual geometry.
- [Adafruit half-size breadboard, product 64](https://www.adafruit.com/product/64): 82.6 × 55 × 9.3 mm and 400 contacts. Reference CAD: [Adafruit CAD Parts](https://github.com/adafruit/Adafruit_CAD_Parts/tree/main/64%20Halfsize%20Breadboard).
- [Adafruit jumper wire reference](https://www.adafruit.com/product/826): standard 2.54 mm breadboard jumper format.

The assembled base, camera mount, component placement, strap shape, and cable routes are estimated from the user's photos. This is a component-based visual reconstruction, not a metrically verified full-object scan or fabrication model. Scan experiments recovered only separated partial groups, so they are not presented as reliable assembled geometry.

## Rebuild

Install numpy, scipy, Pillow, and trimesh in a Python environment, then run:

```sh
python build_model.py
python texture_model.py
python package_preview.py
```

The first step creates the geometric GLB and untextured OBJ/MTL; the second replaces the GLB with the textured edition; the third embeds it in the offline viewer. Use GLB for the full surface appearance. The ZIP includes these files and the source assets.

## Attribution

The Arduino Nano CAD is by Arduino, licensed CC BY-SA 4.0; the original license accompanies the board source in references/arduino-nano. The Nano geometry and silkscreen adaptation are shared under that license. Three.js uses the included MIT license. The environment is Poly Haven's Venice Sunset HDR, distributed under CC0, obtained from the Three.js example assets. Camera, plate, and fabric textures derive from the user's supplied photographs. Component brand text identifies the reference design, not a verified manufacturer of the physical prototype.
