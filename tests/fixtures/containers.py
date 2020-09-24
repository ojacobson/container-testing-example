import pytest

@pytest.fixture
def containers(bundle_server, container_engine):
    return Containers(bundle_server, container_engine)

class Containers:
    def __init__(self, bundle_server, container_engine):
        self._bundle_server = bundle_server
        self._container_engine = container_engine
        self._containers = dict()

    def run_bundle(self, name, *, bundle):
        bundle_url = self._bundle_server.url_for(bundle)
        container = self._container_engine.start_bundle(bundle_url)
        self._containers[name] = container

    def wait_for(self, name):
        container = self._containers[name]
        container.wait()

    def output_of(self, name):
        container = self._containers[name]
        return container.stdout.decode()

    def exit_status_of(self, name):
        container = self._containers[name]
        return container.exit_status
