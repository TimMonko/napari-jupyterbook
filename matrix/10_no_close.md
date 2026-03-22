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

# Matrix 10: True baseline — no viewer.close()

**Hypothesis:** The original `00_baseline.md` included `viewer.close()` at the end, which may
have made the CI screenshot look deceptively correct. This notebook is a truly minimal case —
one viewer, one screenshot, no cleanup.

If this looks wrong, then the "correct" result in 00 was coincidental. If this also looks
correct, the problem is something that happens *after* the first add_image (consistent with
05's findings where screenshot 2, which follows an `add_image`, is mis-sized).

```{code-cell} ipython3
import napari
import numpy as np
from napari.utils import nbscreenshot

rng = np.random.default_rng(42)
data = rng.integers(0, 255, (256, 256), dtype=np.uint8)

viewer = napari.Viewer()
viewer.add_image(data, name='no-close-test')
nbscreenshot(viewer)
```

No `viewer.close()` is called — the kernel finalizes the viewer when it exits.
