from unittest import TestCase
import os
import io
import tempfile
from csci_utils.luigi import suffix_preserving_atomic_file, SuffixPreservingLocalTarget
from luigi.mock import MockTarget, MockFileSystem
from luigi.format import Nop


class Luigi_Suffix_Tests(TestCase):
    def test_temppath(self):
        _suffix = ".pth"
        pathobj = tempfile.NamedTemporaryFile(suffix=_suffix)
        with pathobj as f:
            x = suffix_preserving_atomic_file(f.name)
            filename, temp_suff = os.path.split(x.path)
            filename, suff = temp_suff.split('.')
            suff = "." + suff
            self.assertEqual(suff, _suffix)

    def test_SuffixPreservingLocalTarget_open_r(self):
        _suffix = ".pth"
        temporary = tempfile.NamedTemporaryFile(suffix=_suffix)
        x = SuffixPreservingLocalTarget(temporary.name)
        print(x.open(mode="r"))
        self.assertIsInstance(x.open(mode="r"), io.TextIOWrapper)

    def test_SuffixPreservingLocalTarget_open_w(self):
        _suffix = ".pth"
        temporary = tempfile.NamedTemporaryFile(suffix=_suffix)
        x = SuffixPreservingLocalTarget(temporary.name)
        self.assertIsInstance(x.open(mode="w"), io.TextIOWrapper)

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
        x = SuffixPreservingLocalTarget(temporary.name)

from csci_utils.luigi import ContentImage, SavedModel, DownloadModel, DownloadImage
from luigi.contrib.s3 import S3Target

class sub_DownloadModel(DownloadModel):
    def __init__(self):
        self.path = path

    def requires(self):
        # _x = tempfile.NamedTemporaryFile(mode="w+b",delete=False)
        # # with _x as temporaryfile:
        # #     temporaryfile.write(b"cool")
        # return _x
        f = S3Target(path = 'test', format=Nop)
        return f

    def output(self):
        _x = tempfile.NamedTemporaryFile(mode="w",delete=False)
        with _x as temporaryfile:
            return temporaryfile

class Luigi_Download_Tests(TestCase):

    def test_S3Targets(self):

        x = ContentImage
        x.IMAGE_ROOT = "test_directory"
        x.image = "testfile.file"

        y = SavedModel
        y.MODEL_ROOT = "test"
        y.model = "test"

        self.assertEqual(type(x.output(self)), S3Target)
        self.assertEqual(type(y.output(self)), S3Target)

    #TODO - implement tests for DownloadImage and DownloadModel
    # my idea here would be to check that Luigi can open and read and write dummy
    # files, however it is very difficult to implement

    # def test_download_data(self):
    #     x = DownloadModel(self)
    #     x.input = sub_DownloadModel.requires(self)
    #     x.output = sub_DownloadModel.output(self)
    #     x.run()



