"""Launch the existing JARVIS main loop or vision demo from the correct directory."""
import argparse
import os
from pathlib import Path
import runpy
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vision-only", action="store_true", help="Camera/face/gesture/object demo; no API keys or microphone")
    args = parser.parse_args()
    os.chdir(ROOT)
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
    sys.path.insert(0, str(ROOT / "src"))
    tracker = Path(os.getenv("OPENSEEFACE_PATH") or ROOT / "external" / "OpenSeeFace").expanduser().resolve()
    sys.path.insert(0, str(tracker))
    missing = [str(path) for path in [tracker / "tracker.py", ROOT / "src/jarvis_core/gesture_recognizer.task"] if not path.is_file()]
    if missing:
        raise SystemExit("Run scripts/setup.py first. Missing: " + ", ".join(missing))
    if os.getenv("ENABLE_SMART_LIGHTS", "false").lower() == "true":
        keys = ["IP_Address_right", "IP_Address_left", "IP_Address_LED1", "IP_Address_LED2"]
        if any(not os.getenv(key, "").strip() for key in keys):
            raise SystemExit("Fill all four Kasa IP addresses in .env, or set ENABLE_SMART_LIGHTS=false.")
    if not args.vision_only:
        if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")) or not os.getenv("ELEVENLABS_API_KEY"):
            raise SystemExit("Fill GEMINI_API_KEY and ELEVENLABS_API_KEY in .env, or run with --vision-only.")
        if shutil.which("mpv") is None:
            raise SystemExit("Install mpv for speech playback. See docs/SETUP.md.")
        if not (ROOT / "src/rag_system/knowledge.txt").is_file():
            raise SystemExit("Run setup to create starter memory, or restore src/rag_system/knowledge.txt.")
    module = "jarvis_core.demo_main" if args.vision_only else "main"
    runpy.run_module(module, run_name="__main__")


if __name__ == "__main__":
    main()
