import atexit
from contextlib import suppress
from datetime import timedelta
import json
import os
from subprocess import check_output
from subprocess import CalledProcessError
import time

import requests
from features.support.assertion import assert_eventually

from sut import SUT

from wiremock import wiremock


def before_all(context):
    # docker network create my-network
    # docker run --network=my-network my-container
    try:
        check_output(["docker", "network", "rm", "reporter_test"])
    except:
        pass
    check_output(["docker", "network", "create", "reporter_test"])

    def start_wiremock(port):
        sut = SUT(
            [
                "docker",
                "run",
                "--network",
                "reporter_test",
                "--name",
                "wiremock",
                "--rm=true",
                f"-p={port}:8080",
                "wiremock/wiremock:2.34.0",
                "--https-port",
                "443",
                "--verbose",
            ]
        )
        sut.start(quiet="verbose" not in os.environ)
        atexit.register(sut.stop)

    start_wiremock(9000)
    assert_eventually(
        lambda: requests.get(
            "http://localhost:9000/__admin/mappings"
        ).raise_for_status(),
        timeout=timedelta(seconds=10),
    )

    context.azure_mock = wiremock("http://localhost:9000", "maps", "requests", "count")

    network_ip = json.loads(
        check_output(["docker", "container", "inspect", "wiremock"])
    )[0]["NetworkSettings"]["Networks"]["reporter_test"]["IPAddress"]
    
    check_output(
        [
            "docker",
            "run",
            "-d",
            "-ti",
            "--rm=true",
            "--name",
            "test",
            "--network",
            "reporter_test",
            "--volume",
            f"{os.getcwd()}:/work",
            "--volume",
            f"{os.getcwd()}/az:/bin/az",
            "-w",
            "/work",
            "--add-host",
            f"dev.azure.com:{network_ip}",  # TODO: Change to something useful :^)
            "--add-host",
            f"login.microsoftonline.com/organizations/oauth2/v2.0/authorize:{network_ip}",
            "python:3.10.10-alpine3.17",
            "sleep",
            "infinity",
        ]
    )

    def stop_docker():
        with suppress(CalledProcessError):
            check_output(["docker", "stop", "test"])

    def remove_network():
        with suppress(CalledProcessError):
            check_output(["docker", "network", "rm", "reporter_test"])

    atexit.register(stop_docker)
    atexit.register(remove_network)

    # Ticket Creation:
    # context.azure_mock.maps.add.get("/**").json({"token": "abc123"})

    # print("Token: ", requests.get("http://dev.azure.com/token").json())


# $ pip3 install --upgrade --pre azure-cli --extra-index-url https://azurecliprod.blob.core.windows.net/edge --no-cache-dir --upgrade-strategy=eager

# docker run --rm=true --name test --volume $(pwd):/work -w /work -ti python:3.10 sleep infinity
