# napari CI Screenshot Sizing — Investigation and Fix

This directory contains diagnostic notebooks used to identify and reproduce the
root cause of "squished" or wrongly-sized `nbscreenshot()` output when building
napari JupyterBook sites on GitHub Actions.

The findings are documented here (via Copilot summarization) for other napari workshop / documentation
maintainers who hit the same problem.

---

## The Symptom

`nbscreenshot()` output looked correct on a local macOS/Windows machine but was
consistently squished (very short height) when built on GitHub Actions via
`jupyter-book build --execute`. A single notebook (`scipy-intro-bioimage-viz.md`)
reproducibly returned correct screenshots on CI while all others were broken.

---

## Root Cause

**Two independent factors combined to cause the problem:**

### 1. mystmd / JupyterBook v2 executes notebooks in parallel by default

`jupyter-book build --execute` launches multiple Jupyter kernels simultaneously.
This means several napari `Viewer()` instances can be open at the same time.

### 2. herbstluftwm tiles all Qt windows

The standard headless display setup for Python CI
([`pyvista/setup-headless-display-action`](https://github.com/pyvista/setup-headless-display-action))
uses **herbstluftwm**, a *tiling* window manager. herbstluftwm divides the
virtual display equally among all open windows.

When three napari viewers are open simultaneously, each gets ~1/3 of the 960 px
display height — roughly 320 px. Qt receives a resize event, but because event
delivery is deferred, the WM shrink event arrives partway through cell
execution, shrinking the window *before* `nbscreenshot()` fires.

### Confirmed by `11_size_diagnostic.md` on CI

The diagnostic notebook printed `window.size()` at several checkpoints:

```
[fresh-immediate]     window size: 1018 x 498   ← one other notebook running (50/50 split)
[after-add-image]     window size: 1018 x 228   ← two other notebooks started (33% each)
[after-processEvents] window size: 1018 x 728   ← some notebooks finished, frame expanded
```

Width was always ~1018 (fills the monitor width). Height varied entirely based
on how many other notebooks were alive at that moment — confirming the tiling
hypothesis beyond doubt.

---

## Why `scipy-intro-bioimage-viz.md` Was Unaffected

That notebook happened to run after most others had already finished,
so it was usually the only open window and got the full display height. A lucky
artifact of execution order, not anything it was doing differently.

---

## Things That Don't Help (or Make It Worse)

| Approach | Result |
|---|---|
| `app.processEvents()` before screenshot | **Makes it worse** — explicitly flushes the Qt event queue, delivering the WM shrink event before the screenshot |
| `sleep(1)` / `sleep(3)` before screenshot | Unreliable — timing-dependent, doesn't prevent the WM from retiling |
| `viewer.window._qt_window.resize(w, h)` | Overrides Qt geometry but herbstluftwm immediately overrides it back |
| `canvas_only=True` | Avoids the side panels but the canvas itself is still resized by the WM |
| Sequential execution (`--execute-parallel 1`) | Doesn't change the behavior and makes builds ~3× slower |

---

## The Fix

### Fix 1 — Float napari windows out of the tiling grid (core fix)

Tell herbstluftwm to exempt any window with title `napari` from the tiling grid.
Floating windows are positioned and sized by Qt, not the WM.

Add this step to `.github/workflows/pages.yml` **after** the headless display
setup and **before** the build step:

```yaml
- name: Configure herbstluftwm
  run: herbstclient rule title=napari floating=on
```

This single line is the essential fix. With it applied, all napari viewers
maintain their Qt-assigned size regardless of how many others are open in
parallel.

### Fix 2 — Seed napari's window geometry before notebooks run (optional, for consistency)

napari persists and restores window geometry via Qt's `QSettings`. When a fresh
viewer opens on CI with no prior config, it uses a default size (often a square
aspect ratio). Seeding the config once before any notebooks run ensures all
viewers open at 1280×720.

This is the project's equivalent of a Sphinx `conf.py` hook — there is no
mystmd pre-execution callback, but pixi's `depends-on` achieves the same effect.

**`scripts/seed_napari_geometry.py`** — opens a viewer, resizes it, saves
geometry to QSettings, closes:

```python
v = napari.Viewer(show=True)
v.window.resize(1280, 720)
app.processEvents()
s = QSettings("napari", "napari")
s.setValue("MainWindow/geometry", v.window._qt_window.saveGeometry())
s.sync()
v.close()
```

**`pyproject.toml`** — run it automatically before any build or start command:

```toml
[tool.pixi.tasks]
seed-geometry = { cmd = "python scripts/seed_napari_geometry.py" }
build         = { cmd = "jupyter-book build --html --execute",
                  depends-on = ["seed-geometry"] }
```

QSettings are written to the normal napari config location. This is harmless:
napari overwrites the same key with the user's actual window position on every
close, so it affects the viewer size for at most one open.

**`pages.yml`** — no extra configuration needed; `pixi run build` handles everything:

---

## Complete CI Workflow Snippet

```yaml
- name: Setup headless display
  uses: pyvista/setup-headless-display-action@...
  with:
    qt: true
    wm: herbstluftwm

- name: Configure herbstluftwm
  run: herbstclient rule title=napari floating=on

- name: Build workshop
  run: pixi run build    # seed-geometry depends-on fires automatically
  env:
    XDG_CONFIG_HOME: /tmp/napari-ci-config
```

---

## Diagnostic Notebook Matrix

| Notebook | What it tests | Key finding |
|---|---|---|
| `00_baseline.md` | Minimal viewer + screenshot + close | Control |
| `01_sleep.md` | sleep(0/1/3) before screenshot | Timing alone unreliable |
| `02_resize.md` | Qt `resize()` before screenshot | Overridden by WM retile |
| `03_process_events.md` | `processEvents()` before screenshot | **Makes things worse** |
| `04_canvas_only.md` | `canvas_only=True` | Canvas still resized |
| `05_viewer_close.md` | Fresh viewer → add_image (the typical pattern) | Captures the bad case |
| `06_multiple_viewers.md` | Simultaneous vs sequential viewers | Simultaneous = bad |
| `07_3d_mode.md` | `ndisplay=3` (3D mode) | Most severely affected |
| `08_combined.md` | resize + sleep combinations | Sleep helps slightly; not reliable |
| `09_kernel_keepalive.md` | `sleep()` placed *after* screenshot | Why scipy notebook survived |
| `10_no_close.md` | No `viewer.close()` at end | Viewer left open; WM can rearrange |
| `11_size_diagnostic.md` | Print `window.size()` at checkpoints | **Confirmed root cause** with CI output |
| `12_floating_validation.md` | All patterns with `floating=on` applied | Validates the fix |

---

## File Paths in Notebooks

### The Problem

JupyterBook/MyST sets each kernel's working directory to the **directory
containing the notebook file** at execution time. A notebook in `notebooks/`
runs with `CWD = .../napari-jupyterbook/notebooks/`. However, when opening
notebooks directly in JupyterLab via `pixi run start`, the kernel starts from
the **JupyterLab server root** (the repo root).

This produces a cross-environment CWD mismatch:

| Environment | `Path().resolve()` | `Path('data').exists()` | `Path('notebooks/data').exists()` |
|---|---|---|---|
| `pixi run build` locally | repo root | ✗ | ✓ |
| `pixi run build` on CI | `notebooks/` | ✓ | ✗ |
| JupyterLab (`pixi run start`) | repo root | ✗ | ✓ |

Actual output from `notebooks/files.md`:

```
# Locally (pixi run start --execute or build)
Current working directory:  C:\Users\...\napari-jupyterbook
Does notebooks/data exist?  True
Does data exist?  False

# On CI (pixi run build)
Current working directory:  /home/runner/work/napari-jupyterbook/napari-jupyterbook/notebooks
Does notebooks/data exist?  False
Does data exist?  True
```

### Recommendation

Use a robust fallback at the top of any notebook that accesses data files,
so the path resolves correctly regardless of CWD:

```python
from pathlib import Path

# Works whether CWD is the repo root or the notebooks/ subdirectory
data_dir = next(p for p in [Path('data'), Path('notebooks/data')] if p.exists())
```

Alternatively, you can pin the execution CWD by adding a `cwd` option to the
pixi task:

```toml
# Force build to run from notebooks/ so CWD always matches CI
build = { cmd = "jupyter-book build --html --execute", cwd = "notebooks", ... }
```

but note that this changes where `jupyter-book` looks for `myst.yml` / `_toc.yml`
so it requires corresponding config adjustments.

---

## Summary for Other Projects

If you maintain a napari JupyterBook / MyST-NB site that builds on GitHub
Actions with `pyvista/setup-headless-display-action`:

1. **Add `herbstclient rule title=napari floating=on`** after the headless
   display setup step. This is the one essential change.
2. Optionally seed `QSettings` to control the default window aspect ratio
   (otherwise napari may open square on first run with no saved config).
3. Set `XDG_CONFIG_HOME` on the pixi build/start tasks so both local Linux and
   CI runs use an isolated config directory — OR just accept that seeding will
   temporarily set your viewer size (napari resets it on the next close).
4. Do **not** add `app.processEvents()` before `nbscreenshot()` — it explicitly
   flushes the WM resize event you want to avoid.
5. Do **not** rely on `sleep()` to stabilise size — it's race-prone.
6. Use a `Path('data') if ... else Path('notebooks/data')` fallback when
   loading data files — the kernel CWD differs between local JupyterLab and
   CI/build execution.
