#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `CSCI_Utils` package."""

import os
from tempfile import TemporaryDirectory
from unittest import TestCase
import pandas as pd
import tempfile

from csci_utils.hash_str.hash_str import hash_str, str_to_byte, get_csci_salt
from csci_utils.hash_str import call_getuserid, parquet_conv
from csci_utils.io import atomic_write


class FakeFileFailure(IOError):
    pass


class Main_Tests(TestCase):
    def test_parquet_conv(self):
        """Ensures parquet converter works with 2 filetypes
        and returns correct parquetfile"""
        df = pd.DataFrame({"hashed_id": [1, 2, 3, 4, 5]})
        for x in [".csv", ".xlsx"]:
            tf = tempfile.NamedTemporaryFile(delete=False, dir=os.getcwd(), suffix=x)
            tf.close()
            with open(tf.name) as temp:
                df.to_csv(temp.name + x)
                result = parquet_conv(
                    filename=temp.name, cwd=os.getcwd(), datasourceformat=x
                )
                print(result)
                pd.testing.assert_frame_equal(df, result)


class HashTests(TestCase):
    def setUp(self):
        self.count = 0

    def test_decorator(self):
        """Ensures str_to_byte turns strings into bytes"""

        @str_to_byte
        def a(x, y):
            if isinstance(x, bytes):
                self.count += 1
            if isinstance(y, bytes):
                self.count += 1
            if self.count == 2:
                return "expected result"

        self.assertEqual(a("test", "test"), "expected result")

    def test_basic(self):
        """Ensures hash_str handles the example hashing correctly"""
        self.assertEqual(hash_str("world!", salt="hello, ").hex()[:6], "68e656")

    def test_getcsci(self):
        """Ensure test_getcsci function can return an example environmental variable"""
        os.environ["test_envvar"] = "yes"
        environ_var = get_csci_salt(keyword="test_envvar", convert_to_bytes="no")
        self.assertEqual(environ_var, "yes")


class AtomicWriteTests(TestCase):
    def test_atomic_write(self):
        """Ensure file exists after being written successfully"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with atomic_write(fp) as f:
                assert not os.path.exists(fp)
                tmpfile = f.name
                f.write("asdf")

            assert not os.path.exists(tmpfile)
            assert os.path.exists(fp)

            with open(fp) as f:
                self.assertEqual(f.read(), "asdf")

    def test_atomic_failure(self):
        """Ensure that file does not exist after failure during write"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with self.assertRaises(FakeFileFailure):
                # with self.assertRaises(FakeFileFailure):
                with atomic_write(fp) as f:
                    tmpfile = f.name
                    assert os.path.exists(tmpfile)
                    raise FakeFileFailure

            assert not os.path.exists(tmpfile)
            assert not os.path.exists(fp)

    def test_check_suffix(self):
        """check to make sure file has suffix"""

        file_suffix = ".txt"
        file_name = "asdf"
        full_file_name = file_name + file_suffix

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, full_file_name)

            with atomic_write(fp) as f:
                assert not os.path.exists(fp)
                tmpfile = f.name
                root, ext = os.path.splitext(tmpfile)

        self.assertEqual(ext, file_suffix)

    def test_file_exists(self):
        """Ensure an error is raised when a file exists"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")
            existing_file = open(os.path.join(tmp, "asdf.txt"), "w+")
            existing_file.close()

            with self.assertRaises(FileExistsError):
                with atomic_write(fp) as f:
                    print("Running test...")
                    # assert not os.path.exists(fp)
                    # tmpfile = f.name
