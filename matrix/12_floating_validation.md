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

# Matrix 12: Parallel execution and window size stability

**Root cause confirmed by 11_size_diagnostic:**

```
[fresh-immediate]   window size: 1018 x 498   ← one other notebook running
[after-add-image]   window size: 1018 x 228   ← two other notebooks now running
[after-processEvents] window size: 1018 x 728 ← notebooks closed, frame expanded
```

Width is always 1018 (full display width). Only **height** changes, in sync with how many
napari viewers herbstluftwm is currently tiling across the shared display.

**Mechanism:** mystmd executes multiple notebooks in parallel (by default). Each notebook creates
a `napari.Viewer()`, which opens a Qt window that herbstluftwm tiles into the current frame by
splitting the available height. As more viewers open/close, herbstluftwm resizes all tiled windows.
Qt defers those WM resize events. The first internal redraw trigger (`add_image`, `processEvents`,
or just elapsed time) delivers the pending shrink — after which `nbscreenshot` captures a squished
window.

**This notebook**: creates a viewer, reports size, deliberately invokes `add_image` multiple
times so you can see the size reported for each step. It expects consistent 1018×498 with the
`herbstclient rule title=napari floating=on` fix applied in CI.

```{code-cell} ipython3
import napari
import numpy as np
from napari.utils import nbscreenshot
from qtpy.QtCore import QSettings

rng = np.random.default_rng(42)
data = rng.integers(0, 255, (256, 256), dtype=np.uint8)

def report_size(viewer, label):
    win = viewer.window._qt_window
    size = win.size()
    print(f"[{label}] {size.width()} x {size.height()}")

def clear_geometry():
    QSettings("napari", "napari").remove("MainWindow/geometry")
```

## Fresh viewer

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='layer-1', colormap='gray')
report_size(viewer, 'after first add_image')
nbscreenshot(viewer)
```

## Second add_image (the historically broken step)

```{code-cell} ipython3
viewer.add_image(data[:128, :128], name='layer-2', colormap='green')
report_size(viewer, 'after second add_image')
nbscreenshot(viewer)
```

## Third add_image

```{code-cell} ipython3
viewer.add_image(data[64:192, 64:192], name='layer-3', colormap='blue')
report_size(viewer, 'after third add_image')
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
clear_geometry()
```

If `floating=on` is working, all three size reports should be identical and all three screenshots should look the same size.
