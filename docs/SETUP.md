# Setup

[Back to JARVIS](../README.md) · [Dependency inventory](DEPENDENCIES.md) · [Hardware](../hardware/README.md)

## Fastest start: camera demo

The demo runs the existing face, hand, and YOLO loop. **No API keys, microphone, Arduino, or smart plugs are required.** You need a webcam, internet access for installation/model downloads, **Python 3.11**, and **Git**.

1. Install [Python 3.11](https://www.python.org/downloads/release/python-31115/) and [Git](https://git-scm.com/downloads). On an Apple Silicon Mac with [Homebrew](https://brew.sh/), use `brew install python@3.11 git`.
2. Clone or download this repository and extract it to a writable folder.
3. On macOS, open **Start.command**; on Windows, open **Start.bat**. The first launch installs the camera dependencies and models. Allow camera access when prompted. Press **Escape** in the camera window to exit.

On macOS, if Finder refuses to open the downloaded launcher, use the terminal instructions below. First-time setup involves sizeable Python/model downloads and can take several minutes; it is not an instant web demo.

Equivalent terminal commands on macOS/Linux:

```bash
git clone https://github.com/kamransalahuddin/JARVIS.git
cd JARVIS
python3.11 scripts/setup.py --vision-only
.venv-jarvis/bin/python scripts/start.py --vision-only
```

On Windows PowerShell:

```powershell
git clone https://github.com/kamransalahuddin/JARVIS.git
cd JARVIS
py -3.11 scripts/setup.py --vision-only
.venv-jarvis\Scripts\python.exe scripts\start.py --vision-only
```

Setup creates `.venv-jarvis`, installs packages, clones a pinned OpenSeeFace checkout, applies the author's two-line OpenCV compatibility fix, downloads vision models, and creates `.env` and starter memory **only when those files do not already exist**. It uses a dedicated `.venv-jarvis` environment, leaving an existing `.venv` untouched. It never resets an existing external checkout. If `.venv-jarvis` belongs to another project or Python version, rename it before setup.

**Platform status:** Apple Silicon macOS is the primary validation target (macOS 15.2, Python 3.11.15). Windows x86-64 and Linux x86-64 have setup paths and a non-MLX speech fallback, but have not been run on those operating systems. Intel macOS and other CPU/OS combinations are not validated; current dependency pins may lack wheels. Do not interpret the launchers as a claim of universal compatibility.

## Full voice assistant

Install host audio tools:

| OS | Host prerequisites |
| --- | --- |
| macOS | `brew install mpv ffmpeg` |
| Debian/Ubuntu | `sudo apt install python3.11-venv git mpv ffmpeg libportaudio2 libgl1 libglib2.0-0` (Python 3.11 availability depends on the distribution) |
| Windows | Install [mpv](https://mpv.io/installation/) and [FFmpeg](https://ffmpeg.org/download.html), and add their executable folders to `PATH` |

SoundDevice's macOS/Windows wheels normally include PortAudio. If the macOS audio library cannot be found, use `brew install portaudio`; Linux needs the system library. See [SoundDevice installation](https://python-sounddevice.readthedocs.io/en/0.5.6/installation.html).

Upgrade the demo environment to the full application:

```bash
python3.11 scripts/setup.py
```

Windows: `py -3.11 scripts/setup.py`.

Edit the newly created `.env`:

| Variable | Setting |
| --- | --- |
| `GEMINI_API_KEY` | Your Google Gen AI API key (or use `GOOGLE_API_KEY`) |
| `ELEVENLABS_API_KEY` | Your ElevenLabs API key |
| `GEMINI_MODEL` | Defaults to `gemini-3.1-flash-lite`; requires access to models and interactions APIs |
| `ELEVENLABS_VOICE_ID` | Defaults to `NNl6r8mD7vthiJatiJt1`; choose an available voice for your account |
| `ELEVENLABS_MODEL` | Defaults to `eleven_flash_v2_5` |
| `CAMERA_INDEX` | Defaults to `0`; choose another index if needed |
| `ARDUINO_PORT` | Leave blank to run without servos; otherwise use your actual serial port |
| `ENABLE_SMART_LIGHTS` | Defaults to `false`; set `true` only after configuring every plug |
| `IP_Address_right`, `IP_Address_left`, `IP_Address_LED1`, `IP_Address_LED2` | LAN addresses for four compatible Kasa `SmartPlug` devices |
| `OPENSEEFACE_PATH` | Optional absolute path to a complete alternative checkout; omit to use `external/OpenSeeFace` |

Use your own account credentials. Model/API availability and account billing are external prerequisites. The launcher checks that keys exist, not whether they are valid. Do not set both Gemini key names to different accounts.

Then launch:

```bash
.venv-jarvis/bin/python scripts/start.py
```

Windows: `.venv-jarvis\Scripts\python.exe scripts\start.py`.

The launcher switches to the repository root, preserving the application's existing relative file paths. Allow microphone access for the terminal/IDE running Python. The default microphone must accept mono audio at 16 kHz. Apple Silicon uses MLX Whisper; other platforms use the OpenAI Whisper `tiny` model through PyTorch.

First use downloads the Qwen embedding and Whisper models. Allow several gigabytes of disk and memory; a practical minimum has not been benchmarked. GPU/CUDA installation is not required for the CPU fallback, though inference can be slow.

## Memory and data

`examples/knowledge.example.txt` contains non-personal starter facts. Setup copies it to `src/rag_system/knowledge.txt` when absent. Edit that local file with facts separated by `#`. Small knowledge bases are supported; retrieval returns up to three entries. New memory is appended to that same file.

Existing root `knowledge.txt` files from older runs are preserved. If you want those older memories loaded at startup, review and merge them into `src/rag_system/knowledge.txt`, separating entries with `#`.

The application prints loaded memory on startup. Transcription runs locally; conversation text and retrieved context go to Gemini; scene requests upload camera images; generated response text goes to ElevenLabs. The vision-only demo does not use those services. Generated frames, chat logs, credentials, and personal memory are ignored by Git. Files removed from current Git tracking can still exist in older commits; this cleanup does not rewrite history.

## Manual dependency and asset installation

The setup helper automates this work, but every input is listed here for inspection:

- `requirements.txt`: complete pinned runtime graph for Apple Silicon macOS/Python 3.11.
- `requirements/vision.txt`: camera-only direct dependencies.
- `requirements/runtime.txt`: full direct dependencies with platform markers for speech.
- `requirements/experiments.txt`: extra packages for the standalone transcription experiment.
- OpenSeeFace: `https://github.com/emilianavt/OpenSeeFace.git`, revision `85aa70fc67582d046e771ea73625182a0d8f7475`, plus `patches/openseeface-opencv-shape.patch`.
- Gesture model: [MediaPipe float16 version 1](https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task), saved beside `hand_tracker.py`.
- YOLO: `yolo26n.pt` in the repository root, downloaded by `YOLO("yolo26n.pt")`.
- Qwen: `Qwen/Qwen3-VL-Embedding-2B`, downloaded through Sentence Transformers.
- MLX speech: `mlx-community/whisper-tiny`; other platforms: OpenAI Whisper `tiny`.

Do **not** install a PyPI package named `tracker`. OpenSeeFace needs its helper modules and complete `models/` directory. Do not run `pip install .` in its checkout: its historical packaging specifies Python below 3.11 and older packages; JARVIS imports its source with the dependencies above.

Both OpenCV distributions are pinned to `4.11.0.86` because MediaPipe requires `opencv-contrib-python` and Ultralytics requires `opencv-python`. They share `cv2` files. Avoid independently upgrading or uninstalling one distribution; recreate the environment if OpenCV becomes damaged.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Missing Python / Git | Install the prerequisites and reopen your terminal |
| macOS launcher not executable | Run `bash Start.command` from the extracted repo |
| Package conflict in existing `.venv-jarvis` | Rename the environment and rerun setup; do not merge archived requirements |
| `No module named tracker` | Run setup; use `scripts/start.py` or a valid `OPENSEEFACE_PATH` |
| Existing OpenSeeFace has another revision | Preserve it elsewhere, or use the pinned revision in a new checkout |
| Serial port error | Correct `ARDUINO_PORT`, close Arduino Serial Monitor, or leave the port blank |
| Cannot read camera | Check permissions, camera connection, and `CAMERA_INDEX` |
| No gesture model | Rerun setup; the model belongs beside `hand_tracker.py` |
| `mpv not found` | Install mpv and ensure the launching process can find it on `PATH` |
| API/model/voice error | Check `.env`, account permissions, and service availability |
| `look` before any scene | Wait for `frame2.jpg` after approximately two minutes; the app now reports when no frame exists |
| Kasa failure | Configure all four LAN addresses; this integration does not provide authenticated-device credentials |
| Linux GUI/audio library error | Install the system libraries listed above |

Useful checks: `.venv-jarvis/bin/python -m pip check` and, after installing the full dependencies, `.venv-jarvis/bin/python -m unittest discover -s tests -v` (replace the executable path on Windows).

## Experiments

`voice_transcription.py` uses Transformers, `datasets[audio]`, Accelerate, and Safetensors. Install `requirements/experiments.txt` in a separate environment. It downloads `openai/whisper-large-v3-turbo` and `distil-whisper/librispeech_long`. This optional experiment is not validated by the main runtime lock.

`gemini-testing.py` uses a separate fixed preview TTS model. `media_see.py` is an API exploration snippet. Neither is a supported launch path.
