import csv
import pytest
import zipfile
from playwright.sync_api import BrowserContext, Page, expect

@pytest.fixture()
def auth_context(browser):
    return browser.new_context(storage_state = "playwright/.auth/storage_state.json")

class TestPublicationWorkflow:
    def test_a_published_and_visible_item_appears_in_Digital_Collections_PUI_search_results_and_OAIPMH_queries_and_its_public_detail_page_may_be_accessed(self, auth_context):
        published_and_visible_item_url_archelon = 'https://archelon-test.lib.umd.edu/catalog/https:%2F%2Ffcrepo-test.lib.umd.edu%2Ffcrepo%2Frest%2Fdc%2F2024%2F1%2F47%2F94%2Faf%2Fc8%2F4794afc8-474b-469c-9aee-5e659e75bf36'
        handle = '1903.1/3843'
        search_term = 'High School, Seaford, Delaware'

        page:Page = auth_context.new_page()
        page.goto(published_and_visible_item_url_archelon)

        assert handle in page.content()

        publication_status = page.locator("dd.blacklight-publication_status")
        assert publication_status.inner_text() == 'Published'

        visibility = page.locator("dd.blacklight-visibility")
        assert visibility.inner_text() == 'Visible'

        page.close()

        digital_collections_url = 'https://digital.lib.umd.edu/resultsnew'
        page:Page = auth_context.new_page()
        page.goto(digital_collections_url)

        search_box = page.get_by_role('textbox', name="Query")
        search_box.fill(search_term)

        search_button = page.get_by_role('button', name='Search')

        search_button.click()

        search_link = page.locator("//div/a[text()='High School, Seaford, Delaware']")
        search_link.click()

        assert f"{handle}" in page.content()
        page.close()


    def test_publish_button_on_the_items_detail_page_means_the_item_is_in_the_unpublished_state(self, auth_context):
        unpublished_page_url = 'https://archelon-test.lib.umd.edu/catalog/https:%2F%2Ffcrepo-test.lib.umd.edu%2Ffcrepo%2Frest%2Fdc%2F2024%2Ftest%2Fd3%2Ff9%2F90%2F91%2Fd3f99091-0e27-4fd6-87e2-5283ea7b8add'
        page = auth_context.new_page()
        page.goto(unpublished_page_url)

        publish_button = page.get_by_role('button', name='Publish', exact=True)
        expect(publish_button).to_be_visible()

        publication_status = page.locator("dd.blacklight-publication_status")
        assert publication_status.inner_text() == 'Unpublished'
        page.close()

    def test_unpublish_button_on_the_items_detail_page_means_the_item_is_in_the_published_state(self, auth_context):
        unpublished_page_url = 'https://archelon-test.lib.umd.edu/catalog/https:%2F%2Ffcrepo-test.lib.umd.edu%2Ffcrepo%2Frest%2Fdc%2F2024%2F1%2F39%2Fcb%2F45%2Fc7%2F39cb45c7-9ec7-4e2a-82e3-dda1e958380d'
        page = auth_context.new_page()
        page.goto(unpublished_page_url)
        publish_button = page.get_by_role('button', name='Unpublish', exact=True)
        expect(publish_button).to_be_visible()

        publication_status = page.locator("dd.blacklight-publication_status")
        assert publication_status.inner_text() == 'Published'
        page.close()

class TestPresentationSet:
    def test_users_can_see_the_changes_made_in_the_exported_spreadsheet(self, auth_context, tmp_path):
        # Given the URL of an item in a presentation set
        page_url = 'https://archelon-test.lib.umd.edu/catalog/https:%2F%2Ffcrepo-test.lib.umd.edu%2Ffcrepo%2Frest%2Fdc%2F2024%2F1%2Fa2%2F5e%2F9a%2Fbf%2Fa25e9abf-a0f4-4b9e-919f-6df7c718e996'

        page:Page = auth_context.new_page()
        page.goto(page_url)
        presentation_set = page.locator("dd.blacklight-presentation_set_label")
        expect(presentation_set).to_contain_text("Test Presentation Set")


        # When the item is exported as a CSV file
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

        download_filepath = tmp_path / download.suggested_filename
        download.save_as(download_filepath)

        # Then the exported Zip file contains a CSV file with PUBLISH, HIDDEN, and Presentation Set columns
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
        page.goto(page_url)
        select_item_checkbox = page.locator("input.toggle_bookmark")
        if select_item_checkbox.is_checked():
            select_item_checkbox.click()

        # TODO Remove temporary file download
