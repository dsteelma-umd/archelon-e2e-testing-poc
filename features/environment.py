from playwright.sync_api import sync_playwright

def before_scenario(context, _scenario):
    context.playwright = sync_playwright().start()
    headless = context.config.userdata.get("headed") != 'true'

    slow_mo = 0
    if context.config.userdata.get("slow_mo"):
        slow_mo = int(context.config.userdata.get("slow_mo"))

    context.browser = context.playwright.chromium.launch(
        headless = headless,
        slow_mo = slow_mo,
    )
    context.auth_context = context.browser.new_context(storage_state = "playwright/.auth/storage_state.json")
    context.page = context.auth_context.new_page()

def after_scenario(context, _scenario):
    context.auth_context.close()
    context.browser.close()
    context.playwright.stop()

