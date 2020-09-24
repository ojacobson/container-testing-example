import pytest
import socket
import uuid

@pytest.fixture
def bundle_server(httpserver):
    return BundleServer(httpserver)

# The HTTP server used to make this all work needs to be visible inside of the
# Docker container running on this host, and not just on this host. Using this
# host's FQDN at least works well on a Mac, where Docker's DNS asks the Mac, and
# the Mac will respond positively to its own FQDN regardless of its own DNS
# configuration.
#
# The port 9000 is a meaningless number.
@pytest.fixture
def httpserver_listen_address():
    return (socket.getfqdn(), 9000)

class BundleServer:
    def __init__(self, httpserver):
        self.bundle_ids = dict()
        self.httpserver = httpserver

    def register(self, name, bundle):
        bundle_id = str(uuid.uuid4)
        self.bundle_ids[name] = bundle_id

        self.httpserver.expect_request(
            self.path_for(name),
            method='GET',
        ).respond_with_data(
            bundle.encode(),
        )

    def id_for(self, name):
        return self.bundle_ids[name]

    def path_for(self, name):
        id = self.id_for(name)
        return f'/bundles/{id}'

    def url_for(self, name):
        path = self.path_for(name)
        return self.httpserver.url_for(path)
