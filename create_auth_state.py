from playwright.sync_api import sync_playwright

def create_auth(url):
    browser = playwright.chromium.launch(headless=False, slow_mo=1500)

    context = browser.new_context()

    # Create a new page
    page = context.new_page()

    # Visit the protected web site
    page.goto(url)

    # Pause Playwright until we get back to the website
    page.pause()

    context.storage_state(
        path="playwright/.auth/storage_state.json"
    )

    context.close()

with sync_playwright() as playwright:
    url = 'https://archelon-test.lib.umd.edu'
    create_auth(url)
