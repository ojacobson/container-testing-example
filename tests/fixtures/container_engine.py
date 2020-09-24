import docker as d
import pytest

@pytest.fixture
def container_engine(docker, container_tag):
    engine = ContainerEngine(docker, container_tag)
    try:
        yield engine
    finally:
        engine.cleanup()

@pytest.fixture
def docker():
    return d.from_env()

class ContainerEngine:
    def __init__(self, docker, container_tag):
        self.docker = docker
        self.container_tag = container_tag
        self.containers = []

    def start_bundle(self, bundle_url):
        env = self.env_for(bundle_url)
        container = Container.start(self.docker, self.container_tag, env)
        self.containers.append(container)
        return container

    def env_for(self, bundle_url):
        return {
            'BUNDLE_URL': bundle_url,
            'BUNDLE_PROGRAM': './run',
        }

    def cleanup(self):
        for container in self.containers:
            container.remove()

class Container:
    @classmethod
    def start(cls, docker, container_tag, env):
        container = docker.containers.run(
            container_tag,
            detach=True,
            tty=True,
            environment=env,
            hostname='botanist',
        )
        return cls(container)

    def __init__(self, container):
        self.container = container
        self.exit_status = None

    def wait(self):
        exit_info = self.container.wait()
        self.exit_status = exit_info['StatusCode']

    def remove(self):
        self.container.remove()

    @property
    def stdout(self):
        return self.container.logs(stdout=True, stderr=False)
