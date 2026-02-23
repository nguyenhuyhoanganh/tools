import time
import cv2
import numpy as np
import pytesseract
from playwright.sync_api import sync_playwright

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

URL = "https://web.sunwin.pw"

CHAN = {"x": 225, "y": 340, "width": 60, "height": 25}
LE   = {"x": 485, "y": 345, "width": 50, "height": 15}
BATRANG = {"x": 405, "y": 425, "width": 50, "height": 15}
BADO = {"x": 495, "y": 425, "width": 50, "height": 20}
SAPDOI = {"x": 355, "y": 345, "width": 50, "height": 15}
TONGTIEN = {"x": 80, "y": 132, "width": 90, "height": 20}

def cap(page, region):
    b = page.screenshot(clip=region)
    img = cv2.imdecode(np.frombuffer(b, np.uint8), cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, None, fx=3, fy=3)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return img

def ocr(img):
    t = pytesseract.image_to_string(img, config="--psm 7 -c tessedit_char_whitelist=0123456789")
    return int(t) if t.strip().isdigit() else -1

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False, 
        args=["--disable-blink-features=AutomationControlled"]
    )
    context = browser.new_context(viewport={"width": 800, "height": 600})
    page = context.new_page()
    page.goto(URL)

    time.sleep(40)

    while True:
        # page.mouse.click(645, 465)
        # time.sleep(2)

        # tongtien = ocr(cap(page, TONGTIEN))
        # if tongtien < 10000:
        #     break

        chan = ocr(cap(page, CHAN))
        le = ocr(cap(page, LE))
        sapdoi = ocr(cap(page, SAPDOI))
        batrang = ocr(cap(page, BATRANG))
        bado = ocr(cap(page, BADO))

        # print(chan)

        if chan < 20000:
            # print("Đặt CHẴN")
            page.mouse.click(255, 352)
            time.sleep(0.5)

        if le < 20000:
            # print("Đặt LẺ")
            page.mouse.click(510, 357)
            time.sleep(0.5)

        # if batrang < 10000:
        #     # print("Đặt 3 TRẮNG")
        #     page.mouse.click(430, 455)
        #     time.sleep(0.5)

        # if bado < 10000:
        #     # print("Đặt 3 ĐỎ")
        #     page.mouse.click(535, 455)
        #     time.sleep(0.5)
        
        # if sapdoi < 10000:
        #     # print("Đặt SẤP ĐÔI")
        #     page.mouse.click(380, 370)
        #     time.sleep(0.5)

        time.sleep(2)
