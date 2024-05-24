Feature: Publish Workflow - Display of the publication statuses on the item's detail page

  Scenario: A Published and Visible item appears in Digital Collections PUI search results and OAI-PMH queries, and its public detail page may be accessed.
    Given the URL of a published and visible item
     When we search for the item in the Digital Collections PUI
     Then the item appears in the Digital Collections PUI search results
      And the detail page for the item can be accessed
      And the item appears in OAI-PMH queries

  Scenario: A Published and Hidden item does not appear in Digital Collections PUI search results or OAI-PMH queries, but its public detail may be accessed (provided the user has the direct URL to it)
    Given the URL of a published and hidden item
     When we search for the item in the Digital Collections PUI
     Then the item does not appear in the Digital Collections PUI search results
      But its public detail may be accessed, provided the user has the direct URL to it
      And the item appears in OAI-PMH queries

  Scenario: Publish button on the item's detail page means the item is in the unpublished state.
    Given the URL of an unpublished item
     When we display the item's detail page
     Then a Publish button will be displayed

  Scenario: Unpublish button on the item's detail page means the item is in the published state.
    Given the URL of a published item
     When we display the item's detail page
     Then an Unpublish button will be displayed

  Scenario: Users unpublish a single item using the unpublish button from an item's detail page.
    Given the URL of a published item
     When we display the item's detail page
      And click the Unpublish button
     Then the item is unpublished
