#!/bin/bash
cd -- "$(dirname -- "$0")" || exit 1
if [ ! -f .venv-jarvis/.jarvis-vision-ready ]; then
    python3.11 scripts/setup.py --vision-only || { read -r -p "Setup stopped. Press Enter to close."; exit 1; }
    touch .venv-jarvis/.jarvis-vision-ready
fi
.venv-jarvis/bin/python scripts/start.py --vision-only
read -r -p "Press Enter to close."
