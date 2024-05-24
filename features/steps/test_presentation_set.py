import csv
import zipfile

from behave import given, then, when
from playwright.sync_api import expect, Page

@given('the URL of an item in a presentation set')
def step_given(context):
    context.page_url = 'https://archelon-test.lib.umd.edu/catalog/https:%2F%2Ffcrepo-test.lib.umd.edu%2Ffcrepo%2Frest%2Fdc%2F2024%2F1%2Fa2%2F5e%2F9a%2Fbf%2Fa25e9abf-a0f4-4b9e-919f-6df7c718e996'

    page: Page = context.page
    page.goto(context.page_url)
    presentation_set = page.locator("dd.blacklight-presentation_set_label")
    expect(presentation_set).to_contain_text("Test Presentation Set")

@when('the item is exported as a CSV file')
def step_when(context):
    page: Page = context.page

    select_item_checkbox = page.locator("input.toggle_bookmark")
    if not select_item_checkbox.is_checked():
        select_item_checkbox.click()

    selected_items_link = page.locator("a#bookmarks_nav")
    selected_items_link.click()


    export_button = page.get_by_role("link", name="Export")
    export_button.click()

    next_button = page.get_by_role("button", name="Next")
    next_button.click()

    submit_job_button = page.get_by_role("button", name="Submit Job")
    submit_job_button.click()

    most_recent_job_entry = page.locator("tbody tr").first
    job_download_button = most_recent_job_entry.locator("a.btn.btn-sm.btn-success")

    with page.expect_download() as download_info:
        # Perform the action that initiates download
        job_download_button.click()

    download = download_info.value
    download_filepath = "/tmp/" + download.suggested_filename
    download.save_as(download_filepath)
    context.download_filepath = download_filepath
    context.download = download


@then('the exported Zip file contains a CSV file with PUBLISH, HIDDEN, and Presentation Set columns')
def step_then(context):
    download_filepath = context.download_filepath
    archive = zipfile.ZipFile(download_filepath, 'r')
    archive_filenames = archive.namelist()
    metadata_filename = [str for str in archive_filenames if "Item_metadata.csv" in str][0]
    csv_data = archive.read(metadata_filename)
    csv_str = csv_data.decode("utf-8")
    reader = csv.DictReader(csv_str.splitlines())
    fieldnames = reader.fieldnames

    assert 'PUBLISH' in fieldnames
    assert 'HIDDEN' in fieldnames
    assert 'Presentation Set' in fieldnames

    # Undo selected item checkbox
    page: Page = context.page
    page.goto(context.page_url)
    select_item_checkbox = page.locator("input.toggle_bookmark")
    if select_item_checkbox.is_checked():
        select_item_checkbox.click()

    # TODO Remove temporary file download
