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
the window to a known, full size, fixing the squished appearance.

Two sizes are tested: `800×600` and `1280×960`.

**Each section uses a distinct colormap** so you can confirm the screenshots are genuinely
different viewer instances and not a cached/stale render.

```{code-cell} ipython3
import napari
import numpy as np
from napari.utils import nbscreenshot

rng = np.random.default_rng(42)
data = rng.integers(0, 255, (256, 256), dtype=np.uint8)
```

## No resize (control) — colormap: gray

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='no-resize', colormap='gray')
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
```

## resize(800, 600) — colormap: green

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='resize-800', colormap='green')
viewer.window._qt_window.resize(800, 600)
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
```

## resize(1280, 960) — colormap: red

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='resize-1280', colormap='red')
viewer.window._qt_window.resize(1280, 960)
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
```
