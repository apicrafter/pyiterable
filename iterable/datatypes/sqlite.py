from __future__ import annotations
import typing
import sqlite3
from pathlib import Path

from ..base import BaseFileIterable, BaseCodec


class SQLiteIterable(BaseFileIterable):
    datamode = 'binary'
    def __init__(self, filename:str = None, stream:typing.IO = None, codec: BaseCodec = None, mode='r', table:str = None, query:str = None, options:dict={}):
        super(SQLiteIterable, self).__init__(filename, stream, codec=codec, mode=mode, binary=True, noopen=True, options=options)
        self.table = table
        self.query = query
        if 'table' in options:
            self.table = options['table']
        if 'query' in options:
            self.query = options['query']
        if stream is not None:
            raise ValueError("SQLite requires a filename, not a stream")
        if filename is None:
            raise ValueError("SQLite requires a filename")
        self.connection = None
        self.cursor = None
        self.reset()
        pass

    def reset(self):
        """Reset iterable"""
        super(SQLiteIterable, self).reset()
        if self.connection is not None:
            self.connection.close()
        
        self.connection = sqlite3.connect(self.filename)
        self.connection.row_factory = sqlite3.Row  # Return rows as dict-like objects
        
        if self.mode in ['w', 'wr']:
            # Write mode - initialize but don't create cursor yet
            # Table will be created on first write if needed
            self.cursor = None
            self.keys = None
        else:
            # Read mode
            if self.query:
                # Use custom query
                self.cursor = self.connection.execute(self.query)
            elif self.table:
                # Query specific table
                self.cursor = self.connection.execute(f"SELECT * FROM {self.table}")
            else:
                # Get first table
                cursor = self.connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name LIMIT 1"
                )
                first_table = cursor.fetchone()
                if first_table is None:
                    raise ValueError("No tables found in SQLite database")
                self.table = first_table[0]
                self.cursor = self.connection.execute(f"SELECT * FROM {self.table}")
            
            # Get column names from cursor description
            if self.cursor.description:
                self.keys = [description[0] for description in self.cursor.description]
            else:
                self.keys = None
        self.pos = 0

    @staticmethod
    def has_totals():
        """Has totals indicator"""
        return True        

    def totals(self):
        """Returns file totals"""
        if self.query:
            # For custom queries, we need to count manually
            count_cursor = self.connection.execute(f"SELECT COUNT(*) as count FROM ({self.query})")
            return count_cursor.fetchone()[0]
        elif self.table:
            count_cursor = self.connection.execute(f"SELECT COUNT(*) FROM {self.table}")
            return count_cursor.fetchone()[0]
        return 0

    @staticmethod
    def id() -> str:
        return 'sqlite'

    @staticmethod
    def is_flatonly() -> bool:
        return True

    def read(self) -> dict:
        """Read single SQLite record"""
        row = self.cursor.fetchone()
        if row is None:
            raise StopIteration
        # Convert Row to dict
        result = dict(zip(self.keys, row))
        self.pos += 1
        return result

    def read_bulk(self, num:int = 10) -> list[dict]:
        """Read bulk SQLite records"""
        chunk = []
        for n in range(0, num):
            try:
                chunk.append(self.read())
            except StopIteration:
                break
        return chunk

    def write(self, record:dict):
        """Write single SQLite record"""
        if self.mode not in ['w', 'wr']:
            raise ValueError("Write mode not enabled")
        if self.table is None:
            raise ValueError("Table name required for writing")
        
        if self.connection is None:
            self.connection = sqlite3.connect(self.filename)
        
        # Get column names from record keys or use existing keys
        if not hasattr(self, 'keys') or self.keys is None:
            self.keys = list(record.keys())
            # Create table if it doesn't exist
            columns_def = ', '.join([f"{key} TEXT" for key in self.keys])
            create_query = f"CREATE TABLE IF NOT EXISTS {self.table} ({columns_def})"
            self.connection.execute(create_query)
            self.connection.commit()
        
        # Build INSERT statement
        columns = ', '.join(self.keys)
        placeholders = ', '.join(['?' for _ in self.keys])
        values = [record.get(key) for key in self.keys]
        
        insert_query = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
        self.connection.execute(insert_query, values)
        self.connection.commit()
        self.pos += 1

    def write_bulk(self, records: list[dict]):
        """Write bulk SQLite records"""
        if self.mode not in ['w', 'wr']:
            raise ValueError("Write mode not enabled")
        if self.table is None:
            raise ValueError("Table name required for writing")
        
        if self.connection is None:
            self.connection = sqlite3.connect(self.filename)
        
        if not records:
            return
        
        # Get column names from first record or use existing keys
        if not hasattr(self, 'keys') or self.keys is None:
            self.keys = list(records[0].keys())
            # Create table if it doesn't exist
            columns_def = ', '.join([f"{key} TEXT" for key in self.keys])
            create_query = f"CREATE TABLE IF NOT EXISTS {self.table} ({columns_def})"
            self.connection.execute(create_query)
            self.connection.commit()
        
        # Build INSERT statement
        columns = ', '.join(self.keys)
        placeholders = ', '.join(['?' for _ in self.keys])
        insert_query = f"INSERT INTO {self.table} ({columns}) VALUES ({placeholders})"
        
        # Prepare all values
        all_values = [[record.get(key) for key in self.keys] for record in records]
        
        self.connection.executemany(insert_query, all_values)
        self.connection.commit()
        self.pos += len(records)

    def close(self):
        """Close SQLite connection"""
        if self.connection is not None:
            self.connection.close()
            self.connection = None
        super(SQLiteIterable, self).close()
