from __future__ import annotations

import typing

try:
    import mapbox_vector_tile
    HAS_MVT = True
except ImportError:
    HAS_MVT = False

from ..base import BaseCodec, BaseFileIterable


class MVTIterable(BaseFileIterable):
    datamode = 'binary'

    def __init__(self, filename: str = None, stream: typing.IO = None, codec: BaseCodec = None,
                 mode: str = 'r', options: dict = None):
        if options is None:
            options = {}
        if not HAS_MVT:
            raise ImportError("MVT support requires 'mapbox-vector-tile' package")
        
        self.options = options
        super().__init__(filename, stream, codec=codec, binary=True, mode=mode, options=options)
        self.reset()

    def reset(self):
        """Reset iterable"""
        super().reset()
        self.pos = 0
        if self.mode == 'r':
            # Read tile data
            tile_data = self.fobj.read()
            
            # Decode MVT
            try:
                self.decoded = mapbox_vector_tile.decode(tile_data)
            except Exception as e:
                raise ValueError(f"Failed to decode MVT data: {e}")
            
            self.iterator = self.__iterator()
        else:
            raise NotImplementedError("MVT writing not yet supported")

    def __iterator(self):
        """Iterator for reading MVT features"""
        # MVT structure: {layer_name: {'features': [...], ...}}
        # We'll flatten all features from all layers
        for layer_name, layer_data in self.decoded.items():
            features = layer_data.get('features', [])
            for feature in features:
                # Add layer name to each feature
                feature_dict = {
                    'layer': layer_name,
                    'geometry': feature.get('geometry'),
                    'properties': feature.get('properties', {}),
                    'type': feature.get('type'),
                    'id': feature.get('id')
                }
                yield feature_dict

    @staticmethod
    def id() -> str:
        return 'mvt'

    @staticmethod
    def is_flatonly() -> bool:
        return False

    @staticmethod
    def has_totals():
        return True

    def totals(self):
        if hasattr(self, 'decoded'):
            total = 0
            for layer_data in self.decoded.values():
                total += len(layer_data.get('features', []))
            return total
        return 0

    def close(self):
        super().close()

    def read(self) -> dict:
        row = next(self.iterator)
        self.pos += 1
        return row

    def read_bulk(self, num: int = 10) -> list[dict]:
        chunk = []
        for _n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk
