import os
import subprocess
from datetime import timedelta

from assertion import assert_eventually


class SUT:
    """This class allows to start and stop the specified System Under Test."""

    def __init__(self, args):
        self.args = args
        self.p = None

    def start(self, shell=False, timeout=timedelta(seconds=10), quiet=False, environment=None):
        if self.running():
            return

        env = dict(os.environ)
        if environment is not None:
            env.update(environment)

        self.p = subprocess.Popen(  # pylint: disable=consider-using-with
            self.args,
            stdout=subprocess.DEVNULL if quiet else None,
            stderr=subprocess.DEVNULL if quiet else None,
            shell=shell,  # noqa: S602
            env=env,
        )

        def assert_is_running():
            assert self.running(), 'unable to start SUT'

        assert_eventually(assertion=assert_is_running, timeout=timeout)

    def stop(self, timeout=timedelta(seconds=5)):
        if self.running():
            self.p.terminate()
            try:
                self.p.wait(timeout=timeout.total_seconds())
            except subprocess.TimeoutExpired:
                self.p.kill()
                self.p.wait()
        self.p = None

    def running(self):
        if self.p is None:
            return False
        self.p.poll()
        return self.p.returncode is None
