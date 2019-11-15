import os
from unittest import TestCase
from tempfile import TemporaryDirectory
from luigi import Task, LocalTarget, build

from csci_utils.luigi.dask.target import ParquetTarget, CSVTarget

class Luigi_Task_Requires_Test(TestCase):
    def test_ParquetTarget(self):
        ...
