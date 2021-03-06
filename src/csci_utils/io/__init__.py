# You can import and rename things to work with them internally,
# without exposing them publicly or to avoid naming conflicts!
from atomicwrites import atomic_write as _backend_writer
from atomicwrites import AtomicWriter
from atomicwrites import DEFAULT_MODE
from contextlib import contextmanager
import os
import io
import tempfile

# You probably need to inspect and override some internals of the package
class SuffixWriter(AtomicWriter):
    def get_fileobject(self, suffix="", prefix=tempfile.template, dir=None, **kwargs):
        """override the get_fileobject function to ensure suffix is maintained
		inheritance is used so all functionality of AtomicWriter is maintained"""
        root, ext = os.path.splitext(self._path)
        if dir is None:
            dir = os.path.normpath(os.path.dirname(self._path))
        descriptor, name = tempfile.mkstemp(suffix=ext, prefix=prefix, dir=dir)
        # io.open() will take either the descriptor or the name, but we need
        # the name later for commit()/replace_atomic() and couldn't find a way
        # to get the filename from the descriptor.
        os.close(descriptor)
        kwargs["mode"] = self._mode
        kwargs["file"] = name
        return io.open(**kwargs)


@contextmanager
def atomic_write(path, writer_cls=SuffixWriter, **cls_kwargs):
    """overrides the atomic_write function to use modified SuffixWriter writer_cls"""
    with _backend_writer(path, writer_cls=SuffixWriter, **cls_kwargs) as f:
        # Don't forget to handle the as_file logic!
        yield f
