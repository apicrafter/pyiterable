from __future__ import annotations
import typing
import json
try:
    import geojson
    HAS_GEOJSON = True
except ImportError:
    HAS_GEOJSON = False

from ..base import BaseFileIterable, BaseCodec


class GeoJSONIterable(BaseFileIterable):
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode:str='r', encoding:str = 'utf8', options:dict={}):
        super(GeoJSONIterable, self).__init__(filename, stream, codec=codec, binary=False, mode=mode, encoding=encoding, options=options)
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(GeoJSONIterable, self).reset()
        self.pos = 0
        if self.mode == 'r':
            # Try to parse as a single JSON document first
            try:
                # Save current position
                current_pos = self.fobj.tell()
                self.fobj.seek(0)
                data = json.load(self.fobj)
                # GeoJSON can be FeatureCollection or single Feature
                if data.get('type') == 'FeatureCollection':
                    self.features = data.get('features', [])
                elif data.get('type') == 'Feature':
                    self.features = [data]
                else:
                    # Try to find features in the data
                    self.features = data if isinstance(data, list) else []
                self.iterator = iter(self.features)
            except (json.JSONDecodeError, ValueError):
                # If single JSON parse fails, try JSONL format (one JSON object per line)
                self.fobj.seek(0)
                self.features = []
                for line in self.fobj:
                    line = line.strip()
                    if line:
                        try:
                            feature = json.loads(line)
                            self.features.append(feature)
                        except json.JSONDecodeError:
                            # Skip invalid JSON lines
                            continue
                self.iterator = iter(self.features)

    @staticmethod
    def id() -> str:
        return 'geojson'

    @staticmethod
    def is_flatonly() -> bool:
        return False

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True

    def totals(self):
        """Returns file totals"""
        if hasattr(self, 'features'):
            return len(self.features)
        return 0

    def read(self) -> dict:
        """Read single GeoJSON feature"""
        feature = next(self.iterator)
        self.pos += 1
        # Return feature as dict (it already is)
        return feature

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk GeoJSON features"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single GeoJSON feature"""
        # Ensure it's a valid GeoJSON feature
        if 'type' not in record:
            record['type'] = 'Feature'
        if HAS_GEOJSON:
            feature = geojson.Feature(**record)
            geojson.dump(feature, self.fobj, ensure_ascii=False)
        else:
            json.dump(record, self.fobj, ensure_ascii=False)
        self.fobj.write('\n')

    def write_bulk(self, records:list[dict]):
        """Write bulk GeoJSON features"""
        # Write as FeatureCollection
        if HAS_GEOJSON:
            features = [geojson.Feature(**r) for r in records]
            fc = geojson.FeatureCollection(features)
            geojson.dump(fc, self.fobj, ensure_ascii=False)
        else:
            fc = {
                'type': 'FeatureCollection',
                'features': records
            }
            json.dump(fc, self.fobj, ensure_ascii=False)
