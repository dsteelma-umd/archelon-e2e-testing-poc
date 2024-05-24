
from playwright.sync_api import sync_playwright

def get_auth_context(browser):
    return browser.new_context(storage_state = "playwright/.auth/storage_state.json")

with sync_playwright() as playwright:
    # Launch a browser
    browser = playwright.chromium.launch(headless=False, slow_mo=10)

    context = get_auth_context(browser)

    # Create a new page
    page = context.new_page()

    page.goto("https://archelon-test.lib.umd.edu/")

    # Do whatever testing is necessary...
    page.pause()

    context.close()
