"""Install JARVIS dependencies and assets without overwriting personal settings."""
import argparse
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import urllib.request
import venv

ROOT = Path(__file__).resolve().parents[1]
OPENSEEFACE_COMMIT = "85aa70fc67582d046e771ea73625182a0d8f7475"
GESTURE_URL = "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task"


def run(*args):
    subprocess.run([str(arg) for arg in args], cwd=ROOT, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vision-only", action="store_true", help="Skip voice/API/memory dependencies")
    args = parser.parse_args()
    if sys.version_info[:2] != (3, 11):
        raise SystemExit("Use Python 3.11: python3.11 scripts/setup.py (Windows: py -3.11 scripts/setup.py)")
    if shutil.which("git") is None:
        raise SystemExit("Install Git, then run setup again: https://git-scm.com/downloads")

    env = ROOT / ".venv-jarvis"
    if not env.exists():
        venv.EnvBuilder(with_pip=True).create(env)
    python = env / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    if not python.exists():
        raise SystemExit("Existing .venv-jarvis is incomplete. Rename it and run setup again.")
    run(python, "-c", "import sys; assert sys.version_info[:2] == (3, 11), 'Existing .venv-jarvis must use Python 3.11'")
    run(python, "-m", "pip", "install", "--upgrade", "pip")
    if args.vision_only:
        requirements = "requirements/vision.txt"
    elif platform.system() == "Darwin" and platform.machine() == "arm64":
        requirements = "requirements.txt"
    else:
        requirements = "requirements/runtime.txt"
    run(python, "-m", "pip", "install", "-r", requirements)
    run(python, "-m", "pip", "check")

    checkout = ROOT / "external" / "OpenSeeFace"
    if not checkout.exists():
        checkout.parent.mkdir(exist_ok=True)
        run("git", "clone", "https://github.com/emilianavt/OpenSeeFace.git", checkout)
        run("git", "-C", checkout, "checkout", OPENSEEFACE_COMMIT)
    actual = subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip()
    if actual != OPENSEEFACE_COMMIT:
        raise SystemExit("Existing external/OpenSeeFace uses another revision. Move it aside or use the documented revision; setup will not reset your checkout.")
    patch = ROOT / "patches" / "openseeface-opencv-shape.patch"
    patched = subprocess.run(["git", "-C", str(checkout), "apply", "--reverse", "--check", str(patch)], capture_output=True)
    if patched.returncode != 0:
        run("git", "-C", checkout, "apply", "--check", patch)
        run("git", "-C", checkout, "apply", patch)

    model = ROOT / "src" / "assistant_runtime" / "gesture_recognizer.task"
    if not model.exists():
        temporary = model.with_suffix(".download")
        try:
            with urllib.request.urlopen(GESTURE_URL, timeout=120) as response, temporary.open("wb") as target:
                shutil.copyfileobj(response, target)
            temporary.replace(model)
        finally:
            temporary.unlink(missing_ok=True)
    run(python, "-c", 'from ultralytics import YOLO; YOLO("yolo26n.pt")')
    for source, destination in [(".env.example", ".env"), ("examples/knowledge.example.txt", "src/rag_system/knowledge.txt")]:
        if not (ROOT / destination).exists():
            shutil.copyfile(ROOT / source, ROOT / destination)
    print("Setup complete. Vision demo: .venv-jarvis Python + scripts/start.py --vision-only")
    if not args.vision_only:
        print("For the full assistant, install mpv/FFmpeg, fill .env API keys, then run scripts/start.py.")


if __name__ == "__main__":
    try:
        main()
    except (subprocess.CalledProcessError, OSError) as error:
        raise SystemExit(f"Setup stopped: {error}. See docs/SETUP.md; you can rerun setup after fixing this.")
