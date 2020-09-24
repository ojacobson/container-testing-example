import io
import posixpath
import pytest
import tarfile

@pytest.fixture
def bundle_maker(programs):
    return BundleMaker(programs)

class BundleMaker():
    def __init__(self, programs):
        self._programs = programs

    def stdout_bundle(self, *, stdout):
        program = self._programs.stdout_program(stdout)
        return self.program_bundle(program=program)

    def program_bundle(self, *, program):
        return self.bundle(*program.files)

    def bundle(self, *files):
        files = [f.with_prefix('app') for f in files]
        return Archive.with_files(*files)

class Archive:
    @classmethod
    def with_files(cls, *files):
        archive = cls()
        for file in files:
            archive.add_file(file.path, file.content, file.mode)
        return archive

    def __init__(self):
        self.paths = set()
        self.entries = list()

    def add_directory(self, path, mode):
        prefix, name = posixpath.split(path)
        if prefix != '' and prefix not in self.paths:
            self.add_directory(prefix, mode)

        header = tarfile.TarInfo(path)
        header.type = tarfile.DIRTYPE
        header.uid = header.gid = 1000
        header.uname = header.gname = 'app'
        header.mode = mode

        entry = Entry(header, None)

        self.paths.add(path)
        self.entries.append(entry)

    def add_file(self, path, body, mode):
        prefix, name = posixpath.split(path)
        if prefix != '' and prefix not in self.paths:
            self.add_directory(prefix, self.directory_mode(mode))

        header = tarfile.TarInfo(path)
        header.type = tarfile.REGTYPE
        header.size = len(body)
        header.uid = header.gid = 1000
        header.uname = header.gname = 'app'
        header.mode = mode

        entry = Entry(header, body)

        self.paths.add(path)
        self.entries.append(entry)

    def encode(self):
        buffer = io.BytesIO()
        with tarfile.open(mode='w:gz', fileobj=buffer) as archive:
            for entry in self.entries:
                archive.addfile(entry.tarinfo, io.BytesIO(entry.content))
        return buffer.getvalue()

    def directory_mode(self, file_mode):
        r_bits = file_mode & 0o444
        x_bits = r_bits >> 2
        return file_mode | x_bits

class Entry:
    def __init__(self, tarinfo, content):
        self.tarinfo = tarinfo
        self.content = content
