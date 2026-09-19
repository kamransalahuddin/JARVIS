# Vision, voice, and device integration

This directory contains JARVIS's MediaPipe gestures, OpenSeeFace tracking integration, YOLO experiments, voice assistant, scene monitoring, and Kasa control.

Use the repository-level [setup guide](../../docs/SETUP.md) and [architecture map](../../docs/ARCHITECTURE.md). Run `scripts/start.py --vision-only` from the root for the camera demo, or `scripts/start.py` for the full assistant. There is no `demo.py`; the camera demo is `demo_main.py`.

`gesture_recognizer.task` is downloaded here by setup and ignored by Git. The local `requirements.txt` is retained as the original minimal MediaPipe reference; it does not install all JARVIS dependencies.

The gesture component preserves its original author credit to Joey Musante and its [Apache 2.0 license](LICENSE.txt). Integration and portability changes are described in the root documentation.
