Feature: Installation

  Scenario: Install from pypi
    Given the azure behave reporter library is installed
    And azure cli is logged in
    And behave ini is correctly set up
      """
      [behave.formatters]
      azure_devops = azure_devops_formatter:AzureFormatter

      [behave.userdata]
      orga_id = hello123
      project_id = abcdefg
      """
    And config json is correctly set up
      """
      {
      "orga_id": "hello123",
      "project_id": "abcdefg",
      }
      """
    When I run the example tests
    Then a new ticket will be created