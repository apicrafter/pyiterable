# -*- coding: utf-8 -*-
import os
from json import load, dumps


class ProjectState:
    """Keeps project state"""

    def __init__(self, filename=None, reset=True, autosave=True):
        self.data = {}
        self.filename = filename
        self.autosave = autosave
        if not reset and filename and os.path.exists(filename):
            self.load(filename)
        else:
            self.stages = []
            self.last_stage = None

    def add(self, name, status="success", results={}):
        """Add stage"""
        self.stages.append({'name': name, 'status': status, 'results': results})
        self.last_stage = name
        if self.autosave:
            self.save(self.filename)

    def load(self, filename):
        """Load"""
        f = open(filename, 'r', encoding='utf8')
        self.data = load(f)
        f.close()
        self.stages = self.data['stages']
        self.last_stage = self.stages[-1]['name']
        pass

    def save(self, filename=None):
        if not filename:
            filename = self.filename
        if filename:
            f = open(filename, 'w', encoding='utf8')
            self.data['stages'] = self.stages
            f.write(dumps(self.data, indent=4))
            f.close()
