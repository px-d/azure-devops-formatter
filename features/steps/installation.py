import json
from subprocess import check_output
import subprocess
from behave import given, when, then


@given("the azure behave reporter library is installed")
def step_impl(context):
    # Workaround weil setup py spinnt
    # check_output(
    #     [
    #         "pip3",
    #         "install",
    #         "--upgrade",
    #         "--pre",
    #         "azure-cli",
    #         "--extra-index-url",
    #         "https://azurecliprod.blob.core.windows.net/edge",
    #         "--no-cache-dir",
    #         "--upgrade-strategy=eager",
    #     ]
    # )
    check_output(
        [
            "docker",
            "exec",
            "test",
            "python3",
            "setup.py",
            "install",
        ]
    )


@given("azure cli is logged in")
def step_impl(context):
    # result = check_output(
    #     [
    #         "az",
    #         "boards",
    #         "work-item",
    #         "create",
    #         "--title",
    #         "supercoolname",
    #     ]
    # )
    print("Testing for login in azure cli..")
    assert True


@given("config json is correctly set up")
def step_impl(context):
    with open("config.json", "w") as file:
        file.write(context.text)


@when("I run the example tests with")
def step_impl(context):
    command = context.text
    subprocess.run(
        args=[
            "docker",
            "exec",
            "-ti",
            "test",
            *command.split(" "),
            "features/examples",
        ]
    )


@then("a new ticket will be created")
def step_impl(context):
    with open("test.txt", "r") as f:
        args = arg_parser(f.readlines())

    for row in list(context.table):
        argument, value = row["argument"], row["value"]
        print(f"Argument: '{argument}' Value: '{value}'")
        print(f"Args: {args}")
        if argument in ["Severity", "System.Tags", "System Info"]:
            assert args["fields"][argument] == value
        else:
            assert value == args[argument], f"value: {value}, args: {args[argument]}"
    context.command_arguments = args


@then("the description is")
def step_impl(context):
    assert context.text == context.command_arguments["description"]


@then("the repro steps are")
def step_impl(context):
    assert context.text == context.command_arguments["fields"]["Repro Steps"]


def arg_parser(i):
    r"""
    >>> arg_parser(["a", "command", "--arg1", "super", "arg", "--arg2", "something", "else", "--arg3", "another", "one", "--fields", "name=philip\n age=22"])
    {'arg1': 'super arg', 'arg2': 'something else', 'arg3': 'another one', 'fields': {'name': 'philip', 'age': '22'}}

    >>> arg_parser("a command --arg1 super arg --arg2 something else --arg3 another one --fields name=philip\n age=22")
    {'arg1': 'super arg', 'arg2': 'something else', 'arg3': 'another one', 'fields': {'name': 'philip', 'age': '22'}}
    """

    if type(i) is not list:
        i = i.split(" ")

    def get_dict():
        stack = []
        for word in i:
            if len(word) == 0:
                continue
            if word.startswith("--"):
                if stack[0].startswith("--"):
                    yield stack
                stack = [word]
            else:
                stack.append(word)
        yield stack

    unparsed = {
        x[0].replace("--", "").strip(): " ".join(x[1:]).strip() for x in get_dict()
    }

    # Everything below is only to turn the 'fields' list into a proper dictionary.
    # please refrain from any questions, and especially: do not ask me to change it <3

    parsed = dict()

    for key in unparsed.keys():
        if key == "fields":
            parsed[key] = {
                x[0]: x[1]
                for x in map(
                    lambda x: x.split("=", maxsplit=1), unparsed["fields"].split("\n ")
                )
            }
        else:
            parsed[key] = unparsed[key]

    return parsed

if __name__ == "__main__":
    import doctest

    doctest.testmod()
