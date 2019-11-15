import os
from unittest import TestCase
from tempfile import TemporaryDirectory
from luigi import Task, LocalTarget, build

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
            requires = Requires()
            other = Requirement(OtherTask)

            def run(self):
                z = MyTask.requires.__call__(self)
                requirement_taskname = z.get("other")
                assert type(requirement_taskname) == OtherTask

        build([MyTask()], local_scheduler=True)


    def test_target_output(self):
        with TemporaryDirectory() as tmp:
            outputfilename = os.path.join(tmp, 'file')
            class SomeTask(Task):
                output = TargetOutput(file_pattern=outputfilename, ext=".csv")

                def run(self):
                        if self.output().path == outputfilename + ".csv":
                            return True
                        else:
                            raise Exception

            build([SomeTask()], local_scheduler=True)





