"""Seed napari's saved window geometry to 1280x720.

napari restores QSettings on every startup, so running this script once before
any notebook execution sets the default window size for all notebooks — without
any per-notebook code. This is the project's equivalent of a Sphinx conf.py for
controlling viewer dimensions.

On Linux/CI, call this with XDG_CONFIG_HOME pointing at an isolated directory
(set in pages.yml) so it does not overwrite your personal napari configuration.
On Windows/macOS, QSettings is stored in the OS registry / plist; you may want
to skip this script locally if you prefer your own napari window size.

Usage:
    python scripts/seed_napari_geometry.py          # via pixi run seed-geometry
"""

import sys

# Skip on platforms where it would overwrite personal config and the user hasn't
# explicitly opted in. The CI workflow sets XDG_CONFIG_HOME to an isolated path.
import os

_is_ci = bool(os.environ.get("CI") or os.environ.get("XDG_CONFIG_HOME", "").startswith("/tmp"))
if sys.platform != "linux" and not _is_ci:
    print("seed_napari_geometry: skipping on non-Linux outside CI (would overwrite personal config)")
    sys.exit(0)

import napari
from qtpy.QtCore import QSettings
from qtpy.QtWidgets import QApplication

WIDTH, HEIGHT = 1280, 720

app = QApplication.instance() or QApplication(sys.argv)

v = napari.Viewer(show=True)
v.window._qt_window.resize(WIDTH, HEIGHT)
# Process events so Qt registers the resize before we serialise geometry.
app.processEvents()

s = QSettings("napari", "napari")
s.setValue("MainWindow/geometry", v.window._qt_window.saveGeometry())
s.sync()

v.close()
print(f"seed_napari_geometry: saved {WIDTH}x{HEIGHT} to QSettings")
