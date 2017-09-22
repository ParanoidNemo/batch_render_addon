#! /usr/bin/env python

import bpy

# Camera panel properties


class CamProp(bpy.types.PropertyGroup):

    @classmethod
    def register(cls):

        bpy.types.Object.custom = bpy.props.PointerProperty(
            name="Custom properties",
            description="Custom Properties for Objects",
            type=cls,
            )

        cls.isSelected = bpy.props.BoolProperty(
            description="True if Camera is selected to be used",
            default=False
            )

    @classmethod
    def unregister(cls):
        del bpy.types.Object.custom