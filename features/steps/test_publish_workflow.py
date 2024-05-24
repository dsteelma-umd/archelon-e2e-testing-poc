"""Publish Workflow feature tests."""

from playwright.sync_api import Page, expect

from behave import given, then, when
@given('the URL of a published and visible item')
def step_given(context):
    context.page_url = 'https://archelon-test.lib.umd.edu/catalog/https:%2F%2Ffcrepo-test.lib.umd.edu%2Ffcrepo%2Frest%2Fdc%2F2024%2F1%2F47%2F94%2Faf%2Fc8%2F4794afc8-474b-469c-9aee-5e659e75bf36'

    # Make sure item is actually published and visible
    page: Page = context.page
    page.goto(context.page_url)
    context.page_title = page.locator("//h1[@itemprop='name']").inner_text()
    publication_status = page.locator("dd.blacklight-publication_status")
    visibility = page.locator("dd.blacklight-visibility")
    expect(publication_status).to_contain_text("Published")
    expect(visibility).to_contain_text("Visible")

@given('the URL of a published and hidden item')
def step_given(context):
    context.page_url = 'https://archelon-test.lib.umd.edu/catalog/https:%2F%2Ffcrepo-test.lib.umd.edu%2Ffcrepo%2Frest%2Fdc%2F2024%2F1%2F20%2F18%2F6b%2F92%2F20186b92-4bc8-465b-972e-86eb43486736'
    context.digital_collections_page_url = 'https://digital-test.lib.umd.edu/result/id/20186b92-4bc8-465b-972e-86eb43486736?relpath=dc/2024/1'

    # Make sure item is actually published and hidden
    page: Page = context.page
    page.goto(context.page_url)
    context.page_title = page.locator("//h1[@itemprop='name']").inner_text()
    publication_status = page.locator("dd.blacklight-publication_status")
    visibility = page.locator("dd.blacklight-visibility")
    expect(publication_status).to_contain_text("Published")
    expect(visibility).to_contain_text("Hidden")

@given('the URL of an unpublished item')
def given_an_unpublished_item(context):
    context.page_url = 'https://archelon-test.lib.umd.edu/catalog/https:%2F%2Ffcrepo-test.lib.umd.edu%2Ffcrepo%2Frest%2Fdc%2F2024%2Ftest%2Fd3%2Ff9%2F90%2F91%2Fd3f99091-0e27-4fd6-87e2-5283ea7b8add'

@given('the URL of a published item')
def given_an_unpublished_item(context):
    context.page_url = 'https://archelon-test.lib.umd.edu/catalog/https:%2F%2Ffcrepo-test.lib.umd.edu%2Ffcrepo%2Frest%2Fdc%2F2024%2F1%2F39%2Fcb%2F45%2Fc7%2F39cb45c7-9ec7-4e2a-82e3-dda1e958380d'

@when('we display the item\'s detail page')
def when_display_item_detail_page(context):
    context.page.goto(context.page_url)
    print("When")

@when('we search for the item in the Digital Collections PUI')
def step_when(context):
    page:Page = context.page
    search_url = 'https://digital-test.lib.umd.edu/searchnew'
    query = context.page_title
    page.goto(search_url)
    search_field = page.get_by_role('textbox', name='Find...')
    search_field.fill(query)
    search_button = page.get_by_role('button', name='Apply')
    search_button.click()

@when('click the Unpublish button')
def step_when(context):
    page:Page = context.page
    unpublish_button = page.get_by_role('button', name="Unpublish")
    unpublish_button.click()


@then('a Publish button will be displayed')
def then_publish_button_is_displayed(context):
    page = context.page
    publish_button = page.get_by_role('button', name='Publish', exact=True)
    expect(publish_button).to_be_visible()
    page.close()

@then('an Unpublish button will be displayed')
def then_unpublish_button_is_displayed(context):
    page = context.page
    publish_button = page.get_by_role('button', name='Unpublish', exact=True)
    expect(publish_button).to_be_visible()

@then('the item appears in the Digital Collections PUI search results')
def step_then(context):
    page:Page = context.page
    search_result = page.get_by_role('link', name=context.page_title, exact=True)
    expect(search_result).to_be_visible()
    search_result.click()

@then('the detail page for the item can be accessed')
def step_then(context):
    page:Page = context.page
    expect(page.get_by_role('heading', name=context.page_title, exact=True)).to_be_visible()

@then('the item appears in OAI-PMH queries')
def step_then(context):
    context.scenario.skip(reason='TODO. OAI-PMH is not available on digital-test.lib.umd.edu')

@then('the item does not appear in the Digital Collections PUI search results')
def step_then(context):
    page:Page = context.page
    expect(page.locator('//body')).not_to_contain_text(context.page_title)

@then('its public detail may be accessed, provided the user has the direct URL to it')
def step_then(context):
    page: Page = context.page

@then('the item is unpublished')
def step_then(context):
    page: Page = context.page
    page.wait_for_timeout(2000) # Need to give Solr a change to index the change
    page.reload()
    publication_status = page.locator("dd.blacklight-publication_status")
    expect(publication_status).to_contain_text("Unpublished")

    # Cleanup changes
    publish_button = page.get_by_role('button', name="Publish")
    publish_button.click()

