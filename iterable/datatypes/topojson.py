from __future__ import annotations

import json
import typing

try:
    import topojson
    HAS_TOPOJSON = True
except ImportError:
    HAS_TOPOJSON = False

from ..base import BaseCodec, BaseFileIterable


class TopoJSONIterable(BaseFileIterable):
    def __init__(self, filename: str = None, stream: typing.IO = None, codec: BaseCodec = None,
                 mode: str = 'r', encoding: str = 'utf8', options: dict = None):
        if options is None:
            options = {}
        super().__init__(filename, stream, codec=codec, binary=False, mode=mode, encoding=encoding, options=options)
        self.reset()

    def reset(self):
        """Reset iterable"""
        super().reset()
        self.pos = 0
        if self.mode == 'r':
            # Load TopoJSON document
            try:
                self.fobj.seek(0)
                self.data = json.load(self.fobj)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse TopoJSON: {e}")
            
            # If topojson library is available, convert to GeoJSON
            if HAS_TOPOJSON:
                try:
                    # topojson library provides conversion utilities
                    # We'll extract features from all objects
                    self.features = []
                    objects = self.data.get('objects', {})
                    for obj_name, obj_data in objects.items():
                        # Convert TopoJSON to GeoJSON using the library
                        topo = topojson.Topology(self.data)
                        geojson_data = topo.to_geojson(obj_name)
                        if geojson_data.get('type') == 'FeatureCollection':
                            self.features.extend(geojson_data.get('features', []))
                        else:
                            self.features.append(geojson_data)
                except Exception:
                    # If library conversion fails, fall back to raw data
                    self.features = [self.data]
            else:
                # Without library, just return the raw TopoJSON structure
                self.features = [self.data]
            
            self.iterator = iter(self.features)

    @staticmethod
    def id() -> str:
        return 'topojson'

    @staticmethod
    def is_flatonly() -> bool:
        return False

    @staticmethod
    def has_totals():
        return True

    def totals(self):
        if hasattr(self, 'features'):
            return len(self.features)
        return 0

    def read(self) -> dict:
        feature = next(self.iterator)
        self.pos += 1
        return feature

    def read_bulk(self, num: int = 10) -> list[dict]:
        chunk = []
        for _n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record: dict):
        """Write single TopoJSON record"""
        json.dump(record, self.fobj, ensure_ascii=False)
        self.fobj.write('\n')

    def write_bulk(self, records: list[dict]):
        """Write bulk TopoJSON records"""
        # Write as TopoJSON structure
        # This is simplified - proper TopoJSON encoding requires topology computation
        topo_data = {
            'type': 'Topology',
            'objects': {'collection': {'type': 'GeometryCollection', 'geometries': records}},
            'arcs': []
        }
        json.dump(topo_data, self.fobj, ensure_ascii=False)
