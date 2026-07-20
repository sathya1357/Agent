# My Personal Chatbot with OCR

This repository contains a small Streamlit-based chatbot with OCR support using Tesseract and the `pytesseract` Python wrapper.

**Quick overview**
- **Python app**: `agent.py`
- **Verifier script**: `verify_tesseract.py`

## Prerequisites

- Windows with Python (this workspace uses Python 3.14 in the configured environment).
- Tesseract OCR installed on your machine (see install options below).
- Python dependencies: `pytesseract`, `pillow`, `streamlit`, `ollama` (if used by your agent).

## Install Python dependencies

From the workspace root, install required Python packages (use the configured Python executable):

```powershell
C:/Python314/python.exe -m pip install -r requirements.txt
C:/Python314/python.exe -m pip install pytesseract pillow
```

## Install Tesseract (Windows)

Recommended (manual GUI):

1. Download the UB Mannheim build from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer and accept defaults. Note the install location (commonly under your user profile or Program Files).

Optional (package managers — requires admin / elevated PowerShell):

```powershell
# winget (preferred when available)
winget install --id UB-Mannheim.Tesseract -e --accept-source-agreements --accept-package-agreements

# or Chocolatey
choco install tesseract -y
```

After installation, verify Tesseract is available:

```powershell
where tesseract
tesseract --version
```

If `tesseract` is not globally available, note the full path to `tesseract.exe` (example: `C:\Users\sathy\AppData\Local\Programs\Tesseract-OCR\tesseract.exe`).

## Configure the app to find Tesseract

There are two options:

- Add the Tesseract install folder to your system `PATH` (recommended for convenience). Restart your terminal/IDE after updating PATH.
- Or let the app point directly to the executable at runtime. `agent.py` already attempts to set `pytesseract.pytesseract.tesseract_cmd` to the user-local path `C:\Users\sathy\AppData\Local\Programs\Tesseract-OCR\tesseract.exe` if it exists.

If you need to set it manually in code, add:

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\sathy\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
```

## Run the Streamlit app

From the workspace root run:

```powershell
C:/Python314/python.exe -m streamlit run agent.py
```

Open the browser URL printed by Streamlit (usually http://localhost:8501).

## Verify OCR functionality

1. Place a sample image `test.png` in the workspace or upload via the Streamlit UI.
2. Use the included `verify_tesseract.py` script to check the configured binary:

```powershell
C:/Python314/python.exe verify_tesseract.py
```

The verifier prints `FOUND:` with the path and `TESSERACT_VERSION:` when successful.

## Troubleshooting

- If you see `TesseractNotFoundError`, confirm the executable path and that the `tessdata` folder exists alongside the binary.
- If OCR output is empty or poor quality, try preprocessing the image (convert to grayscale, increase contrast) before passing to `pytesseract`.

## Files

- `agent.py`: main Streamlit app
- `verify_tesseract.py`: small helper that locates `tesseract.exe` and prints its version

## Next steps (optional)

- Add the Tesseract install folder to your system PATH (admin) so `tesseract` is globally available.
- If you want, I can add PATH for you (requires elevated privileges) or update `agent.py` to fallback to a configurable environment variable.

---
Created to help get OCR working quickly with the Streamlit chatbot.