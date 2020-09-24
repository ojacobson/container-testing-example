import posixpath
import pytest

@pytest.fixture
def programs():
    return Programs()

@pytest.fixture
def environment_probe(programs):
    return programs.environment_probe_program()

class Programs:
    def __init__(self):
        pass

    def stdout_program(self, stdout):
        return StdoutProgram(stdout)

    def environment_probe_program(self):
        return EnvironmentProbeProgram()

class Program:
    files = []

class File:
    @classmethod
    def new(cls, path, content, mode):
        return cls(path, content, mode)

    def __init__(self, path, content, mode):
        self.path = path
        self.content = content
        self.mode = mode

    def with_prefix(self, prefix):
        path = posixpath.join(prefix, self.path)
        return self.new(path, self.content, self.mode)

class StdoutProgram(Program):
    def __init__(self, stdout):
        self.files = [
            File('stdout', stdout, 0o644),
            File('run', self.script, 0o755),
        ]

    script = b'''#!/bin/bash -e
cat stdout
'''

class EnvironmentProbeProgram(Program):
    script = b'''#!/bin/bash -e

if grep BUNDLE_URL /proc/*/environ; then
    exit 1
fi
'''

    files = [
        File('run', script, 0o755),
    ]