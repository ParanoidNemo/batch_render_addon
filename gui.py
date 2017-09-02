#! /usr/bin/env python

# < pep8 compliant>

import bpy


class BatchRenderPanel(bpy.types.Panel):
    bl_idname = "PROPERTIES_PT_batch"
    bl_label = "Batch Render"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def pool(cls, context):
        return context.object is not None
    
    def draw(self, context):
        layout = self.layout
                
        split = layout.split()
        col = split.column()
        
        elements = []
        for item in bpy.data.objects:
                if item.type == 'CAMERA':
                    elements.append(item)
        
        i = 0
        for item in elements:
            if i < len(elements)/2:
                col.prop(item.custom, "isSelected", text=item.name)
            elif i == len(elements)/2 or i == (len(elements)+1)/2:
                col = split.column()
                col.prop(item.custom, "isSelected", text=item.name)
            else:
                col.prop(item.custom, "isSelected", text=item.name)
            i += 1
            
        row = layout.row(align=True)
        row.operator("render.batch", text="Batch Render", icon='RENDER_STILL')