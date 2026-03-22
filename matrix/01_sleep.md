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

# Matrix 01: sleep() before screenshot

**Hypothesis:** `time.sleep(N)` gives the Qt event loop and the window manager (herbstluftwm on CI)
time to finish laying out/sizing the window before the screenshot is captured. This replicates the
`sleep(3)` present (tagged `remove-cell`) in `scipy-intro-bioimage-viz.md`, which is the
**one notebook that renders correctly on CI**.

Three comparisons are made: no sleep, `sleep(1)`, and `sleep(3)`.
Each creates a **fresh viewer** so the results are independent.

## No sleep

```{code-cell} ipython3
import napari
import numpy as np
from napari.utils import nbscreenshot
from time import sleep

rng = np.random.default_rng(42)
data = rng.integers(0, 255, (256, 256), dtype=np.uint8)
```

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='no-sleep')
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
```

## sleep(1)

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='sleep-1')
sleep(1)
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
```

## sleep(3)

This mirrors the pattern used in `scipy-intro-bioimage-viz.md`.

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='sleep-3')
sleep(3)
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
```
