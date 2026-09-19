# Dependency manifests

| File | Purpose |
| --- | --- |
| `../requirements.txt` | Default installation: includes the full Apple Silicon/Python 3.11 lock |
| `macos-arm64-py311.lock.txt` | Every resolved runtime package, including transitive dependencies |
| `runtime.txt` | Direct runtime dependencies and non-Apple-Silicon speech fallback |
| `vision.txt` | Direct dependencies for the camera-only demo |
| `experiments.txt` | Additional standalone transcription experiment dependencies |
| `archive/` | Historical requirement lists retained for provenance; not installation inputs |

Do not combine the archive with the current manifests. See [dependency inventory](../docs/DEPENDENCIES.md) for libraries, external source, model files, OS tools, hardware, and verification limits.
