from playwright.sync_api import Playwright, sync_playwright, expect
import time

#this is just random testing. 
#I was able to generate this template by running playwright codegen on CLI
#See: https://playwright.dev/python/docs/codegen#running-codegen
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.pinterest.com.au/search/pins/?q=2%20tier%20wedding%20cake%20blue")
    page.wait_for_load_state()
    #using time.sleep to encourage more loading since wait_for_load_state doesn't seem sufficient
    time.sleep(10)
    page.locator("a").filter(has_text="Openthebridesofoklahoma.com;").click()
    with page.expect_download() as download_info:
        page.locator("[data-test-id=\"more-options-download\"]").get_by_role("button", name="Download image").click(button="right")
    download = download_info.value
    page.goto("https://www.pinterest.com.au/search/pins/?q=2%20tier%20wedding%20cake%20blue")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

