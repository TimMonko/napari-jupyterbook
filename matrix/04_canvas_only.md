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

# Matrix 04: canvas_only=True

**Hypothesis:** `nbscreenshot(viewer)` captures the full Qt window, which includes the napari
chrome (layer list, controls, menus). On headless CI this window may not have its full size set,
resulting in a squished composite screenshot.

`nbscreenshot(viewer, canvas_only=True)` captures only the OpenGL canvas widget directly,
bypassing the window manager's size allocation for the outer window. This may produce a
correctly-sized image even when the full-window screenshot is squished.

```{code-cell} ipython3
import napari
import numpy as np
from napari.utils import nbscreenshot

rng = np.random.default_rng(42)
data = rng.integers(0, 255, (256, 256), dtype=np.uint8)

viewer = napari.Viewer()
viewer.add_image(data, name='test-image')
```

## Default (full window)

```{code-cell} ipython3
nbscreenshot(viewer)
```

## canvas_only=True

```{code-cell} ipython3
nbscreenshot(viewer, canvas_only=True)
```

```{code-cell} ipython3
viewer.close()
```
