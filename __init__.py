#! /usr/bin/env python

# <pep8 compliant>

import bpy

from . import properties
from . import operator
from . import gui

bl_info = {
    "name": "Batch Render",
    "author": "Andrea Calzavacca",
    "version": (0, 2, 0),
    "blender": (2, 7, 8),
    "location": "Render > Batch Render",
    "description": "Make possible to render more than one camera without manually start every render",
    "warning": "Beta version: 2.0",
    "category": "Render"}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
