import json
from subprocess import check_output
import traceback
from behave.model_core import Status
import pystache
from behave.formatter.base import Formatter
from behave import model


class AzureFormatter(Formatter):
    def __init__(self, stream_opener, config):
        super().__init__(stream_opener, config)

        with open("config.json", "r") as f:
            self.config = json.loads(f.read().strip())

    generated_reports = []
    current_scenario = None
    error_step = None
    step_exception = None
    steps = []

    def step(self, step):
        """Before Step"""
        self.steps.append(step)
        callback = step.store_exception_context

        def store_exception_context(exception):
            self.step_exception = dict(
                exception=exception, traceback=traceback.format_exc()
            )

            callback(exception)

        step.store_exception_context = store_exception_context

    def result(self, step):
        """After Step"""
        if self.step_exception is not None:
            # If it is None, the step didn't fail
            # If it is not none, the step failed and the scenario is over --> After Scenario workaround
            self.error_step = step
            print(f"config: {self.config['orga_id']}")
            self.generated_reports.append(
                publish_report(
                    Report(
                        scenario_name=self.current_scenario.name,
                        steps=self.steps,
                        error_type=type(self.step_exception["exception"]),
                        traceback=self.step_exception["traceback"],
                        versions={
                            "youtube": "7.8.2",
                            "github": "1.2.3",
                        },
                    ),
                    config=self.config,
                )
            )

    def scenario(self, scenario):
        print(scenario)
        """Before scenario"""
        self.current_scenario = scenario
        self.error_step = None
        self.steps = []
        self.step_exception = None

    def close(self):
        """After All"""
        for idx, gr in enumerate(self.generated_reports):
            print(gr, idx)
        self.close_stream()


class Report:
    def __init__(
        self, /, scenario_name, steps, error_type, traceback, versions
    ) -> None:
        self.scenario_name = scenario_name
        self.steps = steps
        self.error_type = error_type
        self.traceback = traceback
        self.versions = versions

    def prettify(self, template=None):
        if template is None:
            template = "<h3>Scenario: {{ scenario_name }}</h3>Error: {{ error_type }}<br>Log:<br><fontⶩcolor='red'>{{ traceback }}</font>"
        return (
            pystache.render(
                template,
                scenario_name=self.scenario_name,
                error_type=self.error_type.__name__,
                traceback=self.traceback,
            )
            .replace(" ", "&nbsp;")
            .replace("\n", "<br>")
            .replace("ⶩ", " ")
        )

    def repro_steps(self, template=None):
        repro = []
        for step in self.steps:
            repro.append(f"<li>{step.keyword} {step.name}</li>")
            if step.table:
                repro.append(convert_table(step.table))

        return create_list(content=repro, template=template)

    def get_versions(self, separator=" - "):
        return create_list(
            [f"{k}{separator}{v}" for k, v in self.versions.items()],
            template="{{#steps}}<li>{{.}}</li>{{/steps}}",
        )


def create_list(content, template=None):
    """
    Converts a behave.model.Table into a html table.
    When providing a template make sure to use the 'steps' keyword to access data
    >>> create_list(["A", "B"], template="{{#steps}}<li>{{.}}</li>{{/steps}}")
    '<li>A</li><li>B</li>'
    """
    if template is None:
        template = """{{#steps}}{{.}}{{/steps}}"""
    return (
        pystache.render(
            template,
            steps=content,
        )
        .replace("&lt;", "<")
        .replace("&gt;", ">")
    )


def convert_table(input_table: model.Table):
    """
    >>> convert_table(model.Table(headings=["A", "B"], rows=[["Q", "W"], ["E", "R"]]))
    '<table><tr><th>A</th><th>B</th></tr><tr><td>Q</td><td>W</td></tr><tr><td>E</td><td>R</td></tr></table>'
    """
    template = "<table><tr>{{#headings}}<th>{{.}}</th>{{/headings}}</tr>{{#rows}}<tr>{{#.}}<td>{{.}}</td>{{/.}}</tr>{{/rows}}</table>"
    return pystache.render(
        template,
        headings=input_table.headings,
        rows=[row.cells for row in input_table],
    )


def publish_report(
    bugreport: Report, severity="1 = low", assignee="", tags=None, config=None
):
    """
    Report a bug to Azure DevOps
    bugreport: BugReport object containing the information about the error and where it occurred
    severity: SeverityLevel object containing the severity of the bug (LOW, MEDIUM, HIGH, CRITICAL)
        Convention: '1 = low', '2 = medium', etc.
    assignee: The person you want to associate the bugreport with (either name or email <- please use email ;))
    tags: List of tags to add to the bug report (Automated, Test, Foo, Bar, ...)
    """
    result = check_output(
        [
            "/bin/az",
            "boards",
            "work-item",
            "create",
            "--title",
            bugreport.scenario_name,
            "--assigned-to",
            assignee,
            "--type",
            "Bug",
            "--organization",
            config["orga_id"],
            "--project",
            config["project_id"],
            "--description",
            bugreport.prettify(),
            "--fields",
            f"Severity={severity}",
            f"Repro Steps=<style>table, th, td {{ border: 1px solid black; border-collapse: collapse;}}</style>{bugreport.repro_steps()}",
            f"System.Tags={';'.join(tags if tags else [])}",
            f"System Info={bugreport.get_versions()}",
        ]
    )
    js = json.loads(result.decode())
    bugreport_id = js["id"]
    return f"https://dev.azure.com/vwac/Data%20Collection/_workitems/edit/{bugreport_id}/#/'"


def get_config():
    with open("config.json", "r") as cfg:
        contents = json.loads(cfg.read().strip())
    return contents
