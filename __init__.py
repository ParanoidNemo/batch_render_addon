#! /usr/bin/env python

# <pep8 compliant>

import bpy

from . import properties as p
from . import gui as g
from . import function as f

bl_info = {
    "name": "Batch Render",
    "author": "Andrea Calzavacca",
    "version": (0, 0, 1),
    "blender": (2, 7, 8),
    # "api": 53207,
    "location": "Render > Batch Render",
    "description": "Make possible to render more than one camera without manually start every render",
    "warning": "",
    "category": "Render"}


def register():
    bpy.utils.register_class(p.CamProp)
    bpy.utils.register_class(g.BatchRenderPanel)
    bpy.utils.register_class(f.BatchRender)


def unregister():
    bpy.utils.unregister_class(p.CamProp)
    bpy.utils.unregister_class(g.BatchRenderPanel)
    bpy.utils.unregister_class(f.BatchRender)

