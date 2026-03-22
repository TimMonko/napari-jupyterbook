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

# Matrix 11: Window size diagnostic

**Purpose:** Print the actual Qt window size at the moment each screenshot is taken.
This tells us what size the window actually is on CI vs locally, and confirms whether
the squished screenshots are caused by a small window or by something else (e.g. a
render/vispy issue at correct size).

Also prints the WM_CLASS / window title that herbstluftwm would see, which we need
to write correct `herbstclient rule` patterns.

```{code-cell} ipython3
import napari
import numpy as np
from napari.utils import nbscreenshot
from qtpy.QtWidgets import QApplication

rng = np.random.default_rng(42)
data = rng.integers(0, 255, (256, 256), dtype=np.uint8)

def report_and_screenshot(viewer, label):
    win = viewer.window._qt_window
    size = win.size()
    print(f"[{label}] window size: {size.width()} x {size.height()}")
    print(f"[{label}] window title: {win.windowTitle()!r}")
    print(f"[{label}] object name: {win.objectName()!r}")
    return nbscreenshot(viewer)
```

## Fresh viewer, immediate screenshot

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='s1', colormap='gray')
report_and_screenshot(viewer, 'fresh-immediate')
```

## Same viewer, add_image (the failing pattern from 05)

```{code-cell} ipython3
viewer.add_image(data[:128, :128], name='s2', colormap='green')
report_and_screenshot(viewer, 'after-add-image')
```

```{code-cell} ipython3
viewer.close()
```

## Fresh viewer after close

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='s3', colormap='red')
report_and_screenshot(viewer, 'fresh-after-close')
```

```{code-cell} ipython3
viewer.close()
```

## Fresh viewer after processEvents (the broken pattern from 03)

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='s4', colormap='blue')
QApplication.processEvents()
report_and_screenshot(viewer, 'after-processEvents')
```

```{code-cell} ipython3
viewer.close()
```
