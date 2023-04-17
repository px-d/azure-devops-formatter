# Azure Devops direct BugReport creation for behave

Config Example:

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

> Note: The `ⶩ` char in templates > prettify is very important since this character helps the html being translated properly

### Severity (whitespace is important):

- 1 = low
- 2 = medium
- 3 = high
