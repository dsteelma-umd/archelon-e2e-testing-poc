from playwright.sync_api import sync_playwright

# def create_auth():
#     browser = playwright.chromium.launch(headless=False, slow_mo=1500)

#     context = browser.new_context()

#     # Create a new page
#     page = context.new_page()

#     # Visit the protected web site - using Grove as an example
#     page.goto("https://grove-test.lib.umd.edu/")

#     page.pause()

#     context.storage_state(
#         path="playwright/.auth/storage_state.json"
#     )

#     context.close()

# def get_auth_context(browser):
#     return browser.new_context(storage_state = "playwright/.auth/storage_state.json")

# def fail_on_request():
#     print("--- Request was made: FAIL")

with sync_playwright() as playwright:
    create_auth()
    # # Launch a browser
    # browser = playwright.chromium.launch(headless=False, slow_mo=10)

    # context = get_auth_context(browser)

    # # Create a new page
    # page = context.new_page()

    # page.goto("https://grove-test.lib.umd.edu/")


    # page.get_by_role("link", name="Test").first.click()

    # page.once('request', fail_on_request)
    # page.get_by_role("button", name="Add Term").click()

    # context.close()
