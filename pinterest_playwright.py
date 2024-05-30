from playwright.sync_api import Playwright, sync_playwright, expect
from bs4 import BeautifulSoup
import time

def extract_alt_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img', alt=True)
    alt_texts = [img.get('alt', '') for img in img_tags]
    return alt_texts

#great success - plan is to add img alts to a list and then iterate through them
# with a function that clicks into them, downloads the image and then resets
# the local storage unauth download to 0 (so we can have unlimited downloads)
# also want to simulate scrolling down so we can load more images - because
# pinterest has lazy loading.
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.pinterest.com.au/search/pins/?q=2%20tier%20wedding%20cake%20blue")
    page.wait_for_load_state()
    time.sleep(5)
    content = page.content()
    alt_texts = extract_alt_text(content)
    print(alt_texts)
    time.sleep(200)
    #using time.sleep to encourage more loading since wait_for_load_state doesn't seem sufficient

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

