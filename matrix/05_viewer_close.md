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

**CI findings so far:**
- Screenshot 1 (fresh viewer) → correct ✓
- Screenshot 2 (same viewer, `add_image` called) → **mis-sized** ✗
- Screenshot 3 (close + fresh viewer) → correct ✓

**Hypothesis:** `add_image()` internally updates Qt widgets (adds a row to the layer list, repaints
controls), which flushes queued WM resize events — shrinking the window before the screenshot.
Adding a `sleep()` after `add_image` (but before the screenshot) may allow the window to stabilise
but probably won't help because `sleep()` does not drain the Qt event queue — it just idles the
kernel thread while the WM events are still queued.

A more direct fix is `processEvents()` — but 03 showed that makes things **worse** (it flushes
the WM shrink event). So sleep is the only candidate that idles without queue-flushing.

```{code-cell} ipython3
import napari
import numpy as np
from napari.utils import nbscreenshot
from time import sleep

rng = np.random.default_rng(42)
data = rng.integers(0, 255, (256, 256), dtype=np.uint8)
```

## Screenshot 1 — fresh viewer (control, expected good)

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='fresh-viewer', colormap='gray')
nbscreenshot(viewer)
```

## Screenshot 2a — same viewer, add_image, NO sleep (expected bad — reproduced from first run)

```{code-cell} ipython3
viewer.add_image(data[:128, :128], name='second-layer', colormap='green')
nbscreenshot(viewer)
```

## Screenshot 2b — same viewer, add another layer, sleep(1) before screenshot

```{code-cell} ipython3
viewer.add_image(data[64:192, 64:192], name='third-layer', colormap='blue')
sleep(1)
nbscreenshot(viewer)
```

## Screenshot 2c — same viewer, add another layer, sleep(3) before screenshot

```{code-cell} ipython3
viewer.add_image(data[32:96, 32:96], name='fourth-layer', colormap='red')
sleep(3)
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
```

## Screenshot 3 — close and reopen (control, expected good)

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='after-close', colormap='magenta')
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
```
