from behave import given, when, then


@given("an innocent step in background")
def background(context):
    assert True


@given('this steps outputs "{message}"')
def step_impl(context, message):
    print(message)


@when("this step fails")
def step_impl(context):
    assert False


@then("not reached here")
def a(context):
    import sys

    sys.exit(-1)
