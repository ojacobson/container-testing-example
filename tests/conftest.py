import pytest

from fixtures.bundle_maker import *
from fixtures.bundle_server import *
from fixtures.bundles import *
from fixtures.container_engine import *
from fixtures.containers import *
from fixtures.programs import *

def pytest_addoption(parser):
    parser.addoption(
        "--container-version",
        action="store",
        default="latest",
        help="container version under test",
    )

@pytest.fixture
def container_version(request):
    return request.config.getoption("--container-version")

@pytest.fixture
def container_tag(container_version):
    return f'botanist:{container_version}'
