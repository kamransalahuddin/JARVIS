# Dependency inventory and validation

[Back to JARVIS](../README.md) · [Setup](SETUP.md)

Audited on **2026-09-19** from every Python file in this repository, installed distribution metadata, the external OpenSeeFace source/models, local model files, Arduino files, and host executables. Dependencies are grouped by what actually uses them. A package list alone cannot include accounts, model assets, device firmware, or OS permissions.

## Python dependencies

| Area | Required distributions | Why |
| --- | --- | --- |
| Images and numbers | `numpy`, `opencv-python`, `opencv-contrib-python`, `pillow` | Camera frames, image conversion, array math; both OpenCV package names are required by upstream metadata |
| Hand gestures | `mediapipe` | Tasks GestureRecognizer |
| Face tracking | `onnxruntime` plus the OpenSeeFace checkout | `from tracker import Tracker` and ONNX inference |
| Object tracking | `ultralytics`, `lap`, `torch`, `torchvision` | YOLO26 and tracker assignment |
| Serial controller | `pyserial` | Imported even when physical servo output is disabled |
| Smart plugs | `python-kasa` | Imported by the gesture modules; device commands are optional |
| Configuration | `python-dotenv` | Load `.env` |
| Audio capture | `sounddevice` | Mono 16 kHz microphone stream |
| Apple Silicon transcription | `mlx-whisper`, `mlx` and resolved `mlx-metal` | Current Mac voice path |
| Other-platform transcription | `openai-whisper` | PyTorch Whisper fallback; installed only outside Apple Silicon |
| Memory and image embeddings | `sentence-transformers`, `transformers`, `torch`, `torchvision`, `pillow` | Qwen3-VL model and multimodal inputs |
| Conversation / scene API | `google-genai` | Gemini models, interactions, image upload |
| Speech output | `elevenlabs` | Streaming text-to-speech |
| Legacy import | `ollama` | Imported in `AI.py`; the active path does not contact an Ollama server |
| Shared constrained dependency | `protobuf` | Explicit compatibility pin; included in the resolved graph |
| Separate speech experiment | `datasets[audio]`, `accelerate`, `safetensors`, existing Torch/Transformers | `voice_transcription.py`; optional, not part of the main entry point |

**The complete Apple Silicon runtime lock contains 107 packages**, including every transitive package selected by pip. See [the lock](../requirements/macos-arm64-py311.lock.txt). These include HTTP/authentication clients, model/tokenizer utilities, scientific libraries, and native runtimes; they are installed automatically, not manually one at a time. Build-time tooling and OS packages are separate. The portable fallback and experiment manifests resolve additional platform-specific dependencies and are not covered by the macOS lock.

Python's standard-library imports (`os`, `sys`, `time`, `threading`, `asyncio`, `wave`, `base64`, `pathlib`, `typing`, `platform`) require no pip installation. OpenSeeFace's training-only `model.py` imports `geffnet`; training the external project is outside JARVIS's inference path and is not installed by setup.

No active JARVIS import requires ChromaDB, LangChain, Gensim, the OpenAI API client, or a running Ollama service, although unrelated packages were present in the original environment. Freezing the entire old environment would add unrelated dependencies and its conflicts.

## Source and model assets

| Asset | Required location / acquisition |
| --- | --- |
| `Tracker` and helper modules | Setup clones `external/OpenSeeFace` at `85aa70fc67582d046e771ea73625182a0d8f7475` and applies the recorded local compatibility patch |
| OpenSeeFace ONNX/JSON files | Preserve the checkout's complete `models/` directory; type 3 uses `lm_model3_opt.onnx`, with detector/prior-box and other supporting files |
| `gesture_recognizer.task` | Setup downloads MediaPipe float16 version 1 beside `hand_tracker.py` |
| `yolo26n.pt` | Setup downloads the YOLO26 nano weights into the repository root |
| `Qwen/Qwen3-VL-Embedding-2B` | Sentence Transformers/Hugging Face cache; first full run |
| `mlx-community/whisper-tiny` | MLX Whisper/Hugging Face cache; first transcription on Apple Silicon |
| OpenAI Whisper `tiny` | Whisper model cache; first transcription on other platforms |
| Personal knowledge | `src/rag_system/knowledge.txt`; setup seeds a non-personal example if absent |
| Arduino firmware | Included unchanged at `hardware/facetracker/facetracker.ino` |
| Optional speech experiment assets | `openai/whisper-large-v3-turbo` and `distil-whisper/librispeech_long` |

