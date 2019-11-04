from unittest import TestCase
import os
import io
import tempfile
from .target import suffix_preserving_atomic_file, SuffixPreservingLocalTarget
from luigi import Task, format
from luigi.mock import MockTarget, MockFileSystem

class SimpleTask(Task):
    def output(self):
        return MockFile("SimpleTask", mirror_on_stderr=True)

    def run(self):
        _out = self.output().open('w')
        _out.write(u"Hello World!\n")
        _out.close()

class Luigi_Tests(TestCase):
    def test_temppath(self):
        _suffix = ".pth"
        pathobj = tempfile.NamedTemporaryFile(suffix=_suffix)
        with pathobj as f:
            x = suffix_preserving_atomic_file(f.name)
            filename, temp_suff = os.path.split(x.path)
            filename, suff = temp_suff.split('.')
            suff = "." + suff
            self.assertEqual(suff, _suffix)

    def test_SuffixPreservingLocalTarget_open(self):
        _suffix = ".pth"
        temporary = tempfile.NamedTemporaryFile(suffix=_suffix)
        x = SuffixPreservingLocalTarget(temporary.name)
        self.assertIsInstance(x.open(), io.TextIOWrapper)

    def test_SuffixPreservingLocalTarget_temporary_path(self):
        _suffix_list = [".pth", ".npy.gz", ".csv", ".this.that.test.example"]
        test_function = lambda x: x
        for _suffix in _suffix_list:
            temporary = tempfile.NamedTemporaryFile(delete=False, suffix=_suffix)
            x = SuffixPreservingLocalTarget(temporary.name)
            with x.temporary_path() as temp_output_path:
                test_function(temp_output_path)
                assert os.path.exists(temporary.name)
                assert os.path.exists(temp_output_path)
            assert not os.path.exists(temporary.name)
            assert not os.path.exists(temp_output_path)

    def test_SuffixPreservingLocalTarget(self):
        _suffix = ".pth"
        temporary = tempfile.NamedTemporaryFile(suffix=_suffix)
        mockfilesystem = MockFileSystem()
        mocktarget = MockTarget(mockfilesystem)
        print(mocktarget.path)
        x = SuffixPreservingLocalTarget(temporary.name)
        print(x.path)

        # y = x.open(mocktarget.open().name())
        # print(y)
