#! /usr/bin/env python

# <pep8 compliant>

# import standard modules
import sys

# import blender module
import bpy


class BatchRender(bpy.types.Operator):
    """Batch Render"""
    bl_idname = "render.batch"
    bl_label = "Subsequently render all selected cameras"
    bl_options = {'REGISTER', 'UNDO'}

    # Define some variables to register
    _timer = None
    shots = []
    stop = None
    rendering = None
    fr = True                              # needed for break infinite render loop
    path = None

    # Define the handler functions. I use pre and
    # post to know if Blender "is rendering"
    def pre(self, dummy):
        self.rendering = True

    def post(self, dummy):
        self.shots.pop(0)
        self.rendering = False

    def cancelled(self, dummy):
        self.stop = True

    def execute(self, context):
        # Define the variables during execution. This allows
        # to define when called from a button
        self.stop = False
        self.rendering = False
        
        while self.fr:
            for item in bpy.data.objects:
                if item.type == 'CAMERA' and item.custom.isSelected:
                    self.shots.append(item)
            self.fr = False                 # make the loop work only once per instance   

        self.path = bpy.context.scene.render.filepath

        bpy.app.handlers.render_pre.append(self.pre)
        bpy.app.handlers.render_post.append(self.post)
        bpy.app.handlers.render_cancel.append(self.cancelled)

        # The timer gets created and the modal handler
        # is added to the window manager
        self._timer = context.window_manager.event_timer_add(0.5, context.window)
        context.window_manager.modal_handler_add(self)

        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if event.type == 'TIMER': # This event is signaled every half a second
                                  # and will start the render if available

            # If cancelled or no more shots to render, finish.
            if True in (not self.shots, self.stop is True): 

                # We remove the handlers and the modal timer to clean everything
                bpy.app.handlers.render_pre.remove(self.pre)
                bpy.app.handlers.render_post.remove(self.post)
                bpy.app.handlers.render_cancel.remove(self.cancelled)
                context.window_manager.event_timer_remove(self._timer)

                return {"FINISHED"}

            elif self.rendering is False: # Nothing is currently rendering.
                                          # Proceed to render.

                sceneKey = bpy.data.scenes.keys()[0]

                bpy.data.scenes[sceneKey].camera = self.shots[0]
                bpy.data.scenes[sceneKey].render.filepath = self.path + self.shots[0].name
                bpy.ops.render.render("INVOKE_DEFAULT", write_still=True)

        return {"PASS_THROUGH"}