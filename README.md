# WhatsApp-Bot

## Install dependencies
Install "Tesseract OCR" on your PC:   
Binaries for Windows: https://digi.bib.uni-mannheim.de/tesseract/?ref=nanonets.com
```commandline
pip install -r requirements.txt
```

## Set parameters

Edit **"config.json"**:
1) **type** - Type of the document (passport/credit/insurance/additional)
2) **"path"** - Absolute path to source image
3) **"preprocess"** - (DEV TOOL! DON'T EDIT!) - settings for image processing
4) **"language"** - language to recognize (**'eng'** by default)

## Launch
```commandline
python -m main
```