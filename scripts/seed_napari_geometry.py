"""Seed napari's saved window geometry to 1280x720.

napari restores QSettings on every startup, so running this script once before
any notebook execution sets the default window size for all notebooks — without
any per-notebook code. This is the project's equivalent of a Sphinx conf.py for
controlling viewer dimensions.

QSettings are written to the normal napari config location (OS registry on
Windows, plist on macOS, ~/.config/napari on Linux). This is harmless: napari
overwrites the same key with the user's actual window position on every close.

Usage:
    python scripts/seed_napari_geometry.py          # via pixi run seed-geometry
"""

import sys

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
