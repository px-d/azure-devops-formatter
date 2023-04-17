# Azure Devops direct BugReport creation for behave


config example:

```json
{
  "orga_id": "hello123",
  "project_id": "abcdefg",
  "report_settings": {
    "severity": "1 = low",
    "tags": ["automated"],
    "assignee": "max@mustermann.de"
  },
  "templates": {
    "list": "{{#steps}}{{.}}{{/steps}}",
    "prettify": "<h3>Scenario: {{ scenario_name }}</h3>Error: {{ error_type }}<br>Log:<br><fontⶩcolor='red'>{{ traceback }}</font>",
    "table": "<table><tr>{{#headings}}<th>{{.}}</th>{{/headings}}</tr>{{#rows}}<tr>{{#.}}<td>{{.}}</td>{{/.}}</tr>{{/rows}}</table>"
  }
}
```