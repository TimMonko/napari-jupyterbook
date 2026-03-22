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

# Matrix 00: Baseline (no tricks)

**Hypothesis:** Control case. Minimal napari viewer + `nbscreenshot` with no special handling.

**Expected failure on CI:** The viewer window may be very small (squished), because Qt has not had
time to lay out and render the window before the screenshot is captured.

If this looks correct, the problem lies elsewhere. If squished, all other matrix notebooks test
potential fixes.

```{code-cell} ipython3
import napari
import numpy as np
from napari.utils import nbscreenshot

rng = np.random.default_rng(42)
data = rng.integers(0, 255, (256, 256), dtype=np.uint8)

viewer = napari.Viewer()
viewer.add_image(data, name='test-image')
```

Screenshot taken immediately after creating the viewer — no sleep, no resize, no event processing:

```{code-cell} ipython3
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
```
