---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Matrix 02: Explicit Qt window resize

**Hypothesis:** On headless CI, Qt/the window manager assigns a very small default size to the
window. Explicitly calling `viewer.window._qt_window.resize(W, H)` before the screenshot forces
the window to a known size.

**Note on QSettings carryover:** `viewer.close()` triggers Qt to call `saveGeometry()`, storing
the window size in QSettings (`~/.config/napari/napari.ini`). Subsequent `napari.Viewer()` calls
restore from QSettings, so sizing done in one notebook can contaminate the next. To prevent
this, each section below explicitly resets the saved geometry after closing.

Sizes tested: no resize (Qt default), `800×600`, `1280×720` (16:9 target).

**Each section uses a distinct colormap** so you can confirm screenshots are fresh captures.

```{code-cell} ipython3
import napari
import numpy as np
from napari.utils import nbscreenshot
from qtpy.QtCore import QSettings

rng = np.random.default_rng(42)
data = rng.integers(0, 255, (256, 256), dtype=np.uint8)

def clear_geometry():
    """Remove saved window geometry from QSettings to prevent carryover."""
    QSettings("napari", "napari").remove("MainWindow/geometry")
```

## No resize (control) — colormap: gray

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='no-resize', colormap='gray')
win = viewer.window._qt_window
print(f"default size: {win.size().width()} x {win.size().height()}")
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
clear_geometry()
```

## resize(800, 600) — colormap: green

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='resize-800', colormap='green')
viewer.window._qt_window.resize(800, 600)
print(f"resized to: {viewer.window._qt_window.size().width()} x {viewer.window._qt_window.size().height()}")
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
clear_geometry()
```

## resize(1280, 720) — 16:9 target — colormap: red

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='resize-1280x720', colormap='red')
viewer.window._qt_window.resize(1280, 720)
print(f"resized to: {viewer.window._qt_window.size().width()} x {viewer.window._qt_window.size().height()}")
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
clear_geometry()
```
