import io
import os
from luigi.local_target import LocalTarget, atomic_file
from luigi.format import FileWrapper
from contextlib import contextmanager
from luigi import Task, ExternalTask, Parameter
from luigi.contrib.s3 import S3Target


class suffix_preserving_atomic_file(atomic_file):
    def generate_tmp_path(self, path):
        return path


class BaseAtomicProviderLocalTarget(LocalTarget):
    # Allow some composability of atomic handling
    atomic_provider = atomic_file

    def open(self, mode='r'):
        # leverage super() as well as modifying any code in LocalTarget
        # to use self.atomic_provider rather than atomic_file
        rwmode = mode.replace('b', '').replace('t', '')
        if rwmode == 'w':
            self.makedirs()
            return self.format.pipe_writer(self.atomic_provider(self.path))

        elif rwmode == 'r':
            open = super().open(mode='r')
            with open as o:
                return o

        else:
            raise Exception("mode must be 'r' or 'w' (got: %s)" % mode)

    @contextmanager
    def temporary_path(self):
        # NB: unclear why LocalTarget doesn't use atomic_file in its implementation
        self.makedirs()
        with self.atomic_provider(self.path) as af:
            yield af.tmp_path


class SuffixPreservingLocalTarget(BaseAtomicProviderLocalTarget):
    atomic_provider = suffix_preserving_atomic_file

image_name = "Waluigi.jpeg"
model_name = "udnie.pth"
IMAGE_ROOT = 's3://pset4data/pset_4/images'
MODEL_ROOT = 's3://pset4data/pset_4/saved_models/'
S3_ROOT = 's3://pset4data/'
LOCAL_ROOT = os.path.abspath('data')
SHARED_RELATIVE_PATH = 'saved_models'


class ContentImage(ExternalTask):
    IMAGE_ROOT = IMAGE_ROOT # Root S3 path, as a constant

    # Name of the image
    image = Parameter(image_name)  # Filename of the image under the root s3 path

    def output(self, format):
        if format:
            return S3Target(IMAGE_ROOT + "/" + image_name)  # return the S3Target of the image
        else:
            return S3Target(IMAGE_ROOT + "/" + image_name, format=format.Nop)  # return the S3Target of the image


class SavedModel(ExternalTask):
    MODEL_ROOT = MODEL_ROOT

    model = Parameter(model_name) # Filename of the model

    def output(self, format):
        if format:
            return S3Target(MODEL_ROOT + "/" + model_name) # return the S3Target of the model
        else:
            return S3Target(MODEL_ROOT + "/" + model_name, format=format.Nop)


class DownloadModel(Task):
    S3_ROOT = S3_ROOT
    LOCAL_ROOT = LOCAL_ROOT
    SHARED_RELATIVE_PATH = SHARED_RELATIVE_PATH

    model = Parameter(model_name) #luigi parameter

    def requires(self):
        # Depends on the SavedModel ExternalTask being complete
        # i.e. the file must exist on S3 in order to copy it locally
        return SavedModel()

    def output(self):
        targetpath = os.path.join(os.getcwd(), 'data/')
        target = os.path.join(targetpath, model_name)

        return LocalTarget(target, format=format.Nop)

    def run(self):
        # Use self.output() and self.input() targets to atomically copy
        # the file locally!
        with self.input().open('r') as f:
            result = f.read()
            with self.output().open('w') as outfile:
                outfile.write(result)

class DownloadImage(Task):
    S3_ROOT = S3_ROOT
    LOCAL_ROOT = LOCAL_ROOT
    SHARED_RELATIVE_PATH = SHARED_RELATIVE_PATH

    image = Parameter(image_name) # Luigi parameter

    def requires(self):
        # Depends on the ContentImage ExternalTask being complete
        return ContentImage()

    def output(self):
        targetpath = os.path.join(os.getcwd(), 'data/')
        target = os.path.join(targetpath, image_name)

        return LocalTarget(target, format=format.Nop)

    # TODO - replace with atomicwrite
    def run(self):
        # Use self.output() and self.input() targets to atomically copy
        # the file locally!
        with self.input().open('r') as f:
            result = f.read()
            with self.output().open('w') as outfile:
                outfile.write(result)

