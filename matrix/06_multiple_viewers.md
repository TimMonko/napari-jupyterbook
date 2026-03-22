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

# Matrix 06: Multiple simultaneous viewers

**Hypothesis:** When two or more `napari.Viewer()` instances exist simultaneously in the same
kernel, window management resources (Xvfb display connections, OpenGL contexts, Qt window
stacking) may compete, causing screenshots of non-frontmost viewers to appear squished or blank.

This notebook creates two viewers without closing the first one, then screenshots each.

For comparison, a sequential version (close first, open second) is included at the end.

```{code-cell} ipython3
import napari
import numpy as np
from napari.utils import nbscreenshot

rng = np.random.default_rng(42)
data_a = rng.integers(0, 255, (256, 256), dtype=np.uint8)
data_b = rng.integers(0, 255, (256, 256), dtype=np.uint8)
```

## Simultaneous viewers

Both viewers are open at the same time.

```{code-cell} ipython3
viewer_a = napari.Viewer()
viewer_a.add_image(data_a, name='viewer-a')
```

```{code-cell} ipython3
viewer_b = napari.Viewer()
viewer_b.add_image(data_b, name='viewer-b')
```

```{code-cell} ipython3
# Screenshot of viewer_a while viewer_b is also open
nbscreenshot(viewer_a)
```

```{code-cell} ipython3
# Screenshot of viewer_b while viewer_a is also open
nbscreenshot(viewer_b)
```

```{code-cell} ipython3
viewer_a.close()
viewer_b.close()
```

## Sequential viewers (close before reopening)

For reference: create, screenshot, close, then create second viewer.

```{code-cell} ipython3
viewer_a = napari.Viewer()
viewer_a.add_image(data_a, name='sequential-a')
nbscreenshot(viewer_a)
```

```{code-cell} ipython3
viewer_a.close()

viewer_b = napari.Viewer()
viewer_b.add_image(data_b, name='sequential-b')
nbscreenshot(viewer_b)
```

```{code-cell} ipython3
viewer_b.close()
```
