from __future__ import annotations
import typing
try:
    import h5py
    HAS_H5PY = True
except ImportError:
    HAS_H5PY = False

from ..base import BaseFileIterable, BaseCodec


class HDF5Iterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', dataset_path:str='/data', options:dict={}):
        if not HAS_H5PY:
            raise ImportError("HDF5 support requires 'h5py' package")
        if dataset_path is None and 'dataset_path' in options:
            dataset_path = options['dataset_path']
        self.dataset_path = dataset_path
        super(HDF5Iterable, self).__init__(filename, stream, codec=codec, binary=True, mode=mode, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(HDF5Iterable, self).reset()
        self.pos = 0
        if self.mode == 'r':
            # HDF5 requires file path or file-like object
            if self.filename:
                self.h5file = h5py.File(self.filename, 'r')
            else:
                # Try to use file object if it has a name
                if hasattr(self.fobj, 'name'):
                    self.h5file = h5py.File(self.fobj.name, 'r')
                else:
                    raise ValueError("HDF5 file reading requires filename or named file object")
            
            if self.dataset_path in self.h5file:
                self.dataset = self.h5file[self.dataset_path]
                self.iterator = self.__iterator()
            else:
                raise ValueError(f"Dataset path '{self.dataset_path}' not found in HDF5 file")
        else:
            if self.filename:
                self.h5file = h5py.File(self.filename, 'w')
            else:
                raise ValueError("HDF5 file writing requires filename")

    def __iterator(self):
        """Iterator for reading HDF5 dataset"""
        # HDF5 datasets are typically arrays/tables
        if len(self.dataset.shape) == 1:
            # 1D array - treat as single column
            for i in range(len(self.dataset)):
                yield {self.dataset_path.split('/')[-1]: self.dataset[i]}
        elif len(self.dataset.shape) == 2:
            # 2D array - treat as table
            if hasattr(self.dataset, 'dtype') and self.dataset.dtype.names:
                # Structured array
                for row in self.dataset:
                    yield {name: row[name] for name in self.dataset.dtype.names}
            else:
                # Regular 2D array
                for i in range(self.dataset.shape[0]):
                    yield {f'col_{j}': self.dataset[i, j] for j in range(self.dataset.shape[1])}
        else:
            raise ValueError("HDF5 dataset must be 1D or 2D for iteration")

    @staticmethod
    def id() -> str:
        return 'hdf5'

    @staticmethod
    def is_flatonly() -> bool:
        return True

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True

    def totals(self):
        """Returns file totals"""
        if hasattr(self, 'dataset'):
            if len(self.dataset.shape) >= 1:
                return self.dataset.shape[0]
        return 0

    def close(self):
        """Close HDF5 file"""
        if hasattr(self, 'h5file'):
            self.h5file.close()
        super(HDF5Iterable, self).close()

    def read(self) -> dict:
        """Read single HDF5 record"""
        row = next(self.iterator)
        self.pos += 1
        return row

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk HDF5 records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single HDF5 record"""
        self.write_bulk([record, ])

    def write_bulk(self, records:list[dict]):
        """Write bulk HDF5 records"""
        if not hasattr(self, 'dataset') or self.dataset is None:
            # Create dataset on first write
            if records:
                keys = list(records[0].keys())
                dtype = [(key, type(records[0][key]).__name__) for key in keys]
                max_len = len(records)
                self.dataset = self.h5file.create_dataset(
                    self.dataset_path,
                    shape=(max_len,),
                    dtype=dtype,
                    maxshape=(None,)
                )
        
        start_idx = self.pos if hasattr(self, 'pos') else 0
        for i, record in enumerate(records):
            if hasattr(self.dataset, 'dtype') and self.dataset.dtype.names:
                # Structured array
                self.dataset[start_idx + i] = tuple(record.values())
            else:
                # Need to handle differently
                raise NotImplementedError("Writing to non-structured HDF5 datasets not yet supported")
