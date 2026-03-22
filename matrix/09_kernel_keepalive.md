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

# Matrix 09: sleep at kernel exit (scipy pattern)

**Hypothesis:** The `sleep()` in `scipy-intro-bioimage-viz.md` is placed **after** the final
`nbscreenshot()`, with the comment *"sleep to allow screenshot to finish before notebook closes"*.
It is a **kernel keepalive**, not a pre-capture pause. Without it, the kernel may exit while the
last screenshot's PNG is still being encoded and returned from the kernel, dropping the final
cell output.

This notebook tests whether the sleep placement (before vs after) changes what you see, and
whether it only protects the last screenshot or all of them.

```{code-cell} ipython3
import napari
import numpy as np
from napari.utils import nbscreenshot
from time import sleep

rng = np.random.default_rng(42)
data = rng.integers(0, 255, (256, 256), dtype=np.uint8)
```

## Screenshot at first cell (no sleep anywhere before)

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='first-shot')
nbscreenshot(viewer)
```

## Second screenshot later in the same kernel session

More kernel time has elapsed since viewer creation.

```{code-cell} ipython3
viewer.add_image(data[:128, :128] * 2, name='second-layer')
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
```

## Fresh viewer — immediate screenshot and then sleep AFTER

This replicates the exact scipy pattern: screenshot first, sleep after.

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='scipy-pattern')
nbscreenshot(viewer)
```

```{code-cell} ipython3
:tags: [remove-cell]

# keep kernel alive so the screenshot above finishes encoding before exit
sleep(3)
```

```{code-cell} ipython3
viewer.close()
```
