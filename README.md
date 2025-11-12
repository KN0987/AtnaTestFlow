# TemplateGeneration GUI

This project contains a small Tkinter GUI to drive the template generation logic provided in `AtnaTestFlow.py`.

How to run

1. From the project folder, run with Python 3 (Tkinter is included with standard CPython on Windows):

```powershell
python gui.py
```

2. Enter a full part number (example: XXX9356YYY) and click Generate.

Notes

- The GUI uses the same logic as `main.py` but runs it in a background thread so the UI stays responsive.
- No external dependencies beyond the Python standard library.
