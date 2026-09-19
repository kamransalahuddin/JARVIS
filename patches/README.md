# OpenSeeFace compatibility patch

`openseeface-opencv-shape.patch` reproduces the author's pre-existing local change to `tracker.py`: flatten OpenCV rotation and translation vectors to three elements instead of transposing them. Setup applies it to OpenSeeFace revision `85aa70fc67582d046e771ea73625182a0d8f7475` in the ignored `external/` directory, and recognizes an already-applied patch on subsequent runs.

The original checkout in `~/OpenSeeFace` is not modified. Its unrelated standalone landmark-dot size change is not needed by JARVIS and is not included. OpenSeeFace retains its upstream license and model licenses in the downloaded checkout.
