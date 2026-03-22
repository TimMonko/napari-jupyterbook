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

# Matrix 08: Combined fixes (kitchen sink)

**Hypothesis:** Combining `resize` + `processEvents()` + `sleep()` eliminates the squished
screenshot problem even if no single fix is sufficient alone.

**Based on CI findings:** `processEvents()` makes things WORSE (it flushes the WM shrink event).
So only resize + sleep variants remain interesting here. The baseline is included for comparison.

All resize sections use `clear_geometry()` after close to prevent QSettings carryover.

```{code-cell} ipython3
import napari
import numpy as np
from napari.utils import nbscreenshot
from qtpy.QtCore import QSettings
from time import sleep

rng = np.random.default_rng(42)
data = rng.integers(0, 255, (256, 256), dtype=np.uint8)

def clear_geometry():
    QSettings("napari", "napari").remove("MainWindow/geometry")
```

## Baseline (no fixes)

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='baseline')
print(f"size: {viewer.window._qt_window.size().width()} x {viewer.window._qt_window.size().height()}")
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
clear_geometry()
```

## resize(1280, 720) only

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='resize-only')
viewer.window._qt_window.resize(1280, 720)
print(f"size: {viewer.window._qt_window.size().width()} x {viewer.window._qt_window.size().height()}")
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
clear_geometry()
```

## resize(1280, 720) + sleep(1)

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='resize+sleep1')
viewer.window._qt_window.resize(1280, 720)
sleep(1)
print(f"size: {viewer.window._qt_window.size().width()} x {viewer.window._qt_window.size().height()}")
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
clear_geometry()
```

## resize(1280, 720) + sleep(3)

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='resize+sleep3')
viewer.window._qt_window.resize(1280, 720)
sleep(3)
print(f"size: {viewer.window._qt_window.size().width()} x {viewer.window._qt_window.size().height()}")
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
clear_geometry()
```