Model IDs are fixed by the application/dependency defaults, but remote model revisions are not fully pinned. Python version pins alone do not make model downloads immutable. See [third-party sources](THIRD_PARTY.md) for provenance.

## Host, hardware, and services

- Python 3.11, pip/venv, Git, a writable project folder, and internet access for installation/model downloads.
- Webcam and OS camera permission for both launch modes; camera index is configurable.
- Microphone, OS recording permission, mono 16 kHz input, and speakers for full voice mode.
- `mpv` for the actual ElevenLabs streaming call. FFmpeg for Whisper file decoding and the non-streaming ElevenLabs helper. SoundDevice/PortAudio for capture; Linux also needs GUI/OpenGL libraries for OpenCV windows.
- Gemini API key and model/API access; ElevenLabs API key, model access, and an available voice. These services can incur charges.
- Optional Arduino-compatible controller, board package, Arduino IDE, Servo library, two servos, suitable power/wiring, and a serial driver appropriate to the actual USB chipset.
- Optional compatible Kasa plugs, four configured LAN addresses, and reachable network access. The integration does not supply device-login credentials.

## What was found on the author's Mac

- `~/OpenSeeFace/tracker.py` exists. Its checkout has the pinned revision above plus a pre-existing two-line OpenCV vector-shape change. Setup now reproduces that change in its own external checkout. The original checkout is untouched.
- `~/Documents/Arduino/facetracker/facetracker.ino` was initially an iCloud placeholder, then became readable. The included firmware is an exact copy. A second `testarduion` sketch was indexed but is not established as a runtime dependency.
- The gesture model and YOLO weights were already present locally and absent from Git.
- Python 3.11.15, mpv, FFmpeg, and Arduino IDE were installed. No separate Homebrew PortAudio formula was installed; the wheel-provided library was available.
- The original configured serial device was not connected. Board model, servo models, USB chipset, and physical wiring could not be established from the available files.
- File-name searches covered the repo, home directory, common project/document locations, and Spotlight-indexed files. Cloud-only/unindexed or inaccessible files cannot be exhaustively certified from a software audit.

## Problems corrected

The root requirements file was absent; one old list was empty and the gesture snapshot omitted voice, API, embedding, and configuration packages. The existing environment mixed NumPy 1.x with OpenCV 5's NumPy 2 requirement and contained unrelated protobuf conflicts. MediaPipe 0.10.21 installed a working universal binary but reported incompatible wheel platform metadata to `pip check` on ARM64. The new manifests use MediaPipe 0.10.35 and aligned OpenCV 4.11 distributions.

The author's absolute OpenSeeFace path and fixed serial device have been replaced with configuration/default local paths. Hardware actions are optional. The starter memory, memory-file consistency, small-memory retrieval, early camera-read errors, and image format at the scene-embedding boundary are handled without replacing the architecture.

## Validation scope

- Full runtime packages installed into a separate temporary Python 3.11 environment; `pip check` passed after correcting MediaPipe.
- Main third-party imports succeeded, including MLX Whisper, Sentence Transformers, Gemini, and ElevenLabs.
- OpenSeeFace initialized its models and returned no faces on a synthetic blank frame.
- MediaPipe initialized the gesture model and processed a synthetic blank frame.
- YOLO26 completed tracking on a synthetic blank frame. The complete vision launcher also ran one synthetic camera iteration and released its camera handle.
- Qwen loaded from the existing model cache and produced 2048-dimensional text and RGB-image embeddings.
- The full setup helper completed in an isolated folder, downloaded external assets, and preserved configuration/memory on a repeat run.
- Six regression tests passed for optional serial output, unchanged serial protocol, disabled lights, small-memory retrieval, RGB scene inputs/missing frames, and credential checks before application startup.

Camera/microphone capture, live Gemini/ElevenLabs requests, real servo motion, and smart-plug switching are not claimed as validated. Windows/Linux hardware and speech fallback execution still need native testing. See the setup guide for platform qualifications.
