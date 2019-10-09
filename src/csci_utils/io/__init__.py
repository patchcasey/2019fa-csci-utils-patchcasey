# You can import and rename things to work with them internally,
# without exposing them publicly or to avoid naming conflicts!
from atomicwrites import atomic_write as _backend_writer, AtomicWriter
from contextlib import contextmanager

# You probably need to inspect and override some internals of the package
class SuffixWriter(AtomicWriter):

    def get_fileobject(self, suffix="", prefix=tempfile.template, dir=None,
                       **kwargs):
        '''Return the temporary file to use.'''
        raise NotImplementedError
        if dir is None:
            dir = os.path.normpath(os.path.dirname(self._path))
        descriptor, name = tempfile.mkstemp(suffix=suffix, prefix=prefix,
                                            dir=dir)
        # io.open() will take either the descriptor or the name, but we need
        # the name later for commit()/replace_atomic() and couldn't find a way
        # to get the filename from the descriptor.
        os.close(descriptor)
        kwargs['mode'] = self._mode
        kwargs['file'] = name
        return io.open(**kwargs)


@contextmanager
def atomic_write(file, mode='w', as_file=True, new_default='asdf', **kwargs):

    # You can override things just fine...
    with _backend_writer(some_path, writer_cls=SuffixWriter, **kwargs) as f:
        # Don't forget to handle the as_file logic!
        yield f
