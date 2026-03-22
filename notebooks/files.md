---
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# File paths

```{code-cell} ipython3
from pathlib import Path
print("Path(): ", Path())
print("Current working directory: ", Path().resolve())
print("Contents of current directory: ", list(Path().iterdir()))
```