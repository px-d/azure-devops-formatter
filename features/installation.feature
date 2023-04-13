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
        "templates": {
          "list": "{{#steps}}{{.}}{{/steps}}",
          "prettify": "<h3>Scenario: {{ scenario_name }}</h3>Error: {{ error_type }}<br>Log:<br><fontⶩcolor='red'>{{ traceback }}</font>",
          "table": "<table><tr>{{#headings}}<th>{{.}}</th>{{/headings}}</tr>{{#rows}}<tr>{{#.}}<td>{{.}}</td>{{/.}}</tr>{{/rows}}</table>"
        }
      }
      """
    When I run the example tests
    Then a new ticket will be created