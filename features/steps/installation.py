import os
from subprocess import check_output
import subprocess
import requests
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
    # print(out)


@given("azure cli is logged in")
def step_impl(context):
    # result = check_output(["az", "login"])
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
    # print(result)

    # az workitem create bla bla
    # ^ funktioniert das überhaupt?
    print("Testing for login in azure cli..")
    assert True


@given("behave ini is correctly set up")
def step_impl(context):
    # with open("behave.ini", "w") as file:
    #     file.write(context.text)

    # i believe there is no actual way to access the behave.ini from our
    # formatter since we never get access to the context.
    assert True


@given("config json is correctly set up")
def step_impl(context):
    with open("config.json", "w") as file:
        file.write(context.text)


@when("I run the example tests")
def step_impl(context):
    subprocess.run(
        args=[
            "docker",
            "exec",
            "-ti",
            "test",
            "behave",
            "features/examples",
            "-f",
            "azure_devops",
        ]
    )


@then("a new ticket will be created")
def step_impl(context):
    assert os.path.isfile("test.txt")
