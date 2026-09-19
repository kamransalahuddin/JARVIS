"""Regression checks for startup options and data boundaries; no live devices/APIs."""
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import Mock, patch

import numpy as np
import cv2
from google import genai

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def load_file(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PortabilityTests(unittest.TestCase):
    def test_no_serial_device_is_opened_by_default(self):
        serial = Mock()
        with patch.dict(os.environ, {}, clear=True), patch.dict(sys.modules, {
            "serial": serial, "tracker": Mock(), "dotenv": Mock()
        }):
            module = load_file("nose_test", "src/jarvis_core/nose_cam.py")
            module.send_coordinates_to_arduino(12, -7)
        serial.Serial.assert_not_called()

    def test_configured_serial_protocol_is_preserved(self):
        serial = Mock()
        with patch.dict(os.environ, {"ARDUINO_PORT": "COM9"}, clear=True), patch.dict(sys.modules, {
            "serial": serial, "tracker": Mock(), "dotenv": Mock()
        }), patch("time.sleep"):
            module = load_file("nose_test", "src/jarvis_core/nose_cam.py")
            module.send_coordinates_to_arduino(12, -7)
        serial.Serial.assert_called_once_with("COM9", 115200)
        serial.Serial.return_value.write.assert_called_once_with(b"12,-7\r")

    def test_disabled_lights_do_not_send_commands(self):
        import jarvis_core
        plugs = Mock()
        with patch.dict(sys.modules, {"jarvis_core.tp_link": plugs}), patch.object(
            jarvis_core, "tp_link", plugs, create=True
        ), patch.dict(os.environ, {"ENABLE_SMART_LIGHTS": "false"}):
            module = load_file("lights_test", "src/jarvis_core/light_logic.py")
            for gesture in ["Pointing_Up", "Victory", "Open_Palm", "Closed_Fist"]:
                module.light_logic(gesture)
        self.assertEqual(plugs.mock_calls, [])

    def test_retrieval_with_one_or_zero_memories(self):
        fake_rag = types.ModuleType("rag_system.rag")
        fake_rag.read_context = lambda: ["one fact"]
        fake_sentence = Mock()
        fake_sentence.SentenceTransformer.return_value.encode.return_value = np.array([1.0, 0.0])
        with patch.dict(sys.modules, {"rag_system.rag": fake_rag, "sentence_transformers": fake_sentence}):
            module = load_file("rag_system.embedding_test", "src/rag_system/embedding.py")
        self.assertEqual(module.embed("query"), ["one fact"])
        module.context.clear()
        module.doc_embeddings_list.clear()
        self.assertEqual(module.embed("query"), [])

    def test_scene_images_are_rgb_and_missing_frame_skips_api(self):
        fake_embedding = Mock()
        fake_embedding.model.encode.return_value = np.array([1.0, 0.0])
        fake_ai = Mock()
        fake_genai = Mock()
        with patch.dict(sys.modules, {
            "rag_system.embedding": fake_embedding,
            "jarvis_core.AI": fake_ai,
            "google.genai": fake_genai,
        }), patch("google.genai", fake_genai):
            module = load_file("jarvis_core.scene_test", "src/jarvis_core/scene_monitor.py")
        frame = np.array([[[10, 20, 30]]], dtype=np.uint8)
        module.compare_scenes(frame, frame)
        image = fake_embedding.model.encode.call_args_list[0].args[0]["image"]
        self.assertEqual(image.getpixel((0, 0)), (30, 20, 10))
        with patch.object(module.os.path, "isfile", return_value=False):
            module.pass_image()
        fake_genai.Client.return_value.files.upload.assert_not_called()

    def test_launcher_checks_keys_before_importing_application(self):
        module = load_file("start_test", "scripts/start.py")
        previous = Path.cwd()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "external/OpenSeeFace").mkdir(parents=True)
            (root / "external/OpenSeeFace/tracker.py").touch()
            (root / "src/jarvis_core").mkdir(parents=True)
            (root / "src/jarvis_core/gesture_recognizer.task").touch()
            try:
                with patch.object(module, "ROOT", root), patch.dict(os.environ, {}, clear=True), patch.object(sys, "argv", ["start.py"]), patch.object(module.runpy, "run_module") as run:
                    with self.assertRaisesRegex(SystemExit, "GEMINI_API_KEY"):
                        module.main()
                    run.assert_not_called()
            finally:
                os.chdir(previous)


if __name__ == "__main__":
    unittest.main()
