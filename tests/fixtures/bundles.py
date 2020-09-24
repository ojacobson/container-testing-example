import pytest

@pytest.fixture
def bundles(bundle_maker, bundle_server):
    return Bundles(bundle_maker, bundle_server)

class Bundles:
    def __init__(self, bundle_maker, bundle_server):
        self._bundle_maker = bundle_maker
        self._bundle_server = bundle_server

    def make_bundle_with_output(self, name, *, stdout):
        bundle = self._bundle_maker.stdout_bundle(stdout=stdout.encode())
        self._bundle_server.register(name, bundle=bundle)

    def make_bundle_with_program(self, name, *, program):
        bundle = self._bundle_maker.program_bundle(program=program)
        self._bundle_server.register(name, bundle=bundle)
