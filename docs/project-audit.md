# Project audit and verification

Inspection date: 2026-11-02. Scope: original application source, local resources, dependency metadata, and existing remote history.

## Source inventory

| File | Responsibility | Publication decision |
| --- | --- | --- |
| finaltest.py | First-frame GUI counts and annotated full-video playback | Recommended entry point; retain original filename |
| testfile.py | Separate annotated first-frame result buttons | Keep as a distinct working variant, not an automated test |
| traffic_gui.py | Compact result GUI and last raw frame | Keep; document its narrower behavior |
| traffic_management.py | Sequential detection accumulation and terminal timing simulation | Keep; do not change its timing algorithm |
| tempCodeRunnerFile.py | Byte-identical duplicate of original traffic_management.py | Ignore; preserve locally |
| README.py | Earlier documentation stored in a Python docstring | Replace with README.md for publication; preserve locally |

No application modules imported another original script. All four now import `project_config.py`. Original root Python files were copied into ignored `local_originals/` before modification. No originals were deleted.

## Changes

- Resolve weights and `Source_vids/*.mp4` relative to the source directory, independent of the shell working directory.
- Require local model and all four inputs with an actionable missing-resource message.
- Correct `motorbike` to the standard model's `motorcycle` label in two GUIs.
- Surface GUI decode and inference errors instead of silently reporting an empty road; release capture on first-frame decode failure.
- Preserve GUI layout, sequential playback, both timing formulas, and the conditional custom-model emergency branch.
- Preserve the existing remote MIT LICENSE without edits and base local main on its initial commit.

## Local resources excluded

| Resource | Approximate size | Reason |
| --- | --- | --- |
| Source_vids/north.mp4 | 4.8 MB | Provenance/redistribution rights not supplied |
| Source_vids/east.mp4 | 6.5 MB | Same |
| Source_vids/south.mp4 | 4.5 MB | Same |
| Source_vids/west.mp4 | 3.7 MB | Same |
| yolov8n.pt | 6.5 MB | Third-party model; official acquisition documented separately |
| Working_screenshots/ | 10.9 MB total | Concept dashboards do not match source; detection images contain third-party footage, including visible stock watermarks |
| Blue Doodle Project Presentation.pptx | 2.4 MB | Supporting presentation with unverified embedded-asset rights; not needed at runtime |
| venv/ | Local installed environment | Nonportable generated dependencies |

Caches, editor state, logs, secrets patterns, generated Ultralytics runs, duplicate Code Runner output and original backups are ignored. No LFS configuration was added. Excluded assets remain local. MIT covers project source, not third-party dependencies or footage; dependency licensing is linked in README.md.

## Verification actually performed

Environment: Windows, Python 3.13.5, Ultralytics 8.4.188, OpenCV 5.0.0.93, NumPy 2.5.4, Pillow 13.0.0, PyTorch 2.14.1+cpu.

- Imported OpenCV, Tkinter, PyTorch and Ultralytics; loaded the local model and inspected its class names. Car, motorcycle, bus and truck are present; ambulance and firetruck are absent.
- Decoded each video's first frame and performed real CPU inference: North 28, East 20, South 15, West 18 detections in the vehicle classes. GUI proposals were 30, 28, 23 and 26 seconds. These are observations on these local inputs, not accuracy measurements.
- Executed all four entry points through a bounded `runpy` harness. The harness replaced Tkinter's main loop to update the window, invoke its first button and close it; OpenCV imshow was real, while waitKey returned q to stop playback after one frame. CLI sleep was bypassed. The CLI visited all four directions and proposed 45 seconds for each first-frame sample. No full-duration or unattended GUI behavior is claimed.
- Four standard-library unit tests passed: normal playback end-of-file, portable path locations, missing-resource diagnostics, and explicit first-frame decode failure in each GUI.
- Python compilation passed for all published modules and tests.
- `python -m pip check` reported no broken requirements in the existing environment.
- Git whitespace validation passed. Publication uses an explicit source/documentation allowlist and a staged text/size review.

Not verified: a fresh dependency installation, full-length playback, GPU execution, other operating systems, unique-vehicle tracking, quantitative accuracy, safe intersection control, emergency-model behavior or real-world congestion improvements. Dependencies are pinned to observed installed versions; the environment is not a full transitive lockfile.
