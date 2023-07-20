# WhatsApp-Bot

## Install dependencies
Install "Tesseract OCR" on your PC:   
Binaries for Windows: https://digi.bib.uni-mannheim.de/tesseract/?ref=nanonets.com
```commandline
pip install -r requirements.txt
```

## Set parameters

Edit **"config.json"**:    
1) **"pathToImg"** - Absolute path to source image
2) **"preprocess"** - (DEV TOOL! DON'T EDIT!) - settings for image processing
3) **"language"** - language to recognize (**'eng'** by default)

## Launch
```commandline
python -m tools.convert
```