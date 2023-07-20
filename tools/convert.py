import cv2
import pytesseract
from os import path, getpid, remove
from PIL import Image
from json import load

config_path = path.join('../', 'config.json')
PARAMS = load(open(config_path, 'r'))


def covert_img() -> str:
    """
    Recognize text from image
    :return: Characters found in image
    """
    image = cv2.imread(PARAMS['pathToImg'])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if "thresh" in PARAMS["preprocess"]:
        gray = cv2.threshold(gray, 0, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    if "blur" in PARAMS["preprocess"]:
        gray = cv2.medianBlur(gray, 3)

    filename = path.join("../tmp", f"{getpid()}.png")
    cv2.imwrite(filename, gray)
    # cv2.imshow("Output", gray)
    text = pytesseract.image_to_string(Image.open(filename), lang=PARAMS["language"])
    remove(filename)
    print(text)
    # input("pause…")
    return text


def parse_text(chars: str) -> str:
    """
    Get data from recognized text
    :param chars: Unprocessed text-data
    :return: Text in usable format
    """
    pass
