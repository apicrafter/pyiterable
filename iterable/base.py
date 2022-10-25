# -*- coding: utf-8 -*-
ITERABLE_TYPE_STREAM = 10
ITERABLE_TYPE_FILE = 20
ITERABLE_TYPE_CODEC = 30
DEFAULT_BULK_NUMBER = 100

import io


class BaseCodec:
    """Basic codec class"""
    def __init__(self, filename=None, fileobj=None, mode='r', open_it=False):
        self._fileobj = fileobj
        self.filename = filename
        self.mode = mode
        if open_it:
            self.open()
        pass

    @staticmethod
    def fileexts():
        raise NotImplementedError
    

    def reset(self):
        self._fileobj.seek(0)

    def open(self):
        raise NotImplementedError
 
    def fileobj(self):
        return self._fileobj
    
    def close(self):
        raise NotImplementedError

    def textIO(self, encoding='utf8'):
        """Return text wrapper over binary stream"""
        return io.TextIOWrapper(self.fileobj(), encoding=encoding, write_through=True)


class BaseIterable:
    """Base iterable data class"""
    def __init__(self):
        pass

    def reset(self):
        """Reset iterator"""
        raise NotImplementedError

    @staticmethod
    def id():
        """Identifier of selected destination"""
        raise NotImplementedError

    def read(self, skip_empty=True):
        """Read single record"""
        raise NotImplementedError

    def read_bulk(self, num=DEFAULT_BULK_NUMBER):
        """Read multiple records"""
        raise NotImplementedError

    @staticmethod
    def is_flatonly():
        """Is source flat by only. Default: False"""
        return False

    def is_flat(self):
        """Is source flat. Default: """ 
        if self.__class__().is_flatonly():
            return True
        raise NotImplementedError

    def is_streaming(self):
        """Is source streaming. Default: False"""
        return False

    def __next__(self):
        return self.read()

    def __iter__(self):
        self.reset()
        return self

    def write(self, rec):
        """Write single record"""
        raise NotImplementedError

    def write_bulk(self, records):
        """Write multiple records"""
        raise NotImplementedError


class BaseFileIterable(BaseIterable):
    """Basic file iterable"""
    datamode = 'text'

    def __init__(self, filename=None, stream=None, codec=None, binary=False, encoding='utf8', noopen=False, mode='r'):
        """Init basic file iterable"""
        self.filename = filename
        self.noopen = noopen
        self.encoding = encoding
        self.binary = binary
        self.mode = mode
        self.codec = codec
        if stream is not None:
            self.stype = ITERABLE_TYPE_STREAM
        elif filename is not None:
            self.stype = ITERABLE_TYPE_FILE
        elif codec is not None:
            self.stype = ITERABLE_TYPE_CODEC
        self.fobj = None

        if self.stype == ITERABLE_TYPE_FILE:
            if not noopen:                
                self.open()
        elif self.stype == ITERABLE_TYPE_STREAM:
            self.fobj = stream
        elif self.stype == ITERABLE_TYPE_CODEC:
            if not noopen:                
                self.fobj = self.codec.open() 
                if self.datamode == 'text':
                    self.fobj = self.codec.textIO(encoding=self.encoding) 
                  

    def open(self):
        """Open file as file data source"""
        if self.stype ==  ITERABLE_TYPE_FILE:
            self.fobj = open(self.filename, self.mode + 'b') if self.binary else open(self.filename, self.mode, encoding=self.encoding)
            return self.fobj
        else:
            raise NotImplementedError
	

    def reset(self):
        """Reset file using seek(0)"""
        if self.stype == ITERABLE_TYPE_FILE:
            if self.fobj is not None:
                self.fobj.seek(0)
        elif self.stype == ITERABLE_TYPE_CODEC:
            if self.fobj is not None and self.mode not in ['w', 'wb']:
                self.fobj.seek(0)
#            self.codec.reset()

    def close(self):
        """Close file as file data source"""
        if self.stype == ITERABLE_TYPE_FILE:
            if self.fobj is not None:
                self.fobj.close()
        elif self.stype == ITERABLE_TYPE_CODEC:
            if self.codec is not None:
                self.codec.close()
