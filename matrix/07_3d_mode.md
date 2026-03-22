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

# Matrix 07: 3D mode before screenshot

**Hypothesis:** Switching to 3D rendering mode (`viewer.dims.ndisplay = 3`) before a screenshot
forces napari/vispy to perform a full re-render of the canvas at the correct size, effectively
"flushing" any deferred sizing operations that cause squished 2D screenshots.

This is a specific behavior observed in `scipy-intro-bioimage-viz.md`, where the final screenshot
is taken after switching to `ndisplay=3` with explicit camera settings.

```{code-cell} ipython3
import napari
import numpy as np
from napari.utils import nbscreenshot

rng = np.random.default_rng(42)
data = rng.integers(0, 255, (64, 256, 256), dtype=np.uint8)  # 3D data
```

## 2D mode screenshot (control)

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='data-2d')
nbscreenshot(viewer)
```

## Switch to 3D mode, then screenshot

```{code-cell} ipython3
viewer.dims.ndisplay = 3
nbscreenshot(viewer)
```

## Switch back to 2D after 3D — does the size persist?

```{code-cell} ipython3
viewer.dims.ndisplay = 2
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
```
