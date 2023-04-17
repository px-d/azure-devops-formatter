Feature: Installation

  Scenario: Install from pypi
    Given the azure behave reporter library is installed
    And azure cli is logged in
    And behave ini is correctly set up
      """
      [behave.formatters]
      azure_devops = azure_devops_formatter:AzureFormatter
      """
    And config json is correctly set up
      """
      {
        "orga_id": "hello123",
        "project_id": "abcdefg",
        "report_settings": {
          "severity": "1 = low"
        }
      }
      """
    When I run the example tests with
      """
      behave -f azure_devops
      """
    Then a new ticket will be created
      | argument     | value                                           |
      | title        | First scenario                                  |
      | assigned-to  |                                                 |
      | type         | Bug                                             |
      | organization | hello123                                        |
      | project      | abcdefg                                         |
      | Severity     | 1 = low                                         |
      | System.Tags  |                                                 |
      | System Info  | <li>youtube - 7.8.2</li><li>github - 1.2.3</li> |

    And the description is
      """
      <h3>Scenario:&nbsp;First&nbsp;scenario</h3>Error:&nbsp;AssertionError<br>Log:<br><font color='red'>Traceback&nbsp;(most&nbsp;recent&nbsp;call&nbsp;last):<br>&nbsp;&nbsp;File&nbsp;&quot;/usr/local/lib/python3.10/site-packages/behave-1.2.6-py3.10.egg/behave/model.py&quot;,&nbsp;line&nbsp;1329,&nbsp;in&nbsp;run<br>&nbsp;&nbsp;&nbsp;&nbsp;match.run(runner.context)<br>&nbsp;&nbsp;File&nbsp;&quot;/usr/local/lib/python3.10/site-packages/behave-1.2.6-py3.10.egg/behave/matchers.py&quot;,&nbsp;line&nbsp;98,&nbsp;in&nbsp;run<br>&nbsp;&nbsp;&nbsp;&nbsp;self.func(context,&nbsp;*args,&nbsp;**kwargs)<br>&nbsp;&nbsp;File&nbsp;&quot;features/examples/steps/example.py&quot;,&nbsp;line&nbsp;16,&nbsp;in&nbsp;step_impl<br>&nbsp;&nbsp;&nbsp;&nbsp;assert&nbsp;False<br>AssertionError<br></font>
      """
    And the repro steps are
      """
      <style>table, th, td { border: 1px solid black; border-collapse: collapse;}</style><li>Given an innocent step in background</li><li>Given this steps outputs &quot;hello&quot;</li><li>When this step fails</li><li>Then not reached here</li>
      """
  Scenario: Install from pypi
    Given the azure behave reporter library is installed
    And azure cli is logged in
    And behave ini is correctly set up
      """
      [behave.formatters]
      azure_devops = azure_devops_formatter:AzureFormatter
      """
    And config json is correctly set up
      """
      {
        "orga_id": "hello123",
        "project_id": "abcdefg",
        "report_settings": {
          "severity": "3 = high"
        }
      }
      """
    When I run the example tests with
      """
      behave -f azure_devops
      """
    Then a new ticket will be created
      | argument | value    |
      | Severity | 3 = high |