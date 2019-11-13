import os
from unittest import TestCase
from tempfile import TemporaryDirectory, NamedTemporaryFile
from luigi import Task, LocalTarget, IntParameter, build, Parameter
from luigi.mock import MockTarget, MockFileSystem

from csci_utils.luigi.task import Requirement, Requires, TargetOutput

class Luigi_Task_Requires_Test(TestCase):
    def test_Requirement(self):

        class OtherTask(Task):
            def output(self):
                return LocalTarget('words.txt')

            def run(self):
                with self.output().open('w') as f:
                    f.write("foo")

        class MyTask(Task):
            test = Parameter(OtherTask)
            # Replace task.requires()
            requires = Requires()
            other = Requirement(OtherTask)

            def output(self):
                return LocalTarget('test.txt')

            def run(self):
                with self.other.output().open('r') as f:
                    for line in f:
                        print(line)


        build([MyTask()], local_scheduler=True)
        # os.remove('test.txt')
    # def test_Requirement(self):
    #     with TemporaryDirectory() as tmp:
    #
    #         class MockTask(Task):
    #
    #             def output(self):
    #                 return LocalTarget('words.txt')
    #
    #             def run(self):
    #                 with self.output().open('w') as f:
    #                     f.write("foo")
    #
    #         requirementfile = os.path.join(tmp, 'file')
    #
    #         class MyTask(Task):
    #             def requires(self):
    #                 return MockTask()
    #
    #             test = Parameter(MockTask)
    #             _requirement = Requirement(MockTask)
    #
    #             def run(self):
    #                 print(self._requirement())
    #     build([MyTask()], local_scheduler=True)


    # def test_target_output(self):
    #     with TemporaryDirectory() as tmp:
    #         outputfilename = os.path.join(tmp, 'file')
    #         class SomeTask(Task):
    #             output = TargetOutput(file_pattern=outputfilename, ext=".csv")
    #
    #             def run(self):
    #                     if self.output().path == outputfilename + ".csv":
    #                         return True
    #                     else:
    #                         raise Exception
    #
    #         build([SomeTask()], local_scheduler=True)





