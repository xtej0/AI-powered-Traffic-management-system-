"""Regression checks without loading weights, opening windows or requiring footage."""
import ast
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import project_config as config

ROOT = Path(__file__).resolve().parents[1]


def load_function(filename, name, namespace):
    tree = ast.parse((ROOT / filename).read_text(encoding="utf-8"))
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    exec(compile(ast.Module(body=[function], type_ignores=[]), filename, "exec"), namespace)
    return namespace[name]


class ResourceTests(unittest.TestCase):
    def test_paths_are_independent_of_working_directory(self):
        self.assertEqual(Path(config.video_path("north")), ROOT / "Source_vids" / "north.mp4")
        self.assertEqual(config.MODEL_PATH, ROOT / "yolov8n.pt")

    def test_missing_resources_explain_setup(self):
        with TemporaryDirectory(dir=ROOT) as directory:
            base = Path(directory)
            with patch.object(config, "MODEL_PATH", base / "yolov8n.pt"), patch.object(config, "VIDEO_DIR", base):
                with self.assertRaisesRegex(FileNotFoundError, "README.md") as error:
                    config.validate_resources()
                self.assertIn("north.mp4", str(error.exception))
                self.assertIn("yolov8n.pt", str(error.exception))
                for name in ["yolov8n.pt", "north.mp4", "east.mp4", "south.mp4", "west.mp4"]:
                    (base / name).touch()
                config.validate_resources()

    def test_unreadable_first_frame_is_not_zero_traffic(self):
        class Capture:
            released = False
            def read(self):
                return False, None
            def release(self):
                self.released = True
        class CV:
            def VideoCapture(self, path):
                return capture
        for filename, function in [("finaltest.py", "count_vehicles"), ("testfile.py", "detect_vehicles"), ("traffic_gui.py", "detect_vehicles")]:
            with self.subTest(filename=filename):
                capture = Capture()
                detect = load_function(filename, function, {"cv2": CV()})
                with self.assertRaisesRegex(RuntimeError, "Cannot read video"):
                    detect("broken.mp4")
                self.assertTrue(capture.released)


if __name__ == "__main__":
    unittest.main()
