import time
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        context = browser.new_context(
            viewport={"width": 800, "height": 600}
        )

        page = context.new_page()

        page.goto("https://web.sunwin.pw")

        print("Login và vào bàn, sau đó CLICK vào vị trí cần lấy toạ độ")

        # Inject script bắt click
        page.evaluate("""
            window.clickedX = -1;
            window.clickedY = -1;

            document.addEventListener('click', function(e) {
                window.clickedX = e.clientX;
                window.clickedY = e.clientY;
            }, true);
        """)

        last_x = -1
        last_y = -1

        while True:

            x = page.evaluate("window.clickedX")
            y = page.evaluate("window.clickedY")

            if x != last_x or y != last_y:
                print(f"CLICK tại: X={x}, Y={y}")
                last_x = x
                last_y = y

            time.sleep(0.1)

main()
