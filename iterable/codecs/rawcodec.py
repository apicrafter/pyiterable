from ..base import BaseCodec


class RAWCodec(BaseCodec):
    def __init__(self, filename, mode='r'):
        super(RAWCodec, self).__init__(filename, mode=mode, open_it=open_it)

    def open(self):
        self._fileobj = open(self.filename, self.mode)
        return self._fileobj

    def close(self):
        self._fileobj.close()


    @staticmethod
    def fileexts():
        return None
