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

# Matrix 03: QApplication.processEvents()

**Hypothesis:** After the viewer window is created, Qt has queued paint/resize/show events that
have not yet been processed. Calling `QApplication.processEvents()` flushes those events
synchronously, allowing the window to reach its final rendered state before `nbscreenshot` captures
it.

This is a zero-sleep alternative to Matrix 01 — it drains the event queue rather than waiting
for a fixed wall-clock time.

```{code-cell} ipython3
import napari
import numpy as np
from napari.utils import nbscreenshot
from qtpy.QtWidgets import QApplication

rng = np.random.default_rng(42)
data = rng.integers(0, 255, (256, 256), dtype=np.uint8)
```

## No processEvents (control)

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='no-process-events')
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
```

## Single processEvents()

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='process-events-once')
QApplication.processEvents()
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
```

## processEvents() called twice

Some deferred callbacks can re-queue events. Calling twice ensures two full cycles are drained.

```{code-cell} ipython3
viewer = napari.Viewer()
viewer.add_image(data, name='process-events-twice')
QApplication.processEvents()
QApplication.processEvents()
nbscreenshot(viewer)
```

```{code-cell} ipython3
viewer.close()
```
