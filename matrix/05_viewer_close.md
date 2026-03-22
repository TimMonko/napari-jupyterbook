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

# Matrix 05: viewer.close() between screenshots

**Hypothesis A:** Reusing a single viewer across multiple screenshots is fine.

**Hypothesis B:** Accumulating open viewer state (GPU resources, Qt widgets) between screenshots
causes degradation. Calling `viewer.close()` and creating a fresh `napari.Viewer()` for each
screenshot session ensures a clean slate.

This notebook takes three screenshots:
1. Fresh viewer → screenshot
2. Same viewer → screenshot (reuse)
3. Closed and fresh viewer → screenshot (reset)

All three should look identical if reuse is safe.

```{code-cell} ipython3
import napari
import numpy as np
from napari.utils import nbscreenshot

rng = np.random.default_rng(42)
data = rng.integers(0, 255, (256, 256), dtype=np.uint8)
```

## Screenshot 1 — fresh viewer

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='fresh-viewer')
nbscreenshot(viewer)
```

## Screenshot 2 — same viewer, new layer added

```{code-cell} ipython3
viewer.add_image(data * 0.5, name='second-layer')
nbscreenshot(viewer)
```

## Screenshot 3 — close and reopen

```{code-cell} ipython3
viewer.close()

viewer = napari.Viewer()
viewer.add_image(data, name='after-close')
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
```
